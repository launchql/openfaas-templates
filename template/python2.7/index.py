import os
import time
import json 
import BaseHTTPServer

from function import handler

hostName = "0.0.0.0"
PORT = int(os.environ['PORT'])

class FaasServer(BaseHTTPServer.BaseHTTPRequestHandler):
    def getHeader (s, header):
        # in python 3 this is different
        head = s.headers.getheaders(header)
        return head[0] if head else None
        
    def setJobHeaders(s):
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.send_header("X-Worker-Id", s.getHeader('X-Worker-Id'))
        s.send_header("X-Job-Id", s.getHeader('X-Job-Id'))
        s.end_headers()
    
    def sendError(s, msg):
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.send_header("X-Worker-Id", s.getHeader('X-Worker-Id'))
        s.send_header("X-Job-Id", s.getHeader('X-Job-Id'))
        s.send_header("X-Job-Error", True)
        s.end_headers()
        s.wfile.write(json.dumps({'message': msg}))
    
    def getReqParams(s):
        content_length = s.headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0
        
        if length > 0:
            content = s.rfile.read(length)
            return json.loads(content)
        else:
            return json.loads('{}')

    def do_POST(s):
        params = s.getReqParams()
        try:
            val = handler.handle(params)
            s.setJobHeaders()
            s.wfile.write(json.dumps(val))
        except Exception as e:
            s.sendError(str(e))

if __name__ == "__main__":        
    webServer = BaseHTTPServer.HTTPServer((hostName, PORT), FaasServer)
    print("Server started http://%s:%s" % (hostName, PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
