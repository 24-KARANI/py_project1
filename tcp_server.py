import socket
import threading

IP = '0.0.0.0'
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # passing the ip and port the server will listen to 
    server.bind((IP, PORT)) 
    
    # Listening with a maximum of 5
    server.listen(5) 
    print(f'[*] listening on {IP}:{PORT}')
    
    while True:
        # recieving, client socket in 'client' variable and connection details in 'address' variable
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Recieved: {request.decode('utf-8')}')
        sock.send(b'ACK')

if __name__ == '__main__':
    main()        