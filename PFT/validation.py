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
                if int(i) in ids:
                    group = names[int(i)-1]
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
                amt = float(amt)
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
                elif amt > 20000:
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


# Checked 1/2
def select_enelope(conn, mode):
    if mode == 'fund':
        while True:
            ids, names, amts = f.print_envs(conn)
            i = input("Envelope To Fund ('q' to quit): ")
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
                    if int(i) in ids:
                        env = names[int(i)-1]
                        return env
                    else:
                        print("Select envelope by number.")
                        continue
            else:
                print("You didnt enter anything, please try again.")
    if mode == 'transferFrom':
        while True:
            ids, names, amts = f.print_envs(conn)
            i = input("From Envelope ('q' to quit): ")
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
                    if int(i) in ids:
                        env = names[int(i)-1]
                        return env
                    else:
                        print("Select envelope by number.")
                        continue
            else:
                print("You didnt enter anything, please try again.")


# Checked
def transfer_amt(conn, mode):
    if mode == 'fund':
        pool = SQL.create_env_object(conn, 'Income Pool')
        limit = pool.amt
        while True:
            amt = input('Fund Amount: ')
            if amt is not '' and not None:
                try:
                    amt = float(amt)
                except ValueError:
                    if amt == 'q':
                        return amt
                    else:
                        print("Please enter a number.")
                        continue
                else:
                    if amt < 0:
                        print('You cannot fund a negative amount.')
                        continue
                    elif amt > limit:
                        print("You only have ${} avaliable"
                              " for funding.".format(limit))
                        continue
                    else:
                        return amt
            else:
                print("You didnt enter amount, please try again.")
