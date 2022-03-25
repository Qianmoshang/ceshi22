from multiprocessing import *
from time import sleep
from random import randint

#创建列队消息
q=Queue(5)

def handle():
    for i in range(6):
        x=randint(1,33)
        q.put(x)      #消息入队
    q.put(randint(1,16))

def request():
    l=[]
    for i in range(6):
        l.append(q.get())
    l.sort()
    l.append(q.get())
    print(l)

if __name__=='__main__':
    P1=Process(target=handle)
    P2=Process(target=request)
    P1.start()
    P2.start()
    P1.join()
    P2.join()
