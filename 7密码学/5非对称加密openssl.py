import rsa
import base64
from OpenSSL.crypto import PKey #处理公钥私钥
from OpenSSL.crypto import TYPE_RSA,FILETYPE_PEM,FILETYPE_ASN1  #处理文件
from OpenSSL.crypto import dump_publickey,dump_privatekey   #key写入文件

pk = PKey() #openssl 加密标准,制造key
pk.generate_key(TYPE_RSA,1024)  #rsa类型,1024位
publickeyfile = dump_publickey(FILETYPE_PEM,pk) #导入到文件
privatekeyfile = dump_privatekey(FILETYPE_ASN1,pk)

publickey = rsa.PublicKey.load_pkcs1_openssl_pem(publickeyfile) #获取
privatekey = rsa.PrivateKey.load_pkcs1(privatekeyfile,"DER")

print(publickey.save_pkcs1())   #保存
print(privatekey.save_pkcs1())


data = rsa.encrypt("你好啊我是要加密的消息".encode(),publickey)
data = base64.b64encode(data)
print("加密后结果",data)
data_d = rsa.decrypt(base64.b64decode(data), privatekey)
print("解密后二进制结果",data_d)
print("解密后结果",data_d.decode())


