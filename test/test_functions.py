import PFT.SQLite as s
import PFT.functions as f
import unittest
import sqlite3
import os

class TestTableInit(unittest.TestCase):
    """
    Test the database setup
    """

    @classmethod
    def setUpClass(self):
        """
        Setup a temporary database
        """
        conn = sqlite3.connect("test/test_db.db")


    @classmethod
    def tearDownClass(self):
        """
        Delete the database
        """
        os.remove("test/test_db.db")


    def test_table_init(self):
        """
        Test that the database is properly initialized by testing the
        table names and the number of attributes for each table
        """
        # Connect to database
        conn = sqlite3.Connection("test_db.db")
        c = conn.cursor()

        f.table_init(conn) # initialize tables

        # Query for tables
        result = c.execute("SELECT name from sqlite_master WHERE type='table';")
        table_names = [name[0] for name in result] #create list of table names

        # expected tables and the expected number of attributes
        desired_tables = {'accounts': 4,
                          'groups': 2,
                          'envelopes': 4,
                          'transactions': 10,
                          'payees':2}

        # Test that the  correct number of tables were made
        self.assertEqual(len(desired_tables), len(table_names))

        # Test that the tables are named correctly
        for k in desired_tables.keys():
            self.assertIn(k, table_names)

        # Test each table has the correct number of attriutes
        for k, v in desired_tables.items():
            result = c.execute("PRAGMA table_info({})".format(k))
            self.assertEqual(len([i for i in result]), v)

class TestEnvGroupAcct(unittest.TestCase):
    """
    Test interaction with an initialized, empty database including:
    Initializing Default Envelopes and groups
    Creating new accounts, groups, and envelopes
    """

    @classmethod
    def setUpClass(self):
        """
        initialize a temporary database with necessary tables
        """
        conn = sqlite3.connect("test/test_db.db")
        cursor = conn.cursor()

        # Create envelopes table
        cursor.execute('''CREATE TABLE envelopes(
                            env_id INTEGER PRIMARY KEY NOT NULL,
                            env_group STRING NOT NULL
                            REFERENCES groups (group_id),
                            env_name STRING NOT NULL UNIQUE,
                            env_amt DECIMAL NOT NULL
                            );''')

        # Create groups table
        cursor.execute('''CREATE TABLE groups(
                            group_id INTEGER PRIMARY KEY NOT NULL,
                            group_name STRING UNIQUE NOT NULL
                            );''')

        # Create accounts table
        cursor.execute('''CREATE TABLE accounts(
                            acct_id   INTEGER PRIMARY KEY NOT NULL,
                            acct_type STRING,
                            acct_name STRING  NOT NULL UNIQUE,
                            acct_amt  DECIMAL NOT NULL
                            );''')

    @classmethod
    def tearDownClass(self):
        """
        Delete the database
        """
        os.remove("test/test_db.db")


    def test_env_init(self):
        # Connect to database
        conn = sqlite3.Connection("test_db.db")
        c = conn.cursor()

        # Initialize envelopes
        f.env_init(conn)

        # Query for groups
        c.execute("SELECT * FROM groups")
        rows = c.fetchall()

        # Test the right number of groups
        self.assertEqual(8, len(rows))

        # Query for envelopes
        c.execute("SELECT * FROM envelopes;")
        rows = c.fetchall()

        # Test the name of the first envelope is Income Pool
        self.assertEqual('Income Pool', rows[0][2])
