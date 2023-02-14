import torch
import numpy as np
import open3d as o3d
from d3tool.vis3d_ani import Vis3D
from d3tool.utils.shapeGen import make_cube
from pytorch3d.transforms import (quaternion_to_matrix, matrix_to_quaternion, 
                                  quaternion_multiply, quaternion_apply, 
                                  quaternion_invert, random_quaternions)


def decomposite_quat(q):
    scaler, vector = q[:, :1], q[:, 1:]
    angle = torch.acos(scaler)
    axis = vector / torch.sin(angle)
    return angle, axis



source = make_cube()
target = source.copy()

q_gt = random_quaternions(n=1)
q_rand = random_quaternions(n=1)

src_color = np.zeros_like(source)
tgt_color = np.zeros_like(source)
tgt_color[:, 1] = 1

target = quaternion_apply(q_gt, torch.tensor(target)).numpy()
source_rand_trans = quaternion_apply(q_rand, torch.tensor(source)).numpy()
source_rand_trans_color = np.zeros_like(source_rand_trans)
source_rand_trans_color[:, 0] = 1

# source is black
# target is green
# random transformed source is red
angle_gt, axis_gt = decomposite_quat(q_gt)
angle_rand, axis_rand = decomposite_quat(q_rand)


vis = Vis3D(target).add_color(tgt_color)
vis.add_pcd(source).add_color(src_color)
vis.add_pcd(source_rand_trans).add_color(source_rand_trans_color)
vis.show()
