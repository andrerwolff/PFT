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

    def transaction(self, env, amt, mode, payee, memo=''):
        if mode == 'deposit':
            self.amt += amt
            env.amt += amt
        elif mode == 'withdraw':
            self.amt -= amt
            env.amt -= amt
        else:
            print('error in acct.transaction')
        t = transaction(self, env, amt, mode, payee, memo)
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
        payee = None
        t = transaction(self, envIn, amt, 'transfer', payee, memo)
        return t


class payee:
    def __init__(self, name, type, id=0):
        self.id = id
        self.name = name
        self.type = type


class transaction:
    def __init__(self, a, b, amt, type, payee=None, memo=''):
        # transfer out - deposit acct - withdrawal acct
        self.tA = a
        # transfer in - pool env - withdrawal env
        self.tB = b
        self.amt = amt
        self.type = type
        self.payee = payee
        self.memo = memo
        self.date = datetime.datetime.today().strftime('%Y-%m-%d')
