# import random module
import random

class Drafter:
    
    # constructor
    def __init__(self, player_list: list, civ_list = None):
        self.player_list = player_list
        self.civ_list = civ_list

    # generate list of civilizations excluding bans
    def ban(self, civ: str):
        self.civ_list.remove(civ)
        return self.civ_list

    # reformat list into words separated by commas
    def format_list(self,the_list):
        return ", ".join(the_list)

    # generate the picks for each person
    def draft(self):
        msg = ""
        for player in self.player_list:
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
            msg += player + ": " + self.format_list(picks) + "\n"
        return msg

    def set_player_list(self, player_list):
        self.player_list = player_list

    def get_player_list(self):
        return self.format_list(self.player_list)
    
    def set_civ_list(self, civ_list):
        self.civ_list = civ_list

    def get_civ_list(self):
        return self.format_list(self.civ_list)