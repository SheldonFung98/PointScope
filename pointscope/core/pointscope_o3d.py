from .base import PointScopeScaffold
import open3d as o3d
import numpy as np
import logging


class PointScopeO3D(PointScopeScaffold):

    
    def __init__(self,
                 show_coor=True, 
                 bg_color=[0.5, 0.5, 0.5],
                 window_name=None,
                 vis=None, 
                 vis_params=None) -> None:
        super().__init__(__class__.__name__, dict(
            show_coor=show_coor, 
            bg_color=bg_color,
            window_name=window_name,
            vis=vis
        ), vis_params)
        self.vis = vis if vis is not None else o3d.visualization.Visualizer()
        window_name = window_name if window_name else self.__class__.__name__
        if self.params["window_params"]:
            self.vis.create_window(
                window_name=window_name,
                width=self.params["window_params"]["width"],
                height=self.params["window_params"]["height"],
            )
        else:
            self.vis.create_window(window_name=window_name)
        opt = self.vis.get_render_option()
        opt.show_coordinate_frame = show_coor
        opt.background_color = np.asarray(bg_color)

    def show(self, save_params=True):
        ctr = self.vis.get_view_control()
        if self.params["perspective"] and self.params["window_params"]:
            camera_params = o3d.camera.PinholeCameraParameters()
            camera_params.extrinsic = self.params["perspective"]["extrinsic"]
            camera_params.intrinsic = o3d.camera.PinholeCameraIntrinsic(
                width=self.params["window_params"]["width"],
                height=self.params["window_params"]["height"],
                intrinsic_matrix=self.params["perspective"]["intrinsic"]
            )
            ctr.convert_from_pinhole_camera_parameters(camera_params)

        while self.vis.poll_events():
            self.vis.update_renderer()
            
        camera_params = ctr.convert_to_pinhole_camera_parameters()
        self.params["perspective"] = dict(
            intrinsic=camera_params.intrinsic.intrinsic_matrix,
            extrinsic=camera_params.extrinsic
        )
        self.params["window_params"] = dict(
            height=camera_params.intrinsic.height,
            width=camera_params.intrinsic.width,
        )
        self.vis.destroy_window()
        return super().show(save_params)

    def draw_at(self, pos: int):
        logging.warning(f"draw_at is not implemented in {self.__class__.__name__}.")
        return super().draw_at(pos)

    def add_pcd(self, point_cloud: np.ndarray, tsfm: np.ndarray = None):
        """Add a new point cloud to visulize.
        
        Note that all the following operations would focus on
        the added point cloud. An additional argument tsfm can
        be added to transform the point cloud.
        
        Args:
            point_cloud (np.ndarray): (n, 3)
            tsfm (np.ndarray): (4, 4) 
        """
        pcd_input = point_cloud.copy()
        self.current_pcd = o3d.geometry.PointCloud()
        self.current_pcd.points = o3d.utility.Vector3dVector(point_cloud)
        if tsfm is not None:
            self.current_pcd.transform(tsfm)
        self.current_pcd.estimate_normals()
        self.vis.add_geometry(self.current_pcd)
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
            return super().add_color(colors)

        assert colors.shape == self.curr_pcd_np.shape
        
        if colors.max() > 1.0:
            colors = np.asarray(colors, dtype=np.float32) / 255
            
        self.current_pcd.colors = o3d.utility.Vector3dVector(colors)
        return super().add_color(colors_input)
    
    def add_normal(self, normals: np.ndarray = None, normal_length_ratio: float = 0.05):
        """Add normals to current point cloud.
        
        normal should match the shape of the corresponding 
        point cloud.

        Args:
            normals (np.ndarray): (n, 3)
        """
        if normals is None:
            normals = np.asarray(self.current_pcd.normals)
        
        assert normals.shape == self.curr_pcd_np.shape
        start = self.curr_pcd_np
        end = self.curr_pcd_np + normals*normal_length_ratio
        self.add_lines(start, end, color=[1, 0, 0])
        return super().add_normal(normals, normal_length_ratio)
    
    def add_lines(self, starts: np.ndarray, ends: np.ndarray, color: list = [1, 0, 0], colors: np.ndarray = None):
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
            colors = np.asarray([color for i in range(len(lines))])
        else:
            assert starts.shape == colors.shape
            
        line_set = o3d.geometry.LineSet(
            points=o3d.utility.Vector3dVector(np.concatenate((starts, ends))),
            lines=o3d.utility.Vector2iVector(lines),
        )
        line_set.colors = o3d.utility.Vector3dVector(colors)
        self.vis.add_geometry(line_set)
        return super().add_lines(starts, ends, color, colors)
    