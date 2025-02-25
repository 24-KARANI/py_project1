Netcat Clone

Overview:

This is a custom netcat clone built in Python as part of my resume projects. 
It replicates core netcat functionality by allowing you to connect to remote hosts or listen for incoming connections. 
In listener mode, it can spawn an interactive command shell for remote administration.

Features:

• Supports both client and server modes. 
• Listener mode (-l) to accept incoming connections. 
• Option to spawn an interactive command shell (-c) when running as a listener. 
• Interactive, real-time communication between client and server.

Prerequisites:

• Python 3.x
Files Included:

    clone_netcat.py - The netcat clone script.

Usage Instructions:

    Listener (Server) Mode: In one terminal, start the netcat clone in listener mode with a command shell by running:

python3 clone_netcat.py -t 192.168.1.101 -p 5555 -l -c

This command sets the target IP to 192.168.1.101 and the port to 5555. 
The flags -l and -c tell the script to listen for incoming connections and spawn a command shell upon connection.

Client Mode: In another terminal, connect to the listener using the netcat clone in client mode by running:

    python3 clone_netcat.py -t 192.168.1.101 -p 5555

    Replace the IP address and port with the appropriate values for your environment.

Additional Notes:

• This tool is intended for educational purposes and should only be used in environments where you have explicit permission. 
• Feel free to modify the script to add functionality or customize it for your specific needs.
