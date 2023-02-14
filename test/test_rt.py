import open3d as o3d
import numpy as np
from d3tool.vis3d_ani import Vis3DAni
from PIL import Image
import torch
from d3tool.utils.shapeGen import make_cube
from pytorch3d.transforms import (quaternion_to_matrix, 
                                  matrix_to_quaternion, 
                                  quaternion_multiply, 
                                  quaternion_apply, 
                                  random_rotation)



o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)


source = make_cube()
# source -= 0.5

target = source.copy()

source_pt = torch.from_numpy(source)

source_weights = np.zeros_like(source)
source_weights[:1000, :] = 1/1000


# source_gravity = source_pt.mean(0)
source_gravity = (source_pt * source_weights).sum(0)

def update(current_pcd):
    def callback(vis):
        
        rot = random_rotation(dtype=torch.float64)
        source_shift = source_pt - source_gravity
        source_trans = torch.mm(source_shift, rot)
        source_trans += source_gravity
        current_pcd.points = o3d.utility.Vector3dVector(source_trans) 

        vis.update_geometry(current_pcd)

    return callback


src_color = source_weights*500
src_color[:, :1] = 0

target_color = np.ones_like(target)
target_color[:, :] = 0.5

Vis3DAni(target).add_color(target_color).add_pcd(source).add_color(src_color).add_animation(update).show().save()
