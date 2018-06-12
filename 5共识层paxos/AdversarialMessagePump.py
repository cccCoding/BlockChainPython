#对抗消息传输,延迟消息并任意顺序传递
from MessagePump import MessagePump
import random
class AdversarialMessagePump(MessagePump):

    def __init__(self,owner,port,timeout=3):
        MessagePump.__init__(self,owner,port,timeout)  #初始化父类
        self.messages=set() #集合避免重复

    def waitForMessage(self):
        try:
            msg=self.queue.get(True,0.1)    #从队列抓取消息,timeout=0.1
            self.messages.add(msg)          #添加消息
        except Exception as e:
            print(e)
        #随机处理消息,模拟网络延迟,消息乱序
        if len(self.messages)>0 and random.random()<0.95:
            msg=random.choice(list(self.messages))
            self.messages.remove(msg)
        else:
            msg=None
        return msg


