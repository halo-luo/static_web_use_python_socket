import socket

from conda.auxlib.logz import response_header_sort_dict


def get_page():
    pass


if __name__ == "__main__":
    print()
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    tcp_server_socket.bind(('0.0.0.0', 65000))
    tcp_server_socket.listen(64)

    while True:
        client_socket, client_addr = tcp_server_socket.accept()
        recv_data = client_socket.recv(4096)
        recv_content = recv_data.decode('utf-8')
        print(recv_content)
        if recv_content == 'q':
            break

        with open("../resource/index.html", "rb") as f:
            file_data = f.read()

        resp_line = "HTTP/1.1 200 OK\r\n"
        resp_header = "Server: BWS1.1\r\n"
        resp_body = file_data

        resp_data = (resp_line + resp_header + '\r\n').encode('utf-8') + resp_body

        client_socket.send(resp_data)
        client_socket.close()

    tcp_server_socket.close()
