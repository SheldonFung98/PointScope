import open3d as o3d
import numpy as np
from pointscope.vis3d_ani import Vis3DAni
from PIL import Image


o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)

def anti_guassian(x):
    maxmum = 100
    minimum = 0
    y = maxmum*(1-np.exp(-np.square(x-50)/np.square(20)))
    y=np.clip(y, a_min=minimum, a_max=maxmum)
    y /= y.sum() # normalize
    return y

region = np.arange(100)
source = source = np.random.choice(region, (10000, 3), p=anti_guassian(region)) / 100
target = source.copy()
target_pcd = o3d.geometry.PointCloud()
target_pcd.points = o3d.utility.Vector3dVector(target)

target_pcd.estimate_normals(
search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

trans = np.array([[0.862, 0.011, -0.507], 
                [-0.139, 0.967, -0.215],
                [0.487, 0.255, 0.835]])
source = source.dot(trans)

def update(current_pcd):
    def callback(vis):
        # global current_pcd
        threshold = 0.4
        reg_p2l = o3d.pipelines.registration.registration_icp(
            current_pcd, target_pcd, threshold, np.identity(4),
            o3d.pipelines.registration.TransformationEstimationPointToPoint(),
            o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=1))
        
        current_pcd.transform(reg_p2l.transformation)
        vis.update_geometry(current_pcd)
        
    return callback


src_color = np.ones_like(source)
src_color[:, :] = 0
Vis3DAni(target_pcd.points).add_pcd(source).add_color(src_color).add_animation(update).show().save()
