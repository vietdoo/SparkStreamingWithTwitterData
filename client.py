import socket
TCP_IP = "127.0.0.1"
TCP_PORT = 2999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
import time

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(bytes('connect','utf-8'))
    data = s.recv(1024)
    print(data)
    if len(data) == 0:
        print ("Disconnected!")
    try:
        while True:
            x = input("write your message >")
            s.send(bytes(x,'utf-8'))
            if (x == 'q'):
                print('-----------------------------------------')
                time.sleep(3)
                s.close()
                break
    except Exception as e:
        print("error is",e)