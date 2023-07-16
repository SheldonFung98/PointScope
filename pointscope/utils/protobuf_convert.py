import numpy as np
from ..protos import pointscope_pb2


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