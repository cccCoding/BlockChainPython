#领导者协议
from Message import Message

class PaxosLeaderProtocol:
    STATE_UNDEFINED = -1    # 协议没有定义
    STATE_PROPOSED = 0      # 协议消息
    STATE_REJECTED = 1      # 拒绝链接
    STATE_AGREED = 2        # 同意链接
    STATE_ACCEPTED = 3      # 同意请求
    STATE_UNACCEPTED = 4    # 拒绝请求

    def __init__(self,leader):
        self.leader=leader
        self.state=PaxosLeaderProtocol.STATE_UNDEFINED
        self.proposeID=(-1,-1)  #初始化,网络好坏的情况,同意拒绝的情况
        self.agreeCount,self.accptCount=(0,0)
        self.rejectCount,self.unacceptCount=(0,0)
        self.InstanceID=-1
        self.highesteen=(0,0)   #最高的协议

    def propose(self,value,pID,instanceID):      #提议
        self.proposeID=pID
        self.value=value
        self.instanceID=instanceID

        message=Message(Message.MSG_PROPOSE)    #创建提议消息
        message.proposalID=pID
        message.instanceID=instanceID
        message.value=value

        for server in self.leader.getAccepter():   #遍历服务器
            message.to=server
            self.leader.sendMessage(message)
        self.state=PaxosLeaderProtocol.STATE_PROPOSED
        return self.proposeID

    def doTransition(self,message): #过度 根据状态机运行协议
        if self.state==PaxosLeaderProtocol.STATE_PROPOSED:
            if message.command==Message.MSG_ACCEPTOR_ACCEPT:    #同意协议
                self.agreeCount+=1
                if self.agreeCount>self.leader.getQuorumSize(): #选举
                    if message.value!=None:
                        if message.sequence[0]>self.highesteen[0] or \
                                (message.sequence[0]==self.highesteen[0] and \
                                        message.sequence[1]>self.highesteen[1]):
                            self.value=message.value        #数据同步
                            self.highesteen=message.sequence
                        self.state=PaxosLeaderProtocol.STATE_AGREED #同意更新
                        #发送同意消息
                        msg=Message(Message.MSG_ACCEPT)
                        msg.copyAsReply(message)
                        msg.value=self.value
                        msg.leaderID=self.to
                        for server in self.leader.getAccepter():    #广播消息
                            msg.to=server
                            self.leader.sendMessage(msg)
                        self.leader.notifyLeader(self,message)  #通知leader
                return True
            if message.command==Message.MSG_ACCEPTOR_REJECT:    #拒绝
                self.rejectCount+=1
                if self.rejectCount>=self.leader.getQuorumSize():
                    self.state=PaxosLeaderProtocol.STATE_REJECTED
                    self.leader.notifyLeader(self,message)      #传递消息
                return True


        if self.state==PaxosLeaderProtocol.STATE_AGREED:
            if message.command==Message.MSG_ACCEPTOR_ACCEPT:    #同意协议
                self.accptCount+=1
                if self.accptCount>=self.leader.getQuorumSize():    #投票
                    self.state=PaxosLeaderProtocol.STATE_ACCEPTED  #接受
                    self.leader.notifyLeader(self,message)
            if message.command==Message.MSG_ACCEPTOR_UNACCEPT:  #不同意协议
                self.unacceptCount+=1
                if self.unacceptCount>=self.leader.getQuorumSize(): #投票
                    self.state=PaxosLeaderProtocol.STATE_UNACCEPTED
                    self.leader.notifyLeader(self,message)


