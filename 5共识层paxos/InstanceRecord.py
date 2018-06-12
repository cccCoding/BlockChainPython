#本地记录类,追随者,领导者之间的协议

class InstanceRecord:

    def __init__(self):
        self.protocols={}   #协议字典
        self.highestID=(-1,1)   #最高的编号
        self.value=None

    def addProtocol(self,protocol): #增加协议
        self.protocols[protocol.protocolID]=protocol
        if (protocol.protocolID[1]==self.highestID[1] \
            and protocol.protocolID[0]>self.highestID[0]):
            self.highestID=protocol.protocolID      #取得编号最多的协议????


    def getProtocol(self,protocolID):   #根据编号抓取协议
        return self.protocols[protocolID]

    def cleanProtocol(self):        #清理协议
        keys=self.protocols.keys()
        for key in keys:
            del self.protocols[key]     #删除协议