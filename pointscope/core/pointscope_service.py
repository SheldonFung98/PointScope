from pointscope.protos import pointscope_pb2, pointscope_pb2_grpc
from .pointscope_vedo import PointScopeVedo as PS_Vedo
from .pointscope_o3d import PointScopeO3D as PS_O3D
from ..utils.common import protoMatrix2np
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
            window_name=request.vedo_init.window_name,
            bg_color=protoMatrix2np(request.vedo_init.bg_color),
            subplot=request.vedo_init.subplot)
    
    def o3d_init(self, request):
        self.psdelegator = PS_O3D(
            show_coor=request.o3d_init.show_coor,
            bg_color=protoMatrix2np(request.o3d_init.bg_color),
            window_name=request.o3d_init.window_name)

    def save(self, request):
        file_name = request.save.file_name
        file_name = file_name if file_name else None
        self.psdelegator.save(
            file_name=file_name)

    def draw_at(self, request):
        self.psdelegator.draw_at(
            pos=request.draw_at.pos)
        
    def add_pcd(self, request):
        self.psdelegator.add_pcd(
            point_cloud=protoMatrix2np(request.add_pcd.pcd),
            tsfm=protoMatrix2np(request.add_pcd.tsfm))
        
    def add_color(self, request):
        self.psdelegator.add_color(colors=protoMatrix2np(request.add_color.colors))
        
    def add_lines(self, request):
        self.psdelegator.add_lines(
            starts=protoMatrix2np(request.add_lines.starts),
            ends=protoMatrix2np(request.add_lines.ends),
            colors=protoMatrix2np(request.add_lines.colors))


class PointScopeServicer(pointscope_pb2_grpc.PointScopeServicer):
    
    def __init__(self) -> None:
        super().__init__()

    def VisualizationSession(self, request_iterator, context):
        logging.info("Visualization session.")
        logging.info("Receiving commands...")
        req_queue = list()
        for request in request_iterator:
            field_name = request.ListFields()[0][0].name
            command = "{}{}".format(
                "" if field_name.endswith("init") else " -> ", 
                field_name
            )
            print(command, end="", flush=True)
            req_queue.append({"name": field_name, "action": request})

        print("\nDone.")
        logging.info("Start visualization.")
        p = Process(target=PointScopeRunner, args=(req_queue, ))
        p.start()
        p.join()
        return pointscope_pb2.VisResponse(
            status=pointscope_pb2.Status(ok=True)
        )