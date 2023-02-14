import open3d as o3d
import numpy as np
    

class Vis3D:
    """
        This class can be used to visulize point cloud data.
        Particularly, it's helpful when debugging code.
        
        This is an example code:
        
        >>> pointcloud = np.random.random((100, 3))
        >>> Vis3D(pointcloud).show()
    """
    
    def __init__(self, 
                 point_cloud: np.ndarray=None, 
                 show_coor=True, 
                 bg_color=[0.5, 0.5, 0.5]) -> None:
        # point_cloud should be a numpy array
        # point_cloud.shape == (n, 3)
        assert point_cloud is not None
        assert point_cloud.shape[1] == 3
        
        # Initialize visulizer
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        opt = self.vis.get_render_option()
        opt.show_coordinate_frame = show_coor
        opt.background_color = np.asarray(bg_color)
        
        if point_cloud is not None:
            self.add_pcd(point_cloud)
    
    def show(self):
        self.vis.run()
        self.vis.destroy_window()
        
    def add_pcd(self, point_cloud: np.ndarray):
        self.point_cloud = point_cloud
        self.current_pcd = o3d.geometry.PointCloud()
        self.current_pcd.points = o3d.utility.Vector3dVector(point_cloud)
        self.vis.add_geometry(self.current_pcd)
        return self

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
        self.current_pcd.colors = o3d.utility.Vector3dVector(colors)
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
    
    def add_lines(self, starts, ends, color=[1, 0, 0], colors=None):
        # starts & ends should be numpy arrays 
        # with the same shape
        assert starts.shape == ends.shape
        
        lines = [[each, each+starts.shape[0]] for each in range(starts.shape[0])]
        if colors is None:
            colors = [color for i in range(len(lines))]
        else:
            assert starts.shape == colors.shape
            
        line_set = o3d.geometry.LineSet(
            points=o3d.utility.Vector3dVector(np.concatenate((starts, ends))),
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

