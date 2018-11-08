# coding:utf-8
import socket


from multiprocessing import Process
import PortScanner as ps


def handle_client(client_socket):
    """
    处理客户端请求
    """
    request = client_socket.recv(1024)
    ip = str(request).split()[1].split("?")[1]
    print ip

    # Initialize a Scanner object that will scan top 1000 commonly used ports.
    scanner = ps.PortScanner(target_ports=1000)
    message = ''
    scanner.set_thread_limit(1500)
    scanner.set_delay(15)

    openPorts = scanner.scan(ip, message)
    # result = ('.'.join(list(map(str, openPorts))))
    print openPorts



    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    response_body = openPorts
    response = response_start_line + response_headers + "\r\n" + response_body

    # 向客户端返回响应数据
    client_socket.send(bytes(response))

    # 关闭客户端连接
    client_socket.close()


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", 8000))
    server_socket.listen(128)

    while True:
        client_socket, client_address = server_socket.accept()
        print("[%s, %s]用户连接上了" % client_address)
        handle_client_process = Process(target=handle_client, args=(client_socket,))
        handle_client_process.start()
        client_socket.close()