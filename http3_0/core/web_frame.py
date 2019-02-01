#coding=utf-8
'''
模拟网站后端处理程序
'''
import sys,os
from socket import *
from select import *
frame_ip = 'localhost'
frame_port = 8888

STATIC_DIR = './static'
print(STATIC_DIR)
#终端输入，只在linux下可使用
# if len(sys.argv) < 3:
#     exit()
# else:
#     frame_ip = sys.argv[1]
#     frame_port = sys.argv[2]

#url列表，表示我们处理的数据请求

frame_addr = (frame_ip, frame_port)
BASE_DIR = os.path.dirname(os.path.dirname \
                               (os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from handle.views import *
#静态网页位置
urls = [
    ('/time',show_time),
    ('/hello',say_hello),
    ('/bye',say_bye)
]


#应用类，封装功能

class Application(object):
    def __init__(self):
        self.socket = socket()
        self.socket.setsockopt(SOL_SOCKET,\
                               SO_REUSEADDR,1)
        self.socket.bind(frame_addr)
        # 添加关注列表
        self.rlist = [self.socket]
        self.wlist = []
        self.xlist = []

    def runserver(self):
        self.socket.listen(5)
        print('listen the port %d'%frame_port)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist,\
                                self.xlist)
            #接收客户端的连接
            for r in rs:
                if r is self.socket:
                    conn,addr = r.accept()
                    print('connect from', addr)
                    self.rlist.append(conn)
                else:
                    request = r.recv(1024).decode()
                    self.handle(r, request)  # 处理请求

    def handle(self, conn, request):
        method = request.split(' ')[0]
        path_info = request.split(' ')[1]

        if method == 'GET':
            if path_info == '/' or path_info[-5:]=='.html':
                response = self.get_html(path_info)  # 获取网页
            else:
                response = self.get_date(path_info)
        elif method == 'POST':
            pass
        conn.send(response.encode())
        conn.close()
        self.rlist.remove(conn)
        # conn.send(b'Hello World')
        # self.rlist.remove(conn)

    def get_html(self,path_info):
        if path_info == '/':
            get_file = STATIC_DIR + '/index.html'
        else:
            get_file = STATIC_DIR + path_info
        try:
            fd = open(get_file,encoding='utf-8')
            print(fd)
        except IOError:
            response = '404'
        else:
            response = fd.read()
        finally:
            return response
    def get_date(self,path_info):
        for url,func in urls:
            if path_info == url:
                response = func()
                break
        else:
            response = '404'
        return response


if __name__ == '__main__':
    app = Application()
    app.runserver()  # 启动应用框架服务