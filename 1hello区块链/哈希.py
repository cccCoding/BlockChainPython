import hashlib  #加密模块

sha=hashlib.sha256()    #加密算法,sha256
sha.update("123456".encode("utf-8"))    #转化二进制
print(sha.hexdigest())  #哈希值