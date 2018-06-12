import rsa

pubkey,privatekey = rsa.newkeys(1024)
message = "发了一个消息"
sign = rsa.sign(message.encode(),privatekey,"SHA-1")    #私钥签名后消息
print(rsa.verify(message.encode(),sign,pubkey)) #用公钥验证密文
