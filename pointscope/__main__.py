from .core import PointScopeServer
import argparse
import logging
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

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
    
args = parser.parse_args()

if args.server:
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