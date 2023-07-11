import numpy as np
# from pointscope.core.server import GRPCServer
from sklearn.manifold import TSNE


class PointScopeScaffold:
    current_pcd = None
    curr_pcd_np = None

    def __init__(self) -> None:
        super().__init__()
    
    def add_pcd(self, point_cloud: np.ndarray, tsfm: np.ndarray=None):
        """Add a new point cloud to visulize.
        
        Note that all the following operations would focus on
        the added point cloud. An additional argument tsfm can
        be added to transform the point cloud.
        
        Args:
            point_cloud (np.ndarray): (n, 3)
            tsfm (np.ndarray): (4, 4) 
        """
        self.curr_pcd_np = point_cloud
        self.add_color(np.zeros_like(point_cloud)+np.random.rand(3))
        return self
    
    def add_color(self, colors: np.ndarray=None):
        """Add color to current point cloud.
        
        color should match the shape of the curren`t focused 
        point cloud. Random color will be added to the point
        cloud if color is not specified.

        Args:
            color (np.ndarray): (n, 3)
        """
        return self

    
    def add_lines(self, starts: np.ndarray, ends: np.ndarray, color: list=[1, 0, 0], colors: np.ndarray=None):
        """Add arbitrary lines to visulize.

        Args:
            starts (np.ndarray): (m, 3) 
            ends (np.ndarray): (m, 3)
            color (list, optional): (R, G, B). Defaults to [1, 0, 0].
            colors (np.ndarray, optional): (m, 3). Defaults to None.

        """
        return self

    def add_normal(self, normals: np.ndarray=None, normal_length_ratio: float=0.05):
        """Add normals to current point cloud.
        
        normal should match the shape of the corresponding 
        point cloud.

        Args:
            normals (np.ndarray): (n, 3)
        """
        return self

    def draw_at(self, pos: int):
        """ Decide which grid to draw at 

        Args:
            pos (int): grid index

        Returns:
            PointScopeScaffold: self
        """
        return self


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
