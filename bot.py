import discord
from discord.errors import HTTPException
from discord.ext import commands

# used to get token from .env file
import os

# import csv module
import csv

import drafter

# enable accessing members
intents = discord.Intents.default()
intents.members = True


# initialize Bot object
prefix = '!'
activity = discord.Activity(type=discord.ActivityType.listening, name=f"{prefix}help")
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None, activity=activity)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def members(ctx):
    guild = ctx.guild
    for member in guild.members:
        await ctx.send(member.display_name)

# initialize Drafter object with empty player_list, civ_list, and player_bans
drafter = drafter.Drafter([], [], {})

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

    # initalize list of civs
    # copy() necessary here because otherwise ban will remove item
    # from full_civ_list
    # (references in python point to the same object)
    drafter.set_civ_list(full_civ_list)

    # store guild object of guild where command is used
    guild = ctx.guild
    # initialize list of players (excluding bots)
    player_names = [member.display_name for member in guild.members if not member.bot]
    drafter.set_player_list(player_names)
    # dictionary used to track number of bans made by each player
    # Note: this only work if every player has a unique name since dict key values are unique
    player_bans = dict.fromkeys(player_names, 0)
    drafter.set_player_bans(player_bans)
    print(player_bans)
    msg = "Starting the draft! Here's the list of players:\n" + "\n".join(drafter.player_list)
    await ctx.send(msg)

@bot.command()
async def ban(ctx, civ):
    # catch message author not being in the player_bans dictionary
    try:
        # limit number of bans per player to 2
        if drafter.get_player_bans()[ctx.author.nick] < 2:
            # catch invalid civilization name
            try:
                # remove civ from list of civs
                drafter.ban(civ)
                # increment player's number of bans
                drafter.get_player_bans()[ctx.author.nick] += 1
                # print updated dict to terminal
                print(drafter.get_player_bans())
                await ctx.send(f"**{civ}** is now banned!")
            except ValueError:
                await ctx.send(f"**{civ}** is not a valid civilization. Try again.")
        else:
            await ctx.send(f"**{ctx.author.nick}**, you've already banned two civilizations!")
    except KeyError:
        await ctx.send(f"**{ctx.author.nick}**, you're not in the list of players. Try using `{prefix}addplayer {{player_name}}` to add yourself to the list.")

@bot.command()
async def draft(ctx):
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
        # this occurs when civ_list is empty; ctx.send can't send an empty message
        await ctx.send(f"HTTPException: Make sure you ran `{prefix}start` first.")

@bot.command()
async def playerlist(ctx):
    try:
        await ctx.send(drafter.get_player_list())
    except HTTPException:
        # this occurs when player_list is empty; ctx.send can't send an empty message
        await ctx.send(f"HTTPException: Make sure you ran `{prefix}start` first.")

@bot.command()
async def removeplayer(ctx, player: str):
    try:
        # removes player from player list
        drafter.player_list.remove(player)
        # removes player from player_bans dictionary
        drafter.get_player_bans().pop(player)
        await ctx.send(f"**{player}** has been removed from the list.")
    except ValueError:
        # this occurs when the player is not in the player list
        await ctx.send(f"**{player}** is not in the player list. Try again.")
    except KeyError:
        await ctx.send(f"**{player}** is not in the player_bans dictionary. Cedric, debug this.")
        raise KeyError

@bot.command()
async def addplayer(ctx, player: str):
    drafter.player_list.append(player)
    await ctx.send(f"**{player}** has been added to the list.")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Drafter Commands", description=f"- `{prefix}start`: Initialize the list of players and the list of civs.\n- `{prefix}ban {{civ_name}}`: Remove specified civ from list of draftable civs. Limited to 2 per player. \n- `{prefix}draft`: Generate the civ picks for each person.\n- `{prefix}civlist`: Print the list of draftable civs.\n- `{prefix}playerlist`: Print the list of players who will be assigned civ picks.\n- `{prefix}removeplayer {{player_name}}`: Remove specified player from list of players who will be assigned civ picks. \n- `{prefix}addplayer {{player_name}}`: Add specified player to list of players who will be assigned civ picks.", color=discord.Color.blue())
    await ctx.send(embed=embed)

bot.run("OTI1NTM1MTUwMTE1MjY2NjMw.Ycuhxw.j4tCN3vkEZ6PDmVJ6mW1vtFW6-4")