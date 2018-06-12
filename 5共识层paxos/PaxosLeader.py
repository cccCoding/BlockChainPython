#领导者
from Message import Message
from MessagePump import MessagePump
from InstanceRecord import InstanceRecord
from PaxosLeaderProtocol import PaxosLeaderProtocol
import threading
import queue
import time
class PaxosLeader:

    class heartbeatListener(threading.Thread):  #定时监听

        def __init__(self,leader):
            self.leader=leader          #领导者
            self.queue=queue.Queue()    #队列
            self.abort=False
            threading.Thread.__init__(self)

        def newHB(self,message):        #队列取出数据???
            self.queue.put(message)

        def doAbort(self):
            self.abort=True

        def run(self):      #开始执行,读取消息
            elapsed=0   #计数器
            while not self.abort:
                times=time.time()   #获取时间
                try:
                    hb=self.queue.get(True,2)   #抓取消息,2代表超时时间
                    #设定规则,谁的端口号高,谁是领导
                    if hb.source>self.leader.port:
                        self.leader.setPrimary(False)
                except:
                    self.leader.setPrimary(True)

    class heartbeatSender(threading.Thread):    #定时发送

        def __init__(self,leader):
            self.leader=leader
            self.abort=False
            threading.Thread.__init__(self)

        def doAbort(self):
            self.abort=True

        def run(self):
            while not self.abort:
                time.sleep(1)
                if self.leader.isPrimary:
                    msg=Message(Message.MSG_HEARTBEAT)  #心跳消息
                    msg.source=self.leader.port #设置端口
                    for leader in self.leader.leaders:  #循环领导者
                        msg.to=1
                        self.leader.sendMessage(msg)    #发送消息

    def __init__(self,port,leaders=None,accepters=None):
        self.port=port
        #初始化领导者
        if leaders==None:
            self.leaders=[]
        else:
            self.leaders=leaders

        #初始化追随者
        if accepters==None:
            self.accepters=[]
        else:
            self.accepters=accepters

        self.group=self.leaders+self.accepters  #组
        self.isPrimary=False    #自身是不是领导
        self.proposalCount=0    #协议数量
        self.msgPump=MessagePump(self,port) #消息传送器
        self.instances={}   #接口,实例
        self.hbListener=PaxosLeader.heartbeatListener(self) #监听
        self.hbSender=PaxosLeader.heartbeatSender(self)     #发送
        self.highestInstance=-1     #协议状态
        self.stoped=True            #状态 是否正在运行
        self.lasttime=time.time()   #最后一次时间

    def start(self):
        self.hbListener.start() #开启心跳监听线程
        self.hbSender.start()   #开启心跳发送线程
        self.msgPump.start()
        self.stoped=False

    def stop(self):
        self.hbListener.doAbort()
        self.hbSender.doAbort()
        self.msgPump.doAbort()
        self.stoped = False

    def sendMessage(self,message):
        self.msgPump.sendMessage(message)

    def recvMessage(self,message):
        if self.stoped:
            return
        if message==None:
            if self.isPrimary and time.time()-self.lasttime>15.0:
                self.findAndFillGaps()
                self.garbageCollect()
            return
        if message.command==Message.MSG_HEARTBEAT:  #处理心跳信息
            self.hbListener.newHB(message)
            return True
        if message.command==Message.MSG_EXT_PROPOSE:    #额外协议
            print("额外协议",self.port,self.highestInstance)
            if self.isPrimary:
                self.newProposal(message.value) #创建新的协议
            return True
        if self.isPrimary and message.command != Message.MSG_ACCEPTOR_ACCEPT:
            self.instances[message.instanceID].getProtocol(message.proposalID).doTransition(message)
        if message.command==Message.MSG_ACCEPTOR_ACCEPT:
            if message.instanceID not in self.instances:
                self.instances[message.instanceID]=InstanceRecord()
            record=self.instances[message.instanceID]   #记录
            if message.proposalID not in record:    #创建
                protocal=PaxosLeaderProtocol(self)
                protocal.state=PaxosLeaderProtocol.STATE_AGREED
                protocal.proposalID=message.proposalID
                protocal.instanceID=message.instanceID
                protocal.value=message.value
                record.addProtocol(protocal)
            else:
                record.getProtocol(message.proposalID)  #取出
            protocal.doTranition()   #处理???不加参数message???
        return True

    def setPrimary(self,primary):   #设置领导者
        if primary:
            print("设置我是leader"%self.port)
        else:
            print("设置我不是leader"%self.port)
        self.isPrimary=primary

    def getGroup(self):     #获取组所有成员
        return self.group

    def getLeaders(self):   #获取所有领导
        return self.leaders

    def getAccepter(self):  #获取所有追随者
        return self.accepters

    def getQuorumSize(self):    #必须获得1/2以上追随者支持
        return (len(self.getAccepter())/2)+1

    def getInstanceValue(self,instanceID): #获取接口数据
        if instanceID in self.instances:
            return self.instances[instanceID].value
        return None

    def getHistory(self):   #抓取历史
        return [self.getInstanceValue(i) for i in range(1,self.highestInstance+1)]

    def getNumAccepted(self):   #获取同意的数量
        return len([v for v in self.getHistory() if v!=None])

    def garbageCollect(self):   #采集无用消息
        for i in self.instances:
            self.instances[i].cleanProtocol()

    def findAndFillGaps(self):  #抓取空白时间处理事务
        for i in range(1,self.highestInstance):
            if self.getInstanceValue(i)==None:
                print("填充空白",i)
                self.newProposal(0,i)
        self.lasttime=time.time()

    def newProposal(self,value,instance=None):  # 发起一个新的提议
        protocol=PaxosLeaderProtocol(self)
        if instance==None:          #创建协议标号
            self.highestInstance += 1
            instanceID = self.highestInstance
        else:
            instanceID = self.highestInstance
        self.proposalCount += 1      #协议追加
        id=(self.port,self.proposalCount)   #保存端口,协议信息
        if instanceID in self.instances:
            record=self.instances[instanceID]
        else:
            record=InstanceRecord()
            self.instances[instanceID]=record
        protocol.propose(value,id,instanceID)
        record.addProtocol(protocol)    #追加协议

    def notifyLeader(self,protocol,message):  # 通知领导
        if protocol.state==PaxosLeaderProtocol.STATE_ACCEPTED:
            print("协议接口%s 被%s 接受"%(message.instanceID,message.value))
            self.instances[message.instanceID].accepted=True
            self.instances[message.instanceID].value=message.value
            self.highestInstance=max(message.instanceID,self.highestInstance)
            return
        if protocol.state==PaxosLeaderProtocol.STATE_REJECTED:  #重试
            self.proposalCount=max(self.proposalCount,message.highestPID[1])
            self.newProposal(message.value)
            return True
        if protocol.state==PaxosLeaderProtocol.STATE_UNDEFINED:
            pass