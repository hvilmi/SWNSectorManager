import tkinter as tk
import tkinter.ttk as ttk

COST_ERROR = "Not enough facCreds."
PLANET_ERROR = "No planet chosen."


class BoIAdderUI:
    def __init__(self, parent, world_list):
        self.parent = parent
        self.window = tk.Toplevel()
        main_frame = tk.Frame(self.window)
        main_frame.grid(column=0, row=0)

        tk.Label(main_frame, text='Cost of Base of Influence:').grid(column=0, row=0)

        self.boi_cost = tk.IntVar()
        self.boi_cost.set(0)
        tk.Entry(main_frame, textvariable=self.boi_cost).grid(column=1, row=0)

        self.world_selection = tk.StringVar()
        tk.OptionMenu(main_frame, self.world_selection, *world_list).grid(row=1, column=1)
        self.world_selection.set(world_list[0])
        # self.world_selection.trace('w', self.filter_change)

        tk.Button(main_frame, text='Add BoI', command=self.buy_pressed).grid(column=0, row=2)

        self.error_text = tk.StringVar()
        tk.Label(main_frame, textvariable=self.error_text).grid(column=1, row=2)

    def buy_pressed(self):
        self.parent.acquire_boi(self.boi_cost.get(), self.world_selection.get())

    def raise_error(self, error):
        self.error_text.set(error)
