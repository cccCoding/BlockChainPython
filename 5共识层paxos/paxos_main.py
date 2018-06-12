#测试运行模块
from Message import Message
from MessagePump import MessagePump
from InstanceRecord import InstanceRecord
from PaxosAccepterProtocol import PaxosAccepterProtocol
from PaxosLeaderProtocol import PaxosLeaderProtocol
from PaxosAccepter import PaxosAccepter
from PaxosLeader import PaxosLeader
import threading,socket,pickle,queue
import random
import time

if __name__=="__main__":
    #设定5个客户端
    numClients=5
    clients=[PaxosAccepter(port,[54321,54322]) for port in range(65432,65432+numClients)]   #???
    #两个领导者
    leader1=PaxosLeader(54321,[54322],[c.port for c in clients])
    leader2=PaxosLeader(54322,[54321],[c.port for c in clients])

    #开启领导者与追随者
    leader1.start()
    leader1.setPrimary(True)
    leader2.start()
    leader2.setPrimary(True)
    for c in clients:
        c.start()

    #模拟破环情况,客户端不链接
    clients[0].fail()
    clients[1].fail()

    #通信
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)   #UDP协议
    start=time.time()

    for i in range(1000):
        m=Message(Message.MSG_EXT_PROPOSE)
        m.value=0+i #消息参数
        m.to=54322  #设置传递的端口
        bytes=pickle.dumps(m)   #提取二进制数据
        s.sendto(bytes,"localhost",m.to)    #发送消息

    while leader2.getNumAccepted()<999:
        print("休眠的这一秒%d"%leader2.getNumAccepted())
        time.sleep(1)

    print(u"休眠10秒")
    time.sleep(10)

    print(u"停止leaders")
    leader1.stop()
    leader2.stop()

    print(u"停止客户端")
    for c in clients:
        c.stop()

    print(u"leader1历史记录 %s")
    print(leader1.getHistory())

    print(u"leader2历史记录 %s")
    print(leader2.getHistory())


    end=time.time()
    print(u"一共用了%f秒"%(end-start))