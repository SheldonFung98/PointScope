from pointscope.protos import pointscope_pb2_grpc
from pointscope.protos import pointscope_pb2
import logging
import numpy as np
import open3d as o3d


class PointScopeServicer(pointscope_pb2_grpc.PointScopeServicer):
    
    def __init__(self, vis_delegate) -> None:
        super().__init__()
        self.PointScopeDelegate = vis_delegate

    @staticmethod
    def protoMatrix2np(protoMatrix):
        np_array = np.array(protoMatrix.data)
        if np_array.size:
            return np_array.reshape(protoMatrix.shape)
        else:
            return None

    def VisualizationSession(self, request_iterator, context):
        logging.info("Received visualization session.")
        psdelegator = self.PointScopeDelegate()
        for request in request_iterator:
            if request.HasField("add_pcd"):                
                psdelegator.add_pcd(
                    point_cloud=PointScopeServicer.protoMatrix2np(request.add_pcd.pcd),
                    tsfm=PointScopeServicer.protoMatrix2np(request.add_pcd.tsfm))
            elif request.HasField("add_color"):                
                psdelegator.add_color(colors=PointScopeServicer.protoMatrix2np(request.add_color.colors))
            elif request.HasField("add_lines"):                
                psdelegator.add_lines(
                    starts=PointScopeServicer.protoMatrix2np(request.add_lines.starts),
                    ends=PointScopeServicer.protoMatrix2np(request.add_lines.starts),
                    colors=PointScopeServicer.protoMatrix2np(request.add_lines.colors))

            response = pointscope_pb2.VisResponse(
                status=pointscope_pb2.Status(ok=True)
            )
            yield response
        
        psdelegator.show()
