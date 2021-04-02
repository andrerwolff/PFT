import datetime
from nose.tools import assert_equal
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

    p = payee("Payee1", "test")
    d = acct.transaction(env, 100, "deposit", p)
    assert_equal(d.tA.name, 'Test')
    assert_equal(d.tB.name, 'Rent')
    assert_equal(d.amt, 100)
    assert_equal(d.memo, '')
    assert_equal(d.date, today.strftime('%Y-%m-%d'))

    assert_equal(acct.amt, 2100)
    assert_equal(env.amt, 100)

    w = acct.transaction(env, 50, "withdraw", p, 'Pay Rent')
    assert_equal(w.tA.name, 'Test')
    assert_equal(w.tB.name, 'Rent')
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
    print(tt.memo)
    assert_equal(tt.tA.name, 'Income Pool')
    assert_equal(tt.tB.name, 'Savings')
    assert_equal(tt.amt, 300)
    assert_equal(tt.memo, 'Savings Sweep')
    assert_equal(tt.date, today.strftime('%Y-%m-%d'))

    assert_equal(pool.amt, 700)
    assert_equal(env.amt, 500)
