'''
文件服务器
'''
import os
from socket import *
from threading import Thread
import sys
import time

#全局变量
HOST='0.0.0.0'
PORT=8080
ADDR=(HOST,PORT)
FTP='/FTP'

#创建类实现服务器文件处理功能
class Ftp_Server(Thread):
    '''
    查看列表 下载 上传 退出
    '''
    def __init__(self,confd):
        self.confd=confd
        super().__init__()

    def do_list(self):
        #获取文件列表
        files=os.listdir(FTP)
        if not files:
            self.confd.send('文件库为空'.encode())
            return
        else:
            self.confd.send(b'OK')
            time.sleep(0.1)
        '''拼接文件'''
        filelist=''
        for i in files:
            '''判断文件不是隐藏文件并且是文件则拼接后发送'''
            if i[0] !='.'and os.path.isfile:
                filelist+=i+'\n'
        self.confd.send(filelist.encode())

    def run(self):
        while True:
            data=self.confd.recv(1024).decode()
            if data=='L':
                self.do_list()

#搭建网络服务端模型
def main():
    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    print('Listen the port 8080.....')

    # 循环等待客户端连接
    while True:
        try:
            c, addr = s.accept()
            print('Connect from', addr)
        except KeyboardInterrupt:
            sys.exit('退出服务器')
        except Exception as e:
            print(e)
            continue

        # 创建线程处理请求
        client = Ftp_Server(c)
        client.setDaemon=True
        client.start()

if __name__=='__main__':
    main()
