import socket

target_host = "0.0.0.0"
target_port = 9998

# socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
try:
    client.connect((target_host, target_port))
except Exception as e:
    print(f'Connection failed: {e}')

# send data
client.send(b'This is a simple tcp client')

# recieve data
response = client.recv(4096)

print(response.decode())
client.close()