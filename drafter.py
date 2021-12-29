# import random module
import random

# import csv module
import csv

class Drafter:
    # open csv file
    with open('civ-list.csv') as f:
        # create a reader object
        reader = csv.reader(f)
        # initialize empty list for civ names
        full_civ_list = []
        # iterate over reader and append civ name to civs list
        for civ in reader:
            # index 0 used to unwrap list containing the civ name
            full_civ_list.append(civ[0])
    
    def __init__(self, name_list: list, civ_list = None):
        self.name_list = name_list
        # use None default because pythonic, avoids unintended behavior
        if civ_list is None:
            # use copy to prevent modifying full_civ_list in ban
            self.civ_list = Drafter.full_civ_list.copy()
        else:
            self.civ_list = civ_list

    # generate list of civilizations excluding bans
    def ban(self, civ: str):
        self.civ_list.remove(civ)
        return self.civ_list

    # reformat list into words separated by commas
    def format_picks(self, picks):
        return ", ".join(picks)

    # generate the picks for each person
    def draft(self):
        msg = ""
        for name in self.name_list:
            # initialize empty list for civ picks
            picks = []
            for i in range(3):
                # length of civs list
                num_of_civs = len(self.civ_list)
                # select random civ and remove it from list
                pick = self.civ_list.pop(random.randint(0, num_of_civs - 1))
                # add civ to list of picks
                picks.append(pick)
            # return picks for each person
            msg += name + ": " + self.format_picks(picks) + "\n"
        return msg

    def set_name_list(self, name_list):
        self.name_list = name_list
    
    def set_civ_list(self, civ_list):
        self.civ_list = civ_list
