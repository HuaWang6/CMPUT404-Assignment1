#  coding: utf-8 
import socketserver
import os


# Copyright 2023 Hua Wang
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        request = self.data.decode("utf-8");
        request_lines = request.splitlines()
        print(request_lines)
        
        info = request_lines[0].split(" ")
        command = info[0]
        url = info[1]
        http = info[2]
        #check whether file is a css file or not
        css_file = False 

        #command is not GET
        if(command != "GET"):
            response = http + " 405 Method Not Allowed\r\n"
            response += "\r\n"
            self.request.send(response.encode("utf-8"))
        else:
            
            
            # correct the path with no / end by 301 
            if(url[-5:] != ".html" and url[-1] != "/" and url[-4:] != ".css"):
                response = http + " 301 Moved Permanently\r\n"
                response += "Location: "
                response += url
                response += "/\r\n" #add "/"
                self.request.send(response.encode("utf-8"))
                
             
            #if path end with "/" , give index.html content 
            if(url[-1] == "/"):
                url += "index.html"
                
            #file is css file
            if(url[-4:] == ".css"):
                css_file = True
                
            #read file content   
            try:
                f = open(os.getcwd() + "/www" + url,"rb")
            except:
                response = http + " 404 Not Found\r\n"
                response += "\r\n"
                self.request.send(response.encode("utf-8"))
            else:
                html_content = f.read()
                f.close()
                response = http + " 200 OK\r\n"
                
                # supports mime-types
                if(css_file):
                    response += "Content-Type: text/css\r\n"
                else:
                    response += "Content-Type: text/html\r\n"
                response += "\r\n"
                self.request.send(response.encode("utf-8"))
                self.request.send(html_content)
            


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
