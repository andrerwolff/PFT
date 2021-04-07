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
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen

sm = ScreenManager()

for i in range(4):
    screen = Screen(name="Title %d" % i)
    sm.add_widget(screen)

sm.current = 'Title 2'

class PFT(Widget):
    pass

class PFTApp(App):
    def build(self):
        return PFT()


def main():
    """TEMP KIVY STUFF"""
    PFTApp().run()

    
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
    SQL.check_empty_db(conn)

    # main decision loop, quits when user enters 'q'.
    while answer != 'q':
        f.print_options()
        answer = v.menu_choice()
        d.OPTIONS[answer](conn)
        f.clear()
    conn.commit()
    conn.close()
