from PFT import functions as f
sql_cmd = {'accountsTable': '''CREATE TABLE IF NOT EXISTS accounts (
                                    acct_id   INTEGER PRIMARY KEY NOT NULL,
                                    acct_type STRING,
                                    acct_name STRING  NOT NULL UNIQUE,
                                    acct_amt  DECIMAL NOT NULL
                                );''',
           'groupsTable': '''CREATE TABLE IF NOT EXISTS groups (
                                    group_id INTEGER NOT NULL UNIQUE,
                                    group_name STRING PRIMARY KEY NOT NULL
                                );''',
           'envelopesTable': '''CREATE TABLE IF NOT EXISTS envelopes (
                                    env_id INTEGER PRIMARY KEY NOT NULL,
                                    env_group STRING NOT NULL
                                    REFERENCES groups (group_name),
                                    env_name STRING NOT NULL UNIQUE,
                                    env_amt DECIMAL NOT NULL
                                );''',
           'transactionsTable': '''CREATE TABLE IF NOT EXISTS transactions (
                                    trans_id INTEGER PRIMARY KEY NOT NULL,
                                    trans_date DATE NOT NULL,
                                    trans_type STRING,
                                    trans_memo STRING NOT NULL,
                                    trans_amt DECIMAL NOT NULL,
                                    trans_acct_to_id   INTEGER
                                    REFERENCES accounts (acct_id),
                                    trans_acct_from_id INTEGER
                                    REFERENCES accounts (acct_id),
                                    trans_env_to_id    INTEGER
                                    REFERENCES envelopes (env_id),
                                    trans_env_from_id  INTEGER
                                    REFERENCES envelopes (env_id)
                                );''',
           'createAcct': '''INSERT INTO  accounts (acct_type,acct_name,acct_amt)
                                            VALUES(?,?,?) ''',
           'selectAcctName': '''SELECT acct_type, acct_name, acct_amt
                                FROM accounts WHERE acct_name = ''',
           'updateAcct': '''.''',
           'createGrp': '''INSERT INTO  groups (group_id, group_name)
                                            VALUES(?,?) ''',
           'listGroups': '''SELECT group_id, group_name FROM groups''',
           'createEnv': '''INSERT INTO  envelopes (env_group,env_name,env_amt)
                                            VALUES(?,?,?) ''',
           'selectEnvName': '''SELECT env_group, env_name, env_amt
                                FROM envelopes WHERE env_name = ''',
           'updateEnv': ''' UPDATE envelopes
                            SET env_amt = ?
                            WHERE env_name = ?''',
           'createTrans': '''INSERT INTO  transactions (trans_date, trans_type,
                                                        trans_memo, trans_amt,
                                                        trans_acct_to_id,
                                                        trans_acct_from_id,
                                                        trans_env_to_id,
                                                        trans_env_from_id)
                                            VALUES(?,?,?,?,?,?,?,?) '''}

ENV_GROUPS = {1: '*', 2: 'Bills', 3: 'Daily', 4: 'Monthly', 5: 'Periodic',
              6: 'Giving', 7: 'Goals', 8: 'Other'}

OPTIONS = {'f': f.fund, 'a': f.new_acct_i, 'e': f.new_env_i,
           't': f.env_trans, 'q': f.quit}

OPTIONS_P = ('a - New Account', 'e - New Envelope', 'f - Fund Envelope',
             't - Transfer Between Envelopes', 'q - Quit PFT')
