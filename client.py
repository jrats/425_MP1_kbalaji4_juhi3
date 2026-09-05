import socket
HOST = 'fa26-cs425-4801.cs.illinois.edu'
PORT = 65432

pattern = input("Enter a grep pattern: ")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))
    s.sendall(pattern.encode())

    data = s.recv(4096)

    print("Results:")
    print(data.decode())

