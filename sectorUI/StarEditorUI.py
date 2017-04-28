from tkinter import *
from tkinter import ttk
import math


class StarEditorUI:
    def __init__(self, parent, config):
        self.parent = parent
        self.manual_entry = False
        self.config = config

        self.name_window = None
        self.new_name_field = None

        self.edit_planets_window = None
        self.editor_nb = None
        self.planet_info_list = []
        self.current_coord = None

        self.editor_ready = False

    def create_name_window(self, coord):
        self.current_coord = coord

        self.name_window = Toplevel()
        self.name_window.title("Create new star system")

        label = Label(self.name_window, text="Creating new star system at 0" + str(coord[0]) + '0' + str(coord[1]))
        label.grid(row=0, column=0, columnspan=2)

        label2 = Label(self.name_window, text='Enter Name:')
        label2.grid(row=1, column=0)

        self.new_name_field = Entry(self.name_window)
        self.new_name_field.grid(row=1, column=1)

        button_create = Button(self.name_window, text='Create', command=self.send_star_name)
        button_create.grid(row=2, column=0)

        button_cancel = Button(self.name_window, text='Cancel', command=self.close_name_window)
        button_cancel.grid(row=2, column=1)

    def send_star_name(self):
        self.parent.create_new_star(self.new_name_field.get(), self.current_coord)
        self.name_window.destroy()

    def close_name_window(self):
        self.name_window.destroy()

    def create_editor_window(self, star_name, coord):
        self.editor_ready = False

        self.current_coord = coord
        if not self.edit_planets_window:
            self.edit_planets_window = Toplevel()
            self.edit_planets_window.title('Editing ' + star_name + ' system')

        if self.editor_nb:
            self.editor_nb.destroy()
            self.planet_info_list = []
        self.editor_nb = ttk.Notebook(self.edit_planets_window)
        self.editor_nb.grid(row=0, column=0, sticky=(N, W, E, S), columnspan=5)

        self.editor_nb.bind('<<NotebookTabChanged>>', self.on_tab_change)

        Button(self.edit_planets_window, text='Save', command=self.send_changes).grid(row=1, column=0)
        Button(self.edit_planets_window, text='Cancel', command=self.discard_changes).grid(row=1, column=1)
        Button(self.edit_planets_window, text='Delete', command=self.delete_planet).grid(row=1, column=2)

        add_new_tab = Frame(self.editor_nb)
        self.editor_nb.add(add_new_tab, text='<New Planet>')

    def place_planet_info_widget(self, parent, m_row, m_column, text, options):
        attr_var = StringVar()
        attr_var.set(text)
        if self.manual_entry:
            Entry(parent, textvariable=attr_var).grid(row=m_row, column=m_column)
        else:
            OptionMenu(parent, attr_var, *options).grid(row=m_row, column=m_column)
        return attr_var

    def show_planet(self, name='', pop='', desc='', tags=None, tl='', atmosphere='', biosphere='', temperature=''):
        if tags is None:
            tags = ['']
        self.planet_info_list.append({})

        planet_frame = Frame(self.editor_nb)
        self.editor_nb.insert(self.editor_nb.index(self.editor_nb.select()), planet_frame, text=name)

        planet_info_frame = LabelFrame(planet_frame, text='Planet Info', width=200)
        planet_info_frame.grid(row=0, column=0, sticky=(N, W, S))

        Label(planet_info_frame, text='Name: ').grid(column=0, row=0)
        planet_name_entry = Entry(planet_info_frame)
        planet_name_entry.insert(END, str(name))
        planet_name_entry.grid(column=1, row=0)
        self.planet_info_list[len(self.planet_info_list) - 1]['name'] = planet_name_entry

        Label(planet_info_frame, text='Atmosphere: ').grid(column=2, row=0)
        planet_atmosphere_entry = self.place_planet_info_widget(planet_info_frame, 0, 3, atmosphere,
                                                                self.config['atmosphere'])
        self.planet_info_list[len(self.planet_info_list) - 1]['atmosphere'] = planet_atmosphere_entry

        Label(planet_info_frame, text='Biosphere: ').grid(column=2, row=1)
        planet_biosphere_entry = self.place_planet_info_widget(planet_info_frame, 1, 3, biosphere,
                                                               self.config['biosphere'])
        self.planet_info_list[-1]['biosphere'] = planet_biosphere_entry

        Label(planet_info_frame, text='Temperature: ').grid(column=2, row=2)
        planet_temperature_entry = self.place_planet_info_widget(planet_info_frame, 2, 3, temperature,
                                                                 self.config['temperature'])
        self.planet_info_list[-1]['temperature'] = planet_temperature_entry

        Label(planet_info_frame, text='Population: ').grid(column=0, row=1)
        planet_pop_entry = Entry(planet_info_frame)
        planet_pop_entry.insert(END, str(pop))
        planet_pop_entry.grid(column=1, row=1)
        self.planet_info_list[len(self.planet_info_list) - 1]['pop'] = planet_pop_entry

        Label(planet_info_frame, text='Tech Level: ').grid(column=0, row=2)
        planet_tl_entry = self.place_planet_info_widget(planet_info_frame, 2, 1, str(tl), self.config['tech level'])
        self.planet_info_list[len(self.planet_info_list) - 1]['tl'] = planet_tl_entry

        Label(planet_info_frame, text='Tags:').grid(column=0, row=3)

        tag_entry_list = []
        for i in range(4):
            tag_entry_list.append(Entry(planet_info_frame))
            tag_entry_list[i].grid(column=math.floor(i / 2) + 1, row=(i % 2) + 3)
            try:
                tag_entry_list[i].insert(END, tags[i])
            except IndexError:
                pass
        self.planet_info_list[len(self.planet_info_list) - 1]['tags'] = tag_entry_list

        planet_desc_label = Label(planet_info_frame, text='Description: ')
        planet_desc_label.grid(column=0, row=6, sticky=NSEW)

        planet_desc_entry = Text(planet_info_frame)
        planet_desc_entry.insert(END, desc)
        planet_desc_entry.grid(column=1, row=6, columnspan=4)
        self.planet_info_list[len(self.planet_info_list) - 1]['desc'] = planet_desc_entry

        # planet_desc_label = Label(planet_desc_frame, text='Description:')
        # planet_desc_label.grid(column=2, row=0)

    def send_changes(self):
        self.parent.save_star_system_from_editor()

    def discard_changes(self):
        pass

    def get_current_star_system(self):
        """Function returns a list containing information of current star system"""
        planet_list = []
        for planet in self.planet_info_list:
            planet_list.append({})
            for field in ['name', 'pop', 'tl', 'atmosphere', 'biosphere', 'temperature']:
                planet_list[-1][field] = planet[field].get()
            planet_list[-1]['desc'] = planet['desc'].get(1.0, END)
            # Tags need to be handled separately
            planet_list[-1]['tags'] = []
            for tag_entry in planet['tags']:
                if tag_entry.get():
                    planet_list[-1]['tags'].append(tag_entry.get())
        return self.current_coord, planet_list

    def on_tab_change(self, event):
        if self.editor_nb.tabs()[-1] == self.editor_nb.select() and self.editor_ready:
            self.show_planet()
            self.editor_nb.select(self.editor_nb.tabs()[-2])

    def set_ready(self):

        self.editor_nb.select(self.editor_nb.tabs()[0])
        self.editor_ready = True

    def delete_planet(self):
        planet_index = self.editor_nb.tabs().index(self.editor_nb.select())
        self.parent.delete_planet(self.planet_info_list[planet_index]['name'].get())
