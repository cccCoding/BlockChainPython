#节点的数据更新，节点的网络共识
import hashlib
import json
import time
from urllib.parse import urlparse       #网络编码解码
from uuid import uuid4                  #唯一序列号
import requests                         #请求
from flask import Flask,jsonify,request #网络框架
from typing import Any,Dict,List,Optional   #数据结构

class TaoBlockChain:
    def __init__(self):
        self.current_transactions=[]    #交易列表
        self.chain=[]   #区块链
        self.nodes=set()    #网络中其他节点,set去重
        self.new_block(prev_hash="1",proof=100)  #创建创世区块

    def new_block(self,
                  proof:int,    #确定proof为int类型
                  prev_hash:Optional[str]   #prev_hash为字符串类型
                  )->Dict[str,Any]:     #指定返回值类型为字典数据类型
        block={
            "index":len(self.chain)+1,  #索引
            "timestamps":time.time(),   #当前时间
            "transactions":self.current_transactions,
            "proof":proof,
            "prev_hash":prev_hash or self.hash(self.chain[-1])  #前一块的hash
        }
        self.current_transactions=[]    #开辟新的区块,交易被加入,需清空
        self.chain.append(block)
        return block

    def new_transactions(self,sender:str,receiver:str,amount:int)->int:
        #生成交易信息,交易加入到下一个有待挖掘的区块
        self.current_transactions.append({
            "sender":sender,
            "receiver":receiver,
            "amount":amount
        })
        return self.last_block["index"]+1   #索引加一,索引标记交易数量

    @property
    def last_block(self)->Dict[str,Any]:   #取得最后一个区块
        return self.chain[-1]

    @staticmethod
    def hash(block:Dict[str,any])->str:     #hash加密 #传递一个字典,返回字符串
        blockstr=json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(blockstr).hexdigest()


    def proof_of_work(self,last_proof):        #工作量证明,挖矿过程
        proof=0
        while self.validate_proof(last_proof,proof) is False:
            proof+=1
        return proof

    @staticmethod   #第n个区块依赖n-1个区块
    def validate_proof(last_proof:int,proof:int)->bool:       #验证工作量证明
        guess=f'{last_proof*proof}'.encode()
        guess_hash=hashlib.sha256(guess).hexdigest()
        return guess_hash[-3:]=="000"   #验证是否符合条件

    def validate_chain(self,chain:List[Dict[str,Any]])->bool:   #区块链校验
        last_block=chain[0]
        curr_index=1
        while curr_index<len(chain):
            block=chain[curr_index]
            #hash校验,校验区块链的链接
            if block["prev_hash"] != self.hash(last_block):
                return False
            #工作量校验
            if not self.validate_proof(last_block["proof"],block["proof"]):
                return False
            last_block=block
            curr_index+=1
        return True

    def register_node(self,addr:str)->None:        #加入网络中其他节点,用于更新
        now_url=urlparse(addr)  #网络解析
        if now_url.netloc:
            self.nodes.add(now_url.netloc)  #增加网络节点
        elif now_url.path:
            self.nodes.add(now_url.path)
        else:
            raise ValueError("url无效")

    def resolve_conflicts(self)->bool:    #共识算法
        #网络中多个节点,取出链最长的
        neighbours=self.nodes   #取出所有节点
        new_chain=None
        max_length=len(self.chain)
        for node in neighbours:
            response=requests.get(f'http://{node}/chain')   #访问网络节点
            if response.status_code==200:
                length=response.json()["length"]    #取出长度
                chain=response.json()["chain"]      #取出区块链
                #如果当前区块链更长且检验没问题,更新
                if length>max_length and self.validate_chain(chain):
                    max_length=length
                    new_chain=chain
        if new_chain:   #不为空
            self.chain=new_chain
            return True
        return False

t1=TaoBlockChain()  #创建一个网络节点
node_id=str(uuid4()).replace("-","")    #节点替换,生成密钥
print("当前节点钱包地址:",node_id)

app=Flask(__name__) #初始化flask框架
@app.route("/")
def index_page():
    return "欢迎来到TaoCoin系统"

@app.route("/chain")
def chain():       #查看所有区块链
    response={
        "chain":t1.chain,
        "length":len(t1.chain),
    }
    return jsonify(response),200

@app.route("/mine")     #挖矿
def mine():
    last_block=t1.last_block
    last_proof=last_block["proof"]
    proof=t1.proof_of_work(last_proof)  #挖矿计算
    #系统奖励比特币,挖矿产生交易
    t1.new_transactions(
        sender="0",         #0表示系统奖励
        receiver=node_id,   #当前钱包地址
        amount=10
    )
    block=t1.new_block(proof,None)   #增加一个新的区块
    response = {
        "message": "新的区块创建",
        "index": block["index"],        #创建的索引
        "transactions":block["transactions"],   #交易
        "proof":block["proof"],         #工作量证明
        "prev_hash":block["prev_hash"], #上一块hash
    }
    return jsonify(response), 200

@app.route("/new_transactions",methods=["POST"])    #创建一个新的交易
def new_transactions():
    values=request.get_json()   #抓取网络传输的信息
    required=["sender","receiver","amount"]
    if not all(key in values for key in required):
        return "数据不完整",400
    index=t1.new_transactions(
        values["sender"],
        values["receiver"],
        values["amount"])
    response={
        "message":f'交易加入到区块{index}',
        "length":len(t1.chain),
    }
    return jsonify(response),200

@app.route("/new_node",methods=["POST"])
def new_node():       #新注册一个节点
    values=request.get_json()   #获取json字符串
    nodes=values.get("nodes")
    if nodes is None:
        return "错错错是我的错"
    for node in nodes:
        t1.register_node(node)  #增加网络节点
    response = {
        "message":f'网络节点已追加',
        "nodes":list(t1.nodes)  #查看所有节点
    }
    return jsonify(response),200

@app.route("/node_refresh")
def node_refresh():       #节点刷新
    replaced=t1.resolve_conflicts() #共识算法进行最长替换
    if replaced:
        response = {
            "message": f'区块链替换为最长',
            "new_chain": t1.chain
        }
    else:
        response = {
            "message": f'区块链已经是最长',
            "new_chain": t1.chain
        }
    return jsonify(response),200

if __name__=="__main__":
    app.run("127.0.0.1",port=5002)