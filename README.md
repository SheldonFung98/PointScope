<div align="center">
    <img src="assets/logo.png" alt="logo">
    <h1>PointScope</h1>
</div>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

PointScope is a tool aiming to help 3D computer vision researcher to visulize 3D point cloud easily. 

It provides:
- Point cloud visualization with one-liner style command.
- Visualize point cloud locally or remotely.
- Easy to switch backend (Open3D/Vedo).
- Auto-save camera perspective.
- Savable visualization session.

## Dependencies
* Numpy 
* Open3D
* vedo
* grpc

## Installation
Use conda environment (optional)
```
conda create --name psc python==3.8
conda activate psc
```
Install via Github
```
pip3 install git+https://github.com/SheldonVon98/PointScope.git
```

## Usage
Initiate some variables for visulization
```
import numpy as np
point_cloud = np.random.random((1000, 3))
point_cloud_color = np.random.random((1000, 3))
point_cloud_normal = np.random.random((1000, 3))
another_pcd = np.random.random((30000, 3))*2+np.array([-0.5, -0.5, 2.0])
```
### Local Visualization
```
from pointscope import PointScopeO3D as PSC     # Use Open3D backend
# from pointscope import PointScopeVedo as PSC  # Use Vedo backend
```
Visualize point cloud with color.
```
PSC().add_pcd(point_cloud).add_color(point_cloud_color).show() 
```
Visualize point cloud with normal.
```
PSC().add_pcd(point_cloud).add_normal(point_cloud_normal).show() 
```
Visualize point cloud with both.
```
PSC().add_pcd(point_cloud).add_color(point_cloud_color).add_normal(point_cloud_normal).show() 
```

### Remote Visualization
Start a reverse tunnel with ssh
```
ssh RemoteServer -N -R 50051:0.0.0.0:50051
```
Start PointScope server
```
python3 -m pointscope --server
```
Start PointScope clinet
```
from pointscope import PointScopeClient as PSC

# Use Open3D backend
PSC().o3d(show_coor=False, bg_color=[0.2, 0.3, 0.3]) \
    .add_pcd(point_cloud).add_color(np.zeros_like(point_cloud))\
    .add_pcd(another_pcd)\
    .add_lines(point_cloud[:20], another_pcd[:20]) \
    .show()

# Use Vedo backend
PSC().vedo(subplot=2, bg_color=[0.2, 0.3, 0.3]) \
    .add_pcd(point_cloud).add_color(np.zeros_like(point_cloud))\
    .add_pcd(another_pcd)\
    .draw_at(1) \
    .add_pcd(point_cloud).add_color(np.zeros_like(point_cloud))\
    .add_pcd(another_pcd)\
    .add_lines(point_cloud[:20], another_pcd[:20]) \
    .show()
```

### Visualize PCD in Terminal 
```
# Force the file format 'txt' to be 'xyzn' 
python3 -m pointscope --show pointcloud_1.txt:xyzn airplane_0002.ply

# Show them remotely
python3 -m pointscope --remote --show pointcloud_1.txt:xyzn airplane_0002.ply
```

### Saving & Loading Visulization
This functionality is supported by both local and remote visualization.
```
PSC().add_pcd(point_cloud).add_color(np.zeros_like(point_cloud))\
    .add_pcd(another_pcd)\
    .add_lines(point_cloud[:20], another_pcd[:20]) \
    .show() \
    .save() # Add this line to save the whole session.
```
```
# Load the visualization session.
python3 -m pointscope --load PointScope_2023-08-02T01:01:12.pkl
```



## Call for Contributions
The PointScope project welcomes your expertise and enthusiasm!
