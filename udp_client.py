import socket

target_host = '127.0.0.1'
target_port = 9997

# socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send data
client.sendto(b'You have been pawned', (target_host, target_port))

# recieve data
client.settimeout(10) # set a five second timeout if no server is listening
try:
    data, addr = client.recvfrom(4096)
except socket.timeout:
    print('No response from server')

print(data.decode())
client.close()