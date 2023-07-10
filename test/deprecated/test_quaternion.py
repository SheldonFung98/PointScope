import open3d as o3d
import numpy as np
from pointscope.vis3d_ani import Vis3DAni
from PIL import Image
import torch
from pytorch3d.transforms import (quaternion_to_matrix, 
                                  matrix_to_quaternion, 
                                  quaternion_multiply, 
                                  quaternion_apply)



o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)

def anti_guassian(x):
    maxmum = 100
    minimum = 0
    y = maxmum*(1-np.exp(-np.square(x-50)/np.square(20)))
    y=np.clip(y, a_min=minimum, a_max=maxmum)
    y /= y.sum() # normalize
    return y

region = np.arange(100)
source = np.random.choice(region, (10000, 3), p=anti_guassian(region)) / 100

# source -= 0.5

target = source.copy()
target_pcd = o3d.geometry.PointCloud()
target_pcd.points = o3d.utility.Vector3dVector(target)

target_pcd.estimate_normals(
search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

# trans = np.array([[0.862, 0.011, -0.507], 
#                 [-0.139, 0.967, -0.215],
#                 [0.487, 0.255, 0.835]])
# source = source.dot(trans)

source_pt = torch.from_numpy(source)

angle = 0
axis = [2, 0, 0]

def getQuaternion(angle, axis):
    angle = torch.tensor([angle])
    scaler = torch.cos(angle)
    axis = torch.tensor(axis)
    axis = torch.square(axis) / torch.sum(torch.square(axis))
    vector = torch.sin(angle) * axis
    return torch.concat([scaler, vector])

def update(current_pcd):
    def callback(vis):
        global angle
        angle += torch.pi / 36
        q = getQuaternion(angle, axis)
        print(q)
        source_trans = quaternion_apply(q, source_pt)
        current_pcd.points = o3d.utility.Vector3dVector(source_trans) 

        vis.update_geometry(current_pcd)

        
    return callback


src_color = np.ones_like(source)
src_color[:, :] = 0
Vis3DAni(target_pcd.points).add_pcd(source).add_color(src_color).add_animation(update).show().save()
