from pointscope.protos import pointscope_pb2_grpc
from pointscope.protos import pointscope_pb2
from .pointscope_o3d import PointScopeO3D
from .pointscope_vedo import PointScopeVedo
import logging
import numpy as np
import open3d as o3d


class PointScopeServicer(pointscope_pb2_grpc.PointScopeServicer):
    
    def __init__(self) -> None:
        super().__init__()

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
        for request in request_iterator:
            if request.HasField("vedo_init"):                
                psdelegator = PointScopeVedo()
            elif request.HasField("o3d_init"):                
                psdelegator = PointScopeO3D(
                    show_coor=request.o3d_init.show_coor,
                    bg_color=PointScopeServicer.protoMatrix2np(request.o3d_init.bg_color))
            elif request.HasField("add_pcd"):                
                psdelegator.add_pcd(
                    point_cloud=PointScopeServicer.protoMatrix2np(request.add_pcd.pcd),
                    tsfm=PointScopeServicer.protoMatrix2np(request.add_pcd.tsfm))
            elif request.HasField("add_color"):                
                psdelegator.add_color(colors=PointScopeServicer.protoMatrix2np(request.add_color.colors))
            elif request.HasField("add_lines"):                
                psdelegator.add_lines(
                    starts=PointScopeServicer.protoMatrix2np(request.add_lines.starts),
                    ends=PointScopeServicer.protoMatrix2np(request.add_lines.ends),
                    colors=PointScopeServicer.protoMatrix2np(request.add_lines.colors))

            response = pointscope_pb2.VisResponse(
                status=pointscope_pb2.Status(ok=True)
            )
            yield response
        
        psdelegator.show()
