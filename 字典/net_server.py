'''
搭建服务端
'''
from socket import *
import pymysql
import os
import sys
import time
import signal

# 定义部分全局变量
DICT_TEXT = './dict.txt'
HOST = '0.0.0.0'
port = 8989
add = (HOST, port)


# 网络搭建
def main():
    # 创建数据库连接对象
    db = pymysql.connect('localhost', 'root',\
                         '123456', 'directory')

    # 创建流式套接字
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(add)
    s.listen(5)
    print('waiting for connect')
    #处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    while True:
        try:
            conn, addr = s.accept()
            print('connect from', addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue

        #创建子进程
        pid = os.fork()
        if pid == 0:
            s.close()
            do_child(conn,db)
            sys.exit(0)
        else:
            conn.close()

def do_child(conn,db):
    print('connect from',conn)

main()