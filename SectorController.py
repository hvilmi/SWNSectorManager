import DatabaseController
import sectorUI.StarEditorUI as StarEditorUI
import StarSystem
import faction.FactionController as FactionController
import sectorUI.SectorManagerUI as SectorManagerUI
import ConfigReader


class SectorController:
    def __init__(self):

        self.db_control = DatabaseController.DatabaseController('')
        self.sector = self.db_control.get_sector()
        self.faction_controller = FactionController.FactionController(self.db_control.get_factions(), self.sector)

        self.editor_ui = None
        self.mainUI = SectorManagerUI.MainUI(self)
        self.mainUI.start_ui()
        self.cur_star = None

    def star_system_selected(self, coord):
        star = self.sector.get_star_by_coord(coord)
        if star:
            self.mainUI.purge_planet_info()
            for planet in star.get_planets():
                self.mainUI.show_planet_info(planet.get_name(), planet.get_pop(), planet.get_desc(), planet.get_tags(),
                                             planet.tl, planet.atmosphere, planet.biosphere, planet.temperature)

    def show_stars_on_ui(self):
        self.mainUI.make_sector_grid()
        for star in self.sector.get_stars():
            self.mainUI.place_star_on_map(star.get_name(), star.get_coord())

    def choose_sector(self):
        self.db_control.load_sector()
        self.show_stars_on_ui()
        self.faction_controller.factions = self.db_control.get_factions()
        self.faction_controller.display_factions()

    def edit_star(self, coord):
        self.cur_star = self.sector.get_star_by_coord(coord)
        if not type(self.editor_ui) is StarEditorUI.StarEditorUI:
            self.editor_ui = StarEditorUI.StarEditorUI(self, ConfigReader.read_config())
        if self.cur_star:
            # Create window for editing here if a star already exists
            self.editor_ui.create_editor_window(self.cur_star.get_name(), coord)
            for planet in self.cur_star.get_planets():
                self.editor_ui.show_planet(planet.get_name(), planet.get_pop(), planet.get_desc(), planet.get_tags(),
                                           planet.tl, planet.atmosphere, planet.biosphere, planet.temperature)
            self.editor_ui.set_ready()
        else:
            # Ask for name of the new star before starting the editing
            name = self.editor_ui.create_name_window(coord)

    def save_star_system_from_editor(self):
        edited_coord, planets_info = self.editor_ui.get_current_star_system()
        if self.sector.get_star_by_coord(edited_coord):
            new_star = self.sector.get_star_by_coord(edited_coord)
            new_star.planets = []
        else:
            print('error')
        for planet in planets_info:
            new_star.add_new_planet(planet['name'], planet['pop'], planet['desc'], planet['tags'], planet['tl'],
                                    planet['atmosphere'], planet['biosphere'], planet['temperature'])
        self.show_stars_on_ui()

    def save_sector_to_file(self):
        result = self.db_control.save_sector()

    def create_new_star(self, name, coord):
        new_star = StarSystem.StarSystem(name, coord)
        self.sector.add_star(new_star)
        self.show_stars_on_ui()
        self.edit_star(coord)

    def get_faction_controller(self):
        return self.faction_controller

    def get_sector(self):
        return self.sector

    def create_new_sector(self):
        self.sector.clear()
        self.faction_controller.clear()
        self.mainUI.make_sector_grid()

    def save_sector_new_file(self):
        result = self.db_control.save_sector(new_file=True)

    def delete_star(self, coord):
        self.sector.delete_star(self.sector.get_star_by_coord(coord))
        # TODO: Implement raising a window asking if user is sure.
        self.show_stars_on_ui()

    def delete_planet(self, planet_name):
        self.cur_star.planets.remove(self.cur_star.get_planet_by_name(planet_name))
