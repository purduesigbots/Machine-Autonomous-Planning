from classes.converter import Converter as c
import tkinter as tk
from tkinter import ttk

class Movement:

    def __init__(self, start, end, line_ref, name="Movement"):
        self.start = start
        self.end = end
        self.line_ref = line_ref
        self.options = {
            "speed": 100,
            "flags": {
                "arms::ASYNC": False,
                "arms::ABSOLUTE": False,
                "arms::BACKWARDS": False,
                "arms::THRU": False,
            }
        }
        self.name = name
        self.selected = False

    def clear(self, canvas):
        canvas.delete(self.line_ref)

    def draw(self, canvas):
        line_fill = "lime" if self.selected else "green"
        self.line_ref = canvas.create_line(self.start[0], self.start[1], self.end[0], self.end[1], 
                                     fill=line_fill, width=5, arrow=tk.LAST, arrowshape=(8, 10, 8))
    
    def set_speed(self, val):
        self.options["speed"] = val
    
    def to_string(self):
        joined_flags = " | ".join([f for f in self.options["flags"] if self.options["flags"][f]])
        return f'chassis::move({{{c.convert_x(self.end[0])} , {c.convert_y(self.end[1])}}}, {self.options["speed"]}{", " + joined_flags if len(joined_flags) > 0 else ""});\n'

class SidebarGroup:

    def __init__(self, movement, sidebar, canvas):
        self.movement = movement
        self.sidebar = sidebar
        self.canvas = canvas
        
        self.frame = tk.Frame(self.sidebar)

        self.txt = tk.Label(self.frame, text=self.movement.name, font=("Arial", 18))
        self.txt.grid(row=0, column=0, columnspan=2)

        speed_txt = tk.Label(self.frame, text="Speed: ", font=("Arial", 12))
        speed_txt.grid(row=0, column=3, columnspan=1)

        self.slider = tk.Scale(self.frame, from_=0, to=100, orient="horizontal", command= lambda e: self.movement.set_speed(e))
        self.slider.grid(row=0, column=4, columnspan=2)

        self.frame.pack(side=tk.TOP)

        self.selected = False

        self.txt.bind("<Button-1>", self.click_handler)

    def click_handler(self, event):
        if event.num == 1:
            self.selected = not self.selected
            if self.selected:
                self.txt.configure(foreground="red")
            else:
                self.txt.configure(foreground="black")
            
            self.movement.selected = not self.selected
            self.movement.clear(self.canvas)
            self.movement.draw(self.canvas)