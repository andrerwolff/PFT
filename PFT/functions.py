from PFT import classes as c
from PFT import dict as d
from PFT import SQLite as SQL
import os


def table_init(conn):
    """Initialize tables for first time setup."""
    os.system('clear')
    print('accounts table...', end='')
    SQL.create_table(conn, d.sql_cmd['accountsTable'])
    print('DONE.')
    print('groups table...', end='')
    SQL.create_table(conn, d.sql_cmd['groupsTable'])
    print('DONE.')
    print('envelopes table...', end='')
    SQL.create_table(conn, d.sql_cmd['envelopesTable'])
    print('DONE.')
    print('transactions table...', end='')
    SQL.create_table(conn, d.sql_cmd['transactionsTable'])
    print('DONE.')
    print('Tables created')


def env_init(conn):
    """Initialize envelope groups and initial envelopes."""
    for k in d.ENV_GROUPS:
        SQL.create_grp(conn, k, d.ENV_GROUPS[k])
        print(d.ENV_GROUPS[k], 'group created.')
    # Create utility group and income pool envelope by default.
    e = c.envelope(d.ENV_GROUPS[1], 'Income Pool')
    SQL.create_env(conn, e)
    print(e.name, 'envelope created')


def new_acct_i(conn):
    type = input('Account Type: ').lower()
    name = input('Account Name: ')
    amt = int(input('Account Amount: '))
    acct = c.account(type, name, amt)
    SQL.create_acct(conn, acct)
    print('{} account created, of {} type.'.format(acct.name, acct.type))
    conn.commit()


def new_env_i(conn):
    name = input('Envelope Name: ')
    group = input('Envelope Group (press * for list): ')
    if group == '*':
        ids, names = print_groups(conn)
        i = int(input('Select a group by number: '))
        if i in ids:
            if i == 9:
                group = input("Envelope Group Name: ")
            else:
                group = names[i-1]
    env = c.envelope(group, name)
    SQL.create_env(conn, env)
    print(name + ' envelope created in ' + group + ' group.')
    conn.commit()


def print_options():
    #os.system('clear')
    print('Choose and action from the list.')
    for i in range(len(d.OPTIONS_P)):
        print(':: {}'.format(d.OPTIONS_P[i]))


def print_groups(conn):
    ids, names = SQL.list_groups(conn)
    for i in range(len(ids)):
        print(':: {} - {}'.format(ids[i], names[i]))
    return ids, names


def fund(conn):
    name = input('Which envelope do you want to fund: ')
    amt = int(input('How much do you want to fund: '))
    SQL.env_trans(conn, 'Income Pool', name, amt)
    conn.commit()


def new_env(conn):
    pass


def new_acct(conn):
    pass


def env_trans(conn):
    fromName = input('Which envelope do you want to transfer from: ')
    toName = input('Which envelope do you want to transfer to: ')
    amt = int(input('How much do you want to transfer: '))
    SQL.env_trans(conn, fromName, toName, amt)
    conn.commit()


def quit(conn):
    pass
