import open3d as o3d
import numpy as np
from sklearn.manifold import TSNE
import copy


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
                 bg_color=[0.5, 0.5, 0.5],
                 vis=None) -> None:
        
        # Initialize visulizer
        
        self.vis = vis if vis is not None else o3d.visualization.Visualizer()
        self.vis.create_window()
        opt = self.vis.get_render_option()
        opt.show_coordinate_frame = show_coor
        opt.background_color = np.asarray(bg_color)
        
        if point_cloud is not None:
            self.add_pcd(point_cloud)

    def show(self):
        self.vis.run()
        self.vis.destroy_window()
        
    def add_pcd(self, point_cloud: np.ndarray, tsfm: np.ndarray=None):
        """Add a new point cloud to visulize.
        
        Note that all the following operations would focus on
        the added point cloud. An additional argument tsfm can
        be added to transform the point cloud.
        
        Args:
            point_cloud (np.ndarray): (n, 3)
            tsfm (np.ndarray): (4, 4) 
        """
        self.current_pcd = o3d.geometry.PointCloud()
        self.current_pcd.points = o3d.utility.Vector3dVector(point_cloud)
        if tsfm is not None:
            self.current_pcd.transform(tsfm)
        self.current_pcd.estimate_normals()
            
        self.vis.add_geometry(self.current_pcd)
        self.point_cloud = np.asarray(self.current_pcd.points)
        return self

    def add_color(self, colors: np.ndarray=None):
        """Add color to current point cloud.
        
        color should match the shape of the current focused 
        point cloud. Random color will be added to the point
        cloud if color is not specified.

        Args:
            color (np.ndarray): (n, 3)
        """
        if colors is None:
            colors = np.zeros_like(self.point_cloud)+np.random.rand(3)
        else:
            assert colors.shape == self.point_cloud.shape
            if colors.max() >= 1.0 or colors.min() < 0:
                colors = np.asarray(colors, dtype=np.float32)
                colors = (colors - colors.min()) / colors.max()
        self.current_pcd.colors = o3d.utility.Vector3dVector(colors)
        return self

    def add_normal(self, normals: np.ndarray=None, normal_length_ratio: float=0.05):
        """Add normals to current point cloud.
        
        normal should match the shape of the corresponding 
        point cloud.

        Args:
            normals (np.ndarray): (n, 3)
        """
        if normals is None:
            self.current_pcd.estimate_normals()
            normals = np.asarray(self.current_pcd.normals)
        
        assert normals.shape == self.point_cloud.shape
        normal_offset = np.zeros((self.point_cloud.shape[0] * 2, 3))
        normal_offset[:self.point_cloud.shape[0]] = self.point_cloud
        normal_offset[self.point_cloud.shape[0]:] = self.point_cloud + normals*normal_length_ratio
        lines = [[each, each+self.point_cloud.shape[0]] for each in range(self.point_cloud.shape[0])]
        colors = [[1, 0, 0] for i in range(len(lines))]
        line_set = o3d.geometry.LineSet(
            points=o3d.utility.Vector3dVector(normal_offset),
            lines=o3d.utility.Vector2iVector(lines),
        )
        line_set.colors = o3d.utility.Vector3dVector(colors)
        self.vis.add_geometry(line_set)
        return self
    
    def add_lines(self, starts: np.ndarray, 
                        ends: np.ndarray, 
                        color: list=[1, 0, 0],
                        colors: np.ndarray=None):
        """Add arbitrary lines to visulize.

        Args:
            starts (np.ndarray): (m, 3) 
            ends (np.ndarray): (m, 3)
            color (list, optional): (R, G, B). Defaults to [1, 0, 0].
            colors (np.ndarray, optional): (m, 3). Defaults to None.

        """
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
    
    def add_label(self, labels: np.ndarray):
        """
        Args:
            labels (np.ndarray): (n)

        """
        assert labels is not None
        assert labels.shape[0] == self.point_cloud.shape[0]
        label_uniques = np.unique(labels)
        label_mapper = dict(zip(label_uniques, range(len(label_uniques))))
        random_color = np.random.random((len(label_uniques), 3))
        label_colors = np.array([random_color[label_mapper[each]] for each in labels])
        self.add_color(label_colors)
        return self

    def select_points(self, indices: np.ndarray):
        
        labels = np.zeros((self.point_cloud.shape[0]))
        labels[indices] = 1
        self.add_label(labels)
        return self
        

    def add_feat(self, feat: np.ndarray):
        """Use T-SNE to visualize feature.
        
        Args:
            feat (np.ndarray): (n, f)
        """
        feat_tsne = TSNE(n_components=3, 
                         learning_rate='auto', 
                         init='random').fit_transform(feat)
        self.add_color(feat_tsne)
        return self
