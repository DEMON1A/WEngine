import sys
import os
import time
import threading

from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

from utils.showMessage import showGood
from utils.fileReader import readFile
from utils.headersBuilder import bHeaders
from utils.logsController import writeLogs

from utils.queryParser import parseQuery
from utils.queryParser import parsePath

from HTTPServer.handlerCaller import callHandler
from HTTPServer.securityHeaders import buildHeaders

from main import buildConfig
from config.routes import loadRoutes
from config.ct import __CT__

from config.settings import STATIC_PATH, BLOCKED_PATHS

class serverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.routes = loadRoutes()
        self.realPath = self.path.replace('//' , '/')
        self.realPath = parsePath(self.realPath)
        self.query = parseQuery(self.path)
        self.applicationConfig = buildConfig()
        self.requestHeaders = bHeaders(self.headers)
        self.securityHeaders = buildHeaders(self.requestHeaders)

        self.requestHeaders['client-ip'] = self.client_address[0]
        self.requestHeaders['request-method'] = "GET"

        if self.realPath[-1:] == "/" and len(self.realPath) > 1:
            self.realPath = self.realPath[:-1]

        if self.realPath == "/":
            try:
                serverHandler = self.routes['/']
                print(serverHandler)
                Content, Headers, Code = callHandler(serverHandler, self.requestHeaders, self.query)

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
                print(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

                Content, Headers, Code = callHandler("500Handler.py", self.requestHeaders, self.query)
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
                Content, Headers, Code = callHandler("404Handler.py", self.requestHeaders, self.query)

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
                Content, Headers, Code = callHandler("403Handler.py", self.requestHeaders, self.query)

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
                Content, Headers, Code = callHandler("403Handler.py", self.requestHeaders, self.query)

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
                    serverHandler = self.routes[self.realPath]
                    Content, Headers, Code = callHandler(serverHandler, self.requestHeaders, self.query)

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
                    Content, Headers, Code = callHandler("404Handler.py", self.requestHeaders, self.query)

                    self.send_response(Code)

                    if len(Headers) != 0:
                        for serverHeader,headerValue in Headers.items():
                            self.send_header(serverHeader, headerValue)

                    for serverHeader, headerValue in self.securityHeaders.items():
                        self.send_header(serverHeader , headerValue)

                    self.end_headers()
                    self.wfile.write(Content.encode())
                    writeLogs(clientIP=self.requestHeaders['client-ip'], userAgent=self.requestHeaders['user-agent'], endpointVisited=self.realPath, responseCode=Code, requestMethod=self.requestHeaders['request-method'])

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Working on handling requests in a separate thread"""

class WebServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.host = "localhost"
        self.port = 8080
        self.ws = ThreadedHTTPServer((self.host, self.port), serverHandler)

    def run(self):
        showGood(goodRule="Server Created" , Message=f"The server is running successfully on port {self.port}")

        try:
            self.ws.serve_forever()
        except Exception:
            self.shutdown()

    def shutdown(self):
        # set the two flags needed to shutdown the HTTP server manually
        self.ws._BaseServer__is_shut_down.set()
        self.ws.__shutdown_request = True

        showGood(goodRule="Note", Message="Shutting down the server")
        # call it anyway, for good measure...
        self.ws.shutdown()
        showGood(goodRule="Note", Message="Closed the server")
        self.ws.server_close()
        showGood(goodRule="Note", Message="Closed the thread")
        self.join()

def serveServer(serverPort, defaultDocument):
    try:
        httpServer = WebServer()
        httpServer.run()
    except Exception:
        httpServer.shutdown()