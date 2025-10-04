import json
import urllib.request
import urllib.parse
from .base import PointScopeScaffold
from ..utils.common import np2jsonMatrix, cast_tensor_to_numpy
import numpy as np
import logging

class PointScopeClient(PointScopeScaffold):
	
	def __init__(self, ip="0.0.0.0", port=50051) -> None:
		self.request_pool = list()
		self.server_url = f"http://{ip}:{port}/visualization_session"

	def __del__(self):
		self.request_pool.clear()

	@staticmethod
	def _is_init(r):
		return "vedo_init" in r or "o3d_init" in r
	  
	def append_request(self, request):
		if len(self.request_pool):
			if PointScopeClient._is_init(request):
				logging.warning("Multiple visualizer initialization.")
			else:
				self.request_pool.append(request)
				  
		elif PointScopeClient._is_init(request):
			self.request_pool.append(request)
		else:
			self.o3d()
			self.request_pool.append(request)
	
	def vedo(self, bg_color=[0.5, 0.5, 0.5], window_name=None, subplot=1):
		request = {
			"vedo_init": {
				"window_name": window_name,
				"bg_color": np2jsonMatrix(bg_color),
				"subplot": subplot,
			}
		}
		self.append_request(request)
		return self
	
	def o3d(self, show_coor=True, bg_color=[0.5, 0.5, 0.5], window_name=None):
		request = {
			"o3d_init": {
				"show_coor": show_coor,
				"bg_color": np2jsonMatrix(bg_color),
				"window_name": window_name
			}
		}
		self.append_request(request)
		return self

	def save(self, file_name=None, save_local=False):
		request = {
			"save": {
				"file_name": file_name,
			}
		}
		self.append_request(request)
		return self

	def draw_at(self, pos: int):
		request = {
			"draw_at": {
				"pos": pos
			}
		}
		self.append_request(request)
		return self

	@cast_tensor_to_numpy
	def add_pcd(self, point_cloud: np.ndarray, tsfm: np.ndarray = None):
		request = {
			"add_pcd": {
				"pcd": np2jsonMatrix(point_cloud),
				"tsfm": np2jsonMatrix(tsfm)
			}
		}
		self.append_request(request)
		return self
	
	@cast_tensor_to_numpy
	def add_color(self, colors: np.ndarray):
		request = {
			"add_color": {
				"colors": np2jsonMatrix(colors),
			}
		}
		self.append_request(request)
		return self
	
	@cast_tensor_to_numpy
	def add_lines(self, starts: np.ndarray, ends: np.ndarray, color: list = [], colors: np.ndarray = None):
		request = {
			"add_lines": {
				"starts": np2jsonMatrix(starts),
				"ends": np2jsonMatrix(ends),
				"colors": np2jsonMatrix(colors),
			}
		}
		self.append_request(request)
		return self
	
	@cast_tensor_to_numpy
	def add_normal(self, normals: np.ndarray=None, normal_length_ratio: float=0.05):
		return self

	@cast_tensor_to_numpy
	def add_mesh(self, vertices: np.ndarray, triangles: np.ndarray, colors: np.ndarray=None, normals: np.ndarray=None, tsfm: np.ndarray=None):
		request = {
			"add_mesh": {
				"vertices": np2jsonMatrix(vertices),
				"triangles": np2jsonMatrix(triangles),
				"colors": np2jsonMatrix(colors),
				"normals": np2jsonMatrix(normals),
				"tsfm": np2jsonMatrix(tsfm)
			}
		}
		self.append_request(request)
		return self

	def hint(self, text: str, color: list=[0, 1, 0], scale: float=1.5):
		request = {
			"hint": {
				"text": text,
				"color": np2jsonMatrix(color),
				"scale": scale,
			}
		}
		self.append_request(request)
		return self

	def show(self):
		try:
			# Prepare JSON data
			json_data = {"requests": self.request_pool}
			data = json.dumps(json_data).encode('utf-8')
			
			# Create HTTP request
			req = urllib.request.Request(
				self.server_url,
				data=data,
				headers={'Content-Type': 'application/json'}
			)
			
			# Send request and get response
			with urllib.request.urlopen(req) as response:
				response_data = json.loads(response.read().decode('utf-8'))
				status = "ok" if response_data.get("status", {}).get("ok", False) else "failed"
				print(f"Visualization session: {status}.")
		except urllib.error.URLError as e:
			print(f"Failed to connect to server: {e}")
		except Exception as e:
			print(f"Error during visualization: {e}")
		finally:
			return super().show(save_params=False)
