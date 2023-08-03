import socket

server_address = socket.gethostbyname(socket.gethostname())
server_port = 5000

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
sock.bind((server_address, server_port))

# Listen for incoming connections
sock.listen(1)
print("Waiting for a connection...")

# Accept the connection
conn, addr = sock.accept()
print(f"Connected by {addr}")

# Receive the filename from the client
filename = conn.recv(1024).decode()
print(f"Receiving file: {filename}")

# Receive the contents of the file from the client
with open(filename, 'wb') as f:
    data = conn.recv(1024)
    while data:
        f.write(data)
        data = conn.recv(1024)

# Close the connection
conn.close()
print("File received and saved successfully.")
