"""Handle input validation for PFT application"""
from PFT import functions as f
from PFT import dict as d
from PFT import SQLite as SQL


# Checked
def menu_choice():
    while True:
        ans = input("What would you like to do: ")
        if ans is not '' and not None:
            ans = ans.lower()
            if ans in d.OPTIONS:
                return ans
            else:
                print("That is not a valid choice, please try again.")


# Checked
def new_acct_name():
    while True:
        name = input("New Account Name: ")
        if name is not '' and not None:
            if len(name) > 20:
                print("That name is too long, please use another name.")
            else:
                return name
        else:
            print("You didn't enter a name, please try again. ('q' to cancel)")


# Checked
def new_env_name():
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
    ids, names = f.print_groups(conn)
    while True:
        i = input("Pick Group From List (* To create new group): ")
        if i is not '' and not None:
            try:
                i = int(i)
            except ValueError:
                if i == '*':
                    group = f.new_group_i(conn)
                    if group is not '' and not None:
                            return group
                    else:
                        continue
                elif i == 'q':
                    return i
                else:
                    print('Enter a number from the list of grops.')
                    continue
            else:
                if i in ids:
                    id = ids.index(i)
                    group = names[id]
                    return group
                else:
                    print('That does not match a group, please try again.')
                    continue
        else:
            print("You didn't enter anything, please try again."
                  " ('q' to cancel)")


# Checked
def new_env_grp_usr(conn):
    while True:
        name = input('New Group Name (* back to list): ')
        if name is not '' and not None:
            if len(name) > 20:
                print("That name is too long, please use another name.")
            elif name == '*':
                name = new_env_grp_lst(conn)
                return name
            else:
                return name
        else:
            print("You didn't enter a name, please try again. ('q' to cancel)")


def select_payee_lst(conn, mode):
    ids, names = f.print_payees(conn, mode)
    while True:
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
                    payee = f.new_payee_i(conn, mode)
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
                name = new_payee_lst(conn, mode)
                return name
            else:
                return name
        else:
            print("You didn't enter a name, please try again. ('q' to cancel)")


# Checked
def new_acct_type():
    while True:
        typ = input("[S]avings or [C]hecking: ")
        if typ is not '' and not None:
            typ = typ.lower()
            if typ == 'c' or typ == 'checking':
                typ = 'checking'
                return typ
            elif typ == 's' or typ == 'savings':
                typ = 'savings'
                return typ
            elif typ == 'q':
                return typ
            else:
                print("Please enter a valid account type.")
        else:
            print("You didn't enter a type, please try again. ('q' to cancel)")


# Checked
def new_acct_amt():
    while True:
        amt = input('New Account Balance: ')
        if amt is not '' and not None:
            try:
                amt = int(float(amt)*100)
            except ValueError:
                if amt == 'q':
                    return amt
                else:
                    print("Please try again.")
                    continue
            else:
                if amt < 0:
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
                else:
                    return amt
        else:
            print("You didnt enter amount, please try again.")


# Checked
def select_envelope(conn, mode):
    while True:
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
                i = int(i)
            except ValueError:
                if i == 'q':
                    return i
                else:
                    print("Select envelope by number.")
                    continue
            else:
                if i in ids:
                    id = ids.index(i)
                    env = names[id]
                    return env
                else:
                    print("Select envelope by number.")
                    continue
        else:
            print("You didnt enter anything, please try again.")


def select_account(conn, mode):
    while True:
        ids, names, amts = f.print_accts(conn)
        if mode == 'deposit' or mode == 'withdraw':
            i = input("Select Account ('q' to quit): ")
        else:
            print('error in input validation', mode)
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
                    return acct
                else:
                    print("Select account by number.")
                    continue
        else:
            print("You didn't enter anything, please try again.")


# Checked
def transfer_amt(conn, mode, env=None):
    if mode == 'fund':
        envFrom = SQL.create_env_object(conn, 'Income Pool')
        limit = envFrom.amt
    elif mode == 'transfer' or mode == 'withdraw':
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
            try:
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
                if mode == 'fund' or mode == 'transfer' or mode == 'withdraw':
                    print(amt, limit)
                    if amt > limit:
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
                        return amt
                else:
                    return amt
        else:
            print("You didnt enter amount, please try again.")
