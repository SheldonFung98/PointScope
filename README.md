# 3DTools
3D Data Processing Tools Collection 

## Dependencies
* Numpy 
* Open3D

## Installation
```
git clone https://github.com/SheldonVon98/D3Tools.git
cd D3Tools
pip3 install -e .
```

## Vis3D
import package
```
from d3tool import Vis3D
# from d3tool import Vis3DWeb # Alternatively, you can use web visulizer.
```
Define some variables for illustration
```
point_cloud = np.random.random((10, 3))
point_cloud_color = np.random.random((10, 3))
point_cloud_normal = np.random.random((10, 3))
```
Visualize point cloud with color
```
Vis3D(point_cloud).add_color(point_cloud_color).show()
# Vis3DWeb(point_cloud).add_color(point_cloud_color).show()
```

Visualize point cloud with label
```
Vis3D(point_cloud).add_label(point_cloud_label).show()
# Vis3D(point_cloud).add_label(point_cloud_label).show()
```

Visualize point cloud with normal
```
Vis3D(point_cloud).add_normal(point_cloud_normal).show()
# Vis3D(point_cloud).add_normal(point_cloud_normal).show()
```

Visualize point cloud with color along with normal
```
Vis3D(point_cloud).add_color(point_cloud_color).add_normal(point_cloud_normal).show()
# Vis3D(point_cloud).add_color(point_cloud_color).add_normal(point_cloud_normal).show()
```