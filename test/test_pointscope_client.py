from pointscope import PointScopeClient
import open3d as o3d
import numpy as np

torus = np.asarray(o3d.geometry.TriangleMesh.create_torus().vertices)
sphere = np.asarray(o3d.geometry.TriangleMesh.create_sphere().vertices)
                
PointScopeClient()\
    .o3d()\
    .add_pcd(torus+np.array([0, 0, -1.0])).add_color(np.zeros_like(torus))\
    .add_pcd(sphere)\
    .add_pcd(np.random.random((30000, 3))+np.array([-0.5, -0.5, 1.0]))\
    .add_lines(np.random.random((10, 3)), np.random.random((10, 3))) \
    .show()
