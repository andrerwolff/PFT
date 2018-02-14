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
    """
    Create new account entry in accounts table.

    Function takes account instance, and creates entry in accounts table.
    The balance of the account is then added to income pool envelope.
    """
    try:
        # Gather information from acct instance.
        info = (acct.type, acct.name, acct.amt)
        cur = conn.cursor()
        # Call SQL statement with necessary information to create account.
        cur.execute(d.sql_cmd['createAcct'], info)
        # Create Income Pool Envelope instance from table entry
        pool = create_env_object(conn, 'Income Pool')
        # Add account balance to income pool.
        pool.amt += acct.amt
        # Update income pool entry with new amount.
        cur.execute(d.sql_cmd['updateEnv'], (pool.amt, 'Income Pool'))
    except Error as e:
        print(e)


def create_grp(conn, name):
    """
    Create a new group in groups table.

    See create_acct() for details, similar process.
    """
    cur = conn.cursor()
    try:
        cur.execute(d.sql_cmd['createGrp'], (name,))  # Needs to be list..?
    except Error as e:
        print(e)


def create_env(conn, env):
    """
    Create new envelope entry in envelopes table.

    See create_acct() for details, similar process.
    """
    try:
        info = (env.group, env.name, env.amt)
        cur = conn.cursor()
        cur.execute(d.sql_cmd['createEnv'], info)
    except Error as e:
        print(e, 'env')


def create_payee(conn, name, mode):
    """
    Create new payee entry in envelopes table.

    See create_acct() for details, similar process.
    Modes are deposit and withdraw.
    """
    if mode == 'deposit':
        # If in deposit mode, set type as 1 for payer.
        type = 1
    elif mode == 'withdraw':
        # If in withdraw mode, set type as 2 for payee.
        type = 2
    try:
        info = (name, type)
        cur = conn.cursor()
        cur.execute(d.sql_cmd['createPayee'], info)
    except Error as e:
        print(e, 'payee')


def create_transaction(conn, t, mode):
    """
    Create new transaction entry for each mode using transaction object.

    See create_acct() for details, similar processes.
    Modes are transfer, deposit, or withdraw.
    Transaction entries include the following columns...
    Date, Type, Memo, Amount, To Acct Id, From Acct Id,
    To Envelope Id, From Envelope Id, Payee/Payer Id.
    """
    if mode == 'transfer':
        try:
            # Nothing for account_to and account_from, also no payee.
            info = (t.date, t.type, t.memo, t.amt,
                    '', '', t.tB.id, t.tA.id, '')  # env_to, env_from
            cur = conn.cursor()
            cur.execute(d.sql_cmd['createTrans'], info)
        except Error as e:
            print(e, 'trans')
    if mode == 'deposit':
        try:
            # Nothing for account_from and env_from.
            info = (t.date, t.type, t.memo, t.amt,
                    t.tA.id, '', t.tB.id, '', t.payee.id)  # acct_to, env_to
            cur = conn.cursor()
            cur.execute(d.sql_cmd['createTrans'], info)
        except Error as e:
            print(e, 'dep')
    if mode == 'withdraw':
        try:
            # Nothing for account_to and env_to.
            info = (t.date, t.type, t.memo, t.amt,
                    '', t.tA.id, '', t.tB.id, t.payee.id)  # acct_frm, env_from
            cur = conn.cursor()
            cur.execute(d.sql_cmd['createTrans'], info)
        except Error as e:
            print(e, 'with')


def create_acct_object(conn, name):
    """
    Create an account object with details from table entry.

    Function takes name of existing account in accounts table.
    Using the name, an account object is created with all stored details.
    Returns the created account object.
    """
    # Call SQL statement to select desired account entry in accounts table.
    sql = "{}'{}'".format(d.sql_cmd['selectAcctName'], name)
    cur = conn.cursor()
    cur.execute(sql)
    # Fetch the account entry and parse the info into temp variables.
    i, t, n, a = cur.fetchone()  # ID, Type, Name, Amount
    # Create account object using fetched info.
    acct = c.account(t, n, a, id=i)
    return acct


def create_env_object(conn, name):
    """
    Create an envelope object with details from table entry.

    See create_acct_object() for details, similar process.
    """
    sql = "{}'{}'".format(d.sql_cmd['selectEnvName'], name)
    cur = conn.cursor()
    cur.execute(sql)
    i, g, n, a = cur.fetchone()  # ID, Group, Name, Amount
    # I think 0 in DB is read in as '', so make sure 0 is 0.
    if type(a) is not int:
        a = 0
    env = c.envelope(g, n, amt=a, id=i)
    return env


