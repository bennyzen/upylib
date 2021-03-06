try:
    from uos import stat
except:
    from os import stat

import http
import http.websocket

def MyRequestHandler(request, conn, buffer=128):

    if request.method == b"GET":

        print(request.uri.path, request.uri.file)

        uri = request.uri.path \
                + (b"/" if request.uri.path else b"") \
                + (request.uri.file if request.uri.file else b"index.html")
        
        print(uri)
        
        try:
            stat(uri)
        except:
            conn.send( b"HTTP/1.1 404 Not Found\r\n\r\n" )
            return

        conn.send( b"HTTP/1.1 200 OK\r\n\r\n" )

        _buf = bytearray(buffer)
        buf = memoryview(_buf)
        with open(uri, "rb") as file:
            while True:
                count = file.readinto(buf)
                if count:
                    conn.send(buf[:count])
                else:
                    break 

        conn.send( b"\r\n" )
    
    else:
        # catch all request types
        conn.send(b"HTTP/1.1 403 Not Implemented\r\n\r\n")
    

srv = http.HttpServer(
            callback=MyRequestHandler,
            websocket_handler = http.websocket.WebSocket,
            addr = ("0.0.0.0", 8080)
      )
srv.serve()