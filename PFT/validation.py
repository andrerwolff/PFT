"""Handle input validation for PFT application"""
from PFT import functions as f
from PFT import dict as d
from PFT import SQLite as SQL


# Checked
def menu_choice():
    """
    Menu choices should match list presented or return notice.

    Called by main.py main().
    """
    # Keep in loop untill a valid answer is entered.
    while True:
        # Gather input
        ans = input("What would you like to do: ")
        # Check input is not blank or if it somehow didn't happen.
        if ans is not '' and not None:
            # Cast answer as lowercase.
            ans = ans.lower()
            # Check input is in list of appropriate actions. (see options dict)
            if ans in d.OPTIONS:
                # Pass through user's answer.
                return ans
            else:
                # Will print if user enters something that is not an option.
                print("That is not a valid choice, please try again.")
        else:
            # Nothing was input so restart loop.
            pass


# Checked
def new_acct_name():
    """
    Account names should not be longer than 20 chars or return notice.

    Called by f.new_acct().
    """
    while True:
        name = input("New Account Name: ")
        if name is not '' and not None:
            # Check string length for less than 20 chars.
            if len(name) > 20:
                # If too long, restart loop.
                print("That name is too long, please use another name.")
            else:
                # If not too long, return name (breaks out of loop)
                return name  # If name is 'q' will quit calling function.
        else:
            print("You didn't enter a name, please try again. ('q' to cancel)")


# Checked
def new_env_name():
    """
    Envelop names should not be longer than 20 chars or return notice.

    See new_acct_name() for details, same process.

    Called by f.new_env().
    """
    while True:
        name = input("New Envelope Name: ")
        if name is not '' and not None:
            if len(name) > 20:
                print("That name is too long, please use another name.")
            else:
                return name
        else:
            print("You didn't enter a name, please try again. ('q' to cancel)")


# Checked
def new_env_grp_lst(conn):
    """
    Envelope group should come from list or switch to input mode.

    Called by f.new_env() and new_env_grp_usr().
    """
    # Print list of existing groups.
    ids, names = f.print_groups(conn)
    while True:
        i = input("Pick Group From List (* To create new group): ")
        if i is not '' and not None:
            # This try statement casts input as an integer.
            try:
                i = int(i)
            # If input is not an integer, a char or chars were entered.
            except ValueError:
                # If input was * transfer to new group creation.
                if i == '*':
                    # Calls user to create new group by name, and returns name.
                    group = f.new_group(conn)
                    # Check to make sure it actually worked.
                    if group is not '' and not None:
                            # Return new group name, might be 'q' to quit.
                            return group
                    else:
                        # Shouldn't ever come to this. Restarts while loop.
                        continue
                # If input was q, returns that and quits out of calling fn.
                elif i == 'q':
                    return i
                # If input was a character but not * or q, notify and restart.
                else:
                    print('Enter a number from the list of grops.')
                    continue
            # Below happens if the try statement succeeds. i is now an int.
            else:
                # Check input matches an entry in ids.
                if i in ids:
                    # Set id variable to the index of the selected group_id.
                    id = ids.index(i)
                    # Set name using the same index of selected group_id.
                    group = names[id]
                    # Return selected group name.
                    return group
                # If the input didnt match an existing group id.
                else:
                    print('That does not match a group, please try again.')
                    # Restart loop
                    continue
        else:
            # Loop restarts if nothing was entered.
            print("You didn't enter anything, please try again."
                  " ('q' to cancel)")


# Checked
def new_env_grp_usr(conn):
    """
    New group name should be less than 20 chars or notify.

    This is called from f.newGroup() which is called from new_env_grp_lst.
    The returned name will be used to create a new group.
    If returning to list, a new group will be attempted
    but will fail due to UNIQUE?

    Called by f.new_group().
    """
    while True:
        name = input('New Group Name (* back to list): ')
        if name is not '' and not None:
            if len(name) > 20:
                print("That name is too long, please use another name.")
            # If * send back to selecting from list of existing groups.
            elif name == '*':
                name = new_env_grp_lst(conn)
                # Return name that was selected from list.
                return name  # Note this will try to create a group, will fail?
            else:
                # Return name of new group for group creation.
                return name
        else:
            # Notify and restart loop.
            print("You didn't enter a name, please try again. ('q' to cancel)")


