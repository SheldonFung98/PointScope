import grpc
from .base import PointScopeScaffold
from pointscope.protos import pointscope_pb2_grpc
from pointscope.protos import pointscope_pb2
import numpy as np
import logging


class PointScopeClient(PointScopeScaffold):
    request_pool = []
    
    def __init__(self, ip="0.0.0.0", port="50051") -> None:
        channel = grpc.insecure_channel(f'{ip}:{port}')
        self.stub = pointscope_pb2_grpc.PointScopeStub(channel)

    @staticmethod
    def np2protoMatrix(numpy_array):
        if numpy_array is None:
            return None
        message = pointscope_pb2.Matrix()
        message.shape.extend(numpy_array.shape)
        message.data.extend(numpy_array.flatten())
        return message
    
    def add_pcd(self, point_cloud: np.ndarray, tsfm: np.ndarray = None):
        self.request_pool.append(
            pointscope_pb2.VisRequest(
                add_pcd=pointscope_pb2.AddPointCloud(
                    pcd=PointScopeClient.np2protoMatrix(point_cloud),
                    tsfm=PointScopeClient.np2protoMatrix(tsfm)
                )
            )
        )
        return super().add_pcd(point_cloud, tsfm)
    
    def add_color(self, colors: np.ndarray = None):
        self.request_pool.append(
            pointscope_pb2.VisRequest(
                add_color=pointscope_pb2.AddColor(
                    colors=PointScopeClient.np2protoMatrix(colors),
                )
            )
        )
        return super().add_color(colors)
    
    def add_lines(self, starts: np.ndarray, ends: np.ndarray, color: list = [], colors: np.ndarray = None):
        self.request_pool.append(
            pointscope_pb2.VisRequest(
                add_lines=pointscope_pb2.AddLines(
                    starts=PointScopeClient.np2protoMatrix(starts),
                    ends=PointScopeClient.np2protoMatrix(ends),
                    colors=PointScopeClient.np2protoMatrix(colors),
                )
            )
        )
        return super().add_lines(starts, ends, color, colors)
    
    def show(self):
        responses = self.stub.VisualizationSession(iter(self.request_pool))
        for response in responses:
            logging.info(f"Received response: {response.status}")
