import numpy as np

#原理 s*c=wx+e

#制造key
def createKey(w,m,n):   # w 向量, m,n 范围
    S = (np.random.rand(m,n)*w/(2**16))    #随机数  一般情况  max(S)<w  ???
    return S

#加密
def encrypt(x,S,m,n,w): # x 消息(用于加密), S 密钥 ,w 向量, m,n 范围
    e = (np.random.rand(m)) #创建随机数
    c = np.linalg.inv(S).dot((w*x)+e)   #加密
    return c

#解密
def decrypt(c,S,w): # c 解密的数据, S 密钥 ,w 向量(权重)
    return (S.dot(c)/w).astype("int")   #解密

x = np.array([1,200,100,1000])
print(x)
m = len(x)
print(m)
n = m
w = 16
S = createKey(w,m,n)
print("S",S)
c = encrypt(x,S,m,n,w)
print("c",c)
print(decrypt(c,S,w))