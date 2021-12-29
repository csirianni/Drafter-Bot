import discord
from discord.ext import commands

# used to get token from .env file
import os
from dotenv import load_dotenv

import drafter

# get token
load_dotenv()
TOKEN = os.getenv('TOKEN')

# enable accessing members
intents = discord.Intents.default()
intents.members = True

# initialize Bot object
bot = commands.Bot(command_prefix='.', intents=intents)

# get guild member list

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

    # if message.content.startswith('$hello'):
    #     await message.channel.send('Hello!')

@bot.command()
async def members(ctx):
    guild = ctx.guild
    for member in guild.members:
        await ctx.send(member.display_name)

# initialize Drafter object with empty name_list
drafter = drafter.Drafter([])

@bot.command()
async def start(ctx):
    # store guild object of guild where command is used
    guild = ctx.guild
    # initialize list of names
    drafter.set_name_list([member.display_name for member in guild.members])
    msg = "Starting the draft! Here's the list of players:\n" + "\n".join(drafter.get_name_list())
    await ctx.send(msg)

bot.run(TOKEN)