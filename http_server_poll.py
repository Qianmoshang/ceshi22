from select import *
from socket import *

class HTTPServer:
    def __init__(self, host='0.0.0.0', port=80, dir=None):
        self.host = host
        self.port = port
        self.dir = dir
        self.address = (host, port)
        # 实例化对象时直接创造套接字
        self.create_socket()
        self.bind()

    # 创造套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # 绑定地址
    def bind(self):
        self.sockfd.bind(self.address)

    # 启动服务函数
    def server_forever(self):
        self.sockfd.listen(3)
        print('Listen the port {}'.format(self.port))
        # IO多路复用接收客户端请求
        p = poll()  # 创建对象
        fdmap = {self.sockfd.fileno(): self.sockfd}  # 建立查找字典
        p.register(self.sockfd, POLLIN | POLLERR)  # 关注
        # 循环接收IO
        while True:
            events = p.poll()
            # 循环遍历列表，处理就绪的IO
            for fd, event in events:
                # 区分就绪IO
                if fd == self.sockfd.fileno():
                    c, addr = fdmap[fd].accept()
                    print('Connect from', addr)
                    # 关注客户端连接套接字
                    p.register(c, POLLIN | POLLERR)
                    fdmap[c.fileno()] = c  # 字典维护
                elif event & POLLIN:  # 判断是否为POLLIN
                    # 有客户端发消息
                    data = fdmap[fd].recv(1024).decode()
                    # 有客户端退出
                    if not data:
                        p.unregister(fd)  # 取消关注
                        fdmap[fd].close()
                        del fdmap[fd]
                        continue
                    print(data)
                    fdmap[fd].send(b'OK')


# 用户使用httpserver
if __name__ == '__main__':
    '''通过httpserver类快速搭建服务'''
    # 用户决定的参数
    HOST = '0.0.0.0'
    PORT = 8000
    DIR = './static'  # 网页存储位置

    httpd = HTTPServer(HOST, PORT, DIR)  # 实例化对象
    httpd.server_forever()  # 启动服务

