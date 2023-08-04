import numpy as np
from .base import PointScopeScaffold
from vedo import Points, Spheres, Plotter, Lines
from ..utils.se3_numpy import se3_transform
from multiprocessing import Process


class PointScopeVedo(PointScopeScaffold):
    
    def __init__(self, 
                subplot=1,
                window_name=None, 
                bg_color=[0.5, 0.5, 0.5],
                ) -> None:
        super().__init__(__class__.__name__, dict(
            subplot=subplot,
            window_name=window_name, 
            bg_color=bg_color,
        ))
        self.plt = Plotter(
            N=subplot,
            title=window_name if window_name else self.__class__.__name__,
            bg=bg_color
        )

    def show(self):
        if self.params["perspective"]:
            perspective = self.params["perspective"]
            self.plt.show(camera=perspective).interactive()
        else:
            self.plt.show().interactive()
        self.params["perspective"] = dict(
            pos=self.plt.camera.GetPosition(),
            focal_point=self.plt.camera.GetFocalPoint(),
            distance=self.plt.camera.GetDistance(),
            viewup=self.plt.camera.GetViewUp(),
        )
        self.plt.close()
        return super().show()

    def draw_at(self, pos: int):
        self.plt.at(pos)
        return super().draw_at(pos)
    
    def add_pcd(self, point_cloud: np.ndarray, tsfm: np.ndarray = None):
        pcd_input = point_cloud.copy()
        if tsfm is not None:
            point_cloud = se3_transform(tsfm[:3], point_cloud)
        self.current_pcd = Spheres(point_cloud, r=0.02)
        self.plt.add(self.current_pcd)
        return super().add_pcd(pcd_input, tsfm)
    
    def add_color(self, colors: np.ndarray):
        """Add color to current point cloud.
        
        color should match the shape of the current focused 
        point cloud. Random color will be added to the point
        cloud if color is not specified.

        Args:
            color (np.ndarray): (n, 3)
        """
        colors_input = colors.copy()
        if self.current_pcd is None:
            print("No current operating point cloud.")
            return super().add_color(colors_input)
        
        color_channel = colors.shape[1]
        groups = int(self.current_pcd.ncells / self.curr_pcd_np.shape[0])
        
        if colors.max() <= 1.0:
            colors = np.asarray(colors, dtype=np.float32) * 255
        
        colors = colors[:, None, :].repeat(groups, 1).reshape(-1, color_channel)
        self.current_pcd.cell_individual_colors(colors)
        return super().add_color(colors_input)

    def add_normal(self, normals: np.ndarray = None, normal_length_ratio: float = 0.05):
        """Add normals to current point cloud.
        
        normal should match the shape of the corresponding 
        point cloud.

        Args:
            normals (np.ndarray): (n, 3)
        """
        return super().add_normal(normals, normal_length_ratio)

    def add_lines(self, starts: np.ndarray, ends: np.ndarray, color: list = ..., colors: np.ndarray = None):
        lines = Lines(Points(starts), Points(ends), c=colors, alpha=0.9, lw=8)
        self.plt.add(lines)
        return super().add_lines(starts, ends, color, colors)
