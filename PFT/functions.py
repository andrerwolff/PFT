"""Functions used in PFT application."""


from PFT import classes as c
from PFT import dict as d
from PFT import SQLite as SQL
from PFT import validation as v
import os


def clear():
    """
    Clear prompt screen.
    Windows and Linux use different commands causing an error on Windows.
    """
    if os.name == 'nt':  # Windows
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
    print('DONE')

    print('payee table...', end='')
    SQL.create_table(conn, d.sql_cmd['payeesTable'])
    print('DONE.')

    print('Tables created')


def env_init(conn):
    """Initialize envelope groups and default envelope."""
    for k in d.ENV_GROUPS:
        SQL.create_grp(conn, d.ENV_GROUPS[k])
        print(d.ENV_GROUPS[k], 'group created.')
    # Create income pool envelope object.
    e = c.envelope(d.ENV_GROUPS[1], 'Income Pool')
    # Use object to create entry in envelopes table.
    SQL.create_env(conn, e)
    print(e.name, 'envelope created')
    # Update database.
    conn.commit


def new_acct(conn):
    """Creates a new entry in accounts table, uses user input."""
    # Determine type of account from input, cast as lowercase.
    type = v.new_acct_type()
    if type == 'q':
        return
    # Determine account name from input.
    name = v.new_acct_name()
    if name == 'q':
        return
    # Determine opening balance in account from input, cast as float.
    amt = v.new_acct_amt()
    if amt == 'q':
        return
    # Create account object using input information.
    acct = c.account(type, name, amt)
    # Use object to create entry in accounts table.
    SQL.create_acct(conn, acct)
    print('{} account created, of {} type.'.format(acct.name, acct.type))
    # Update database.
    conn.commit()


def new_env(conn):
    """Creates a new entry in envelopes table, uses user input."""
    # Determine name of envelope from input.
    name = v.new_env_name()
    if name == 'q':
        return
    # Determine group of envelope from input, input * for list of groups.
    group = v.new_env_grp_lst(conn)
    if group == 'q':
        return
    # Create envelope object from input information.
    env = c.envelope(group, name)
    # Use object to create entry in envelopes table.
    SQL.create_env(conn, env)
    print(name + ' envelope created in ' + group + ' group.')
    # Update database.
    conn.commit()


def new_group(conn):
    """Creates a new group entry in groups table, uses user input."""
    # Determine name of group from input.
    name = v.new_env_grp_usr(conn)
    if name == 'q':
        # Return 'q' to indicate user wants to quit.
        return name
    # Create a new group entry in groups table.
    SQL.create_grp(conn, name)
    print(name + ' group created.')
    # Pass name on for envelope creation.
    return name
    conn.commit()


def new_payee(conn, mode):
    """Creates a new payee entry in payees table, uses user input."""
    # Determine name of new payee from input.
    name = v.new_payee_usr(conn, mode)
    if name == 'q':
        # Return 'q' to indicate user wants to quit.
        return name
    # List payees in payees table (payers/payees based on mode)
    ids, names = SQL.list_payees(conn, mode)  # ids,names not used, Delete?
    # Create a new payee in payees table.
    SQL.create_payee(conn, name, mode)
    print(name + ' payee created.')
    # Pass payee name on for transaction creation.
    return name
    conn.commit()


def print_options():
    """Print list of available options from option dictionary."""
    print('Choose an action from the list.')
    # Print main menu options based on dict entry.
    for i in range(len(d.OPTIONS_P)):
        print(':: {}'.format(d.OPTIONS_P[i]))


def print_accts(conn):
    """Print list of accounts and balances."""
    # Collect info on existing accounts.
    ids, names, amts = SQL.list_accts(conn)
    # For each item in acounts table...
    for i in range(len(ids)):
        # Print Account ID, Account Name, Converted cents to dollar amount.
        print(':: {} - {}: ${}'.format(ids[i], names[i],
                                       format(amts[i]/100, '.2f')))
    # Needed to avoid auto clear when displaying accounts stand alone.
    input('Enter to continue...')
    # Return lists if needed.
    return ids, names, amts


