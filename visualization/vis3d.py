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
    

class Viser:
    pcd = o3d.geometry.PointCloud()
    vis = o3d.visualization.Visualizer()
    
    def __init__(self, point_cloud) -> None:
        self.point_cloud = point_cloud
        self.vis.create_window()
        self.pcd.points = o3d.utility.Vector3dVector(self.point_cloud)
        self.vis.add_geometry(self.pcd)

    def show(self):
        self.vis.run()
    
    def __del__(self):
        self.vis.destroy_window()
        
    def add_color(self, colors: np.ndarray):
        # color should be a numpy array and 
        # match the shape of the corresponding 
        # point cloud.
        # i.e. color.shape == (n, 3)
        assert colors is not None
        assert colors.shape == self.point_cloud.shape
        if colors.max() >= 1.0 or colors.min() < 0:
            colors = np.asarray(colors, dtype=np.float32)
            colors = (colors - colors.min()) / colors.max()
        self.pcd.colors = o3d.utility.Vector3dVector(colors)
        return self

    def add_normal(self, normals):
        # normal should be a numpy array and 
        # match the shape of the corresponding 
        # point cloud.
        # i.e. normal.shape == (n, 3)
        assert normals is not None
        assert normals.shape == self.point_cloud.shape

        normal_offset = np.zeros((self.point_cloud.shape[0] * 2, 3))
        normal_offset[:self.point_cloud.shape[0]] = self.point_cloud
        normal_offset[self.point_cloud.shape[0]:] = self.point_cloud + normals/100
        lines = [[each, each+self.point_cloud.shape[0]] for each in range(self.point_cloud.shape[0])]
        colors = [[1, 0, 0] for i in range(len(lines))]
        line_set = o3d.geometry.LineSet(
            points=o3d.utility.Vector3dVector(normal_offset),
            lines=o3d.utility.Vector2iVector(lines),
        )
        line_set.colors = o3d.utility.Vector3dVector(colors)
        self.vis.add_geometry(line_set)
        return self
    
    def add_label(self, labels):
        assert labels is not None
        assert labels.shape[0] == self.point_cloud.shape[0]
        label_uniques = np.unique(labels)
        label_mapper = dict(zip(label_uniques, range(len(label_uniques))))
        random_color = np.random.random((len(label_uniques), 3))
        label_colors = np.array([random_color[label_mapper[each]] for each in labels])
        self.add_color(label_colors)
        return self