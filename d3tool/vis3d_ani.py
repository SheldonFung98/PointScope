from d3tool import Vis3D
import open3d as o3d
import numpy as np
from PIL import Image


class Vis3DAni(Vis3D):
    
    images = []
    callback = None
    
    def __init__(self, point_cloud: np.ndarray = None):

        self.vis = o3d.visualization.VisualizerWithKeyCallback()
        self.vis.create_window()
        if point_cloud is not None:
            self.add_pcd(point_cloud)
            
    def callback_wrap(self, vis):
        self.callback(vis)
        image = vis.capture_screen_float_buffer()
        image = np.uint8(np.array(image)*255)
        self.images.append(Image.fromarray(image))
        
    def add_animation(self, afunc, trigger='a'):
        key = ord(trigger)-32
        self.callback = afunc(self.current_pcd)
        self.vis.register_key_callback(key=key, callback_func=self.callback_wrap)
        return self
    
    def save(self, name="image.gif"):
        print("Saving GIF...")
        img = next(iter(self.images))
        img.save(fp=name, format='GIF', append_images=self.images,
                save_all=True, duration=200, loop=0)
        print("Saved to {}.".format(name))
    
    def show(self):
        while self.vis.poll_events():
            self.vis.update_renderer()
        self.vis.destroy_window()
        return self