from .pointscope_vedo import PointScopeVedo as PS_Vedo
from .pointscope_o3d import PointScopeO3D as PS_O3D
from ..utils.common import jsonMatrix2np
from multiprocessing import Process
import logging


class PointScopeRunner:

    def __init__(self, req_queue) -> None:
        self.psdelegator = None
        for req in req_queue:
            getattr(self, req["name"])(req["action"])
        self.psdelegator.show()
        del self.psdelegator

    def vedo_init(self, request):
        self.psdelegator = PS_Vedo(
            window_name=request["window_name"],
            bg_color=jsonMatrix2np(request["bg_color"]),
            subplot=request["subplot"])
    
    def o3d_init(self, request):
        self.psdelegator = PS_O3D(
            show_coor=request["show_coor"],
            bg_color=jsonMatrix2np(request["bg_color"]),
            window_name=request["window_name"])

    def save(self, request):
        file_name = request["file_name"]
        file_name = file_name if file_name else None
        self.psdelegator.save(
            file_name=file_name)

    def draw_at(self, request):
        self.psdelegator.draw_at(
            pos=request["pos"])
        
    def add_pcd(self, request):
        self.psdelegator.add_pcd(
            point_cloud=jsonMatrix2np(request["pcd"]),
            tsfm=jsonMatrix2np(request["tsfm"]))
        
    def add_color(self, request):
        self.psdelegator.add_color(colors=jsonMatrix2np(request["colors"]))
        
    def add_lines(self, request):
        self.psdelegator.add_lines(
            starts=jsonMatrix2np(request["starts"]),
            ends=jsonMatrix2np(request["ends"]),
            colors=jsonMatrix2np(request["colors"]))

    def add_mesh(self, request):
        self.psdelegator.add_mesh(
            vertices=jsonMatrix2np(request["vertices"]),
            triangles=jsonMatrix2np(request["triangles"]),
            colors=jsonMatrix2np(request["colors"]),
            normals=jsonMatrix2np(request["normals"]),
            tsfm=jsonMatrix2np(request["tsfm"]))

    def hint(self, request):
        self.psdelegator.hint(
            text=request["text"],
            color=jsonMatrix2np(request["color"]),
            scale=request["scale"])


class PointScopeServicer:
    
    def __init__(self) -> None:
        pass

    def visualization_session(self, request_data):
        """Process visualization session from JSON request data."""
        logging.info("Visualization session.")
        logging.info("Receiving commands...")
        req_queue = list()
        
        # Extract requests from JSON data
        requests = request_data.get("requests", [])
        
        for request in requests:
            # Find the field name (key) and its data
            field_name = list(request.keys())[0]
            command = "{}{}".format(
                "" if field_name.endswith("init") else " -> ", 
                field_name
            )
            print(command, end="", flush=True)
            req_queue.append({"name": field_name, "action": request[field_name]})
        logging.info("Done. Start visualization.")
        p = Process(target=PointScopeRunner, args=(req_queue, ))
        p.start()
        p.join()
        return {
            "status": {"ok": True}
        }