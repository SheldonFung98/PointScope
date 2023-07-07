from d3tool import Vis3DWeb
import numpy as np
import open3d as o3d


sample_pcd_data = o3d.data.PCDPointCloud()
sample_pcd_data_1 = np.asarray(o3d.t.io.read_point_cloud(sample_pcd_data.path).to_legacy().points)

Vis3DWeb(sample_pcd_data_1).show()
print("Vis3DWeb started.")

while True:
    pass