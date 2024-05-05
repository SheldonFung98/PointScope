import grpc
from .base import PointScopeScaffold
from ..protos import pointscope_pb2_grpc
from ..protos import pointscope_pb2
from ..utils.common import np2protoMatrix
import numpy as np
import logging

MAX_MESSAGE_LENGTH = 100*1024*1024

class PointScopeClient(PointScopeScaffold):
    
    def __init__(self, ip="0.0.0.0", port="50051") -> None:
        self.request_pool = list()
        channel = grpc.insecure_channel(
            f'{ip}:{port}',
            options=[
                ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
            ],
        )
        self.stub = pointscope_pb2_grpc.PointScopeStub(channel)

    def __del__(self):
        self.request_pool.clear()

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
    
    def vedo(self, bg_color=[0.5, 0.5, 0.5], window_name=None, subplot=1):
        self.append_request(
            pointscope_pb2.VisRequest(
                vedo_init=pointscope_pb2.VedoInit(
                    window_name=window_name,
                    bg_color=np2protoMatrix(bg_color),
                    subplot=subplot,
                )
            )
        )
        return self
    
    def o3d(self, show_coor=True, bg_color=[0.5, 0.5, 0.5], window_name=None):
        self.append_request(
            pointscope_pb2.VisRequest(
                o3d_init=pointscope_pb2.O3DInit(
                    show_coor=show_coor,
                    bg_color=np2protoMatrix(bg_color),
                    window_name=window_name
                )
            )
        )
        return self

    def save(self, file_name=None, save_local=False):
        self.append_request(
            pointscope_pb2.VisRequest(
                save=pointscope_pb2.Save(
                    file_name=file_name,
                )
            )
        )
        return self

    def draw_at(self, pos: int):
        self.append_request(
            pointscope_pb2.VisRequest(
                draw_at=pointscope_pb2.DrawAt(
                    pos=pos
                )
            )
        )
        return self

    def add_pcd(self, point_cloud: np.ndarray, tsfm: np.ndarray = None):
        self.append_request(
            pointscope_pb2.VisRequest(
                add_pcd=pointscope_pb2.AddPointCloud(
                    pcd=np2protoMatrix(point_cloud),
                    tsfm=np2protoMatrix(tsfm)
                )
            )
        )
        return self
    
    def add_color(self, colors: np.ndarray):
        self.append_request(
            pointscope_pb2.VisRequest(
                add_color=pointscope_pb2.AddColor(
                    colors=np2protoMatrix(colors),
                )
            )
        )
        return self
    
    def add_lines(self, starts: np.ndarray, ends: np.ndarray, color: list = [], colors: np.ndarray = None):
        self.append_request(
            pointscope_pb2.VisRequest(
                add_lines=pointscope_pb2.AddLines(
                    starts=np2protoMatrix(starts),
                    ends=np2protoMatrix(ends),
                    colors=np2protoMatrix(colors),
                )
            )
        )
        return self
    
    def add_normal(self, normals: np.ndarray=None, normal_length_ratio: float=0.05):
        return self
    
    def show(self):
        try:
            response = self.stub.VisualizationSession(iter(self.request_pool))
            status = "ok" if response.status.ok else "failed"
            print(f"Visualization session: {status}.")
        except grpc._channel._InactiveRpcError:
            print("Failed to connect to server.")
        finally:
            return super().show(save_params=False)
