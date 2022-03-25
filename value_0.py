import time
from multiprocessing import Value,Process
import random

#创建共享内存
money=Value('i',5000)

#操作共享内存
def man():
    for i in range(30):
        time.sleep(0.2)
        money.value+=random.randint(1,1000)

def girl():
    for i in range(30):
        time.sleep(0.15)
        money.value-=random.randint(100,800)

if __name__=='__main__':
    P1=Process(target=man)
    P2=Process(target=girl)
    P1.start()
    P2.start()
    P1.join()
    P2.join()
    print('余额：',money.value)
    
