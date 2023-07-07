from d3tool import Vis3D
import numpy as np
import open3d as o3d
import copy


T = np.eye(4)
T[:3, :3] = o3d.geometry.get_rotation_matrix_from_xyz((0, np.pi / 3, np.pi / 2))
T[0, 3] = 1
T[1, 3] = 1.3
print(T)

sample_pcd_data = o3d.data.PCDPointCloud()
sample_pcd_data_1 = o3d.t.io.read_point_cloud(sample_pcd_data.path).to_legacy().points
sample_pcd_data_2 = o3d.t.io.read_point_cloud(sample_pcd_data.path).to_legacy().points

Vis3D().add_pcd(sample_pcd_data_1).add_color().add_pcd(sample_pcd_data_2, T).add_color().show()
