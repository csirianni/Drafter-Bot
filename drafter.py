# import random module
import random


class Drafter:
    
    # constructor
    def __init__(self, player_list: list, civ_list: list, player_bans: dict, ban_limit: int):
        self.player_list = player_list
        self.civ_list = civ_list
        self.player_bans = player_bans
        self.ban_limit = ban_limit

    # remove civ from list of civs and return the removed civ
    def ban(self, civ: str) -> str:
        lower_civ_list = list(map(lambda civ: civ.lower(), self.civ_list))
        index = lower_civ_list.index(civ.lower())
        return self.civ_list.pop(index)

    # reformat list into words separated by commas
    def format_list(self, the_list: list) -> list:
        return ", ".join(the_list)

    # generate the picks for each person
    def draft(self) -> str:
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

    def get_player_list(self) -> list:
        return self.format_list(self.player_list)
    
    def set_civ_list(self, civ_list):
        self.civ_list = civ_list

    def get_civ_list(self) -> list:
        return self.format_list(self.civ_list)

    def set_player_bans(self, player_bans):
        self.player_bans = player_bans
    
    def get_player_bans(self) -> dict:
        return self.player_bans

    def set_ban_limit(self, ban_limit):
        self.ban_limit = ban_limit

    def get_ban_limit(self) -> int:
        return self.ban_limit
