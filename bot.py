import discord
from discord.ext import commands
import tracking as t

with open('token.txt', 'r') as file:
    line = file.readline().strip()
token = line
intents = discord.Intents.default()  # Create an instance of Intents
intents.typing = True  # Adjust the intents based on your bot's requirements
intents.presences = True
intents.message_content = True

CATEGORIES = ["Groceries", "Clothes", "Hygiene", "Food", "Events"]

bot = commands.Bot(command_prefix='--', intents=intents)

@bot.command()
async def info(ctx):
    await ctx.send(f"Existing Categories are: {CATEGORIES}\n\nCommands include:\n--info\n--spend <date> <category> <amount> <description>\n--expenses\n--expense_log\n--reset")

@bot.command()
async def spend(ctx, date: str, category: str, amount: float, description: str):
    t.insert_expense(date, category, amount, description)
    await ctx.send(f"You've spent ${amount} on {category}.")

@bot.command()
async def expenses(ctx):
    total_expenses = t.get_expenses()
    await ctx.send(f"Total expenses: \n{total_expenses}")

@bot.command()
async def expense_log(ctx):
    total_expenses = t.get_expense_log()
    await ctx.send(f"Expense Log: \n{total_expenses}")

@bot.command()
async def reset(ctx):
    t.new_cycle()
    total_expenses = t.get_expenses()
    await ctx.send(f"---Reset Expense Log---\nTotal expenses: \n{total_expenses}")

@bot.event
async def on_ready():
    total_expenses = t.get_expenses()
    print(f"Bot connected as {bot.user}. \nTotal expenses: \n{total_expenses}")

@bot.event
async def on_disconnect():
    t.conn.close()

bot.run(token)