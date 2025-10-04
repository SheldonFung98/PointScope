import numpy as np
from .base import PointScopeScaffold
from vedo import Points, Spheres, Plotter, Lines, Text2D, Mesh
from ..utils.se3_numpy import se3_transform
from multiprocessing import Process
from ..utils.common import cast_tensor_to_numpy
import random


class PointScopeVedo(PointScopeScaffold):
	
	def __init__(self, 
				subplot=1,
				window_name=None, 
				bg_color=[0.5, 0.5, 0.5],
				vis_params=None) -> None:
		super().__init__(__class__.__name__, dict(
			subplot=subplot,
			window_name=window_name, 
			bg_color=bg_color,
		), vis_params)
		if self.params["window_params"]:
			height = self.params["window_params"]["height"]
			width = self.params["window_params"]["width"]
			size = (width, height)
		else:
			size = "auto"
		self.plt = Plotter(
			N=subplot,
			title=window_name if window_name else self.__class__.__name__,
			bg=bg_color,
			size=size
		)

	def show(self, save_params=True):
		self.plt.show(camera=self.params["perspective"]).interactive()
		self.params["perspective"] = dict(
			pos=self.plt.camera.GetPosition(),
			focal_point=self.plt.camera.GetFocalPoint(),
			distance=self.plt.camera.GetDistance(),
			viewup=self.plt.camera.GetViewUp(),
		)
		width, height = self.plt.window.GetSize()
		self.params["window_params"] = dict(
			height=height,
			width=width
		)
		self.plt.close()
		return super().show(save_params)

	def draw_at(self, pos: int):
		self.plt.at(pos)
		return super().draw_at(pos)
	
	def scale_color(self, color: np.ndarray):
		if color.max() <= 1.0:
			color = np.asarray(color, dtype=np.float32) * 255
		return color

	@cast_tensor_to_numpy
	def add_mesh(
		self, 
		vertice: np.ndarray, 
		triangles: np.ndarray, 
		colors: np.array = None, 
		normals: np.ndarray = None, 
		tsfm: np.ndarray = None):
		""" Add a new mesh to visulize.

		Args:
			vertice (np.ndarray): (n, 3)
			triangles (np.ndarray): (m, 3)
			colors (np.array): (n, 3)
			normals (np.ndarray): (n, 3)
			tsfm (np.ndarray, optional): (4, 4). Defaults to None.
		"""
		mesh = Mesh([vertice, triangles])
		if colors is not None:
			mesh.pointcolors = self.scale_color(colors)
		if normals is not None:
			mesh.point_normals = normals
		if tsfm is not None:
			mesh.apply_transform(tsfm)
		self.plt.add(mesh)
		return super().add_mesh(vertice, triangles, colors, normals, tsfm)

	@cast_tensor_to_numpy
	def add_pcd(self, point_cloud: np.ndarray, tsfm: np.ndarray = None, colors: np.ndarray = None):
		pcd_input = point_cloud.copy()
		if tsfm is not None:
			point_cloud = se3_transform(tsfm[:3], point_cloud)
		if colors is None:
			colors = np.zeros_like(point_cloud)+[random.random() for _ in range(3)]
		self.current_pcd = Spheres(point_cloud, r=0.02, c=colors)
		self.plt.add(self.current_pcd)
		return super().add_pcd(pcd_input, tsfm)
	
	@cast_tensor_to_numpy
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
		
		colors = self.scale_color(colors)
		colors = colors[:, None, :].repeat(groups, 1).reshape(-1, color_channel)
		self.current_pcd.cellcolors = colors
		return super().add_color(colors_input)
		return self

	@cast_tensor_to_numpy
	def add_normal(self, normals: np.ndarray = None, normal_length_ratio: float = 0.05):
		"""Add normals to current point cloud.
		
		normal should match the shape of the corresponding 
		point cloud.

		Args:
			normals (np.ndarray): (n, 3)
		"""
		return super().add_normal(normals, normal_length_ratio)

	@cast_tensor_to_numpy
	def add_lines(self, starts: np.ndarray, ends: np.ndarray, color: list = [1, 0, 0], colors: np.ndarray = None):
		assert starts.shape == ends.shape
		lines = Lines(Points(starts), Points(ends), alpha=0.5, lw=4, c=color)
		if colors is None:
			colors = np.asarray([color for i in range(starts.shape[0])])
			
		colors = self.scale_color(colors)
		# lines.cell_individual_colors(colors)
		self.plt.add(lines)
		return super().add_lines(starts, ends, color, colors)

	def hint(self, text: str, color=[1, 0, 0], scale=1.5):
		self.plt.add(
			Text2D(text, pos='top-left', font="Calco", s=scale, c=color)
		)
		return super().hint(text, color, scale)