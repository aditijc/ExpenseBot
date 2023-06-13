import discord
from discord.ext import commands
import sqlite3

CATEGORIES = ["Groceries", "Clothes", "Hygiene", "Food", "Events"]

conn = sqlite3.connect('expenses.db')  # Connect to your database file
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS expenses (\
          date VARCHAR(50), category VARCHAR(50), \
          amount DECIMAL(10, 2), description VARCHAR(255))')

budget_conn = sqlite3.connect('budgets.db')  # Connect to your database file
b = budget_conn.cursor()
b.execute('CREATE TABLE IF NOT EXISTS budgets (month VARCHAR(50), balance DECIMAL(10,2))')

for i in CATEGORIES:
    # Check if the column exists
    b.execute(f"PRAGMA table_info('budgets')")
    columns = b.fetchall()
    column_names = [column[1] for column in columns]

    if i not in column_names:
        # Add the column to the table
        b.execute(f"ALTER TABLE budgets ADD COLUMN {i} DECIMAL(10, 2)")

def new_cycle(new_month):
    c.execute('DELETE FROM expenses')
    conn.commit()


def insert_expense(date, category, amount, description):
    if category not in CATEGORIES:
        return -1
    c.execute(f'INSERT INTO expenses (date, category, amount, description) \
              VALUES {(date, category, amount, description)}')
    conn.commit()
    return 0

def add_cat(category):
    CATEGORIES.append(category)
    # Check if the column exists
    b.execute(f"PRAGMA table_info('budgets')")
    columns = b.fetchall()
    column_names = [column[1] for column in columns]
    if category not in column_names:
        b.execute(f"ALTER TABLE budgets ADD COLUMN {category} DECIMAL(10, 2)")

def get_expense_log():
    c.execute('SELECT amount, category, description, date FROM expenses')
    all = c.fetchall()
    output = ""
    for i in all:
        output += f'{i[3]}: Spent ${i[0]} on {i[1]} - {i[2]}'
    return output

def get_expenses():
    expenses = ""
    for cat in CATEGORIES:
        c.execute(f'SELECT amount, category, description, date \
                  FROM expenses WHERE category = \'{cat}\'')
        all = c.fetchall()
        total = 0
        for i in all:
            total += i[0]
        expenses += f'Spent ${total} on {cat}\n'
    return expenses

# def set_budget(month, amt_list):


def get_budget(month):
    budget = ""
    c.execute(f'SELECT * FROM budget WHERE month = \'{month}\'')
    all = c.fetchall()
    # for cat in CATEGORIES:
    #     total = 0
    #     for i in all:
    #         total += i[0]
    #     expenses += f'Spent ${total} on {cat}\n'
    return all