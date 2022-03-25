'''
基于process的多进程开发
'''
from multiprocessing import Process
from socket import *
import os
import signal

#全局变量
HOST='0.0.0.0'
POST=8888
ADDR=(HOST,POST)

#处理客户端请求
def handle(c):
    while True:
        data=c.recv(1024)
        if not data:
            break
        print(data.decode())
        c.send(b'OK')
    c.close()

#创建tcp套接字
s=socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(5)

#处理僵尸进程
signal.signal(signal.SIGCHLD,signal.SIG_IGN)
print('Listen the port 8888........')

while True:
    '''循环处理客户端连接'''
    try:
        c, addr = s.accept()
        print('Connect from', addr)
    except KeyboardInterrupt:
        os._exit(0)
    except Exception as e:
        print(e)
        continue

    #创建子进程处理客户端请求
    p=Process(target=handle,args=(c,))
    p.daemon=True   #父进程结束则所有服务终止
    p.start()

