"""Dictionaries used in PFT application."""


from PFT import functions as f


sql_cmd = {'accountsTable': '''CREATE TABLE IF NOT EXISTS accounts (
                                    acct_id   integer PRIMARY KEY NOT NULL,
                                    acct_type text,
                                    acct_name text  NOT NULL UNIQUE,
                                    acct_amt  integer NOT NULL,
                                    acct_status  NOT NULL
                                );''',
           'groupsTable': '''CREATE TABLE IF NOT EXISTS groups (
                                    group_id integer PRIMARY KEY NOT NULL,
                                    group_name text UNIQUE NOT NULL
                                );''',
           'envelopesTable': '''CREATE TABLE IF NOT EXISTS envelopes (
                                    env_id integer PRIMARY KEY NOT NULL,
                                    env_group text NOT NULL
                                    REFERENCES groups (group_id),
                                    env_name text NOT NULL UNIQUE,
                                    env_amt integer NOT NULL
                                );''',
           'transactionsTable': '''CREATE TABLE IF NOT EXISTS transactions (
                                    trans_id integer PRIMARY KEY NOT NULL,
                                    trans_date date NOT NULL,
                                    trans_type text,
                                    trans_memo text NOT NULL,
                                    trans_amt integer NOT NULL,
                                    trans_acct_to_id   integer
                                    REFERENCES accounts (acct_id),
                                    trans_acct_from_id integer
                                    REFERENCES accounts (acct_id),
                                    trans_env_to_id    integer
                                    REFERENCES envelopes (env_id),
                                    trans_env_from_id  integer
                                    REFERENCES envelopes (env_id),
                                    payee_id integer
                                    REFERENCES payees (payee_id)
                                );''',
           'payeesTable': '''CREATE TABLE IF NOT EXISTS payees (
                                payee_id integer PRIMARY KEY NOT NULL,
                                payee_name text NOT NULL UNIQUE,
                                payee_type integer NOT NULL
                                );''',

           'createAcct': '''INSERT INTO  accounts (acct_type,acct_name,
                                                   acct_amt, acct_status)
                                            VALUES(?,?,?,?) ''',
           'selectAcctName': '''SELECT acct_id,acct_type,acct_name,
                                       acct_amt, acct_status
                                FROM accounts WHERE acct_name = ''',
           'listAccts': '''SELECT acct_id,acct_name,acct_amt
                                FROM accounts WHERE acct_status="o"''',
           'updateAcct': '''UPDATE accounts
                            set acct_amt = ?
                            WHERE acct_name = ?''',
           'closeAccount': '''UPDATE accounts
                              set acct_status = "c"
                              WHERE acct_name = ?''',
           'createGrp': '''INSERT INTO  groups (group_name)
                                            VALUES(?) ''',
           'listGroups': '''SELECT group_id,group_name FROM groups''',
           'createPayee': '''INSERT INTO payees (payee_name,payee_type)
                                            VALUES(?,?) ''',
           'listPayees': '''SELECT payee_id,payee_name
                            FROM payees WHERE payee_type = ''',
           'selectPayeeName': '''SELECT payee_id,payee_name,payee_type
                                 FROM payees WHERE payee_name = ''',
           'createEnv': '''INSERT INTO  envelopes (env_group,env_name,env_amt)
                                            VALUES(?,?,?) ''',
           'selectEnvName': '''SELECT env_id,env_group,env_name,env_amt
                                FROM envelopes WHERE env_name = ''',
           'listEnvs': '''SELECT env_id,env_name,env_amt FROM envelopes''',
           'updateEnv': ''' UPDATE envelopes
                            SET env_amt = ?
                            WHERE env_name = ?''',
           'createTrans': '''INSERT INTO  transactions (trans_date, trans_type,
                                                        trans_memo, trans_amt,
                                                        trans_acct_to_id,
                                                        trans_acct_from_id,
                                                        trans_env_to_id,
                                                        trans_env_from_id,
                                                        payee_id)
                                            VALUES(?,?,?,?,?,?,?,?,?) '''}

ENV_GROUPS = {1: '~', 2: 'Bills', 3: 'Daily', 4: 'Monthly', 5: 'Periodic',
              6: 'Giving', 7: 'Goals', 8: 'Other'}

OPTIONS = {'f': f.fund, 'a': f.new_acct, 'e': f.new_env, 'd': f.deposit,
           'w': f.withdraw, 't': f.transfer, 'la': f.print_accts,
           'le': f.print_envs, 'c': f.close_acct, 'q': f.quit}

OPTIONS_P = ('a - New Account', 'e - New Envelope', 'd - Make Deposit',
             'w - Make Withdrawal', 'f - Fund Envelope',
             't - Transfer Between Envelopes',
             'la - Display Accounts',
             'le - Display Envelopes',
             'c - Close Account', 'q - Quit PFT')
