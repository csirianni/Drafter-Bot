import discord
from discord.errors import HTTPException
from discord.ext import commands

# used to get token from .env file
import os
TOKEN = os.environ['TOKEN']

# import csv module
import csv

# import Drafter methods
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

# initialize Drafter object with empty player_list, civ_list, player_bans and ban_limit = 0
drafter = drafter.Drafter([], [], {}, 0)

@bot.command()
async def start(ctx, ban_limit: int = None):    
    # store guild object of guild where command is used
    guild = ctx.guild
    # initialize list of players (excluding bots)
    # note that display_name is used throughout the program to reference/track players
    player_display_names = [member.display_name for member in guild.members if not member.bot]
    # ensure the list contains only unique display_names
    if len(player_display_names) != len(set(player_display_names)):
        await ctx.send(f"Error! `{prefix}start {{ban_limit}} (optional)` expected  each player to have a unique name. Try again.")
    # ensure the ban limit > 0
    elif ban_limit is not None and ban_limit < 0:
        await ctx.send(f"Error! Invalid ban limit. It must be non-negative. Try again.")
    else:
        drafter.set_player_list(player_display_names)

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

        drafter.set_civ_list(full_civ_list)

        # dictionary used to track number of bans made by each player
        player_bans = dict.fromkeys(player_display_names, 0)
        drafter.set_player_bans(player_bans)
        print(player_bans)

        # set # of bans limit for each player
        if ban_limit is None:
            drafter.set_ban_limit(2)
        else:
            drafter.set_ban_limit(ban_limit)
        
        msg = f"Starting the draft! The ban limit is {drafter.ban_limit} per person. Here's the list of players: " + drafter.get_player_list()
        await ctx.send(msg)

@bot.command()
async def ban(ctx, civ: str):
    # catch message author not being in the player_bans dictionary
    try:
        # limit number of bans per player to 2
        if drafter.get_player_bans()[ctx.author.display_name] < drafter.ban_limit:
            # catch invalid civilization name
            try:
                # remove civ from list of civs
                removed_civ = drafter.ban(civ)
                # increment player's number of bans
                drafter.get_player_bans()[ctx.author.display_name] += 1
                # print updated dict to terminal
                print(drafter.get_player_bans())
                await ctx.send(f"**{removed_civ}** is now banned!")
            except ValueError:
                await ctx.send(f"**{civ}** is not a valid civilization. Try again.")
        else:
            if drafter.ban_limit < 2:
                await ctx.send(f"**{ctx.author.display_name}**, you've already banned {drafter.ban_limit} civilization!")
            else:
                await ctx.send(f"**{ctx.author.display_name}**, you've already banned {drafter.ban_limit} civilizations!")
    except KeyError:
        await ctx.send(f"**{ctx.author.display_name}**, you're not in the list of players. Make sure you ran `{prefix}start {{ban_limit}} (optional)` first. If you have, try using `{prefix}addplayer {{player_name}}` to add yourself to the list.")

@bot.command()
async def draft(ctx):
    msg = drafter.draft()
    try:
        await ctx.send(msg)
    except HTTPException:
        # this occurs when player_list is empty; ctx.send can't send an empty message
        await ctx.send(f"HTTPException: The player list is empty. Make sure you ran `{prefix}start {{ban_limit}} (optional)` first.")

@bot.command()
async def civlist(ctx):
    try:
        await ctx.send(drafter.get_civ_list())
    except HTTPException:
        # this occurs when civ_list is empty; ctx.send can't send an empty message
        await ctx.send(f"HTTPException: The civ list is empty. Make sure you ran `{prefix}start {{ban_limit}} (optional)` first.")

@bot.command()
async def playerlist(ctx):
    try:
        await ctx.send(drafter.get_player_list())
    except HTTPException:
        # this occurs when player_list is empty; ctx.send can't send an empty message
        await ctx.send(f"HTTPException: The player list is empty. Make sure you ran `{prefix}start {{ban_limit}} (optional)` first.")


@bot.command()
async def bancount(ctx):
    try:
        await ctx.send(drafter.get_player_bans())
    except HTTPException:
        # this occurs when player_list is empty; ctx.send can't send an empty message
        await ctx.send(f"HTTPException: The ban count list is empty. Make sure you ran `{prefix}start {{ban_limit}} (optional)` first.")


@bot.command()
async def removeplayer(ctx, player: str):
    try:
        # removes player from player_list
        drafter.player_list.remove(player)
        # removes player from player_bans dictionary
        drafter.get_player_bans().pop(player)
        await ctx.send(f"**{player}** has been removed from the list.")
    except ValueError:
        # this occurs when the player is not in the player list
        await ctx.send(f"**{player}** is not in the player list. Try again.")
    except KeyError:
        # this occurs when the player is not in the player_bans dictionary
        await ctx.send(f"**{player}** is not in the player_bans dictionary. Cedric, debug this.")
        raise KeyError

@bot.command()
async def addplayer(ctx, player: str):
    # enforce uniqueness by checking player_list
    if not player in drafter.player_list:
        drafter.player_list.append(player)
        await ctx.send(f"**{player}** has been added to the list.")
    else:
        await ctx.send(f"**{player}** is already in the list.")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Drafter Commands", description=f"- `{prefix}start {{ban_limit}} (optional)`: Initialize the list of players and the list of civs.\n- `{prefix}ban {{civ_name}}`: Remove specified civ from list of draftable civs. Limited to 2 per player. \n- `{prefix}draft`: Generate the civ picks for each person.\n- `{prefix}civlist`: Print the list of draftable civs.\n- `{prefix}playerlist`: Print the list of players who will be assigned civ picks.\n- `{prefix}bancount`: Print the number of civilizations banned by each player. \n- `{prefix}removeplayer {{player_name}}`: Remove specified player from list of players who will be assigned civ picks. \n- `{prefix}addplayer {{player_name}}`: Add specified player to list of players who will be assigned civ picks.", color=discord.Color.blue())
    await ctx.send(embed=embed)

bot.run(TOKEN)