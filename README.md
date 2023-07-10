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


## Dependencies
* Numpy 
* Open3D
* vedo
* grpc

## Installation
```
git clone https://github.com/SheldonVon98/PointScope.git
cd PointScope
pip3 install -e .
```

## Usage
Initiate some variables for visulization
```
import numpy as np
point_cloud = np.random.random((1000, 3))
point_cloud_color = np.random.random((1000, 3))
point_cloud_normal = np.random.random((1000, 3))
```
### Local Visualization
```
from pointscope import PointScopeO3D as PSC     # Use Open3D backend
# from pointscope import PointScopeVedo as PSC  # Use Vedo backend

# Visualize point cloud with color.
PSC().add_pcd(point_cloud).add_color(point_cloud_color).show() 

# Visualize point cloud with normal.
PSC().add_pcd(point_cloud).add_normal(point_cloud_normal).show() 

# Visualize point cloud with both.
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
PSC().o3d() \ 
    .add_pcd(point_cloud) \
    .add_pcd(np.random.random((30000, 3))+np.array([1, 0, 0])) \
    .add_lines(np.random.random((10, 3)), np.random.random((10, 3))) \
    .show()

# Use Vedo backend
PSC().vedo() \
    .add_pcd(point_cloud) \
    .add_pcd(np.random.random((30000, 3))+np.array([1, 0, 0])) \
    .add_lines(np.random.random((10, 3)), np.random.random((10, 3))) \
    .show()
```

## Call for Contributions
The PointScope project welcomes your expertise and enthusiasm!