def print_envs(conn):
    """Print list of envelopes and balances."""
    # Collect info on existing envelopes.
    ids, names, amts = SQL.list_envs(conn)
    for i in range(len(ids)):
        # Print Env ID, Env Name, Converted cents to dollar amount.
        print(':: {} - {}: ${}'.format(ids[i], names[i],
                                       format(amts[i]/100, '.2f')))
    # Needed to avoid auto clear when displaying envelopes stand alone.
    input('Enter to continue...')
    # Return lists if needed.
    return ids, names, amts


def print_groups(conn):
    """Print list of groups"""
    # Collect info on existing groups.
    ids, names = SQL.list_groups(conn)
    for i in range(len(ids)):
        # Print Group ID, Group Name.
        print(':: {} - {}'.format(ids[i], names[i]))
    # Un-comment if needed to avoid auto clear.
    input('Enter to continue...')
    # Return lists if needed.
    return ids, names


def print_payees(conn, mode):
    """Print list of payees or payers"""
    # Collect info on existing payees or payers based on mode
    ids, names = SQL.list_payees(conn, mode)  # dep - payers/wthdrw - payees
    for i in range(len(ids)):
        # Print payee/payer ID, payee/payer Name.
        print(":: {} - {}".format(ids[i], names[i]))
    # Return lists if needed.
    return ids, names


def env_trans(conn, mode):
    """
    Gather info required to create a new transaction between envelopes.
    A 'fund' is moving money from income pool to another envelope.
    A 'Transfer' is moving money from one envelope to another.
    Calls into SQLite.py for SQL commands.
    """
    clear()
    # Since all funding amounts come from income pool, set from_name to that.
    if mode == 'fund':
        fromName = 'Income Pool'
    # Transfers need user defined fromEnv and toEnv names, 'q' stops function.
    elif mode == 'transfer':
        fromName = v.select_envelope(conn, 'transferFrom')
        if fromName == 'q':
            return
    # Incase mode doesnt come through...
    else:
        print('error in f.env_trans')
        return
    # While loop incase user inputs same envelope for to/from.
    while True:
        toName = v.select_envelope(conn, mode)
        if toName == 'q':
            return
        # If the user enters the same envelope as the fromEnv.
        elif toName == fromName:
            print("You cant transfer in/out of the same envelope.")
            continue
        else:
            break
    # Get amount from user.
    amt = v.transfer_amt(conn, mode, fromName)
    if amt == 'q':
        return
    # Run SQL statement to create new transaction in transactions table.
    SQL.transfer(conn, fromName, toName, amt)
    conn.commit()  # Move to SQL.transfer()?


def transaction(conn, mode):
    """
    Gather info required to create a new transaction between an account and an
    envelope.
    Deposits go into an account and into a chosen envelope, requires a payee.
    Withdrawals come out of an account and out of a chosen envelope,
    requires a payer.
    Calls into SQLite.py for SQL commands.
    """
    clear()
    # Gather all necessary inputs, 'q' stops function.
    acct_name = v.select_account(conn, mode)
    if acct_name == 'q':
        return
    env_name = v.select_envelope(conn, mode)
    if env_name == 'q':
        return
    if mode == 'withdraw':
        amt = v.transfer_amt(conn, mode, env_name)
    else:
        amt = v.transfer_amt(conn, mode)
    if amt == 'q':
        return
    payee = v.select_payee_lst(conn, mode)
    if payee == 'q':
        return
    # Run SQL statement to create new transaction in transactions table.
    SQL.transact(conn, acct_name, env_name, amt, payee, mode)


def transfer(conn):
    """Called from main menu. Calls env_trans in transfer mode."""
    env_trans(conn, 'transfer')
    conn.commit()  # Move to SQL.transfer()?


def fund(conn):
    """Called from main menu. Calls env_trans in fund mode."""
    env_trans(conn, 'fund')
    conn.commit()  # Move to SQL.transfer()?


def deposit(conn):
    """Called from main menu. Calls transaction in deposit mode."""
    transaction(conn, 'deposit')
    conn.commit()  # Move to SQL.transfer()?


def withdraw(conn):
    """Called from main menu. Calls transaction in withdraw mode."""
    transaction(conn, 'withdraw')
    conn.commit()  # Move to SQL.transfer()?


def close_acct(conn):
    """Called from main menu."""
    name = v.select_account(conn, 'close')
    if name == 'q':
        return
    SQL.close_account(conn, name)
    conn.commit()


def quit(conn):
    conn.commit()
