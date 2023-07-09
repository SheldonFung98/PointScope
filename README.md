# PointScope
PointScope is a tool aiming to help 3D computer vision researcher to visulize 3D point cloud. With PointScope you can easily visualize point cloud locally or remotely with one-liner style command.

## Dependencies
* Numpy 
* Open3D
* grpc

## Installation
```
git clone https://github.com/SheldonVon98/PointScope.git
cd PointScope
pip3 install -e .
```

## Local Visualization with Open3D backend
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

