import discord
from discord.errors import DiscordException, HTTPException
from discord.ext import commands

# used to get token from .env file
import os
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
bot = commands.Bot(command_prefix='.', intents=intents)

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
    # store guild object of guild where command is used
    guild = ctx.guild
    # initialize list of players
    drafter.set_player_list([member.display_name for member in guild.members])
    # initalize list of civs
    # copy() necessary here because otherwise ban will remove item
    # from full_civ_list
    # (references in python point to the same object)
    drafter.set_civ_list(drafter.full_civ_list.copy())
    msg = "Starting the draft! Here's the list of players:\n" + "\n".join(drafter.player_list)
    await ctx.send(msg)

@bot.command()
async def ban(ctx, civ):
    try:
        drafter.ban(civ)
        await ctx.send(f"{civ} is now banned!")
    except:
        await ctx.send(f"{civ} is not a valid civilization. Try again.")

@bot.command()
async def draft(ctx):
    msg = drafter.draft()
    try:
        await ctx.send(msg)
    except HTTPException:
        # this occurs when player_list is empty; ctx.send can't send an empty message
        await ctx.send("HTTPException: Make sure you ran `.start` first.")

@bot.command()
async def civlist(ctx):
    try:
        await ctx.send(drafter.get_civ_list())
    except HTTPException:
        await ctx.send("HTTPException: Make sure you ran `.start` first.")

@bot.command()
async def playerlist(ctx):
    try:
        await ctx.send(drafter.get_player_list())
    except HTTPException:
        await ctx.send("HTTPException: Make sure you ran `.start` first.")

@bot.command()
async def removeplayer(ctx, player: str):
    drafter.player_list.remove(player)
    await ctx.send(f"{player} has been removed from the list.")

@bot.command()
async def addplayer(ctx, player: str):
    drafter.player_list.append(player)
    await ctx.send(f"{player} has been added to the list.")

bot.run(TOKEN)