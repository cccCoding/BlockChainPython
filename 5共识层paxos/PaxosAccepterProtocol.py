#追随者协议
from Message import Message #协议依赖消息

class PaxosAccepterProtocol:
    STATE_UNDEFINED=-1          #协议没有定义
    STATE_PROPOSAL_RECEIVED=0   #收到消息
    STATE_PROPOSAL_REJECTED=1   #拒绝链接
    STATE_PROPOSAL_AGREED=2     #同意链接
    STATE_PROPOSAL_ACCEPTED=3   #同意请求
    STATE_PROPOSAL_UNACCEPTED=4 #拒绝请求

    def __init__(self,client):
        self.client=client
        self.state=PaxosAccepterProtocol.STATE_UNDEFINED

    def recvProposal(self,message):     #收取协议
        if message.command==Message.MSG_EXT_PROPOSE:    #处理协议
            self.proposalID=message.proposalID  #协议编号
            (port,count)=self.client.getHighestAgreedProposal(message.instanceID)#端口,协议内容的最高编号
            #编号检测处理消息协议 判断协议是不是最高
            if count<self.proposalID[0] or (count==self.proposalID[0] and \
                    port<self.proposalID[1]):
                self.state=PaxosAccepterProtocol.STATE_PROPOSAL_AGREED  #协议同意
                value=self.client.getInstanceValue(message.instanceID)  #抓取数据
                msg=Message(Message.MSG_ACCEPT) #创建同意协议消息
                msg.copyAsReply(message)    #拷贝并回复
                msg.value=value     #保存值
                msg.sequence=(port,count)   #保存数据
                self.client.sendMessage(msg)    #发送消息
            else:
                self.state=PaxosAccepterProtocol.STATE_PROPOSAL_REJECTED #拒绝状态
            return self.proposalID
        else:
            pass    #错误,重试

    def doTranition(self,message):      #过度
        if self.state==PaxosAccepterProtocol.STATE_PROPOSAL_AGREED and \
            message.command==Message.MSG_ACCEPT:
            self.state=PaxosAccepterProtocol.STATE_PROPOSAL_ACCEPTED    #接受协议
            msg=Message(Message.MSG_ACCEPTOR_ACCEPT)    #创建消息
            msg.copyAsReply(message)    #拷贝并回复
            for leader in self.client.leaders:
                msg.to=1
                self.client.sendMessage(msg)    #给领导发消息
            self.notifyClient(message)  #通知自己
            return True
        raise Exception("并非预期的状态与命令")

    def notifyClient(self,message):     #通知 自己客户端
        self.client.notifyClient(self,message)