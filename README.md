<div align="center">
    <img src="assets/logo.png" alt="logo">
    <h1>PointScope</h1>
</div>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

PointScope is a tool aiming to help 3D computer vision researcher to visulize 3D point cloud. 

It provides:
- Point cloud visualization with one-liner style command.
- Visualize point cloud locally or remotely.
- Easy to switch backend (Open3D/Vedo).


## Dependencies
----------------------
* Numpy 
* Open3D
* vedo
* grpc

## Installation
----------------------
```
git clone https://github.com/SheldonVon98/PointScope.git
cd PointScope
pip3 install -e .
```

## Usage
----------------------
### Local Visualization with Open3D backend
```
from pointscope import PointScopeO3D

point_cloud = np.random.random((10, 3))
point_cloud_color = np.random.random((10, 3))
point_cloud_normal = np.random.random((10, 3))

PointScopeO3D().add_pcd(point_cloud).add_color(point_cloud_color).show() # Visualize point cloud with color

PointScopeO3D().add_pcd(point_cloud).add_label(point_cloud_label).show() # Visualize point cloud with label

PointScopeO3D().add_pcd(point_cloud).add_normal(point_cloud_normal).show() # Visualize point cloud with normal

PointScopeO3D().add_pcd(point_cloud).add_color(point_cloud_color).add_normal(point_cloud_normal).show() # Visualize point cloud with color along with normal
```

### Remote Visualization with Open3D backend
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
python3 test/test_pointscope_client.py
```

## Call for Contributions
----------------------

The PointScope project welcomes your expertise and enthusiasm!
