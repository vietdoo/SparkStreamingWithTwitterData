import socket


TCP_IP = "127.0.1.1"
TCP_PORT = 2910

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for the TCP connection...")

conn, addr = s.accept()
print("Connected successfully... Starting getting tweets.")