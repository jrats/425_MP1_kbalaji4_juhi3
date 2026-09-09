import socket
from protocol import send_msg, recv_msg

HOST = 'fa26-cs425-4801.cs.illinois.edu'
PORT = 65432


pattern = input("Enter a grep pattern: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))
    send_msg(s, pattern.encode())

    data = recv_msg(s)

    print("Results:")
    print(data.decode())

