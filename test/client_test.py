import socket
# built-in library for network communication

HOST = '<server-hostname-or-IP>'
# address of the machine running demo_server.py

PORT = 65432
# must match the server's port

pattern = input("Enter a grep pattern: ")
# ask the user (you) what to search for, interactively,
# instead of hardcoding it - this is the "real input" piece

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # create a TCP/IPv4 socket, auto-closes when done

    s.connect((HOST, PORT))
    # connect out to the server

    s.sendall(pattern.encode())
    # convert the pattern string into bytes and send it
    # this is what the server's conn.recv(1024) will receive

    data = s.recv(4096)
    # wait for and read the server's response (the grep results)

    print("Results:")
    print(data.decode())
    # convert the received bytes back into a readable string and print it
