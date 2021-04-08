from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

from utils.showMessage import showGood
from utils.fileReader import readFile
from utils.headersBuilder import bHeaders
from utils.logsController import writeLogs

from HTTPServer.handlerCaller import callHanlder
from HTTPServer.securityHeaders import buildHeaders

from main import buildConfig
from config.routes import routes
from config.ct import __CT__

from config.settings import STATIC_PATH, BLOCKED_PATHS

class serverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.securityHeaders = buildHeaders()
        self.realPath = self.path.replace('//' , '/')
        self.applicationConfig = buildConfig()
        self.requestHeaders = bHeaders(self.headers)

        self.requestHeaders['client-ip'] = self.client_address[0]
        self.requestHeaders['request-method'] = "GET"

        if self.realPath[-1:] == "/" and len(self.realPath) > 1:
            self.realPath = self.realPath[:-1]

        if self.realPath == "/":
            try:
                serverHandler = routes['/']
                Content, Headers, Code = callHanlder(serverHandler, self.requestHeaders)

                self.send_response(Code)
                if len(Headers) != 0:
                    for serverHeader,headerValue in Headers.items():
                        self.send_header(serverHeader, headerValue)

                for serverHeader, headerValue in self.securityHeaders.items():
                    self.send_header(serverHeader , headerValue)

                self.end_headers()
                self.wfile.write(Content.encode())
                writeLogs(clientIP=self.requestHeaders['client-ip'], userAgent=self.requestHeaders['user-agent'], endpointVisited=self.realPath, responseCode=Code, requestMethod=self.requestHeaders['request-method'])
            except Exception as e:
                Content, Headers, Code = callHanlder("500Handler.py", self.requestHeaders)

                self.send_response(Code)

                if len(Headers) != 0:
                    for serverHeader,headerValue in Headers.items():
                        self.send_header(serverHeader, headerValue)

                for serverHeader, headerValue in self.securityHeaders.items():
                    self.send_header(serverHeader , headerValue)

                self.end_headers()
                self.wfile.write(Content.encode())
                writeLogs(clientIP=self.requestHeaders['client-ip'], userAgent=self.requestHeaders['user-agent'], endpointVisited=self.realPath, responseCode=Code, requestMethod=self.requestHeaders['request-method'])
        elif self.realPath[:len(STATIC_PATH)].replace('/', '') == STATIC_PATH.replace('/', ''):
            # static content should be served
            fileExtension = "".join(self.realPath.split('.')[-1:])

            try:
                contentType = __CT__[fileExtension]
            except Exception:
                contentType = "text/plain"

            responseContent = readFile(self.realPath[1:])

            if not responseContent:
                Content, Headers, Code = callHanlder("404Handler.py", self.requestHeaders)

                self.send_response(Code)

                if len(Headers) != 0:
                    for serverHeader,headerValue in Headers.items():
                        self.send_header(serverHeader, headerValue)

                for serverHeader, headerValue in self.securityHeaders.items():
                    self.send_header(serverHeader , headerValue)

                self.end_headers()
                self.wfile.write(Content.encode())
                writeLogs(clientIP=self.requestHeaders['client-ip'], userAgent=self.requestHeaders['user-agent'], endpointVisited=self.realPath, responseCode=Code, requestMethod=self.requestHeaders['request-method'])
            elif responseContent == True:
                Content, Headers, Code = callHanlder("403Handler.py", self.requestHeaders)

                self.send_response(Code)

                if len(Headers) != 0:
                    for serverHeader,headerValue in Headers.items():
                        self.send_header(serverHeader, headerValue)

                for serverHeader, headerValue in self.securityHeaders.items():
                    self.send_header(serverHeader , headerValue)

                self.end_headers()
                self.wfile.write(Content.encode())
                writeLogs(clientIP=self.requestHeaders['client-ip'], userAgent=self.requestHeaders['user-agent'], endpointVisited=self.realPath, responseCode=Code, requestMethod=self.requestHeaders['request-method'])
            else:
                self.send_response(200)
                self.send_header('content-type', contentType)

                for serverHeader, headerValue in self.securityHeaders.items():
                    self.send_header(serverHeader , headerValue)

                self.end_headers()
                self.wfile.write(responseContent.encode())
                writeLogs(clientIP=self.requestHeaders['client-ip'], userAgent=self.requestHeaders['user-agent'], endpointVisited=self.realPath, responseCode=200, requestMethod=self.requestHeaders['request-method'])
        else:
            if self.realPath[-1:] == "/":
                checkString = self.realPath[:-1]
            else:
                checkString = self.realPath

            if checkString in BLOCKED_PATHS:
                Content, Headers, Code = callHanlder("403Handler.py", self.requestHeaders)

                self.send_response(Code)

                if len(Headers) != 0:
                    for serverHeader,headerValue in Headers.items():
                        self.send_header(serverHeader, headerValue)

                for serverHeader, headerValue in self.securityHeaders.items():
                    self.send_header(serverHeader , headerValue)

                self.end_headers()
                self.wfile.write(Content.encode())
                writeLogs(clientIP=self.requestHeaders['client-ip'], userAgent=self.requestHeaders['user-agent'], endpointVisited=self.realPath, responseCode=Code, requestMethod=self.requestHeaders['request-method'])
            else:
                try:
                    serverHandler = routes[self.realPath]
                    Content, Headers, Code = callHanlder(serverHandler, self.requestHeaders)

                    self.send_response(Code)
                    if len(Headers) != 0:
                        for serverHeader,headerValue in Headers.items():
                            self.send_header(serverHeader, headerValue)

                    for serverHeader, headerValue in self.securityHeaders.items():
                        self.send_header(serverHeader , headerValue)

                    self.end_headers()
                    self.wfile.write(Content.encode())
                    writeLogs(clientIP=self.requestHeaders['client-ip'], userAgent=self.requestHeaders['user-agent'], endpointVisited=self.realPath, responseCode=Code, requestMethod=self.requestHeaders['request-method'])
                except Exception as e:
                    Content, Headers, Code = callHanlder("404Handler.py", self.requestHeaders)

                    self.send_response(Code)

                    if len(Headers) != 0:
                        for serverHeader,headerValue in Headers.items():
                            self.send_header(serverHeader, headerValue)

                    for serverHeader, headerValue in self.securityHeaders.items():
                        self.send_header(serverHeader , headerValue)

                    self.end_headers()
                    self.wfile.write(Content.encode())
                    writeLogs(clientIP=self.requestHeaders['client-ip'], userAgent=self.requestHeaders['user-agent'], endpointVisited=self.realPath, responseCode=Code, requestMethod=self.requestHeaders['request-method'])

def serveServer(serverPort, defaultDocument):
    httpServer = HTTPServer(('' , serverPort), serverHandler)
    showGood(goodRule="Server Created" , Message=f"The Server is Running Successfully On Port {serverPort}")
    httpServer.serve_forever()
