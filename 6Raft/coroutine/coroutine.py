#coding:utf-8

def coroutine(func):
    def start(*args,**kwargs):  #内部函数,协程调用
        g = func(*args,**kwargs)
        g.next()        #下一步
        return g
    start.__doc__ = func.__doc__    #文档属性
    return start

#装时器
import time
def gettime(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print(end - start)
    return wrapper()

@gettime
def go():
    sum = 0
    for i in range(1000000):
        sum += i
go()
# if __name__ == "__main__":
#     go()