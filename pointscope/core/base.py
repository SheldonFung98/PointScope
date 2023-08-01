import os
import numpy as np
import open3d as o3d
from sklearn.manifold import TSNE
import pickle
from datetime import datetime


supported_file_type = [
    "xyz", "xyzn", "xyzrgb", "pts", "ply", "pcd"
]
time_format = "%Y-%m-%dT%H:%M:%S%z"

class PointScopeScaffold:

    def __init__(self, ps_init) -> None:
        super().__init__()
        self.ps_sequence = dict(ps_init=ps_init, commands=list())
        self.current_pcd = None
        self.curr_pcd_np = None
    
    def _append_command(self, command_name, **kargs):
        self.ps_sequence["commands"].append({
            command_name: kargs
        })

    def save(self, file_name=None):
        if file_name is None:
            file_name = "PointScope_{}.pkl".format(datetime.now().strftime(time_format))
        with open(file_name, 'wb') as pickle_file:
            pickle.dump(self.ps_sequence, pickle_file)
        return self

    def add_pcd(self, point_cloud: np.ndarray, tsfm: np.ndarray=None):
        """Add a new point cloud to visulize.
        
        Note that all the following operations would focus on
        the added point cloud. An additional argument tsfm can
        be added to transform the point cloud.
        
        Args:
            point_cloud (np.ndarray): (n, 3)
            tsfm (np.ndarray): (4, 4) 
        """
        self._append_command("add_pcd", point_cloud=point_cloud, tsfm=tsfm)
        self.curr_pcd_np = point_cloud
        self.add_color(np.zeros_like(point_cloud)+np.random.rand(3))
        return self

    def add_color(self, colors: np.ndarray):
        """Add color to current point cloud.
        
        color should match the shape of the curren`t focused 
        point cloud. Random color will be added to the point
        cloud if color is not specified.

        Args:
            color (np.ndarray): (n, 3)
        """
        self._append_command("add_color", colors=colors)
        return self

    
    def add_lines(self, starts: np.ndarray, ends: np.ndarray, color: list=[1, 0, 0], colors: np.ndarray=None):
        """Add arbitrary lines to visulize.

        Args:
            starts (np.ndarray): (m, 3) 
            ends (np.ndarray): (m, 3)
            color (list, optional): (R, G, B). Defaults to [1, 0, 0].
            colors (np.ndarray, optional): (m, 3). Defaults to None.

        """
        self._append_command("add_lines", starts=starts, ends=ends, color=color, colors=colors)
        return self

    def add_normal(self, normals: np.ndarray=None, normal_length_ratio: float=0.05):
        """Add normals to current point cloud.
        
        normal should match the shape of the corresponding 
        point cloud.

        Args:
            normals (np.ndarray): (n, 3)
        """
        self._append_command("add_normal", normals=normals, normal_length_ratio=normal_length_ratio)
        return self

    def draw_at(self, pos: int):
        """ Decide which grid to draw at 

        Args:
            pos (int): grid index

        Returns:
            PointScopeScaffold: self
        """
        self._append_command("draw_at", pos=pos)
        return self

    def add_pcd_from_file(self, file_path: str, format="auto"):
        file_extension = file_path.split(".")[-1]
        if file_extension not in supported_file_type:
            if format not in supported_file_type:
                print(f"{file_extension} file type is not supported.")
                return self
        pcd = o3d.io.read_point_cloud(file_path, format=format)
        point_cloud = np.asarray(pcd.points)
        return self.add_pcd(point_cloud)

    def add_label(self, labels: np.ndarray):
        """
        Args:
            labels (np.ndarray): (n)

        """
        assert labels is not None
        assert labels.shape[0] == self.curr_pcd_np.shape[0]
        label_uniques = np.unique(labels)
        label_mapper = dict(zip(label_uniques, range(len(label_uniques))))
        random_color = np.random.random((len(label_uniques), 3))
        label_colors = np.array([random_color[label_mapper[each]] for each in labels])
        self.add_color(label_colors)
        return self
    
    def select_points(self, indices: np.ndarray):
        labels = np.zeros((self.curr_pcd_np.shape[0]))
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
