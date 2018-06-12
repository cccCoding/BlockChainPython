import hashlib

myhash = hashlib.sha256()   #加密对象
myhash.update("xixi".encode("utf-8"))   #传递数据
print(myhash.hexdigest())       #hash密码

for line in dir(hashlib):
    print(line)
