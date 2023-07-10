from pointscope import PointScopeO3D
import open3d as o3d
import numpy as np


# pcd = np.asarray(o3d.io.read_point_cloud("test/samples/car.xyz").points)


# PointScopeO3D().add_pcd(pcd).add_color(np.zeros_like(pcd)).select_points(np.array([100, 12])).show()
# PointScopeO3D().add_pcd(pcd).add_color(np.zeros_like(pcd)).show()

torus = np.asarray(o3d.geometry.TriangleMesh.create_torus().vertices)
sphere = np.asarray(o3d.geometry.TriangleMesh.create_sphere().vertices)
                
PointScopeO3D(vis=o3d.visualization.ExternalVisualizer())\
    .add_pcd(torus)#.add_color(np.zeros_like(torus)).select_points(np.array([100, 12])).show()
