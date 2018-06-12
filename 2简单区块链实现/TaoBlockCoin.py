import hashlib  #加密模块
import datetime #时间模块
class TaoBlockCoin: #电子货币,涛币
    def __init__(self,
                 index, #索引
                 timestamp, #交易时间
                 data,  #交易记录
                 prevhash): #上个交易hash
        self.index=index
        self.timestamp=timestamp
        self.data=data
        self.prevhash = prevhash  # 上一个hash
        self.selfhash=self.hash_TaoBlockCoin()   #自身hash

    def hash_TaoBlockCoin(self):
        sha=hashlib.sha512()    #加密算法
        datastr=str(self.index)+str(self.timestamp)+str(self.data)+str(self.prevhash)   #对数据整体加密
        sha.update(datastr.encode("utf-8")) #二进制
        return sha.hexdigest()

def create_first_TaoBlock():    #创世区块
    return TaoBlockCoin(0,datetime.datetime.now(),"Hi Tao","0") #prevhash????????

def create_money_TaoBlock(lastblock):    #区块链其他块    #需要上一个区块
    this_index=lastblock.index+1
    this_timestamp=datetime.datetime.now()
    this_data="Hi Tao"+str(this_index)  #模拟交易数据
    this_hash=lastblock.selfhash    #取得上一块的hash
    return TaoBlockCoin(this_index, this_timestamp, this_data, this_hash)

TaoBlockCoins=[create_first_TaoBlock()] #区块链列表,只有一个传世区块
head_block=TaoBlockCoins[0]
print(head_block.index,head_block.selfhash,head_block.prevhash)
for i in range(100):
    TaoBlockCoin_add=create_money_TaoBlock(head_block)  #创建一个区块链
    TaoBlockCoins.append(TaoBlockCoin_add)  #加入区块
    head_block = TaoBlockCoins[-1]  #更新
    print(TaoBlockCoin_add.index,head_block.selfhash,head_block.prevhash)


