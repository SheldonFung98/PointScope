import argparse
import sys
from pointscope.core.server import PointScopeServer
from pointscope.core.pointscope_o3d import PointScopeO3D
import logging
import asyncio


parser = argparse.ArgumentParser(
    description=
    "This module can be run from the command line to start an external visualizer window.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    "--server",
    action="store_true",
    help="Starts the external visualizer with the RPC interface"
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