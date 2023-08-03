import datetime
import socket
import threading

# Define the socket host and port
HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

# Define a list of active clients and chat rooms
active_clients = []
passwords = {}
chat_rooms = {}
chat_history = {}
username = ''
# Function to handle a client connection
def handle_client(client_socket, client_address):

    # Send a welcome message to the client
    client_socket.send('Welcome to the chat server!'.encode())
    x = client_socket.recv(1024).decode()
    f = 0
    # Loop to handle incoming messages from the client
    while True:
        if(f == 0):
            client_socket.send('Type 1 to Register and 2 to Login'.encode())
            x = client_socket.recv(1024).decode()
            message = client_socket.recv(1024).decode()
            if message == '1':
                client_socket.send('Enter Username'.encode())
                x = client_socket.recv(1024).decode()
                username = client_socket.recv(1024).decode()
                print(username)
                if len(active_clients)!=0 and username in [client[0] for client in active_clients]:
                    client_socket.send('ERROR: Username already taken.'.encode())
                    x = client_socket.recv(1024).decode()
                else:
                    client_socket.send('Enter Password'.encode())
                    x = client_socket.recv(1024).decode()
                    password = client_socket.recv(1024).decode()
                    passwords[username] = password
                    active_clients.append((username, client_socket))
                    client_socket.send('OK: Registration successful.\n'.encode())
                    x = client_socket.recv(1024).decode()
                    f = 1
            elif message == '2':
                client_socket.send('Enter Username'.encode())
                x = client_socket.recv(1024).decode()
                username = client_socket.recv(1024).decode()
                client_socket.send('Enter Password'.encode())
                x = client_socket.recv(1024).decode()
                password = client_socket.recv(1024).decode()
                if username in [client[0] for client in active_clients] and passwords[username] == password:
                    client_socket.send('OK: Login successful.\nACTIVE_USERS {}\n'.format(' '.join([client[0] for client in active_clients])).encode())
                    x = client_socket.recv(1024).decode()
                    f = 1
                else:
                    client_socket.send('ERROR: Incorrect Credentials.\n'.encode())
                    x = client_socket.recv(1024).decode()
        else:
            # Receive a message from the client
            client_socket.send('Enter Command\n1. QUIT to Exit\n2. LIST to view Active users\n3. CREATE to Create Chatroom\n4. JOIN to Join Chatroom\n'.encode())
            x = client_socket.recv(1024).decode()
            message = client_socket.recv(1024).decode()
            if message == 'QUIT':
                # Remove the client from the list of active clients
                active_clients.remove(client_socket)
                # Close the client connection
                client_socket.close()
                # Exit the thread
                return
            elif message == 'LIST':
                client_socket.send('ACTIVE_USERS {}\n'.format(' '.join([client[0] for client in active_clients])).encode())
                x = client_socket.recv(1024).decode()
            elif message == 'CREATE':
                client_socket.send('Enter Chatroom Name\n'.encode())
                x = client_socket.recv(1024).decode()
                chatroom = client_socket.recv(1024).decode()
                if chatroom in chat_rooms.keys():
                    client_socket.send('ERROR: Chat room already exists.\n'.encode())
                    x = client_socket.recv(1024).decode()
                else:
                    chat_rooms[chatroom] = [client_socket]
                    chat_history[chatroom] = []
                    client_socket.send('OK: Chat room created.\n'.encode())
                    x = client_socket.recv(1024).decode()
                    # Create chatroom.txt file
                    f = open(chatroom+'.txt', 'w')
                    f.close()
            elif message == 'JOIN':
                client_socket.send('Enter Chatroom Name\n'.encode())
                x = client_socket.recv(1024).decode()
                chatroom = client_socket.recv(1024).decode()
                if chatroom in chat_rooms.keys():
                    chat_rooms[chatroom].append(client_socket)
                    client_socket.send('OK: Joined chat room.\nCHAT_HISTORY \n{}\n'.format(''.join(chat_history[chatroom])).encode())
                    x = client_socket.recv(1024).decode()
                    while True:
                        client_socket.send('Enter Chat else QUIT_CHAT to exit\n'.encode())
                        x = client_socket.recv(1024).decode()
                        message = client_socket.recv(1024).decode()
                        if message == 'QUIT_CHAT':
                            chat_rooms[chatroom].remove(client_socket)
                            break
                        else:
                            # Write to chatroom.txt file
                            print(chatroom)
                            with open(chatroom+'.txt', 'a') as f:
                                # Get the current date and time
                                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                chat_history[chatroom].append('['+timestamp+'] '+username+': '+message+'\n')

                                # Write the message to the file
                                f.write(f'[{timestamp}] {username}: {message}\n')
                else:
                    client_socket.send('ERROR: Chat room does not exist.\n'.encode())
                    x = client_socket.recv(1024).decode()


while True:
    # Wait for a new client connection
    client_socket, client_address = server_socket.accept()

    # Start a new thread to handle the client connection
    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

           
