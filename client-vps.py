import socket

HOST = '104.208.99.173'  # Thay your_server_ip bằng địa chỉ IP của VPS
PORT = 5555  # Sử dụng cổng 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(5) # set timeout sau 5s nếu không nhận được phản hồi từ server
try:
    client_socket.connect((HOST, PORT))
except Exception as e:
    print(f"Error connecting to server: {e}")
    client_socket.close()
    exit(1)

while True:
    message = input('-> ')
    client_socket.send(message.encode())
    try:
        data = client_socket.recv(1024).decode()
    except Exception as e:
        print(f"Error receiving data from server: {e}")
        client_socket.close()
        exit(1)
    print('Received from server:', data)

client_socket.close()