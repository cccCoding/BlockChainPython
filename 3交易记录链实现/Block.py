#区块     还有点问题的
import datetime
import hashlib
from Message import TaoMessage
from Transaction import Transaction
from Message import InvalidMessage
class Block:
    def __init__(self,*args):
        self.messagelist=[] #存储多个交易记录
        self.timestamp=None #存储多个记录最终锁定的时间
        self.hash=None      #自身hash
        self.prev_hash=None #上个块的hash
        if args:
            for arg in args:
                self.add_message(arg)

    def add_message(self,message):  #增加交易信息
        #区分第一条和后面多条,判断是否需要链接
        if len(self.messagelist) > 0:
            message.link(self.messagelist[-1])  #链接
        message.seal()      #密封
        message.validate()  #校验
        self.messagelist.append(message)    #追加记录

    def link(self,block):     #区块链接方法
        self.prev_hash=block.hash

    def seal(self):         #密封
        self.timestamp=datetime.datetime.now()  #密封当前hash
        self.hash=self.hash_block()             #密封当前数据hash

    def hash_block(self):         #密封上一块hash,时间戳和交易记录最后一条????
        return hashlib.sha256((str(self.prev_hash) + str(self.timestamp) + \
                               str(self.messagelist[-1].hash)).encode("utf-8")).hexdigest()

    def validate(self):     #校验
        for i,message in enumerate(self.messagelist):#每个交易记录都校验一下
            message.validate()  #每一条进行校验
            if i>0 and message.prev_hash!=self.messagelist[i-1].hash:#校验hash
                raise InvalidBlock("无效Block,交易记录第{}条被修改".format(i)+str(self))

    def __repr__(self):     #类的对象描述
        return "money block= hash{},prehash:{},len:{},time:{}".format(\
            self.hash,self.prev_hash,len(self.messagelist),self.timestamp)

class InvalidBlock(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

if __name__=="__main__":
    try:
        t1 = Transaction("朱建涛", "猴子", 100)  # 交易类,后期需要整合公钥私钥
        t2 = Transaction("朱建涛", "莽子", 101)
        t3 = Transaction("朱建涛", "树根", 102)

        m1=TaoMessage(t1)
        m2=TaoMessage(t2)
        m3=TaoMessage(t3)

        b1=Block(m1,m2,m3)  #一次加入三条记录
        b1.seal()
        # m2.hash="假hash"
        # m1.data="假数据"
        # m2 = TaoMessage(t1)  # 重新赋值不报错??????
        b1.messagelist[2]=m3
        print(b1.validate())
    except InvalidBlock as e:
        print(e)
    except InvalidMessage as e:
        print(e)

