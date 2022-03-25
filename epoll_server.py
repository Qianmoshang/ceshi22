#select tcp服务
from select import *
from socket import *

#创建监听套接字，作为关注的IO
s=socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(('0.0.0.0',8888))
s.listen(3)

#创建epoll对象
ep=epoll()

#建立查找字典，通过一个IO的fileno找到IO对象
#始终跟register的IO保持一致
fdmap={s.fileno():s}

#关注s
ep.register(s,EPOLLIN|EPOLLERR)

#循环监控IO
while True:
    events=ep.poll()
    #遍历返回值列表，处理就绪的IO
    for fd,event in events:
        #区分那个IO就绪
        if fd==s.fileno():
            c,addr=fdmap[fd].accept()
            print('Connect from',addr)
            #关注客户端连接套接字
            ep.register(c,EPOLLIN|EPOLLERR)
            fdmap[c.fileno()]=c   #维护字典
        elif event & EPOLLIN:    #判断是否为POLLIN
            #有客户端发消息
            data=fdmap[fd].recv(1024).decode()
            #客户端退出
            if not data:
                ep.unregister(fd)   #取消对客户端的关注
                fdmap[fd].close()
                del fdmap[fd]
                continue
            print(data)
            fdmap[fd].send(b'OK')
