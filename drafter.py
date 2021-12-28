# import random module
import random

# generate list of civilizations excluding bans
def bans(civs, bans):
    for ban in bans:
        civs.remove(ban)
    return civs

# reformat list into words separated by commas
def format_picks(picks):
    return ", ".join(picks)

# generate the picks for each person
def draft(civs, names):
    for name in names:
        # initialize empty list for civ picks
        picks = []
        for i in range(3):
            # length of civs list
            num_of_civs = len(civs)
            # select random civ and remove it from list
            pick = civs.pop(random.randint(0, num_of_civs - 1))
            # add civ to list of picks
            picks.append(pick)
        # print picks for each person
        print(name + ": " + format_picks(picks))
