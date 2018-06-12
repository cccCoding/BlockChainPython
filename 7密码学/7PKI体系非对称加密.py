from Crypto import Random   #随机数
from Crypto.Hash import SHA #哈希算法
from Crypto.Cipher import PKCS1_v1_5 as CPKCS1_v1_5   #PKI体系加密解密标准  #别名
from Crypto.Signature import PKCS1_v1_5 as SPKCS1_v1_5    #PKI体系签名标准
from Crypto.PublicKey import RSA    #非对称加密解密
import base64

#随机数生成器
random_maker = Random.new().read

#rsa算法实例
rsa = RSA.generate(1024,random_maker)

#生成密钥 master
private_pem = rsa.exportKey()
public_pem = rsa.publickey().exportKey()

#保存公钥
with open("master-public.pem","wb") as file:
    file.write(public_pem)
#保存私钥
with open("master-private.pem","wb") as file:
    file.write(private_pem)

message = "hello PKI".encode()
with open("master-public.pem","rb") as file:
    key = file.read() #读取key
    rsakey = RSA.import_key(key)    #导入key
    cipher = CPKCS1_v1_5.new(rsakey)    #遵循PKI标准导入key
    c = cipher.encrypt(message)#加密
    cipher_text = base64.b64encode(c)
    print(cipher_text)

with open("master-private.pem","rb") as file:
    key = file.read() #读取key
    rsakey = RSA.import_key(key)    #导入key
    cipher = CPKCS1_v1_5.new(rsakey)    #遵循PKI标准导入key
    text = cipher.decrypt(base64.b64decode(cipher_text),random_maker)
    print(text)

#签名与验证
message = "hello PKI sign".encode()
with open("master-private.pem") as file:
    key = file.read() #读取key
    rsakey = RSA.import_key(key)    #导入key
    signer = SPKCS1_v1_5.new(rsakey)    #签名工具
    digest = SHA.new()#签名算法
    digest.update(message)  #导入签名数据
    sign = signer.sign(digest)  #签名
    signature = base64.b64encode(sign)  #编码
    print(signature)

with open("master-public.pem") as file:
    key = file.read() #读取key
    rsakey = RSA.import_key(key)    #导入key
    signer = SPKCS1_v1_5.new(rsakey)  # 签名工具
    digest = SHA.new()  # 签名算法
    digest.update(message)  # 导入签名数据
    print(signer.verify(digest,base64.b64decode(signature)))#校验

