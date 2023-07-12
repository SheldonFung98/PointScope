from pointscope.protos import pointscope_pb2_grpc
from pointscope.protos import pointscope_pb2
from .pointscope_o3d import PointScopeO3D as PS_O3D
from .pointscope_vedo import PointScopeVedo as PS_Vedo
import logging
import numpy as np
import open3d as o3d


class PointScopeServicer(pointscope_pb2_grpc.PointScopeServicer):
    
    def __init__(self) -> None:
        super().__init__()
        self.p2n = PointScopeServicer.protoMatrix2np
        self.psdelegator = None

    @staticmethod
    def protoMatrix2np(protoMatrix):
        np_array = np.array(protoMatrix.data)
        if np_array.size:
            return np_array.reshape(protoMatrix.shape)
        else:
            return None

    def VisualizationSession(self, request_iterator, context):
        logging.info("Visualization session.")
        logging.info(f"Receiving commands...")
        for request in request_iterator:
            field_name = request.ListFields()[0][0].name
            command = "{}{}".format(
                "" if field_name.endswith("init") else " -> ", 
                field_name
            ) 
            print(command, end="", flush=True)
            getattr(self, field_name)(request)
            response = pointscope_pb2.VisResponse(
                status=pointscope_pb2.Status(ok=True)
            )
            yield response
        print()
        logging.info(f"Done.")
        self.psdelegator.show()
        del self.psdelegator
        self.psdelegator = None

    def vedo_init(self, request):
        self.psdelegator = PS_Vedo(
            window_name=request.o3d_init.window_name,
            bg_color=self.p2n(request.o3d_init.bg_color),
            subplot=request.vedo_init.subplot)
    
    def o3d_init(self, request):
        self.psdelegator = PS_O3D(
            show_coor=request.o3d_init.show_coor,
            bg_color=self.p2n(request.o3d_init.bg_color),
            window_name=request.o3d_init.window_name)
        
    def draw_at(self, request):
        self.psdelegator.draw_at(
            pos=request.draw_at.pos)
        
    def add_pcd(self, request):
        self.psdelegator.add_pcd(
            point_cloud=self.p2n(request.add_pcd.pcd),
            tsfm=self.p2n(request.add_pcd.tsfm))
        
    def add_color(self, request):
        self.psdelegator.add_color(colors=self.p2n(request.add_color.colors))
        
    def add_lines(self, request):
        self.psdelegator.add_lines(
            starts=self.p2n(request.add_lines.starts),
            ends=self.p2n(request.add_lines.ends),
            colors=self.p2n(request.add_lines.colors))