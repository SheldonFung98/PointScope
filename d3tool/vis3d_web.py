import open3d as o3d
from d3tool import Vis3D
import numpy as np
import multiprocessing

class Vis3DWeb(Vis3D):
    
    def __init__(self, point_cloud: np.ndarray=None) -> None:
        # point_cloud should be a numpy array
        # point_cloud.shape == (n, 3)
        assert point_cloud is not None
        assert point_cloud.shape[1] == 3
        self.pcShape = point_cloud.shape
        self.pcd = o3d.geometry.PointCloud()
        self.point_cloud = point_cloud
        self.pcd.points = o3d.utility.Vector3dVector(self.point_cloud)
        try:
            # Initialize visulizer
            o3d.visualization.webrtc_server.enable_webrtc()
        except:
            print ("webrtc_server is already enabled. But no worries.")

    def show(self, non_blocking=True):
        if non_blocking:
            try:
                process = multiprocessing.Process(target=self._show, args=())
                process.start()
            except Exception as e:
                print ("Error: ", e)
            input("Press Enter to stop server.\n")
            process.terminate()
        else:
            self._show()

    def _show(self):
        o3d.visualization.draw(self.pcd, non_blocking_and_return_uid=False)
        
    def add_normal(self):
        print("Method (add_normal) is blocked.")
        return self