def create_payee_object(conn, name):
    """
    Create a payee object with details from table entry.

    See create_acct_object() for details, similar process.
    """
    sql = "{}'{}'".format(d.sql_cmd['selectPayeeName'], name)
    cur = conn.cursor()
    cur.execute(sql)
    i, n, t = cur.fetchone()  # ID, Name, Type (1-Payer, 2-Payeee)
    p = c.payee(n, t, id=i)
    return p


def list_accts(conn):
    """Gather info from accounts table and return list of accounts."""
    cur = conn.cursor()
    cur.execute(d.sql_cmd['listAccts'])
    # Fetch all accounts and parse their info into a list.
    lst = cur.fetchall()
    # Initialize temp storage lists.
    acct_ids = []
    acct_names = []
    acct_amts = []
    # For each account in the list of accounts, parse into separate lists.
    for a in lst:
        acct_ids.append(int(a[0]))  # Cast IDs as integer
        acct_names.append(str(a[1]))  # Cast Names as string
        acct_amts.append(int(a[2]))  # Cast Amounts as Integer.
    return acct_ids, acct_names, acct_amts


def list_groups(conn):
    """
    Gather info from groups table and return lists.

    See list_accts() for details, similar process.
    """
    cur = conn.cursor()
    cur.execute(d.sql_cmd['listGroups'])
    lst = cur.fetchall()
    grp_ids = []
    grp_names = []
    for g in lst:
        grp_ids.append(int(g[0]))  # Cast IDs as integer
        grp_names.append(str(g[1]))  # Cast names as string
    return grp_ids, grp_names


def list_envs(conn):
    """
    Gather info from envelopes table and return lists.

    See list_accts() for details, similar process.
    """
    cur = conn.cursor()
    cur.execute(d.sql_cmd['listEnvs'])
    lst = cur.fetchall()
    env_ids = []
    env_names = []
    env_amts = []
    for e in lst:
        env_ids.append(int(e[0]))  # Cast IDs as integer
        env_names.append(str(e[1]))  # Cast Names as string
        env_amts.append(int(e[2]))  # Cast Amounts as integer
    return env_ids, env_names, env_amts


def list_payees(conn, mode):
    """
    Gather info from payees table and return lists.

    See List_accts() for details, similar process.
    Modes are deposit or withdraw.
    """
    cur = conn.cursor()
    if mode == 'deposit':
        # Payee created with type 1 for Payer
        cur.execute(d.sql_cmd['listPayees'] + '1')
    elif mode == 'withdraw':
        # Payee created with type 2 for Payee
        cur.execute(d.sql_cmd['listPayees'] + '2')
    else:
        print("error in list payees", mode)
    lst = cur.fetchall()
    payee_ids = []
    payee_names = []
    for p in lst:
        payee_ids.append(int(p[0]))  # Cast IDs as integer
        payee_names.append(str(p[1]))  # Cast Names as string
    return payee_ids, payee_names


def transact(conn, acct_name, env_name, amt, payee_name, mode):
    """
    Using supplied info, facilitate a transaction.

    Transactions happen to or from an account and envelope.
    Transactions have payees or payers (referenced as payee).
    This function creates acct, env, payee and transaction objects.
    Using objects, call create_transaction for table entry.
    Updates accounts and envelopes accordingly.
    """
    # Create account object.
    acct = create_acct_object(conn, acct_name)
    # Create envelope object.
    env = create_env_object(conn, env_name)
    # Create payee object.
    p = create_payee_object(conn, payee_name)
    # Create transaction using class method.
    t = acct.transaction(env, amt, mode, payee=p)
    cur = conn.cursor()
    # Call to create transaction entry in table.
    create_transaction(conn, t, mode)
    # Update account entry with transaction amount.
    cur.execute(d.sql_cmd['updateAcct'], (acct.amt, acct.name))
    # Update envelope entry with transaction amount.
    cur.execute(d.sql_cmd['updateEnv'], (env.amt, env.name))


def transfer(conn, fromName, toName, amt):
    """
    Initiate a envelope transfer.

    See transact() for details, similar process.
    """
    fromEnv = create_env_object(conn, fromName)
    toEnv = create_env_object(conn, toName)
    t = fromEnv.envTransfer(toEnv, amt)  # payee default as none since no payee
    cur = conn.cursor()
    create_transaction(conn, t, 'transfer')
    cur.execute(d.sql_cmd['updateEnv'], (fromEnv.amt, fromEnv.name))
    cur.execute(d.sql_cmd['updateEnv'], (toEnv.amt, toEnv.name))
