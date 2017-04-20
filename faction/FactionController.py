import faction.FactionEditController as FactionEditController
import faction.Faction as Faction


# name, hp, force, cunning, wealth, fac_creds, xp, homeworld

class FactionController:
    def __init__(self, factions, sector):
        self.factions = factions
        self.sector = sector
        self.faction_treeview = None

    def faction_chosen(self, faction_name):
        chosen_faction = self.get_faction_by_name(faction_name)
        faction_edit_ui = FactionEditController.FactionEditController(self, chosen_faction)

    def get_faction_by_name(self, name):
        for faction in self.factions:
            if faction.name == name:
                return faction
        print("No faction found")

    def add_new_faction(self):
        self.factions.append(Faction.Faction('', 0, 0, 0, 0, 0, 0, ""))
        faction_edit_ui = FactionEditController.FactionEditController(self, self.factions[-1])

    def register_faction_table(self, faction_treeview):
        self.faction_treeview = faction_treeview
        print(self.factions)
        self.display_factions()

    def display_factions(self):
        self.faction_treeview.clear_factions()
        for faction in self.factions:
            self.faction_treeview.show_faction(name=faction.name, hp=faction.hp, force=faction.force,
                                               cunning=faction.cunning, wealth=faction.wealth, creds=faction.fac_creds,
                                               homeworld=faction.homeworld, xp=faction.xp)

    def get_alphabetical_planet_list(self):
        return self.sector.get_alphabetical_planet_list()

    def delete_faction(self, faction):
        '''Takes Faction object or faction name as input and removes that faction.'''
        if type(faction) == type(Faction.Faction('name', 0, 0, 0, 0, 0, 0, 'example planet')):
            self.factions.remove(faction)
        elif type(faction) == type('examplestring'):
            self.factions.remove(get_faction_by_name(faction))
        self.display_factions()
