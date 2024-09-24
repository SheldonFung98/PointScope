import os
import random
import numpy as np
import open3d as o3d
from sklearn.manifold import TSNE
from datetime import datetime
from abc import ABC, abstractmethod
from pathlib import Path
from ..utils.common import load_pkl, dump_pkl, cast_tensor_to_numpy


SUPPORTED_FILE_TYPE = {
	# Point cloud
	"pcd": ["xyz", "xyzn", "xyzrgb", "pts", "ply", "pcd"], 
	# Mesh
	"mesh": ["stl", "obj", "off", "gltf", "glb"]
}

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
POINTSCOPE_SAVE_PATH = Path.home()/".pointscope"


class PointScopeScaffold(ABC):

	def __init__(self, ps_type, ps_args, vis_params=None) -> None:
		self.current_pcd = None
		self.curr_pcd_np = None
		self.ps_sequence = dict(
			ps_type=ps_type, 
			ps_args=ps_args, 
			commands=list(), 
			params=dict(perspective=None, window_params=None) if vis_params is None else vis_params
		)
		self.params = self.ps_sequence["params"]
		if vis_params is None:
			self._params_io(operation="load")

	def _params_io(self, operation):
		assert operation in ["load", "save"]
		save_path = str(POINTSCOPE_SAVE_PATH/(self.ps_sequence["ps_type"]+"_{}.pkl"))
		if not os.path.exists(POINTSCOPE_SAVE_PATH):
			os.mkdir(POINTSCOPE_SAVE_PATH)
			return
		for params_type in self.params:
			if operation == "load":
				self.params[params_type] = load_pkl(save_path.format(params_type))
			elif operation == "save":
				dump_pkl(save_path.format(params_type), self.params[params_type])
	
	def _append_command(self, command_name, **kargs):
		self.ps_sequence["commands"].append({
			command_name: kargs
		})

	def save(self, file_name=None):
		if file_name is None:
			file_name = "PointScope_{}.pkl".format(datetime.now().strftime(TIME_FORMAT))
		dump_pkl(file_name, self.ps_sequence)
		return self

	@abstractmethod
	def show(self, save_params=True):
		if save_params:
			self._params_io(operation="save")
		return self
	
	@abstractmethod
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
		self.add_color(np.zeros_like(point_cloud)+[random.random() for _ in range(3)])
		return self

	@abstractmethod
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

	
	@abstractmethod
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

	@abstractmethod
	def add_normal(self, normals: np.ndarray=None, normal_length_ratio: float=0.05):
		"""Add normals to current point cloud.
		
		normal should match the shape of the corresponding 
		point cloud.

		Args:
			normals (np.ndarray): (n, 3)
		"""
		self._append_command("add_normal", normals=normals, normal_length_ratio=normal_length_ratio)
		return self

	@abstractmethod
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

		if file_extension in SUPPORTED_FILE_TYPE["pcd"]:
			pass
		elif file_extension in SUPPORTED_FILE_TYPE["mesh"]:
			pass
		else:
			if format not in SUPPORTED_FILE_TYPE:
				print(f"{file_extension} file type is not supported.")
				return self
		pcd = o3d.io.read_point_cloud(file_path, format=format)
		point_cloud = np.asarray(pcd.points)
		pcd_colors = np.asarray(pcd.colors)
		self.add_pcd(point_cloud)
		if pcd_colors.shape[0] == point_cloud.shape[0]:
			self.add_color(pcd_colors)
		return self

	@cast_tensor_to_numpy
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
		return self.add_color(label_colors)
	
	@cast_tensor_to_numpy
	def select_points(self, indices: np.ndarray):
		labels = np.zeros((self.curr_pcd_np.shape[0]))
		labels[indices] = 1
		return self.add_label(labels)
	
	@cast_tensor_to_numpy
	def add_feat(self, feat: np.ndarray):
		"""Use T-SNE to visualize feature.
		
		Args:
			feat (np.ndarray): (n, f)
		"""
		feat_tsne = TSNE(n_components=3, 
						 learning_rate='auto', 
						 init='random').fit_transform(feat)
		feat_tsne -= feat_tsne.min()
		feat_tsne /= feat_tsne.max()
		return self.add_color(feat_tsne)

	@cast_tensor_to_numpy
	def add_cam(self, poses: np.ndarray, color=[1, 0, 0], scale=0.1, show_vertices=False):
		"""Add camera poses to visulize.
		
		Args:
			poses (np.ndarray): (b, 4, 4)
		"""
		cam_vertices = np.array([
			[-0.5, -0.5, -1, 1], 	# 0
			[ 0.5, -0.5, -1, 1],  	# 1
			[ 0.5,  0.5, -1, 1], 	# 2
			[-0.5,  0.5, -1, 1], 	# 3
			[   0,  0,    0, 1] 	# 4
		])
		cam_vertices[:, :3] *= scale
		vertices = np.einsum("hd,bmd->bhm", cam_vertices, poses)[..., :3]
		lines = np.array([[4, 0], [4, 1], [4, 2], [4, 3], [0, 1], [1, 2], [2, 3], [3, 0]])
		
		if show_vertices:
			self.add_pcd(vertices.reshape(-1, 3))
		
		return self.add_lines(*vertices[:, lines.T].transpose(1, 0, 2, 3).reshape(2, -1, 3), colors=color)



	def help(self):
		message = """
		#####################################################################################################################
		add_pcd(self, point_cloud: np.ndarray, tsfm: np.ndarray=None)
			Args:
				point_cloud (np.ndarray): (n, 3)
				tsfm (np.ndarray): (4, 4) 
		---------------------------------------------------------------------------------------------------------------------
		add_color(self, colors: np.ndarray):
			Args:
				color (np.ndarray): (n, 3)
		---------------------------------------------------------------------------------------------------------------------
		add_lines(self, starts: np.ndarray, ends: np.ndarray, color: list=[1, 0, 0], colors: np.ndarray=None):
			Args:
				starts (np.ndarray): (m, 3) 
				ends (np.ndarray): (m, 3)
				color (list, optional): (R, G, B). Defaults to [1, 0, 0].
				colors (np.ndarray, optional): (m, 3). Defaults to None.
		---------------------------------------------------------------------------------------------------------------------
		add_normal(self, normals: np.ndarray=None, normal_length_ratio: float=0.05):
			Args:
				normals (np.ndarray): (n, 3)
		---------------------------------------------------------------------------------------------------------------------
		add_label(self, labels: np.ndarray):
			Args:
				labels (np.ndarray): (n)
		---------------------------------------------------------------------------------------------------------------------
		add_pcd_from_file(self, file_path: str, format="auto"):
		---------------------------------------------------------------------------------------------------------------------
		select_points(self, indices: np.ndarray):
		---------------------------------------------------------------------------------------------------------------------
		add_feat(self, feat: np.ndarray):
			Args:
				feat (np.ndarray): (n, f)
		#####################################################################################################################
		"""
		print(message)