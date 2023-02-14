import numpy as np


def make_cube():
    region = np.arange(100)
    surface = np.random.choice(region, (1000, 3)) / 100
    surface1 = np.zeros_like(surface)
    surface1[:, :2] = surface[:, :2]
    surface1_o = surface1.copy()
    surface1_o[:, 2:] = 1
    surface2 = np.zeros_like(surface)
    surface2[:, 1:3] = surface[:, 1:3]
    surface2_o = surface2.copy()
    surface2_o[:, :1] = 1
    surface3 = np.zeros_like(surface)
    surface3[:, :1] = surface[:, :1]
    surface3[:, -1:] = surface[:, -1:]
    surface3_o = surface3.copy()
    surface3_o[:, 1:2] = 1
    cube = np.concatenate([surface1, surface1_o, 
                           surface2, surface2_o, 
                           surface3, surface3_o])
    return cube

