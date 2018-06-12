import select       #异步通信
import socket       #网络通信
from coroutine import coroutine #装饰器

@coroutine
def handler():      #处理消息
    msg = yield
    while True:
        if msg:
            ret = msg.upper()
        else:
            ret = None
        msg = yield ret

def coroutine_handler(msg): #消息机制
    yield msg.upper()

class Reactor:
    def __init__(self):#初始化
        pass
    def _initialise(self):#初始化资源
        pass
    def _close_conn(self):#关闭链接
        pass
    def _handler_io_event(self):#处理事件
        pass
    def server_forever(self):   #开启服务器
        pass