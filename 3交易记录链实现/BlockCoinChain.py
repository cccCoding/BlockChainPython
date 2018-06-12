#区块链
from Block import Block
from Block import InvalidBlock
from Message import TaoMessage
from Transaction import Transaction
from Message import InvalidMessage
class BlockCoinChain:
    def __init__(self):
        self.blocklist=[]   #区块列表

    def add_block(self,block):
        if len(self.blocklist)>0:
            block.prev_hash=self.blocklist[-1].prev_hash
        block.seal()
        block.validate()
        self.blocklist.append(block)

    def validate(self):
        for i,block in enumerate(self.blocklist):
            try:
                block.validate()
            except InvalidBlock as e:
                raise InvalidBlockCoinChain("第{}个区块校验错误".format(i))
            except InvalidMessage as e:
                raise InvalidBlockCoinChain("第{}个区块校验错误".format(i))

    def __repr__(self):
        return "BlockCoinChain:{}".format(str(len(self.blocklist)))

class InvalidBlockCoinChain(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

if __name__=="__main__":
    try:
        t1 = Transaction("朱建涛", "猴子", 100)
        t2 = Transaction("朱建涛", "莽子", 101)
        t3 = Transaction("朱建涛", "树根", 102)
        t4 = Transaction("朱建涛", "王志豪", 103)
        t5 = Transaction("朱建涛", "大毛", 104)
        t6 = Transaction("朱建涛", "徐淑欢", 105)

        m1 = TaoMessage(t1)
        m2 = TaoMessage(t2)
        m3 = TaoMessage(t3)
        m4 = TaoMessage(t4)
        m5 = TaoMessage(t5)
        m6 = TaoMessage(t6)

        b1 = Block(m1, m2, m3)
        b1.seal()
        b2 = Block(m4, m5, m6)
        b2.seal()

        c1=BlockCoinChain()
        c1.add_block(b1)
        c1.add_block(b2)

        # m4.hash="假hash"
        # b1.messagelist.append(m1)

        print(c1.validate())
    except InvalidBlockCoinChain as e:
        print(e)