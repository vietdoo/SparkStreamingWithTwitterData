import socket
import os

os.system('fuser -k 5004/tcp')

TCP_IP = "127.0.1.1"
TCP_PORT = 6009
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

client_num = 0

while True:
    client_num += 1
    conn, addr = s.accept()
    conn.settimeout(10)
    data = conn.recv(BUFFER_SIZE)
    if data:
        conn.settimeout(None)
        conn.send(b"welcome")
        print(f"client is {client_num} active")
        try:
            while True:
                data = conn.recv(BUFFER_SIZE)  
                if data == b'q':    
                    conn.close()
                    print(f"client is {client_num} stop")
                    break 
                if data:
                    print("here is the message:",data)
                else:
                    conn.close()
                    break
        except Exception as e:
            conn.close()
            print("error is",e)
    else:
        print("client is inactive")

