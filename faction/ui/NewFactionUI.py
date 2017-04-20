import tkinter as tk
import tkinter.ttk as ttk


class NewFactionUI:

    def __init__(self):
        window = tk.Toplevel()
        main_frame = tk.Frame(window)
        main_frame.pack()

        tk.Label(main_frame, text='New faction name: ').grid(column=0, row=0)
        self.name_entry = tk.Entry(main_frame)
        self.name_entry.grid(column=1, row=0)


