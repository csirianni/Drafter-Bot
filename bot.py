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

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

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
    # initalize list of civs
    # copy() necessary here because otherwise ban will remove item
    # from full_civ_list
    # (references in python point to the same object)
    drafter.set_civ_list(drafter.full_civ_list.copy())
    msg = "Starting the draft! Here's the list of players:\n" + "\n".join(drafter.name_list)
    await ctx.send(msg)

@bot.command()
async def ban(ctx, civ):
    drafter.ban(civ)
    await ctx.send(f"{civ} is now banned!")

@bot.command()
async def draft(ctx):
    # TODO: handle error if name_list is empty
    msg = drafter.draft()
    await ctx.send(msg)

@bot.command()
async def civlist(ctx):
    await ctx.send(drafter.civ_list)

bot.run(TOKEN)