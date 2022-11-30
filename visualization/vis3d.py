import open3d as o3d
import numpy as np


def vis(point_cloud, vis_color=None, normal=None):
    pcd = o3d.geometry.PointCloud()
    if vis_color is not None:
        pcd.colors = o3d.utility.Vector3dVector(vis_color)

    pcd.points = o3d.utility.Vector3dVector(point_cloud)

    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    
    if normal is not None:
        normal_offset = np.zeros((point_cloud.shape[0] * 2, 3))
        normal_offset[:point_cloud.shape[0]] = point_cloud
        normal_offset[point_cloud.shape[0]:] = point_cloud + normal/100
        lines = [[each, each+point_cloud.shape[0]] for each in range(point_cloud.shape[0])]
        colors = [[1, 0, 0] for i in range(len(lines))]
        line_set = o3d.geometry.LineSet(
            points=o3d.utility.Vector3dVector(normal_offset),
            lines=o3d.utility.Vector2iVector(lines),
        )
        line_set.colors = o3d.utility.Vector3dVector(colors)
        vis.add_geometry(line_set)
        
    vis.run()
    vis.destroy_window()
