#给予socket传递消息,封装网络类传递消息
import threading    #线程
import pickle       #对象序列化
import socket       #网络信息传输
import queue        #队列
class MessagePump(threading.Thread):

    class MPHelper(threading.Thread):   #内部类,传递消息,封装
        def __init__(self):   #onwer,属于谁
            threading.Thread.__init__(self)     #父类初始化

        def run(self):      #运行
            while not self.owner.abort: #只要所有者线程没结束,一直run
                try:
                    #返回二进制数据,返回地址
                    (bytes,addr)=self.owner.socket.recvfrom(2048)    #收取消息
                    msg=pickle.load(bytes)  #读取二进制数据转化消息
                    msg.addr=addr[1]        #取出地址
                    self.owner.queue.put(msg)   #队列存入消息
                except Exception as e:
                    print(e)

    def __init__(self,owner,port,timeout=3):
        self.owner=owner
        threading.Thread.__init__(self)
        self.abort=False
        self.timeout=timeout        #超时时间
        self.port=port      #端口
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #UDP通信
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,200000)   #通信参数
        self.socket.bind("127.0.0.1",port)  #通信地址绑定,ip,端口
        self.socket.settimeout(self.timeout)
        self.queue=queue.Queue()    #消息队列
        self.helper=MessagePump.MPHelper(self)  #接受消息

    def run(self):
        self.helper.start() #开启收消息的线程
        while not self.abort:
            message=self.waitForMessage()   #阻塞等待消息
            self.owner.recvMessage(message) #收取消息

    def waitForMessage(self):   #等待消息
        try:
            msg=self.queue.get(True,3)  #抓取数据,最多等三秒
            return msg
        except Exception as e:
            print(e)
            return None

    def sendMessage(self,message):      #发消息
        bytes=pickle.dumps(message) #消息转成二进制
        address=("127.0.0.1",message.to)    #地址,ip,端口
        self.socket.sendto(bytes,address)   #发送消息
        return True

    def doAbort(self):          #停止运行,设置状态为放弃
        self.abort=True