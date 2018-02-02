"""Functions used in PFT application."""


from PFT import classes as c
from PFT import dict as d
from PFT import SQLite as SQL
import os

def clear():
    """
    Clear prompt screen.
    Windows and Linux use different commands causing an error on Windows.
    """
    if os.name == 'nt': # Windows
        os.system('cls')
    else:
        os.system('clear')


def table_init(conn):
    """Initialize tables for first time setup."""
    clear()
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
    """Initialize envelope groups and default envelope."""
    for k in d.ENV_GROUPS:
        SQL.create_grp(conn, k, d.ENV_GROUPS[k])
        print(d.ENV_GROUPS[k], 'group created.')
    # Create income pool envelope object.
    e = c.envelope(d.ENV_GROUPS[1], 'Income Pool')
    # Use object to create entry in envelopes table.
    SQL.create_env(conn, e)
    print(e.name, 'envelope created')
    # Update database.
    conn.commit


def new_acct_i(conn):
    """Creates a new entry in accounts table, uses user input.

        TODO:   -input validation
                    -type   :not blank
                            :savings or checking others?
                            :cast as lowercase for consistency
                    -name   :not blank
                    -amt    :not blank
                            :number
    """
    # Determine type of account from input, cast as lowercase.
    type = input('Account Type: ').lower()
    # Determine account name from input.
    name = input('Account Name: ')
    # Determine opening balance in account from input, cast as float.
    amt = float(input('Account Amount: '))
    # Create account object using input information.
    acct = c.account(type, name, amt)
    # Use object to create entry in accounts table.
    SQL.create_acct(conn, acct)
    print('{} account created, of {} type.'.format(acct.name, acct.type))
    # Update database.
    conn.commit()


def new_env_i(conn):
    """Creates a new entry in envelopes table, uses user input.

        TODO:   -input validation
                    -name   :not blank
                    -group  :not blank
                            :in list of groups
                -make new group if name not in group list
    """
    # Determine name of envelope from input.
    name = input('Envelope Name: ')
    # Determine group of envelope from input, input * for list of groups.
    group = input('Envelope Group (* for list): ')
    if group == '*':
        # Print envelop groups and return the info lists if needed.
        ids, names = print_groups(conn)
        while True:
            # Select group by listed number.
            i = input('Select a group by number ("q" to quit): ')
            if i == 'q':
                # If q input cancel envelope creation.
                return
            # If selection is in the id's of the groups, set name of group.
            elif int(i) in ids:
                group = names[int(i)-1]
                break
    # Create envelope object from input information.
    env = c.envelope(group, name)
    # Use object to create entry in envelopes table.
    SQL.create_env(conn, env)
    print(name + ' envelope created in ' + group + ' group.')
    # Update database.
    conn.commit()


def print_options():
    """Print list of available options from option dictionary."""
    clear()
    print('Choose and action from the list.')
    for i in range(len(d.OPTIONS_P)):
        print(':: {}'.format(d.OPTIONS_P[i]))


def print_accts(conn):
    """Print list of accounts and balances."""
    # Collect info on existing accounts.
    ids, names, amts = SQL.list_accts(conn)
    for i in range(len(ids)):
        print(':: {} - {}: {}'.format(ids[i], names[i], amts[i]))
    # Needed to avoid auto clear when displaying accounts stand alone.
    input('Enter to continue...')
    # Return lists if needed.
    return ids, names, amts


def print_envs(conn):
    """Print list of envelopes and balances."""
    # Collect info on existing envelopes.
    ids, names, amts = SQL.list_envs(conn)
    for i in range(len(ids)):
        print(':: {} - {}: {}'.format(ids[i], names[i], amts[i]))
    # Needed to avoid auto clear when displaying envelopes stand alone.
    input('Enter to continue...')
    # Return lists if needed.
    return ids, names, amts


def print_groups(conn):
    """Print list of groups"""
    # Collect info on existing groups.
    ids, names = SQL.list_groups(conn)
    for i in range(len(ids)):
        print(':: {} - {}'.format(ids[i], names[i]))
    # Un-comment if needed to avoid auto clear.
    # input('Enter to continue...')
    # Return lists if needed.
    return ids, names


def fund(conn):
    clear()
    name = input('Which envelope do you want to fund (* for list): ')
    if name == '*':
        ids, names, amts = print_envs(conn)
        while True:
            i = input('Select a envelope by number ("q" to quit): ')
            if i == 'q':
                return
            elif int(i) in ids:
                name = names[int(i)-1]
                break
    amt = int(input('How much do you want to fund: '))
    SQL.env_trans(conn, 'Income Pool', name, amt)
    conn.commit()


def env_trans(conn):
    clear()
    fromName = input('Which envelope do you want to\
transfer from (* for list): ')
    if fromName == '*':
        ids, names, amts = print_envs(conn)
        while True:
            i = input('Select a envelope by number ("q" to quit): ')
            if i == 'q':
                return
            elif int(i) in ids:
                fromName = names[int(i)-1]
                break
    toName = input('Which envelope do you want to transfer to (* for list): ')
    if toName == '*':
        ids, names, amts = print_envs(conn)
        while True:
            i = input('Select a envelope by number ("q" to quit): ')
            if i == 'q':
                return
            elif int(i) in ids:
                toName = names[int(i)-1]
                break
    amt = int(input('How much do you want to transfer: '))
    SQL.env_trans(conn, fromName, toName, amt)
    conn.commit()


def deposit(conn):
    clear()
    name = input('Deposit into which account(* for list): ')
    if name == '*':
        ids, names, amts = print_accts(conn)
        while True:
            i = input('Select a acount by number ("q" to quit): ')
            if i == 'q':
                return
            elif int(i) in ids:
                name = names[int(i)-1]
                break
    amt = int(input('How much is the deposit: '))
    SQL.acct_dep(conn, name, amt)
    conn.commit()


def withdraw(conn):
    clear()
    acct_name = input('Withdraw from which account(* for list): ')
    if acct_name == '*':
        ids, names, amts = print_accts(conn)
        while True:
            i = input('Select a acount by number ("q" to quit): ')
            if i == 'q':
                return
            elif int(i) in ids:
                acct_name = names[int(i)-1]
                break
    env_name = input('Withdraw from which envelope(* for list): ')
    if env_name == '*':
        ids, names, amts = print_envs(conn)
        while True:
            i = input('Select an envelope by number ("q" to quit): ')
            if i == 'q':
                return
            elif int(i) in ids:
                env_name = names[int(i)-1]
                break
    amt = int(input('How much is the withdrawal: '))
    SQL.acct_with(conn, acct_name, env_name, amt)
    conn.commit()


def quit(conn):
    pass
