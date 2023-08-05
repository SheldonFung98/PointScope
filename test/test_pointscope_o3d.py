from pointscope import PointScopeO3D as PSC
import open3d as o3d
import numpy as np

# PointScopeO3D().add_pcd(pcd).add_color(np.zeros_like(pcd)).select_points(np.array([100, 12])).show()
# PointScopeO3D().add_pcd(pcd).add_color(np.zeros_like(pcd)).show()

torus = np.asarray(o3d.geometry.TriangleMesh.create_torus().vertices)
sphere = np.asarray(o3d.geometry.TriangleMesh.create_sphere().vertices)
cube = np.random.random((30000, 3))*2+np.array([-0.5, -0.5, 2.0])

# PointScopeO3D().add_pcd(torus)#.add_color(np.zeros_like(torus)).select_points(np.array([100, 12])).show()

psc = PSC().add_pcd(torus+np.array([0, 0, -1.0])).add_color(np.zeros_like(torus))\
    .add_pcd(sphere)\
    .add_pcd(cube)\
    .add_lines(cube[:20], sphere[:20]).show() \
    .save()
