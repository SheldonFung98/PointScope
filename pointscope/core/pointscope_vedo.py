import numpy as np
from .base import PointScopeScaffold
from vedo import Points, Spheres, Plotter, Lines


class PointScopeVedo(PointScopeScaffold):
    
    def __init__(self) -> None:
        super().__init__()
        self.plt = Plotter()
        
    def show(self):
        self.plt.show().close()
    
    def add_pcd(self, point_cloud: np.ndarray, tsfm: np.ndarray = None):
        self.current_pcd = Spheres(point_cloud, r=0.02)
        self.plt.add(self.current_pcd)
        return super().add_pcd(point_cloud, tsfm)
    
    def add_color(self, colors: np.ndarray = None):
        color_channel = colors.shape[1]
        groups = int(self.current_pcd.ncells / self.current_point_cloud_np.shape[0])
        colors = colors[:, None, :].repeat(groups, 1).reshape(-1, color_channel)
        self.current_pcd.cell_individual_colors(colors)
        return super().add_color(colors)

    def add_lines(self, starts: np.ndarray, ends: np.ndarray, color: list = ..., colors: np.ndarray = None):
        lines = Lines(Points(starts), Points(ends), c=colors, alpha=0.9, lw=8)
        self.plt.add(lines)
        return super().add_lines(starts, ends, color, colors)