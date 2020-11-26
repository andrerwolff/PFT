import streamlit as st
import os

from PFT import SQLite as SQL
from PFT import functions as f
from PFT import validation as v
from PFT import dict as d

st.title("PFT")

# Set database path
database = os.path.join(os.path.curdir, 'PFT', 'PFT.db')

# Create connection to database (creates .db file if not present)
conn = SQL.create_connection(database)

@st.cache() # only run if arguments change
def initial_setup(conn):
    # Initialize tables in database
    f.table_init(conn)
    f.env_init(conn)
    # Set up accounts
    SQL.check_empty_db(conn)


st.sidebar.write('# Pages')
active_page = st.sidebar.radio(label='Select an Option',                                 
                               options=['Record Transaction',
                                        'Display Envelopes',                                                                    
                                        'Display Accounts', 
                                        'Manage Accounts', 
                                        'Manage Envelopes'])


if active_page == 'Record Transaction':
    "## Enter a Transaction"
    amount = st.number_input(label='Amount',)
    mode = st.radio(label='Mode', options=['withdraw', 'deposit'])
    date = st.date_input(label='Transaction Date')
    account = st.selectbox(label='Account', options=SQL.list_accts(conn)[1])
    envelope = st.selectbox(label='Envelope', options=SQL.list_envs(conn)[1])
    payee = st.selectbox('Payee', options=SQL.list_payees(conn, mode)[1])
    
    