import socket
import os

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind and listen
host = 'localhost'
port = 8082
server_socket.bind((host, port))
server_socket.listen(5)
print(f"Server running at http://{host}:{port}")

while True:
    # Accept connection
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # Receive request
    request = client_socket.recv(1024).decode('utf-8')
    print("Request:\n", request)

    # Parse request
    request_lines = request.splitlines()
    if not request_lines:
        client_socket.close()
        continue

    request_line = request_lines[0]
    try:
        method, path, _ = request_line.split()
    except ValueError:
        response = (
            "HTTP/1.1 400 Bad Request\r\n"
            "Content-Type: text/html\r\n"
            "Content-Length: 15\r\n"
            "\r\n"
            "<h1>Bad Request</h1>"
        )
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()
        continue

    # Parse query parameters
    params = {}
    if '?' in path:
        path, query_string = path.split('?', 1)
        if query_string:
            for param in query_string.split('&'):
                key, value = param.split('=', 1)
                params[key] = value

    # Handle request
    if method == 'GET':
        file_path = f"public{path if path != '/' else '/index.html'}"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
            status = '200 OK'
        else:
            status = '404 Not Found'
            content = '<h1>404 Not Found</h1>'
    else:
        status = '405 Method Not Allowed'
        content = '<h1>405 Method Not Allowed</h1>'

    # Build and send response
    response = (
        f"HTTP/1.1 {status}\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(content)}\r\n"
        "\r\n"
        f"{content}"
    )
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()