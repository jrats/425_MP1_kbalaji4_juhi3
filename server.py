import socket
import subprocess
import threading

from protocol import send_msg, recv_msg

HOST = ''  
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def handle_client(conn, addr):
    print(f"connected by {addr}")
    try:
        data = recv_msg(conn)
        pattern = data.decode()

        result = subprocess.run(
            ["grep", "-n", pattern, "machine.1.log"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            output = result.stdout
        elif result.returncode == 1:
            output = ""
        else:
            output = f'grep error: {result.stderr}'
        send_msg(conn, output.encode())
    except Exception as e:
        print(f"error handling {addr}: {e}")
    finally:
        conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(16)
    print(f"Server listening on {PORT}")
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()










    
