'''
httpserver3.0
'''
from socket import *
import sys, os
from threading import Thread

BASE_DIR = os.path.dirname(os.path.dirname \
                               (os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# print(BASE_DIR)
# 导入setting 配置模块
from conf.setting import *
from handle.views import *


def connect_frame(request):
    # 创建流式套接字
    s = socket()
    try:
        s.connect(frame_addr)
    except Exception as e:
        print(e)
    s.send(request.encode())
    response = s.recv(4096).decode()
    return response


# 将功能封装成类
class HttpServer(object):
    def __init__(self, address):
        self.address = address
        self.create_socket()
        self.bind(address)

    # 创建套接字(tcp传输)
    def create_socket(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET,\
                               SO_REUSEADDR, 1)

    # 绑定地址
    def bind(self, address):
        self.ip = address[0]
        self.port = address[1]
        self.socket.bind(address)

    def serve_forever(self):
        self.socket.listen(5)
        print('listen the port %s' % self.port)
        while True:
            conn, addr = self.socket.accept()
            print('connect from ', addr)
            handle_client = Thread(target=self.handle_client, \
                                   args=(conn,))
            handle_client.start()

    # 处理客户端的请求
    def handle_client(self, conn):
        request = conn.recv(buffer)
        if not request:
            conn.close()
            return
        request_lines = request.splitlines()
        # print(request_lines)
        # 获取请求行
        request_line = request_lines[0].decode('utf-8')
        print('请求', request_line)

        # 向webframe发送
        response_body = connect_frame(request_line)

        if response_body == '404':
            response_headlers = "HTTP/1.1 404 Not Found\r\n"
            response_body = "<h1>Not Found</h1>"
        else:
            response_headlers = "HTTP/1.1 200 OK\r\n"
        # 响应头'
        response_headlers+= '\r\n'
        response = response_headlers + response_body
        conn.send(response.encode())
        conn.close()

if __name__ == '__main__':
    httpd = HttpServer(ADDR)
    httpd.serve_forever()  # 启动ｈｔｔｐ服务