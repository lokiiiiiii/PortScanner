# coding:utf-8
import socket
import subprocess
import sys

from multiprocessing import Process


def handle_client(client_socket):
    """
    处理客户端请求
    """
    request = client_socket.recv(1024)
    print str(request)

    command = request.decode('utf-8')
    obj = subprocess.Popen(command,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = obj.stdout.read() + obj.stderr.read()
    # 如果是win还需要转换编码
    if sys.platform == 'win32':
        result = result.decode('gbk').encode('utf-8')
    print result

    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: My server\r\n"
    response_body = "<h1>Python HTTP Test</h1>"
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