"""SQLite related functionality."""

import sqlite3
from sqlite3 import Error
from PFT import dict as d
from PFT import classes as c


def create_connection(database):
    """Connect to database."""
    try:
        conn = sqlite3.Connection(database)
        print('Connected to:', database)
        return conn
    except Error as e:
        print(e)

    return None


def check_empty_db(conn):
    """Check if connected database is empty (no tables) and return bool."""
    cur = conn.cursor()
    cur.execute('SELECT * FROM accounts')

    num = cur.fetchall()

    if not num:
        print('Welcome to PFT. You haven\'t opened any accounts...')
        print("*Hint - press 'a'  and follow prompts to open a new account.")
    else:
        print('Welcome back, setup already complete!')


def create_table(conn, create_table_sql):
    """Create new table using SQL."""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_acct(conn, acct):
    """Create new account entry in accounts table."""
    try:
        info = (acct.type, acct.name, acct.amt)
        cur = conn.cursor()
        cur.execute(d.sql_cmd['createAcct'], info)
        pool = create_env_object(conn, 'Income Pool')
        pool.amt += acct.amt
        cur.execute(d.sql_cmd['updateEnv'], (pool.amt, 'Income Pool'))
    except Error as e:
        print(e)


def create_acct_object(conn, name):
    """Create an account object with details from table entry."""
    sql = "{}'{}'".format(d.sql_cmd['selectAcctName'], name)
    cur = conn.cursor()
    cur.execute(sql)
    i, t, n, a = cur.fetchone()
    acct = c.account(t, n, a, id=i)
    return acct


def list_accts(conn):
    """Gather info from accounts table and return lists."""
    cur = conn.cursor()
    cur.execute(d.sql_cmd['listAccts'])
    lst = cur.fetchall()
    acct_ids = []
    acct_names = []
    acct_amts = []
    for e in lst:
        acct_ids.append(int(e[0]))
        acct_names.append(str(e[1]))
        acct_amts.append(int(e[2]))
    return acct_ids, acct_names, acct_amts


def create_grp(conn, id, name):
    """Create a new group in groups table."""
    cur = conn.cursor()
    try:
        info = (id, name)
        cur.execute(d.sql_cmd['createGrp'], info)
    except Error as e:
        print(e)


def list_groups(conn):
    """Gather info from groups table and return lists."""
    cur = conn.cursor()
    cur.execute(d.sql_cmd['listGroups'])
    lst = cur.fetchall()
    grp_ids = []
    grp_names = []
    for g in lst:
        grp_ids.append(int(g[0]))
        grp_names.append(str(g[1]))
    return grp_ids, grp_names


def create_env(conn, env):
    """Create new envelope entry in envelopes table."""
    try:
        info = (env.group, env.name, env.amt)
        cur = conn.cursor()
        cur.execute(d.sql_cmd['createEnv'], info)
    except Error as e:
        print(e, 'env')


def create_env_object(conn, name):
    """Create an envelope object with details from table entry."""
    sql = "{}'{}'".format(d.sql_cmd['selectEnvName'], name)
    cur = conn.cursor()
    cur.execute(sql)
    i, g, n, a = cur.fetchone()
    if type(a) is not int:
        a = 0
    env = c.envelope(g, n, amt=a, id=i)
    return env


def list_envs(conn):
    """Gather info from envelopes table and return lists"""
    cur = conn.cursor()
    cur.execute(d.sql_cmd['listEnvs'])
    lst = cur.fetchall()
    env_ids = []
    env_names = []
    env_amts = []
    for e in lst:
        env_ids.append(int(e[0]))
        env_names.append(str(e[1]))
        env_amts.append(int(e[2]))
    return env_ids, env_names, env_amts


def create_transaction(conn, t, mode):
    """Create new transaction entry for transfers using transaction object."""
    if mode == 'transfer':
        try:
            info = (t.date, t.type, t.memo, t.amt,
                    '', '', t.tB.id, t.tA.id)
            cur = conn.cursor()
            cur.execute(d.sql_cmd['createTrans'], info)
        except Error as e:
            print(e, 'trans')
    """Create new transaction entry for deposit using transaction object."""
    if mode == 'deposit':
        try:
            info = (t.date, t.type, t.memo, t.amt,
                    t.tA.id, '', t.tB.id, '')
            cur = conn.cursor()
            cur.execute(d.sql_cmd['createTrans'], info)
        except Error as e:
            print(e, 'dep')
    """Create new transaction entry for withdrawal using transacion object."""
    if mode == 'withdraw':
        try:
            info = (t.date, t.type, t.memo, t.amt,
                    '', t.tA.id, '', t.tB.id)
            cur = conn.cursor()
            cur.execute(d.sql_cmd['createTrans'], info)
        except Error as e:
            print(e, 'with')


def transact(conn, acct_name, env_name, amt, mode):
    acct = create_acct_object(conn, acct_name)
    env = create_env_object(conn, env_name)
    t = acct.transaction(env, amt, mode)
    cur = conn.cursor()
    create_transaction(conn, t, mode)
    cur.execute(d.sql_cmd['updateAcct'], (acct.amt, acct.name))
    cur.execute(d.sql_cmd['updateEnv'], (env.amt, env.name))


def transfer(conn, fromName, toName, amt):
    """Initiate a envelope transfer."""
    fromEnv = create_env_object(conn, fromName)
    toEnv = create_env_object(conn, toName)
    t = fromEnv.envTransfer(toEnv, amt)
    cur = conn.cursor()
    create_transaction(conn, t, 'transfer')
    cur.execute(d.sql_cmd['updateEnv'], (fromEnv.amt, fromEnv.name))
    cur.execute(d.sql_cmd['updateEnv'], (toEnv.amt, toEnv.name))
