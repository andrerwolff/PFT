"""Main function for PFT application.

TODO:
    *Input verification on all inputs
    *Develop main loop to keep in app with decision nodes
    *Impliment GUI
"""
import os
from PFT import SQLite as SQL
from PFT import functions as f
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

    # Set up accounts
    #os.system('clear')
    answer = input('Would you like to open accounts? (y/n): ')
    while answer == 'y':
        f.new_acct_i(conn)
        answer = input('Would you like to open another account? (y/n): ')

    # Set up envelopes
    #os.system('clear')
    answer = input('Would you like to create a new envelope? (y/n): ')
    while answer == 'y':
        f.new_env_i(conn)
        answer = input('Would you like to open another envelope? (y/n): ')

    # main decision loop, quits when user enters 'q'.
    while answer != 'q':
        f.print_options()
        answer = input('What would you like to do: ')
        d.OPTIONS[answer](conn)
    conn.commit()
    conn.close()
