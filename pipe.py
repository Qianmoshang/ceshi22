from multiprocessing import Process,Pipe

fd1,fd2=Pipe()

def app1():
    print('启动app1,请登录')
    print('请求app2授权')
    fd1.send('app1请求登录')
    data=fd1.recv()
    if data:
        print('登录成功',data)

def app2():
    data=fd2.recv() #阻塞等待读取管道内容
    print(data)
    fd2.send(('ASD','1235'))

if __name__=='__main__':
    P1=Process(target=app1)
    P2=Process(target=app2)
    P1.start()
    P2.start()
    P1.join()
    P2.join()


