import socket

if __name__ == '__main__':
    print("client start...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 65000))
    client_socket.send(b'hello')
    recv_data = client_socket.recv(4096)
    recv_content = recv_data.decode('utf-8')
    print(recv_content)
    client_socket.close()
