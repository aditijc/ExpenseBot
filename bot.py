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
# TODO: Change categories to read from the column names

bot = commands.Bot(command_prefix='--', intents=intents)

@bot.command()
async def info(ctx):
    await ctx.send(f"Existing Categories are: {CATEGORIES}\n\n\
                   Commands include:\
                   \n--info\
                   \n--spend <date> <category> <amount> <description>\
                   \n--expenses\
                   \n--expense_log\
                   \n--reset")

@bot.command()
async def spend(ctx, date: str, category: str, amount: float, description: str):
    if t.insert_expense(date, category, amount, description) < 0:
        await ctx.send(f"Invalid category. Please run --add_cat <category> to add a category.")
        return
    await ctx.send(f"You've spent ${amount} on {category}.")
    return

@bot.command()
async def add_cat(ctx, category: str):
    t.add_cat(category)
    CATEGORIES.append(category)
    total_expenses = t.get_expenses()
    await ctx.send(f"Category {category} added.\nTotal expenses: \n{total_expenses}")
# TODO: create a rem_cat that removes categories (loss of data is fine)

# TODO: create an add_budget

@bot.command()
async def expenses(ctx):
    total_expenses = t.get_expenses()
    await ctx.send(f"Total expenses: \n{total_expenses}")

@bot.command()
async def expense_log(ctx):
    total_expenses = t.get_expense_log()
    await ctx.send(f"Expense Log: \n{total_expenses}")

@bot.command()
async def reset(ctx, new_month):
    # TODO: add a command to make a new budget for the month
    t.new_cycle(new_month)
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