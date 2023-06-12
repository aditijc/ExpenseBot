import discord
from discord.ext import commands
import sqlite3

CATEGORIES = ["Groceries", "Clothes", "Hygiene", "Food", "Events"]

conn = sqlite3.connect('expenses.db')  # Connect to your database file
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS expenses (date VARCHAR(50), category VARCHAR(50), amount DECIMAL(10, 2), description VARCHAR(255))')

def new_cycle():
    c.execute('DELETE FROM expenses')
    conn.commit()


def insert_expense(date, category, amount, description):
    c.execute(f'INSERT INTO expenses (date, category, amount, description) VALUES {(date, category, amount, description)}')
    conn.commit()

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
        c.execute(f'SELECT amount, category, description, date FROM expenses WHERE category = \'{cat}\'')
        all = c.fetchall()
        total = 0
        for i in all:
            total += i[0]
        expenses += f'Spent ${total} on {cat}\n'
    return expenses