import socket
import subprocess

HOST = ''  
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def handle_client(conn, addr):
    print(f"connected by {addr}")
    data = conn.recv(1024)
    pattern = data.decode()

    result = subprocess.run(
        ["grep", "-n", pattern, "machine.1.log"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        output = result.stdout
    elif result.returncode == 1:
        output = "No matches found."
    else:
        output = f'grep error: {result.stderr}'

    conn.sendall(output.encode())
    conn.close()



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(16)
    print(f"Server listening on {PORT}")
    while True:
        conn, addr = s.accept()
        handle_client(conn, addr)










    
