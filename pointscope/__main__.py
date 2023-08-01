import argparse
import sys


parser = argparse.ArgumentParser(
    description=
    "This module can be run from the command line to start an external visualizer window.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    "--server",
    action="store_true",
    help="Starts the external visualizer with the RPC interface"
)
parser.add_argument(
    "--show",
    nargs='+', default=list(),
    help="Ahow a list of point cloud from files. To manually force a format: pointcloud.txt:xyz"
)
parser.add_argument(
    "--remote",
    action="store_true",
    help="Show point cloud remotely."
)
parser.add_argument("-ip", type=str, default="0.0.0.0", help="Set ip address.")
parser.add_argument("-port", type=str, default="50051", help="Set port.")
parser.add_argument(
    "--load", 
    type=str, 
    help="Load process."
)

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
    
args = parser.parse_args()

if args.server:
    import logging
    from .core import PointScopeServer
    FORMAT = '[%(levelname)s] %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    PointScopeServer(ip=args.ip, port=args.port).run()

elif len(args.show):
    files_num = len(args.show)
    if args.remote:
        from pointscope import PointScopeClient as PSC
        psc = PSC().vedo(subplot=files_num)
    else:
        from pointscope import PointScopeVedo as PSC
        psc = PSC(subplot=files_num)
    for index, file_path in enumerate(args.show):
        file_path = file_path.split(":")
        file_path, force_format = file_path if len(file_path) == 2 else (file_path[0], "auto")
        psc.draw_at(index).add_pcd_from_file(file_path, force_format)
    psc.show()

elif args.load:
    import pickle
    import importlib
    with open(args.load, 'rb') as pickle_file:
        ps_sequence = pickle.load(pickle_file)
    ps_class, ps_args = next(iter(ps_sequence["ps_init"].items()))
    psc = getattr(importlib.import_module("pointscope"), ps_class)(**ps_args)
    for command in ps_sequence["commands"]:
        cmd_func, func_args = next(iter(command.items()))
        getattr(psc, cmd_func)(**func_args)
    psc.show()
