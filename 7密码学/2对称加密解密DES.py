#加密和解密用的同一个密码称为对称加密

import pyDes    #对称加密算法des

password = b"\0\0\0\0\0\0\0\0"  #必须8bytes
data = b"hello"     #b代表二进制
key = pyDes.des(b"DESCRYPT",    #加密算法
                pyDes.CBC,      #加密模式
                password,       #加密密码
                pad=None,
                padmode=pyDes.PAD_PKCS5)    #加密参数
newdata = key.encrypt(data)
print("加密的结果",newdata)
print("解密的结果",key.decrypt(newdata))