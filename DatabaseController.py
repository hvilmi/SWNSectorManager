import StarSystem
import Sector
from tkinter import filedialog
import json
import faction.Faction as Faction


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

        try:
            sector_dict = json.load(f)
            self.sector.set_name(sector_dict['name'])
            for star in sector_dict['stars']:
                new_star = StarSystem.StarSystem(name=star['name'], coord=star['coord'])
                for planet in star['planets']:
                    print(star['planets'])
                    new_star.add_new_planet(planet['name'], planet['pop'], planet['desc'], planet['tags'], planet['tl'])
                self.sector.add_star(new_star)
            for faction in sector_dict['factions']:
                self.factions.append(Faction.Faction(faction['name'], faction['hp'], faction['force'], faction['cunning'], faction['wealth'], faction['fac_creds'], faction['xp'], faction['homeworld']))
        except json.JSONDecodeError as e:
            print("Sector Decoding error: "+str(e))
        print('all the stars', self.sector.stars)
        print('all the factions', self.factions)
        f.close()



    def get_sector(self):
        return self.sector

    def load_sector(self):
        file = filedialog.askopenfile()
        self.path = file.name
        file.close()
        self.read_stars(self.path)

    def get_factions(self):
        return self.factions

    def save_sector(self):
        if self.path != '':
            #This part erases previous contents of the .sector file
            f = open(self.path, 'w')
            f.close()
            #---------#
            sector_dict = {'name':self.sector.get_name(), 'stars':[], 'factions':[]}
            with open(self.path, 'w') as f:
                for star in self.sector.get_stars():
                    star_dict = {'name':None, 'coord':None, 'planets':[]}
                    star_dict['name'] = star.get_name()
                    star_dict['coord'] = star.get_coord()
                    for planet in star.get_planets():
                        planet_dict = {'name':planet.get_name(), 'pop':planet.get_pop(), 'tags':planet.get_tags(), 'tl':planet.get_tl(), 'desc':planet.get_desc()}
                        star_dict['planets'].append(planet_dict)
                    sector_dict['stars'].append(star_dict)
                for faction in self.factions:
                    faction_dict = {'name':faction.name, 'hp':faction.hp, 'force':faction.force, 'cunning':faction.cunning, 'wealth':faction.wealth, 'fac_creds':faction.fac_creds, 'xp':faction.xp, 'homeworld':faction.homeworld}
                    sector_dict['factions'].append(faction_dict)
                print('--------\n Factions when saving')
                print(self.factions)
                json.dump(sector_dict, f, sort_keys=True, indent=4)


        

