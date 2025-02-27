from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        filename = self.path[1:]
        if filename == "":
            self.wfile.write(bytes(fileToString("index.html"), "utf-8"))
        else:
            self.wfile.write(bytes(fileToString(filename), "utf-8"))
        
def fileToString(filename):
    with open(filename, 'r') as file:
        return file.read()
    
if __name__ == "__main__":        
    server = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("Server stopped.")