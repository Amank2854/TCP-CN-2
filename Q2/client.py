import socket

server_address = socket.gethostbyname(socket.gethostname())
server_port = 12345

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
sock.connect((server_address, server_port))
message = sock.recv(1024).decode()
sock.sendall('1'.encode())
print(message)
while True:
    message = sock.recv(1024).decode()
    sock.sendall('1'.encode())
    print(message)
    if message == 'Type 1 to Register and 2 to Login':
        inp = input()
        sock.sendall(inp.encode())
        if inp == '1':
            message = sock.recv(1024).decode()
            sock.sendall('1'.encode())
            print(message)
            inp = input()
            sock.sendall(inp.encode())
            message = sock.recv(1024).decode()
            sock.sendall('1'.encode())
            print(message)
            if message == 'ERROR: Username already taken.':
                continue
            inp = input()
            sock.sendall(inp.encode())
            message = sock.recv(1024).decode()
            sock.sendall('1'.encode())
            print(message)
        elif inp == '2':
            message = sock.recv(1024).decode()
            sock.sendall('1'.encode())
            print(message)
            inp = input()
            sock.sendall(inp.encode())
            message = sock.recv(1024).decode()
            sock.sendall('1'.encode())
            print(message)
            inp = input()
            sock.sendall(inp.encode())
            message = sock.recv(1024).decode()
            sock.sendall('1'.encode())
            print(message)
    else:
        inp = input()
        sock.sendall(inp.encode()) 
        if inp == 'QUIT':
            break
        elif inp == 'LIST':
            message = sock.recv(1024).decode()
            sock.sendall('1'.encode())
            print(message)
        elif inp == 'CREATE':
            message = sock.recv(1024).decode()
            sock.sendall('1'.encode())
            print(message)
            inp = input()
            sock.sendall(inp.encode())
            message = sock.recv(1024).decode()
            sock.sendall('1'.encode())
            print(message)
        elif inp == 'JOIN':
            message = sock.recv(1024).decode()
            sock.sendall('1'.encode())
            print(message)
            inp = input()
            sock.sendall(inp.encode())
            message = sock.recv(1024).decode()
            sock.sendall('1'.encode())
            print(message)
            if message.startswith('OK: Joined chat room.\n'):
                len = 0
                with open(inp+'.txt') as f:
                    for i, l in enumerate(f):
                        len = i
                filename = inp
                while True:
                    message = sock.recv(1024).decode()
                    sock.sendall('1'.encode())
                    with open(filename+'.txt') as f:
                        for i, l in enumerate(f):
                            if i > len:
                                print(l)
                                len = i
                    print(message)
                    inp = input()
                    sock.sendall(inp.encode())
                    if inp == 'QUIT_CHAT':
                        break

        