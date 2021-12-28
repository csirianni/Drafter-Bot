# import csv module
import csv
# import random module
import random
# import draft fucntions
from drafter import draft, bans

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