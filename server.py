from http.server import BaseHTTPRequestHandler, HTTPServer
from api import API
from search import search
import time

hostName = "localhost"
serverPort = 8080
api = API()

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if not self.path.startswith("/api/"):
            returnStaticPage(self)
            return
        
        elif self.path.startswith("/api/network?origin="):
            origin = self.path.removeprefix("/api/network?origin=")
            json = api.getNetwork(origin)
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.end_headers()
            self.wfile.write(bytes(json, "utf-8"))
            return
        
        
def returnStaticPage(handler):
    handler.send_response(200)
    handler.send_header("Content-type", "text/html")
    handler.end_headers()
    filename = handler.path[1:]
    if filename == "":
        handler.wfile.write(bytes(fileToString("index.html"), "utf-8"))
    else:
        handler.wfile.write(bytes(fileToString(filename), "utf-8"))

def fileToString(filename):
    with open(filename, 'r') as file:
        return file.read()
    
if __name__ == "__main__":  
    search("madagascar", 2, 25) 
    server = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("Server stopped.")