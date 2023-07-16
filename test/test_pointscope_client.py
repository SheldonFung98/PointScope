from pointscope import PointScopeClient as PSC
import open3d as o3d
import numpy as np

torus = np.asarray(o3d.geometry.TriangleMesh.create_torus().vertices)
sphere = np.asarray(o3d.geometry.TriangleMesh.create_sphere().vertices)
cube = np.random.random((30000, 3))*2+np.array([-0.5, -0.5, 2.0])


PSC().vedo(subplot=2, bg_color=[0.2, 0.3, 0.3]) \
    .add_pcd(torus+np.array([0, 0, -1.0])).add_color(np.zeros_like(torus))\
    .draw_at(1) \
    .add_pcd(sphere)\
    .add_pcd(cube)\
    .add_lines(cube[:20], sphere[:20]) \
    .show()


PSC().o3d(show_coor=False, bg_color=[0.2, 0.3, 0.3]) \
    .add_pcd(torus+np.array([0, 0, -1.0])).add_color(np.zeros_like(torus))\
    .add_pcd(sphere)\
    .add_pcd(cube)\
    .add_lines(cube[:20], sphere[:20]) \
    .show()