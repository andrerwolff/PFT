"""Classes used in PFT application."""


import datetime


class container:
    def __init__(self, name, amt, type):
        self.name = name
        self.amt = amt
        self.type = type


class account(container):
    def __init__(self, type, name, amt, id=0):
        super().__init__(name, amt, 'acct')
        self.type = type + "_" + self.type
        self.id = id

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
    def __init__(self, group, name, amt=0, id=0):
        super().__init__(name, amt, 'env')
        self.group = group
        self.amt = amt
        self.id = id

    def envTransfer(self, envIn, amt, memo=''):
        self.amt -= amt
        envIn.amt = envIn.amt + amt
        t = transaction(self, envIn, amt, 'transfer', memo)
        return t


class transaction:
    def __init__(self, a, b, amt, type, memo=''):
        # transfer out - deposit acct - withdrawal acct
        self.tA = a
        # transfer in - pool env - withdrawal env
        self.tB = b
        self.amt = amt
        self.type = type
        self.memo = memo
        self.date = datetime.datetime.today().strftime('%Y-%m-%d')
