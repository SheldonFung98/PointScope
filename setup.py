from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.build_py import build_py


class CustomBuildCommand(build_py):
    
    def run(self):
        self.generate_protos()
        build_py.run(self)

    def generate_protos(self):
        from grpc_tools import _protoc_compiler
        base_path = "pointscope"
        grpc_gen_path = os.path.join(base_path, "protos")
        _protoc_compiler.run_main([i.encode() for i in [
            '', '-I.', '--python_out=.', '--grpc_python_out=.',
            os.path.join(grpc_gen_path, "pointscope.proto")
        ]])
        
setup(
    name='PointScope',
    python_requires=">=3",
    version='0.1.0',
    author="Sheldon Fung",
    url="https://github.com/SheldonVon98/PointScope",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.23.5',
        'open3d>=0.17.0',
        'grpcio>=1.56.0',
        'vedo>=2023.4.4',
        'grpcio-tools'
    ],
    setup_requires=[
        'grpcio-tools'
    ],
    cmdclass={
        'build_py': CustomBuildCommand,
    }
)