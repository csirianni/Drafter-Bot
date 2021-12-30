import discord
from discord.errors import DiscordException, HTTPException
from discord.ext import commands

# used to get token from .env file
import os
# import csv module
import csv

from discord.ext.commands.core import Command
from discord.ext.commands.errors import CommandError, CommandInvokeError
from dotenv import load_dotenv

import drafter

# get token
load_dotenv()
TOKEN = os.getenv('TOKEN')

# enable accessing members
intents = discord.Intents.default()
intents.members = True


# initialize Bot object
prefix = '.'
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def members(ctx):
    guild = ctx.guild
    for member in guild.members:
        await ctx.send(member.display_name)

# initialize Drafter object with empty player_list
drafter = drafter.Drafter([])

@bot.command()
async def start(ctx):
    # open csv file
    with open('civ-list.csv') as f:
        # create a reader object
        reader = csv.reader(f)
        # initialize empty list for civ players
        full_civ_list = []
        # iterate over reader and append civ player to civs list
        for civ in reader:
            # index 0 used to unwrap list containing the civ player
            full_civ_list.append(civ[0])
    # store guild object of guild where command is used
    guild = ctx.guild
    # initialize list of players
    drafter.set_player_list([member.display_name for member in guild.members])
    # initalize list of civs
    # copy() necessary here because otherwise ban will remove item
    # from full_civ_list
    # (references in python point to the same object)
    drafter.set_civ_list(full_civ_list)
    msg = "Starting the draft! Here's the list of players:\n" + "\n".join(drafter.player_list)
    await ctx.send(msg)

@bot.command()
async def ban(ctx, civ):
    # TODO: add ban limit
    try:
        drafter.ban(civ)
        await ctx.send(f"**{civ}** is now banned!")
    except ValueError:
        await ctx.send(f"**{civ}** is not a valid civilization. Try again.")

@bot.command()
async def draft(ctx):
    # TODO: add # of civ variable
    msg = drafter.draft()
    try:
        await ctx.send(msg)
    except HTTPException:
        # this occurs when player_list is empty; ctx.send can't send an empty message
        await ctx.send(f"HTTPException: Make sure you ran `{prefix}start` first.")

@bot.command()
async def civlist(ctx):
    try:
        await ctx.send(drafter.get_civ_list())
    except HTTPException:
        await ctx.send(f"HTTPException: Make sure you ran `{prefix}start` first.")

@bot.command()
async def playerlist(ctx):
    try:
        await ctx.send(drafter.get_player_list())
    except HTTPException:
        await ctx.send(f"HTTPException: Make sure you ran `{prefix}start` first.")

@bot.command()
async def removeplayer(ctx, player: str):
    try:
        drafter.player_list.remove(player)
        await ctx.send(f"**{player}** has been removed from the list.")
    except ValueError:
        await ctx.send(f"**{player}** is not in the player list. Try again.")

@bot.command()
async def addplayer(ctx, player: str):
    drafter.player_list.append(player)
    await ctx.send(f"**{player}** has been added to the list.")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Drafter Commands", description=f"- `{prefix}start`: Initialize the list of players and the list of civs.\n- `{prefix}ban {{civ_name}}`: Remove specified civ from list of draftable civs. Limited to 2 per player. \n- `{prefix}draft': Generate the civ picks for each person.\n- `{prefix}civlist`: Print the list of draftable civs.\n- `{prefix}playerlist`: Print the list of players who will be assigned civ picks.\n- `{prefix}removeplayer {{player_name}}`: Remove specified player from list of players who will be assigned civ picks. \n- `{prefix}addplayer {{player_name}}`: Add specified player to list of players who will be assigned civ picks.", color=discord.Color.blue())
    await ctx.send(embed=embed)

bot.run(TOKEN)