def select_payee_lst(conn, mode):
    """
    Selected payee should be in list or switch to input mode.

    Modes are deposit or withdraw. If deposit, interact with payers.
    If withdraw, interact with payees.
    See new_env_grp_lst() for details, similar process.

    Called by f.transaction and new_payee_usr()
    """
    ids, names = f.print_payees(conn, mode)
    while True:
        # Prompts depend on mode
        if mode == 'deposit':
            i = input("Pick Payer From List (* To create new payer): ")
        elif mode == 'withdraw':
            i = input("Pick Payee From List (* To create new payee): ")
        else:
            print("Error in validation", mode)
        if i is not '' and not None:
            try:
                i = int(i)
            except ValueError:
                if i == '*':
                    payee = f.new_payee(conn, mode)
                    if payee is not '' and not None:
                            return payee
                    else:
                        continue
                elif i == 'q':
                    return i
                else:
                    print('Enter a number from the list.')
                    continue
            else:
                if i in ids:
                    id = ids.index(i)
                    payee = names[id]
                    return payee
                else:
                    print('That does not match, please try again.')
                    continue
        else:
            print("You didn't enter anything, please try again."
                  " ('q' to cancel)")


# Checked
def new_payee_usr(conn, mode):
    """
    Payee name should be less than 20 chars.

    See new_group_usr() for detail, same process.

    Called by f.new_payee().
    """
    while True:
        if mode == 'deposit':
            name = input("New Payer Name (* back to list): ")
        elif mode == 'withdraw':
            name = input("New Payee Name (* back to list): ")
        else:
            print("Error in validation", mode)
        if name is not '' and not None:
            if len(name) > 20:
                print("That name is too long, please use another name.")
            elif name == '*':
                name = select_payee_lst(conn, mode)
                return name
            else:
                return name
        else:
            print("You didn't enter a name, please try again. ('q' to cancel)")


# Checked
def new_acct_type():
    """
    Acct type should be s or c or notify.

    Called by f.new_acct().
    """
    while True:
        typ = input("[S]avings or [C]hecking: ")
        if typ is not '' and not None:
            # Cast input as lower.
            typ = typ.lower()
            # Check if checking account.
            if typ == 'c' or typ == 'checking':
                # Return checking as type of account.
                typ = 'checking'
                return typ
            # Check if savings account.
            elif typ == 's' or typ == 'savings':
                # Return savings as type of account.
                typ = 'savings'
                return typ
            # Check if user wants to quit.
            elif typ == 'q':
                # Return to quit calling function.
                return typ
            else:
                # Notify and restart loop.
                print("Please enter a valid account type.")
        else:
            # Notify and restart loop.
            print("You didn't enter a type, please try again. ('q' to cancel)")


# Checked
def new_acct_amt():
    """
    New account amount should be an int (cents), notify if not.

    If the amount is negative, confirm with user.
    If the amount is very large, confirm with user.
    Amounts stored will be integers representing cents (x100).

    Called by f.new_acct().
    """
    while True:
        amt = input('New Account Balance: ')
        if amt is not '' and not None:
            try:
                # Amount cast as int after casted as float and converted.
                amt = int(float(amt)*100)  # Converted to cents for storage
            except ValueError:
                if amt == 'q':
                    return amt
                else:
                    print("Please try again.")
                    continue
            # If the try statement succeds, proceed.
            else:
                # If negative amount, confirm with user.
                if amt < 0:
                    # New loop to ensure confirmation is valid.
                    while True:
                        ans = input('Confirm Negative Balance (y/n): ')
                        if ans is not '' and not None:
                            # cast ans as lowercase
                            ans = ans.lower()
                            if ans == 'y':
                                # Confirmed as negative, return and done.
                                return amt
                            elif ans == 'n':
                                # Not confirmed, break out of if ans not ''.
                                break
                            # You get here by not entering y or n, re-confirm.
                            continue
                        else:
                            # You get here by no answer, re-confirm.
                            continue
                        # You get here from answering n. Back to amt input.
                        break
                # If large amount, confirm with user, see above for details.
                elif amt > 2000000:
                    while True:
                        ans = input('Confirm Balance > $20,000 (y/n): ')
                        if ans is not '' and not None:
                            ans = ans.lower()
                            if ans == 'y':
                                return amt
                            elif ans == 'n':
                                break
                            continue
                        else:
                            continue
                        break
                # If nothing wrong, return amount.
                else:
                    return amt
        else:
            print("You didnt enter amount, please try again.")


