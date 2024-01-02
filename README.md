# Drafter Bot

## About

Drafter Bot helps Sid Meier's Civilization 5 players pick civilizations in a Discord server. The bot runs a draft in which each player is randomly assigned three civilizations to choose from. Before this, players can remove civilizations from the pool of possible choices.

> The bot uses the `!` prefix for commands.

## Instructions

To see the list of possible commands, type `!help`.

1. Begin the draft by running the `!start {ban_limit} (optional)` command. If you do not provide a number of bans per player (e.g. `!start`), the ban limit is set to 2.
   1. To see the player list or civilization list, use `!playerlist` and `!civlist`, respectively.
   2. If you want to add/remove players from the draft, use `!addplayer {player_name}` and `!removeplayer {player_name}`, respectively, where `{player_name}` is the player's Discord display name.
2. Let each player ban their desired civilization(s) using the `!ban {civ_name}` command.
3. Use `!draft` to randomly draw three civilizations for each player from the civilization list excluding any bans.
4. (Optional) Reroll the draft using the same bans if you don't like your choices with `!reroll`.

## Configuration

Make sure you have your Discord Bot Token stored inside an `.env` file. For example,

`.env`

```text
TOKEN=12345
```

Also, set up your environment by installing the required packages. Create a virtual environment:

```console
python3 -m venv env
```

Then, activate the virtual environment via

```console
source env/bin/activate
```

Next, select that environment as your Python interpreter.

Finally, just install the dependendies by running

```console
python3 install -r requirements.txt
```

Then, you should be able to run the bot with the command

```console
python3 -m bot
```
