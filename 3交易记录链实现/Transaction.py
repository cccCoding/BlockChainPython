import datetime

class Transaction:      #交易类
    def __init__(self,
                 payer,     #付款方
                 receiver,  #收款方
                 money):    #数字货币数量
        self.payer=payer
        self.receiver=receiver
        self.money=money
        self.timestamp=datetime.datetime.now()

    def __repr__(self):
        return str(self.payer)+" "+str(self.receiver)+" "+str(self.money)+" "+str(self.timestamp)





