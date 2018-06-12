#交易数据
import datetime
import hashlib
from Transaction import Transaction
class TaoMessage:   #交易记录类
    def __init__(self,data):
        self.hash=None  #自身hash
        self.prev_hash=None #上一个信息hash
        self.timestamp=datetime.datetime.now()  #交易时间
        self.data=data  #交易信息
        self.payload_hash=self._hash_payload()   #交易后的hash

    def _hash_payload(self):    #对交易时间和交易数据进行hash计算
        return hashlib.sha256((str(self.timestamp)+str(self.data)).encode("utf-8")).hexdigest()#取得数据的hash

    def _hash_massage(self):    #对交易进行锁定 防纂改
        return hashlib.sha256((str(self.prev_hash) + str(self.payload_hash)).encode("utf-8")).hexdigest()

    def seal(self):     #密封
        self.hash=self._hash_massage()  #对数据锁定,对交易前的链锁定

    def validate(self): #验证
        if self.payload_hash != self._hash_payload():   #判断有没有人修改(时间戳和交易数据)
            raise InvalidMessage("交易数据与时间被修改"+str(self))
        if self.hash != self._hash_massage():       #判断消息链
            raise InvalidMessage("交易的hash链接被修改"+str(self))
        return "数据正常"+str(self)

    def __repr__(self):     #返回对象的基本信息
        mystr="hash:{},prev_hash:{},data:{}".format(self.hash,self.prev_hash,self.data)
        return mystr

    def link(self, Message):
        self.prev_hash=Message.hash     #hash相链接

class InvalidMessage(Exception):    #异常类
    def __init__(self,*args,**kwargs):  #参数
        Exception.__init__(self,*args,**kwargs)

if __name__=="__main__":    #单独模块测试
    try:
        t1 = Transaction("朱建涛", "猴子", 100)  # 交易类,后期需要整合公钥私钥
        t2 = Transaction("朱建涛", "莽子", 101)
        t3 = Transaction("朱建涛", "树根", 102)

        m1=TaoMessage(t1)
        m2=TaoMessage(t2)
        m3=TaoMessage(t3)
        m1.seal()
        m2.link(m1) #对于m2而言,要先链接,再密封,因为link是给prev_hash赋值的过程
        m2.seal()
        m3.link(m2)
        m3.seal()

        #如果修改数据
        # m2.data="假消息2"
        # m2.prev_hash="假hash"

        print(m1)
        print(m2)
        print(m3)

        m1.validate()
        m2.validate()
        m3.validate()
    except InvalidMessage as e:
        print(e)

