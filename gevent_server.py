from gevent import monkey
monkey.patch_all() #执行脚本，修改socket阻塞
from socket import *
'''基于协程的TCP开发'''

#创建TCP套接字
s=socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(('0.0.0.0',8888))
s.listen(3)

def handle(c):
    while True:
        data=c.recv(1024).decode()
        if not data:
            break
        print(data)
        c.send(b'OK')

#循环接收客户端链接
while True:
    c,addr=s.accept()
    print('Connect from',addr)
    gevent.spawn(handle,c)
