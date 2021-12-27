# import csv module
import csv
# import random module
import random

# generate list of civilizations excluding bans
def bans(civs, bans):
    for ban in bans:
        civs.remove(ban)
    return civs

# reformat list into words separated by commas
def format_picks(picks):
    if len(picks) == 1:  # base case, return element
        return str(picks[0])
    else:  # recursive case, return with comma concatenated to recursive output
        return str(picks[0]) + ", " + format_picks(picks[1:])

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

# print(format_picks(['Russia', 'Polyneisa', 'Mongolia']))
# print(len(['Mongolia']))


# open csv file
with open('civ-list.csv') as f:
    # create a reader object
    reader = csv.reader(f)
    # initialize empty list for civ names
    civ_list = []
    # iterate over reader and append civ name to civs list
    for civ in reader:
        # index 0 used to unwrap list containing the civ name
        civ_list.append(civ[0])

    # print(civs)

# initalize list of players
name_list = ["Angelo", "Cedric", "Luca", "Mars", "Cleo", "Nico", "Halim"]
random.shuffle(name_list)
# initalize list of bans
ban_list = ["America", "Arabia", "Assyria", "Austria", "Aztec", "Babylon",
            "Byzantium", "Carthage", "Celts", "China", "Denmark", "Netherlands"]
# initialize list of civs excluded those banned
pickable_civs = bans(civ_list, ban_list)
# generate the picks for each person
draft(civ_list, name_list)
