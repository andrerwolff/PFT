import datetime
from nose.tools import *
from PFT.classes import *


def test_account_deposit_withdrawal():
    today = datetime.datetime.today()

    acct = account('checking', 'Test', 2000)
    assert_equal(acct.name, 'Test')
    assert_equal(acct.type, 'checking_acct')
    assert_equal(acct.amt, 2000)

    env = envelope('Bills', 'Rent')
    assert_equal(env.name, 'Rent')
    assert_equal(env.group, 'Bills')
    assert_equal(env.amt, 0)

    d = acct.deposit(env, 100)
    assert_equal(d.tAcct.name, 'Test')
    assert_equal(d.tEnv.name, 'Rent')
    assert_equal(d.amt, 100)
    assert_equal(d.memo, '')
    assert_equal(d.date, today.strftime('%Y-%m-%d'))

    assert_equal(acct.amt, 2100)
    assert_equal(env.amt, 100)

    w = acct.withdraw(env, 50, 'Pay Rent')
    assert_equal(w.tAcct.name, 'Test')
    assert_equal(w.tEnv.name, 'Rent')
    assert_equal(w.amt, 50)
    assert_equal(w.memo, 'Pay Rent')
    assert_equal(w.date, today.strftime('%Y-%m-%d'))

    assert_equal(acct.amt, 2050)
    assert_equal(env.amt, 50)


def test_envelope_transfer():
    today = datetime.datetime.today()

    pool = envelope('*', 'Income Pool', 1000)
    env = envelope('Goals', 'Savings', 200)
    assert_equal(pool.amt, 1000)
    assert_equal(env.amt, 200)

    tt = pool.envTransfer(env, 300, 'Savings Sweep')
    assert_equal(tt.ttOut.name, 'Income Pool')
    assert_equal(tt.ttIn.name, 'Savings')
    assert_equal(tt.amt, 300)
    assert_equal(tt.memo, 'Savings Sweep')
    assert_equal(tt.date, today.strftime('%Y-%m-%d'))

    assert_equal(pool.amt, 700)
    assert_equal(env.amt, 500)
