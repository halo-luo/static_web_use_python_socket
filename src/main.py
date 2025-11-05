import socket
import re


def resp_page(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()

    resp_line = "HTTP/1.1 200 OK\r\n"
    resp_header = "Server: BWS1.1\r\n"
    resp_body = file_data
    return (resp_line + resp_header + '\r\n').encode('utf-8') + resp_body


if __name__ == "__main__":
    print()
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    tcp_server_socket.bind(('0.0.0.0', 65000))
    tcp_server_socket.listen(64)

    while True:
        client_socket, client_addr = tcp_server_socket.accept()
        print(client_addr)
        recv_data = client_socket.recv(4096)
        recv_content = recv_data.decode('utf-8')
        # print(recv_content)
        with open("a.txt", "w") as f:
            f.writelines(recv_content)

        if recv_content == 'q':
            client_socket.close()
            break
        if len(recv_content) == 0:
            print("服务器关闭了")
            client_socket.close()
            break

        # 找到content中的url
        request_path = recv_content.split(' ', maxsplit=2)
        print(request_path)

        if len(request_path) == 0:
            # client.py 访问
            resp_data = resp_page("../resource/index.html")
        else:
            url = request_path[1]
            print(f"请求地址：{url}")

            try:
                resp_data = resp_page(f"../resource/{url}.html")
            except FileNotFoundError:
                resp_data = resp_page("../resource/error.html")

        client_socket.send(resp_data)
        client_socket.close()
        # break

    tcp_server_socket.close()
