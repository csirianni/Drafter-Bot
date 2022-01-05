# Drafter Bot

Cedric Sirianni

![](https://heroku-status-badges.herokuapp.com/{drafter-bot})

## About

Drafter Bot is a Discord bot designed to help Sid Meier's Civilization 5 multiplayer lobbies select a civilization for each player. 

The bot runs a draft in which each player is randomly assigned three civilizations to choose from. Prior to this, players have to the option to remove civilizations from the pool of possible choices.

The bot uses the`!` prefix for commands.

## Instructions

To see the list of possible commands, type `!help`.

1. Begin the draft by running the `!start {ban_limit} (optional)` command. If you do not provide a number of bans per player (e.g. `!start`), the value is set to 2.
   1. To see the player list or civilization list, use `!playerlist` and `!civlist`, respectively.
   2. If you want to add/remove players from the draft, use `!removeplayer {player_name}` and `!addplayer {player_name}`, respectively, where `{player_name}` is the player's Discord display name.
2. Let each player ban their desired civilization(s) using the `!ban {civ_name}` command.
3. Use `!draft` to randomly draw three civilizations for each player from the civilization list excluding any bans.

# Hosting

The bot is currently hosted on [Heroku](https://dashboard.heroku.com/login) using the Free Dyno plan. The following files are only necessary if using Heroku:

- `Procfile`
- `requirements.txt`
