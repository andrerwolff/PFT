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
        Test that the database is properly initialized
        """
        # Connect to database
        conn = sqlite3.Connection("test_db.db")
        c = conn.cursor()

        f.table_init(conn) # initialize tables

        # Query for tables
        result = c.execute("SELECT name from sqlite_master WHERE type='table';")
        tables = [name[0] for name in result] #create list of table names

        # Actual tests
        self.assertEqual(len(tables), 5) # There should be 5 Tables
        self.assertEqual(tables[0], 'accounts')
