import socket
# built-in library for network communication

import subprocess
# built-in library to run external programs like grep

HOST = ''
# listen on all available network interfaces

PORT = 65432
# port number to listen on

def handle_client(conn, addr):
    # everything needed to handle ONE client's full request/response

    print(f"connected by {addr}")
    # log who connected

    data = conn.recv(1024)
    # read up to 1024 bytes sent by the client - this is the grep PATTERN
    # (e.g. they might send b"error")

    pattern = data.decode()
    # convert the received bytes into a normal Python string,
    # since subprocess needs a string, not bytes, as its argument

    result = subprocess.run(
        ["grep", "-n", pattern, "notes.txt"],
        # NOTE: pattern is now a VARIABLE, not hardcoded "error" like before
        # this is the actual upgrade from the previous step
        capture_output=True,
        # capture grep's output instead of printing it directly
        text=True
        # get back strings, not bytes
    )

    if result.returncode == 0:
        # 0 means grep found at least one match
        output = result.stdout
    elif result.returncode == 1:
        # 1 means grep ran fine but found NO matches - not an error
        output = "(no matches found)"
    else:
        # 2 or higher means something actually went wrong
        # (bad pattern syntax, file missing, etc.)
        output = f"grep error: {result.stderr}"

    conn.sendall(output.encode())
    # convert our result string back into bytes and send it to the client

    conn.close()
    # done with this client

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # create a TCP/IPv4 socket, auto-closes when the block ends

    s.bind((HOST, PORT))
    # attach to our chosen address/port

    s.listen(16)
    # start listening, allow up to 16 pending connections

    print(f"server listening on port {PORT}")
    # helpful log so we know it's actually running

    while True:
        # keep accepting clients forever, one after another
        # (still not threaded - that's a separate upgrade, not this one)

        conn, addr = s.accept()
        # wait for and accept the next client connection

        handle_client(conn, addr)
        # handle this client's full request before going back to accept()
