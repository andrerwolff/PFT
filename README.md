# PFT - Personal Finance Tracker
PFT uses SQLite to interact with a database to perform basic personal finance functions.

The goal is to help the user create, maintain, and manipulate a **zero-based** envelope style budget.

## TODO:
- [ ] Add more to the README.
- [ ] Add more features.
    - [ ] Make all transactions editable (date/amount/envelopes/etc...)
	- [ ] Use expected income and expected expenses to start a budget.
	- [ ] Create full budget with remaining funds.
    - [ ] Use budget to 'fund' envelopes for beginning of month operations.
    - [ ] CSV/YNAB/QIF Importation.
    - [ ] CSV/YNAB/QIF Exportation.
    - [ ] Web Scrape online account pages for transaction info.
- [ ] Use real documentation practices to document all documentable things.
- [ ] Implement input validation and loops to *'robust-icize'* application.
    - [ ] Make sure transactions that leave balances < 0 are intended. 
- [ ] Implement GUI so people dont get scared off by command-line.
- [ ] Figure out data analysis for fun graphs/charts.
    - [ ] Net Worth line graph
    - [ ] Cash Flow line graph
    - [ ] Account Balance line graph
    - [ ] Expense pie chart
    - [ ] Income pie chart
- [ ] Figure out how to make mobile utility for viewing balances/creating transactions.
- [ ] Package PFT for cross platform quick and easy deployment.
- [ ] Add to this list.

## Running PFT
To run PFT, open a terminal window and navigate to the project folder.

EX: `cd folder_location/PFT`

Then run PFT.py using Python 3

EX: `python3 PFT.py`

If this doesn't work... good luck my friend.

