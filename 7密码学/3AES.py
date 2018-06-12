from Crypto.Cipher import AES
from binascii import b2a_hex,a2b_hex    #二进制转十六进制

class AES_test:
    def __init__(self,key):
        self.key = key  #加密密码
        self.model = AES.MODE_CBC   #加密函数,加密文本必须是16的倍数,不足补0

    def encrypt(self,text):
        cryptor = AES.new(self.key,self.model,self.key)  #新建加密算法
        text = text.encode("utf-8") #文本转成二进制
        length = 16 #密码长度
        count = len(text)   #求出长度
        add = length - (count%length)   #需要填充的位数
        text = text + (b"\0" * add)     #填充0字符
        self.ciphertext = cryptor.encrypt(text) #加密
        return b2a_hex(self.ciphertext).decode("ASCII") #ascii转化16进制

    def decrypt(self,text):
        cryptor = AES.new(self.key,self.model,self.key)  #新建解密算法
        lasttext = cryptor.decrypt(a2b_hex(text))   #文本转16进制
        return lasttext.rstrip(b'\0').decode("utf-8")   #解码

haha = AES_test("k1k2k3k4k5k6k7k8".encode("utf-8")) #key需要是16个字符
ctext = haha.encrypt("text:hahahaha")
print("加密后的结果",ctext)
text = haha.decrypt(ctext)
print("解密后的结果",text)