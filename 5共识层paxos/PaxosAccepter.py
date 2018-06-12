#追随者
from Message import Message
from MessagePump import MessagePump
from InstanceRecord import InstanceRecord
from PaxosAccepterProtocol import PaxosAccepterProtocol

class PaxosAccepter:

    def __init__(self,port,leaders):
        self.port=port  #端口
        self.leaders=leaders    #领导者
        self.instances={}   #接口列表
        self.msgPump=MessagePump(self,self.port)    #消息传送器
        self.failed=False   #状态

    def start(self):    #开始
        self.msgPump.start()

    def stop(self):     #终止
        self.msgPump.doAbort()

    def fail(self):     #失败
        self.failed=True

    def recover(self):  #恢复
        self.failed=False

    def sendMessage(self,message):  #发送消息
        self.msgPump.sendMessage(message)

    def recvMessage(self,message):  #收取消息
        if message==None:
            return
        if self.failed:
            return
        if message.command==Message.MSG_PROPOSE:    #判断消息是不是提议
            if message.instanceID not in self.instances:
                record=InstanceRecord() #记录器
                self.instances[message.instanceID]=record   #记录
            protocol=PaxosAccepterProtocol(self)    #创建协议
            protocol.recvProposal(message)  #收取消息
            self.instances[message.instanceID].addProtocol(protocol)#记录协议
        else:
            self.instances[message.instanceID].getProtocol(message.proposalID)#抓取记录

    def notifyClient(self,protocol,message): #通知客户端
        if protocol.state==PaxosAccepterProtocol.STATE_PROPOSAL_ACCEPTED:
            self.instances[protocol.instanceID].value=message.value#存储信息
            print("协议被客户端接受",message.value)

    def getInstanceValue(self,instanceID): #获取接口数据
        return self.instances[instanceID].value

    def getHighestAgreedProposal(self,instanceID): #获取最高同意的提议
        return self.instances[instanceID].highestID