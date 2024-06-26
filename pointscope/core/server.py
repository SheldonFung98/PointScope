import grpc
from concurrent import futures
from pointscope.protos import pointscope_pb2_grpc
from .pointscope_service import PointScopeServicer
import logging

MAX_MESSAGE_LENGTH = 100*1024*1024

class PointScopeServer:

    def __init__(self, ip="0.0.0.0", port="50051"):
        self.ip = ip
        self.port = port

    def run(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10), 
            options = [
                ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)
            ])
        
        
        pointscope_pb2_grpc.add_PointScopeServicer_to_server(
            PointScopeServicer(), server)

        server.add_insecure_port(f'{self.ip}:{self.port}')
        server.start()
        logging.info(f"Start PointScope gRPC service at {self.ip}:{self.port}")
        try:
            server.wait_for_termination()
        except KeyboardInterrupt:
            logging.info("Exit.")
            