# Checked
def select_envelope(conn, mode):
    """
    Selected envelope should be in list or notify.

    Modes are fund, transferFrom, transfer, withdraw or deposit.
    Fund - f.fund()
    transferFrom - f.env_trans()
    transfer - f.transfer() -> f.env_trans()
    withdraw - f.withdraw() -> f.transaction()
    deposit - f.deposit() -> f.transaction()

    Called by f.env_trans() x2 and f.transaction().
    """
    while True:
        # Print list of existing envelopes and store info.
        ids, names, amts = f.print_envs(conn)
        if mode == 'fund':
            i = input("Envelope To Fund ('q' to quit): ")
        elif mode == 'transferFrom' or mode == 'withdraw':
            i = input("From Envelope ('q' to quit): ")
        elif mode == 'transfer' or mode == 'deposit':
            i = input("To Envelope ('q' to quit): ")
        else:
            print('error in input validation', mode)
        if i is not '' and not None:
            try:
                # Cast as integer
                i = int(i)
            except ValueError:
                if i == 'q':
                    return i
                else:
                    print("Select envelope by number.")
                    continue
            # If try statement worked...
            else:
                # See new_env_grp_lst for details, similar process.
                if i in ids:
                    id = ids.index(i)
                    env = names[id]
                    return env
                else:
                    print("Select envelope by number.")
                    continue
        else:
            print("You didnt enter anything, please try again.")


def select_account(conn, mode=''):
    """Selected account should be in list.

    See select_envelope() for details, similar process.
    Mode may be 'close', in that case, check if account is
    empty before closing. If not empty, cancel action.

    Called by f.transaction().
    """
    while True:
        ids, names, amts = f.print_accts(conn)
        i = input("Select Account ('q' to quit): ")
        if i is not '' and not None:
            try:
                i = int(i)
            except ValueError:
                if i == 'q':
                    return i
                else:
                    print("Select account by number.")
                    continue
            else:
                if i in ids:
                    id = ids.index(i)
                    acct = names[id]
                    if mode == 'close':
                        # Create account obj to check amount.
                        cls_acct = SQL.create_acct_object(conn, acct)
                        if cls_acct.amt == 0:
                            return acct
                        else:
                            input('Empty account before closing.')
                            return 'q'
                    else:
                        return acct
                else:
                    print("Select account by number.")
                    continue
        else:
            print("You didn't enter anything, please try again.")


# Checked
def transfer_amt(conn, mode, env=None):
    """
    Transfer amount should not be negative and not reduce envelope to negative.

    Modes are fund, transfer, withdraw, deposit.
    Fund mode sets from envelope as income pool.
    Transfer or withdraw sets from envelope with passed env object.
    Limits are determined from from envelope balances.
    Default env to none since deposit/fund never use it.
    Deposit has no limit.

    Called by f.env_trans() and f.transaction()
    """
    if mode == 'fund':
        # Call into SQL to create income pool envelope object from table.
        envFrom = SQL.create_env_object(conn, 'Income Pool')
        # Set limit to envelope balance
        limit = envFrom.amt
    elif mode == 'transfer' or mode == 'withdraw':
        # Call into SQL to create
        envFrom = SQL.create_env_object(conn, env)
        limit = envFrom.amt
        print(limit)
    elif mode == 'deposit':
        pass
    else:
        print('error in input validation', mode)
    while True:
        if mode == 'fund':
            amt = input('Fund Amount: ')
        elif mode == 'transfer':
            amt = input('Transfer Amount: ')
        elif mode == 'withdraw':
            amt = input("Withdrawal Amount: ")
        elif mode == 'deposit':
            amt = input("Deposit Amount: ")
        else:
            print('error in input validation', mode)
        if amt is not '' and not None:
            # See new_acct_amt() for details, similar procedure
            try:
                # Convert amount into cents and cast as int.
                amt = int(float(amt)*100)
            except ValueError:
                if amt == 'q':
                    return amt
                else:
                    print("Please enter a number.")
                    continue
            else:
                if amt < 0:
                    print('You cannot enter a negative amount.')
                    continue
                # If required by mode, check if amount exceeds limit.
                if mode == 'fund' or mode == 'transfer' or mode == 'withdraw':
                    if amt > limit:
                        # Display limit for user convert to cents and truncate.
                        print("You only have ${} avaliable."
                              .format(format(limit/100, '.2f')))
                        while True:
                            ans = input('Confirm Negative Balance (y/n): ')
                            if ans is not '' and not None:
                                ans = ans.lower()
                                if ans == 'y':
                                    return amt
                                elif ans == 'n':
                                    break
                                continue
                            else:
                                continue
                            break
                    else:
                        # Amount is under limit, return amount.
                        return amt
                else:
                    # Amount is for deposit so no limit check needed.
                    return amt
        else:
            # Nothing entered, loop again.
            print("You didnt enter amount, please try again.")
