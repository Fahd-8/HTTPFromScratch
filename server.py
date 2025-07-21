import socket

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow port reuse to avoid "Address already in use" errors
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to host and port
host = 'localhost'
port = 8080
server_socket.bind((host, port))

# Listen for incoming connections (queue up to 5)
server_socket.listen(5)
print(f"Server running at http://{host}:{port}")