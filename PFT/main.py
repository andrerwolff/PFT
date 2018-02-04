"""Main function for PFT application.

TODO:
    *Input verification on all inputs
    *Impliment GUI
"""
import os
from PFT import SQLite as SQL
from PFT import functions as f
from PFT import validation as v
from PFT import dict as d


def main():
    """Run main loop for application."""
    # Set database path
    database = os.path.join(os.path.curdir, 'PFT', 'PFT.db')
    # Create connection to database (creates .db file if not present)
    conn = SQL.create_connection(database)

    # Initialize tables in database
    f.table_init(conn)
    f.env_init(conn)

    answer = ''
    # Set up accounts
    f.clear()
    if SQL.check_empty_db(conn):
        answer = input('Would you like to open accounts? (y/n): ')
        while answer == 'y':
            f.new_acct_i(conn)
            answer = input('Would you like to open another account? (y/n): ')

        # Set up envelopes
        f.clear()
        answer = input('Would you like to create a new envelope? (y/n): ')
        while answer == 'y':
            f.new_env_i(conn)
            answer = input('Would you like to open another envelope? (y/n): ')

    # main decision loop, quits when user enters 'q'.
    while answer != 'q':
        f.print_options()
        answer = v.menu_choice()
        d.OPTIONS[answer](conn)
        f.clear()
    conn.commit()
    conn.close()
