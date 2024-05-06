import os
import pickle
import numpy as np
from ..protos import pointscope_pb2

try:
    import torch
    TORCH_INSTALLED = True
except ImportError:
    TORCH_INSTALLED = False
    
    
def protoMatrix2np(protoMatrix):
    np_array = np.array(protoMatrix.data)
    if np_array.size:
        return np_array.reshape(protoMatrix.shape)
    else:
        return None

def np2protoMatrix(numpy_array):
    if isinstance(numpy_array, list):
        numpy_array = np.array(numpy_array)
    if numpy_array is None:
        return None
    message = pointscope_pb2.Matrix()
    message.shape.extend(numpy_array.shape)
    message.data.extend(numpy_array.flatten())
    return message

def load_pkl(path):
    if os.path.exists(path):
        with open(path, 'rb') as pickle_file:
            pkl_obj = pickle.load(pickle_file)
        return pkl_obj

def dump_pkl(path, data):
    with open(path, 'wb') as pickle_file:
        pickle.dump(data, pickle_file)

def tensor2numpy(*args, **kwargs):
    if TORCH_INSTALLED:
        args = list(args)
        for i in range(len(args)):
            if isinstance(args[i], torch.Tensor):
                args[i] = args[i].cpu().detach().numpy()
        for key, value in kwargs.items():
            if isinstance(value, torch.Tensor):
                kwargs[key] = value.cpu().detach().numpy()
    return args, kwargs

def cast_tensor_to_numpy(func):
    def wrapper(*args, **kwargs):
        args, kwargs = tensor2numpy(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper