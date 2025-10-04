import json
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from .pointscope_service import PointScopeServicer

class PointScopeHTTPHandler(BaseHTTPRequestHandler):
    """HTTP request handler for PointScope visualization requests."""
    
    def __init__(self, servicer, *args, **kwargs):
        self.servicer = servicer
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        """Handle POST requests containing visualization commands."""
        try:
            # Parse the request path
            parsed_path = urlparse(self.path)
            
            if parsed_path.path == '/visualization_session':
                # Read the content length and request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                # Parse JSON data
                request_data = json.loads(post_data.decode('utf-8'))
                
                # Process the visualization session
                response = self.servicer.visualization_session(request_data)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                # Unknown endpoint
                self.send_response(404)
                self.end_headers()
                
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {"status": {"ok": False, "error": str(e)}}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to use logging instead of printing to stderr."""
        logging.info(f"{self.address_string()} - {format % args}")

class PointScopeServer:

    def __init__(self, ip="0.0.0.0", port=50051):
        self.ip = ip
        self.port = int(port)  # Ensure port is integer for HTTP server
        self.servicer = PointScopeServicer()

    def run(self):
        # Create a custom handler factory that includes the servicer
        def handler_factory(*args, **kwargs):
            return PointScopeHTTPHandler(self.servicer, *args, **kwargs)
        
        # Create and start the HTTP server
        server = HTTPServer((self.ip, self.port), handler_factory)
        
        logging.info(f"Start PointScope HTTP service at {self.ip}:{self.port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            logging.info("Exit.")
            server.shutdown()
            