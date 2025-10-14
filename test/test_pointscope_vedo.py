from pointscope import PointScopeVedo
import open3d as o3d
import numpy as np


torus = np.asarray(o3d.geometry.TriangleMesh.create_torus().vertices)
sphere = np.asarray(o3d.geometry.TriangleMesh.create_sphere().vertices)

points_start = np.random.random((10, 3))
points_end = np.random.random((10, 3))+1
line_colors = np.random.random((10, 3))
PointScopeVedo(3) \
	.add_pcd(torus) \
	.draw_at(1) \
	.hint("1")\
	.add_pcd(sphere, colors=np.random.random(sphere.shape)) \
	.draw_at(2) \
	.hint("2")\
	.add_pcd(points_start) \
	.add_pcd(points_end) \
	.add_lines(points_start, points_end, colors=line_colors)\
	.show()#.save()
