import StarSystem
import Sector
from tkinter import filedialog
import json
import faction.Faction as Faction
from faction.assets import AssetDatabase
import faction.FactionController as FactionController

CURRENT_VERSION = 3


class DatabaseController:
    def __init__(self, path):
        self.sector = Sector.Sector()
        self.factions = []

        '''Reads files in a given directory and stores info in Sector class'''
        self.path = ''

    def read_stars(self, path):

        f = open(path, 'r')

        self.sector.clear()
        self.factions = []
        asset_db = AssetDatabase.AssetDatabase()

        try:
            sector_dict = json.load(f)
            self.sector.set_name(sector_dict['name'])
            if sector_dict['version'] < CURRENT_VERSION:
                self.old_load(sector_dict, asset_db)
            else:
                for star in sector_dict['stars']:
                    new_star = StarSystem.StarSystem(name=star['name'], coord=star['coord'])
                    for planet in star['planets']:
                        print(star['planets'])
                        new_star.add_new_planet(planet['name'], planet['pop'], planet['desc'], planet['tags'],
                                                planet['tl'], planet['atmosphere'], planet['biosphere'],
                                                planet['temperature'])
                    self.sector.add_star(new_star)

                temp_fac_controller = FactionController.FactionController([], self.sector)
                for faction in sector_dict['factions']:
                    self.factions.append(
                        Faction.Faction(faction['name'], faction['hp'], faction['force'], faction['cunning'],
                                        faction['wealth'], faction['fac_creds'], faction['xp'], faction['homeworld'],
                                        temp_fac_controller))
                    for asset in faction['assets']:
                        self.factions[-1].add_asset(asset['star'], asset['planet'], asset['cur_hp'],
                                                    asset_db.query(name=asset['name'])[0], asset['x'], asset['y'])

        except json.JSONDecodeError as e:
            print("Sector Decoding error: " + str(e))
        f.close()

    def get_sector(self):
        return self.sector

    def load_sector(self):
        file = filedialog.askopenfile()
        if file:
            self.path = file.name
            file.close()
            self.read_stars(self.path)

    def get_factions(self):
        return self.factions

    def save_sector(self, new_file=False):
        """Saves current sector and factions in .sector -file.
            Returns 0 if successful, 1 if no file was specified."""
        if self.path == '' or new_file:
            f = filedialog.asksaveasfile(mode='w', defaultextension='.sector')
            if f is None:
                return 1
            self.path = f.name
            f.close()
        # This part erases previous contents of the .sector file
        f = open(self.path, 'w')
        f.close()
        # ---------#
        print('saving to ' + self.path)
        sector_dict = {'version': CURRENT_VERSION, 'name': self.sector.get_name(), 'stars': [], 'factions': []}
        with open(self.path, 'w') as f:
            for star in self.sector.get_stars():
                star_dict = {'name': star.get_name(), 'coord': star.get_coord(), 'planets': []}
                for planet in star.get_planets():
                    planet_dict = {'name': planet.get_name(), 'pop': planet.get_pop(), 'tags': planet.get_tags(),
                                   'tl': planet.tl, 'desc': planet.get_desc(), 'atmosphere':planet.atmosphere,
                                   'biosphere': planet.biosphere, 'temperature': planet.temperature}
                    star_dict['planets'].append(planet_dict)
                sector_dict['stars'].append(star_dict)
            for faction in self.factions:
                faction_dict = {'name': faction.name, 'hp': faction.hp, 'force': faction.force,
                                'cunning': faction.cunning, 'wealth': faction.wealth,
                                'fac_creds': faction.fac_creds, 'xp': faction.xp, 'homeworld': faction.homeworld,
                                'assets': []}
                for asset in faction.assets:
                    faction_dict['assets'].append(
                        {'name': asset.get_name(), 'star': asset.star, 'planet': asset.planet,
                         'cur_hp': asset.cur_hp, 'x': asset.x_coord, 'y': asset.y_coord})
                    print(faction_dict['assets'][-1])
                sector_dict['factions'].append(faction_dict)
            json.dump(sector_dict, f, sort_keys=True, indent=4)
        return 0

    def old_load(self, sector_dict, asset_db):
        if sector_dict['version'] == 1:
            # Before adding atmosphere, biosphere and temperature fields to planets.
            for star in sector_dict['stars']:
                new_star = StarSystem.StarSystem(name=star['name'], coord=star['coord'])
                for planet in star['planets']:
                    print(star['planets'])
                    new_star.add_new_planet(planet['name'], planet['pop'], planet['desc'], planet['tags'], planet['tl'],
                                            '', '', '')
                self.sector.add_star(new_star)
            for faction in sector_dict['factions']:
                self.factions.append(
                    Faction.Faction(faction['name'], faction['hp'], faction['force'], faction['cunning'],
                                    faction['wealth'], faction['fac_creds'], faction['xp'], faction['homeworld']))
                for asset in faction['assets']:
                    self.factions[-1].add_asset(asset['star'], asset['planet'], asset['cur_hp'],
                                                asset_db.query(name=asset['name'])[0])

        elif sector_dict['version'] == 2:
            for star in sector_dict['stars']:
                new_star = StarSystem.StarSystem(name=star['name'], coord=star['coord'])
                for planet in star['planets']:
                    print(star['planets'])
                    new_star.add_new_planet(planet['name'], planet['pop'], planet['desc'], planet['tags'],
                                            planet['tl'], planet['atmosphere'], planet['biosphere'],
                                            planet['temperature'])
                self.sector.add_star(new_star)
            temp_faction_controller = FactionController.FactionController([], self.sector)
            for faction in sector_dict['factions']:
                self.factions.append(
                    Faction.Faction(faction['name'], faction['hp'], faction['force'], faction['cunning'],
                                    faction['wealth'], faction['fac_creds'], faction['xp'], faction['homeworld'],
                                    temp_faction_controller))
                for asset in faction['assets']:
                    self.factions[-1].add_asset(asset['star'], asset['planet'], asset['cur_hp'],
                                                asset_db.query(name=asset['name'])[0], 0, 0)
