import os
import time
import json 

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from function import handler

hostName = "0.0.0.0"
PORT = int(os.environ['PORT'])

class FaasServer(BaseHTTPRequestHandler):

    def setJobHeaders(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("X-Worker-Id", self.headers.get('X-Worker-Id'))
        self.send_header("X-Job-Id", self.headers.get('X-Job-Id'))
        self.end_headers()
    
    def sendError(self, msg):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("X-Worker-Id", self.headers.get('X-Worker-Id'))
        self.send_header("X-Job-Id", self.headers.get('X-Job-Id'))
        self.send_header("X-Job-Error", True)
        self.end_headers()
        self.wfile.write( bytes(json.dumps({'message': msg}), encoding='utf8') )
    
    def getReqParams(self):
        length = int(self.headers.get('content-length'))
        
        if length > 0:
            content = self.rfile.read(length)
            return json.loads(content)
        else:
            return json.loads('{}')

    def do_POST(self):
        params = self.getReqParams()
        try:
            val = handler.handle(params)
            self.setJobHeaders()
            self.wfile.write( bytes(json.dumps(val), encoding='utf8') )
        except Exception as e:
            self.sendError(str(e))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, PORT), FaasServer)
    print("Server started http://%s:%s" % (hostName, PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
