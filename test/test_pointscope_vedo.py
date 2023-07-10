from pointscope import PointScopeVedo
import open3d as o3d
import numpy as np


torus = np.asarray(o3d.geometry.TriangleMesh.create_torus().vertices)
sphere = np.asarray(o3d.geometry.TriangleMesh.create_sphere().vertices)
                
PointScopeVedo() \
    .add_pcd(torus) \
    .add_pcd(sphere) \
    .add_color(np.random.random(sphere.shape)*255) \
    .add_lines(np.random.random((10, 3)), np.random.random((10, 3))) \
    .show()
