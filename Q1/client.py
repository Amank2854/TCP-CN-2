import socket

filename = 'text.txt'
# filename = 'img.webp'
server_address = socket.gethostbyname(socket.gethostname())
server_port = 5000

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
sock.connect((server_address, server_port))

# Send the filename to the server
sock.sendall(filename.encode())

# Send the contents of the file to the server
with open(f"files/{filename}", "rb") as f:
    data = f.read(1024)
    while data:
        sock.sendall(data)
        data = f.read(1024)

# Close the socket
sock.close()
