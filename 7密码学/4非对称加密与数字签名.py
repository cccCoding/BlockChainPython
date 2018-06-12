"""
129*13=1677
1677%1000=677
677*77=52129
52129%1000=129

13*77=1001
1%1000=1001%1000
a*1%1000=a*1001%1000
a = a*13*77%1000    #当位数小于等于3
"""

import rsa  #非对称加密算法

#生成密钥
pubkey,privatekey = rsa.newkeys(1024)
print(pubkey)
print(privatekey)

#密钥的文件操作
with open("rsa_public.pem","w+") as publicfile: #写入公钥
    publicfile.write(pubkey.save_pkcs1().decode())
with open("rsa_private.pem","w+") as privatefile: #写入私钥
    privatefile.write(privatekey.save_pkcs1().decode())

with open("rsa_public.pem","r") as publicfile: #读取公钥
    pubk = rsa.PublicKey.load_pkcs1(publicfile.read().encode())
    print(pubk)
with open("rsa_private.pem","r") as privatefile: #写入私钥
    privkey = rsa.PrivateKey.load_pkcs1(privatefile.read().encode())
    print(privkey)

message = "你是大傻子"
crypto = rsa.encrypt(message.encode("utf-8"),pubkey)    #加密
print("加密后二进制结果",crypto)
text_b = rsa.decrypt(crypto,privatekey)
print("解密后二进制结果",text_b)
text = rsa.decrypt(crypto,privatekey).decode("utf-8")
print("解密后结果",text)


print("----------数字签名,消息认证---------")
sign = rsa.sign(message.encode(),privatekey,"SHA-1")    #私钥签名
try:
    message = "aaa"
    result = rsa.verify(message.encode(),sign,pubkey)   #公钥验证
    print("验证通过",result)
except:
    print("验证不通过")