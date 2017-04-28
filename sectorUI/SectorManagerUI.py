from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import math
from . import FactionTreeViewUI

HEX_SIZE = 40
GRID_ROWS = 10
GRID_COLUMNS = 8


class MainUI:
    def __init__(self, parent):
        self.parent = parent
        self.prev_hovered = []  # List containing ids of previously hovered hex
        self.prev_current = -1

        self.root = Tk()
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(column=0, row=0, sticky=NSEW)

        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label='New Sector', command=self.new_sector)
        filemenu.add_command(label='Load Sector', command=self.load_sector)
        filemenu.add_command(label='Save Sector', command=self.save_sector)
        filemenu.add_command(label='Save Sector as...', command=self.save_sector_as)
        filemenu.add_separator()
        filemenu.add_command(label='Quit', command=self.quit)

        menubar.add_cascade(label='File', menu=filemenu)
        self.root.config(menu=menubar)

        # Hexagonal sector map UI
        self.mapFrame = None
        self.mapCanvas = None
        self.hexagons = None
        self.make_sector_grid()

        # ///////////////////////////////////////////////
        # Area for showing information on planets
        self.planet_frame = Frame(self.main_frame)
        self.planet_frame.grid(column=1, row=0, sticky=NSEW)
        self.planet_NB = ttk.Notebook(self.planet_frame)
        self.planet_NB.grid(column=0, row=0, sticky=NSEW)

        # popup menu for adding new stars or editing existing stars
        self.planet_menu = Menu(self.root, tearoff=0)
        self.planet_menu.add_command(label='Edit Star', command=self.star_chosen)
        self.planet_menu.add_command(label='Delete Star', command=self.delete_star)

        # ///////////////////////////////////////////////
        # Area for showing information on factions
        faction_info = FactionTreeViewUI.FactionTreeViewUI(self.parent.get_faction_controller(), self.main_frame, 1, 1)

    def make_sector_grid(self):
        if self.mapFrame:
            self.mapFrame.destroy()

        self.mapFrame = Frame(self.main_frame)
        self.mapFrame.grid(column=0, row=0, rowspan=2, sticky=NSEW)
        self.mapCanvas = Canvas(self.mapFrame, width=HEX_SIZE * 1.7 * GRID_COLUMNS,
                                height=HEX_SIZE * math.sqrt(3) * (GRID_ROWS + 1))
        self.mapCanvas.pack()
        # 9 rows, 7 columns
        self.hexagons = []
        for i in range(GRID_COLUMNS):
            for j in range(GRID_ROWS):
                hex_points = self.get_hexagon(self.get_real_coord_by_id(self.get_hex_by_coord((i, j))), HEX_SIZE)
                new_hex = self.mapCanvas.create_polygon(hex_points[0][0], hex_points[0][1], hex_points[1][0],
                                                        hex_points[1][1], hex_points[2][0], hex_points[2][1],
                                                        hex_points[3][0], hex_points[3][1], hex_points[4][0],
                                                        hex_points[4][1], hex_points[5][0], hex_points[5][1],
                                                        fill='white', outline='black')
                self.mapCanvas.itemconfig(new_hex, tags=('hex', 'c:' + str(i) + ',' + str(j)))
                self.mapCanvas.tag_bind(new_hex, '<ButtonPress-1>', self.on_hexagon_click)
                self.mapCanvas.tag_bind(new_hex, '<ButtonPress-3>', self.on_hexagon_right_click)
                self.hexagons.append(new_hex)
                self.mapCanvas.tag_bind(new_hex, '<Enter>', self.hex_enter)
                self.mapCanvas.tag_bind(new_hex, '<Leave>', self.hex_exit)
        self.show_grid_coords()

    def new_sector(self):
        self.parent.create_new_sector()


    def load_sector(self):
        self.parent.choose_sector()

    def save_sector(self):
        self.parent.save_sector_to_file()

    def quit(self):
        self.root.destroy()

    def get_hex_corner(self, center, size, i):
        angle_deg = 60 * i
        angle_rad = math.pi / 180 * angle_deg
        return [center[0] + size * math.cos(angle_rad), center[1] + size * math.sin(angle_rad)]

    def get_hexagon(self, center, size):
        hex_points = []
        for i in range(6):
            hex_points.append(self.get_hex_corner(center, size, i))
        return hex_points

    def show_grid_coords(self):
        for id in range(GRID_COLUMNS * GRID_ROWS):
            coord = self.get_coord_by_id(id)
            coord_str = '0' + str(coord[0]) + '0' + str(coord[1])
            hex_coord = self.get_real_coord_by_id(id)
            text_id = self.mapCanvas.create_text((hex_coord[0], hex_coord[1] - HEX_SIZE * math.sqrt(3) / 3),
                                                 text=coord_str, fill='gray')
            self.mapCanvas.itemconfig(text_id, tags=('text', 'c:' + str(coord[0]) + ',' + str(coord[1])))

    def start_ui(self):
        self.root.mainloop()

    def get_hex_by_coord(self, coord):
        # Top left corner is coordinate (0,0)
        return (coord[0] * 10) + coord[1]

    def get_coord_by_id(self, id):
        '''Returns integer coordinates (x,y) of a given hex id.'''
        return math.floor(float(id) / float(GRID_ROWS)), (id) % GRID_ROWS

    def get_real_coord_by_id(self, id):
        int_coord = self.get_coord_by_id(id)
        width = HEX_SIZE * 2
        height = HEX_SIZE * math.sqrt(3)
        if int_coord[0] % 2 == 0:
            return (int_coord[0] + 1) * width * 3 / 4, (int_coord[1] + 1) * height
        else:
            return (int_coord[0] + 1) * width * 3 / 4, (int_coord[1] + 3 / 2) * height

    def on_hexagon_click(self, event):
        if self.mapCanvas.find_withtag(CURRENT):
            self.parent.star_system_selected(self.get_coord_by_id(self.mapCanvas.find_withtag(CURRENT)[0] - 1))

    def show_planet_info(self, name, pop, desc, tags, tl, atmosphere, biosphere, temperature):

        if tags is None:
            tags = ['']
        planet_frame = Frame(self.planet_NB)
        self.planet_NB.add(planet_frame, text=name, sticky=NSEW)

        planet_info_frame = LabelFrame(planet_frame, text='Planet Info')
        planet_info_frame.grid(row=0, column=0, sticky=(N, W, S))

        Label(planet_info_frame, text='Name: ' + str(name)).grid(column=0, row=0, columnspan=2)

        Label(planet_info_frame, text='Population: ' + str(pop)).grid(column=2, row=0, columnspan=2)

        Label(planet_info_frame, text='Tech Level: ' + str(tl)).grid(column=0, row=1, columnspan=2)

        Label(planet_info_frame, text='Atmosphere: ' + str(atmosphere)).grid(column=2, row=1, columnspan=2)

        Label(planet_info_frame, text='Biosphere: ' + str(biosphere)).grid(column=0, row=2, columnspan=2)

        Label(planet_info_frame, text='Temperature: ' + str(temperature)).grid(column=2, row=2, columnspan=2)

        tag_text = ''
        for i in range(len(tags)):
            if i == len(tags) - 1 and i != 0:
                tag_text = tag_text + ' & '
            elif i != 0:
                tag_text = tag_text + ', '
            tag_text = tag_text + str(tags[i])

        Label(planet_info_frame, text='Tags').grid(row=3, column=0)

        planet_tag_label = Label(planet_info_frame, text=tag_text)
        planet_tag_label.grid(column=1, row=3, columnspan=5)

        # separator = ttk.Separator(planet_frame, orient=VERTICAL)
        # separator.grid(column=1, row=0, rowspan=4)

        planet_desc_frame = LabelFrame(planet_frame, text='Description', width=300)
        planet_desc_frame.grid(column=0, row=4, columnspan=4, sticky=NSEW)

        # planet_desc_label = Label(planet_desc_frame, text='Description:')
        # planet_desc_label.grid(column=2, row=0)

        planet_desc_text = Message(planet_desc_frame, text=str(desc))
        planet_desc_text.pack()

    def purge_planet_info(self):
        self.planet_NB.grid_forget()
        self.planet_NB.destroy()
        self.planet_NB = ttk.Notebook(self.planet_frame)
        self.planet_NB.grid(column=0, row=0, sticky=(N, W, S))

    def place_star_on_map(self, name, coord):
        name_coord = self.get_real_coord_by_id(self.get_hex_by_coord(coord))
        planet_text = self.mapCanvas.create_text((name_coord[0], name_coord[1] + HEX_SIZE * math.sqrt(3) / 4),
                                                 text=name, fill='gray')
        planet_oval = self.mapCanvas.create_oval((name_coord[0] - HEX_SIZE / 5, name_coord[1] - HEX_SIZE / 5,
                                                  name_coord[0] + HEX_SIZE / 5, name_coord[1] + HEX_SIZE / 5),
                                                 fill='gray')
        self.mapCanvas.itemconfig(planet_text, tags=('planet text', 'c:' + str(coord[0]) + ',' + str(coord[1])))
        self.mapCanvas.itemconfig(planet_oval, tags=('planet oval', 'c:' + str(coord[0]) + ',' + str(coord[1])))

    def hex_enter(self, event):
        self.hex_exit(event)
        closest_item = self.mapCanvas.find_closest(self.mapCanvas.canvasx(event.x), self.mapCanvas.canvasy(event.y))
        tags = self.mapCanvas.gettags(CURRENT)
        for tag in tags:
            if tag[:2] == 'c:':
                coord_tag = tag
        items = self.mapCanvas.find_withtag(coord_tag)
        for id in items:
            if not 'hex' in self.mapCanvas.gettags(id):
                self.mapCanvas.itemconfig(id, fill='black')
        self.prev_hovered = items

    def hex_exit(self, event):
        for id in self.prev_hovered:
            if not 'hex' in self.mapCanvas.gettags(id):
                self.mapCanvas.itemconfig(id, fill='gray')

    def on_hexagon_right_click(self, event):
        if self.mapCanvas.find_withtag(CURRENT):
            self.prev_current = self.mapCanvas.find_withtag(CURRENT)
            self.planet_menu.post(event.x_root, event.y_root)

    def star_chosen(self):
        self.parent.edit_star(self.get_coord_by_id(self.prev_current[0] - 1))

    def save_sector(self):
        self.parent.save_sector_to_file()

    def save_sector_as(self):
        self.parent.save_sector_new_file()

    def delete_star(self):
        self.parent.delete_star(self.get_coord_by_id(self.prev_current[0]-1))
