import grpc
from .base import PointScopeScaffold
from pointscope.protos import pointscope_pb2_grpc
from pointscope.protos import pointscope_pb2
import numpy as np
import logging


class PointScopeClient(PointScopeScaffold):
    request_pool = list()
    
    def __init__(self, ip="0.0.0.0", port="50051") -> None:
        channel = grpc.insecure_channel(f'{ip}:{port}')
        self.stub = pointscope_pb2_grpc.PointScopeStub(channel)

    def __del__(self):
        self.request_pool.clear()

    @staticmethod
    def np2protoMatrix(numpy_array):
        if numpy_array is None:
            return None
        message = pointscope_pb2.Matrix()
        message.shape.extend(numpy_array.shape)
        message.data.extend(numpy_array.flatten())
        return message
    
    @staticmethod
    def _is_init(r):
        return r.HasField("vedo_init") or r.HasField("o3d_init")
      
    def append_request(self, request):
        if len(self.request_pool):
            if PointScopeClient._is_init(request):
                logging.warning("Multiple visualizer initialization.")
            else:
                self.request_pool.append(request)
                  
        elif PointScopeClient._is_init(request):
            self.request_pool.append(request)
        else:
            self.o3d()
            self.request_pool.append(request)
    
    def vedo(self):
        self.append_request(
            pointscope_pb2.VisRequest(
                vedo_init=pointscope_pb2.VedoInit(
                )
            )
        )
        return self
    
    def o3d(self, show_coor=True, bg_color=[0.5, 0.5, 0.5],):
        self.append_request(
            pointscope_pb2.VisRequest(
                o3d_init=pointscope_pb2.O3DInit(
                    show_coor=show_coor,
                    bg_color=PointScopeClient.np2protoMatrix(bg_color),
                )
            )
        )
        return self
    
    def add_pcd(self, point_cloud: np.ndarray, tsfm: np.ndarray = None):
        self.append_request(
            pointscope_pb2.VisRequest(
                add_pcd=pointscope_pb2.AddPointCloud(
                    pcd=PointScopeClient.np2protoMatrix(point_cloud),
                    tsfm=PointScopeClient.np2protoMatrix(tsfm)
                )
            )
        )
        return super().add_pcd(point_cloud, tsfm)
    
    def add_color(self, colors: np.ndarray = None):
        self.append_request(
            pointscope_pb2.VisRequest(
                add_color=pointscope_pb2.AddColor(
                    colors=PointScopeClient.np2protoMatrix(colors),
                )
            )
        )
        return super().add_color(colors)
    
    def add_lines(self, starts: np.ndarray, ends: np.ndarray, color: list = [], colors: np.ndarray = None):
        self.append_request(
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
