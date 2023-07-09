from setuptools import setup
import os
from grpc_tools import _protoc_compiler

base_path = "pointscope"
grpc_gen_path = os.path.join(base_path, "protos")
_protoc_compiler.run_main([i.encode() for i in [
    '', '-I.', '--python_out=.', '--pyi_out=.', '--grpc_python_out=.',
    os.path.join(grpc_gen_path, "pointscope.proto")
]])

setup(
    name='PointScope',
    python_requires=">=3",
    version='0.1.0',
    author="Sheldon Fung",
    url="https://github.com/SheldonVon98/PointScope",
    packages=[
        "pointscope",       
    ],
)