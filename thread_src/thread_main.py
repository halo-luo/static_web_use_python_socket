import socket
import threading


def resp_page(file_path):
    with open(file_path, "rb") as f:
        file_data = f.read()

    resp_line = "HTTP/1.1 200 OK\r\n"
    resp_header = "Server: BWS1.1\r\n"
    resp_body = file_data
    return (resp_line + resp_header + '\r\n').encode('utf-8') + resp_body


def deal_client_request(client_socket):
    recv_data = client_socket.recv(4096)
    recv_content = recv_data.decode('utf-8')
    if len(recv_content) == 0 or recv_content == 'q':
        print("服务器关闭了")
        client_socket.close()
        return
    # 找到content中的url
    request_path = recv_content.split(' ', maxsplit=2)
    # print(request_path)

    if len(request_path) == 0 or request_path[1] == '/':
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


if __name__ == '__main__':
    print("server starting...")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(128)

    while True:
        client_socket, client_addr = server_socket.accept()
        print("client connected", client_addr)

        client_thread = threading.Thread(
            target=deal_client_request,
            args=(client_socket,)
        )
        client_thread.daemon = True
        client_thread.start()
