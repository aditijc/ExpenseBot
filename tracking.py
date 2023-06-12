import discord
from discord.ext import commands
import sqlite3

token = "MTExNzczNTU5Mjk5NDgxNjAxMA.GeR3gG.XlnjHQ0Lw2gwthh8Q-dy_Avr6IDOJI9rKZi9Gk"
intents = discord.Intents.default()  # Create an instance of Intents
intents.typing = True  # Adjust the intents based on your bot's requirements
intents.presences = True
intents.message_content = True
CATEGORIES = ["Groceries", "Clothes", "Hygiene", "Food", "Events"]

bot = commands.Bot(command_prefix='--', intents=intents)

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

@bot.command()
async def info(ctx):
    await ctx.send(f"Existing Categories are: {CATEGORIES}\n\nCommands include:\n--info\n--spend <date> <category> <amount> <description>\n--expenses\n--expense_log\n--reset")

@bot.command()
async def spend(ctx, date: str, category: str, amount: float, description: str):
    insert_expense(date, category, amount, description)
    await ctx.send(f"You've spent ${amount} on {category}.")

@bot.command()
async def expenses(ctx):
    total_expenses = get_expenses()
    await ctx.send(f"Total expenses: \n{total_expenses}")

@bot.command()
async def expense_log(ctx):
    total_expenses = get_expense_log()
    await ctx.send(f"Expense Log: \n{total_expenses}")

@bot.command()
async def reset(ctx):
    new_cycle()
    total_expenses = get_expenses()
    await ctx.send(f"---Reset Expense Log---\nTotal expenses: \n{total_expenses}")

@bot.event
async def on_ready():
    total_expenses = get_expenses()
    print(f"Bot connected as {bot.user}. \nTotal expenses: \n{total_expenses}")

@bot.event
async def on_disconnect():
    conn.close()

bot.run(token)
