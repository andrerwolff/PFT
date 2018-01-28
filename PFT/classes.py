"""Classes used in PFT application."""


import datetime


class container:
    def __init__(self, name, amt, type):
        self.name = name
        self.amt = amt
        self.type = type


class account(container):
    def __init__(self, type, name, amt):
        super().__init__(name, amt, 'acct')
        self.type = type + "_" + self.type

    def deposit(self, envIn, amt, memo=''):
        self.amt += amt
        envIn.amt += amt
        t = transaction(self, envIn, amt, 'deposit', memo)
        return t

    def withdraw(self, envOut, amt, memo=''):
        self.amt -= amt
        envOut.amt -= amt
        t = transaction(self, envOut, amt, 'withdrawal', memo)
        return t


class envelope(container):
    def __init__(self, group, name, amt=0):
        super().__init__(name, amt, 'env')
        self.group = group
        self.amt = amt

    def envTransfer(self, envIn, amt, memo=''):
        self.amt -= amt
        print(type(amt))
        print(type(envIn.amt))
        envIn.amt = envIn.amt + amt
        t = transaction(self, envIn, amt, 'transfer', memo)
        return t


class transaction:
    def __init__(self, a, b, amt, type, memo=''):
        self.tOut = a
        self.tIn = b
        self.amt = amt
        self.type = type
        self.memo = memo
        self.date = datetime.datetime.today().strftime('%Y-%m-%d')
