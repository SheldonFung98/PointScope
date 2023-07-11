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

    @staticmethod
    def protoMatrix2np(protoMatrix):
        np_array = np.array(protoMatrix.data)
        if np_array.size:
            return np_array.reshape(protoMatrix.shape)
        else:
            return None

    def VisualizationSession(self, request_iterator, context):
        logging.info("Received visualization session.")
        psdelegator = None
        command_chain = list()
        for request in request_iterator:
            field_name = request.ListFields()[0][0].name
            command_chain.append(field_name)

            if request.HasField("vedo_init"):                
                psdelegator = PS_Vedo(
                    window_name=request.o3d_init.window_name,
                    bg_color=self.p2n(request.o3d_init.bg_color),
                    subplot=request.vedo_init.subplot)
            elif request.HasField("o3d_init"):                
                psdelegator = PS_O3D(
                    show_coor=request.o3d_init.show_coor,
                    bg_color=self.p2n(request.o3d_init.bg_color),
                    window_name=request.o3d_init.window_name)
            elif request.HasField("draw_at"):                
                psdelegator.draw_at(
                    pos=request.draw_at.pos)
            elif request.HasField("add_pcd"):                
                psdelegator.add_pcd(
                    point_cloud=self.p2n(request.add_pcd.pcd),
                    tsfm=self.p2n(request.add_pcd.tsfm))
            elif request.HasField("add_color"):                
                psdelegator.add_color(colors=self.p2n(request.add_color.colors))
            elif request.HasField("add_lines"):                
                psdelegator.add_lines(
                    starts=self.p2n(request.add_lines.starts),
                    ends=self.p2n(request.add_lines.ends),
                    colors=self.p2n(request.add_lines.colors))

            response = pointscope_pb2.VisResponse(
                status=pointscope_pb2.Status(ok=True)
            )
            yield response
        command_chain = "->".join(command_chain)
        logging.info(f"Command Chain: {command_chain}.")
        
        psdelegator.show()
