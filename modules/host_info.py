import socket

def get_host_name():
    return f"Host Name: {socket.gethostname()}"