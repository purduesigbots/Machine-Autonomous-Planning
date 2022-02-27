# import statements
from classes.converter import Converter as c
import tkinter as tk

# Movement class encapsulates code associated with movements
class Movement:

    def __init__(self, start, end, line_ref, name="Movement"):
        # initialize variables
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

    # clear arrow from canvas
    def clear(self, canvas):
        canvas.delete(self.line_ref)

    # draw arrow on canvas
    def draw(self, canvas):
        line_fill = "lime" if self.selected else "green"
        self.line_ref = canvas.create_line(self.start[0], self.start[1], self.end[0], self.end[1], 
                                     fill=line_fill, width=5, arrow=tk.LAST, arrowshape=(8, 10, 8))
    
    # set the speed to val
    def set_speed(self, val):
        self.options["speed"] = val
    
    # toggle async value
    def toggle_async(self):
        self.options["flags"]["arms::ASYNC"] = not self.options["flags"]["arms::ASYNC"]
    
    # get string for exporting to script
    def to_string(self):
        joined_flags = " | ".join([f for f in self.options["flags"] if self.options["flags"][f]])
        return f'chassis::move({{{c.convert_x(self.end[0])} , {c.convert_y(self.end[1])}}}, {self.options["speed"]}{", " + joined_flags if len(joined_flags) > 0 else ""});\n'

# SidebarGroup class encapsulates sidebar widget groups
class SidebarGroup:

    def __init__(self, movement, sidebar, canvas):
        # initialize variables
        self.movement = movement
        self.sidebar = sidebar
        self.canvas = canvas
        
        # create sub-frame
        self.frame = tk.Frame(self.sidebar)

        # add movement name label
        self.txt = tk.Label(self.frame, text=self.movement.name, font=("Arial", 18))
        self.txt.grid(row=0, column=0, columnspan=2)

        # add speed label
        speed_txt = tk.Label(self.frame, text="Speed: ", font=("Arial", 12))
        speed_txt.grid(row=0, column=2, columnspan=1)

        # add speed slider
        self.slider = tk.Scale(self.frame, from_=0, to=100, orient="horizontal", command= lambda e: self.movement.set_speed(e))
        self.slider.set(100)
        self.slider.grid(row=0, column=3, columnspan=2)

        self.async_flag = tk.BooleanVar()
        async_checkbox = tk.Checkbutton(self.frame, text="ASYNC", variable=self.async_flag, onvalue=True, offvalue=False, command=self.set_flags)
        async_checkbox.grid(row=1, column=0, columnspan=1)

        self.absolute_flag = tk.BooleanVar()
        absolute_checkbox = tk.Checkbutton(self.frame, text="ABSOLUTE", variable=self.absolute_flag, onvalue=True, offvalue=False, command=self.set_flags)
        absolute_checkbox.grid(row=1, column=1, columnspan=1)

        self.backwards_flag = tk.BooleanVar()
        backwards_checkbox = tk.Checkbutton(self.frame, text="BACKWARDS", variable=self.backwards_flag, onvalue=True, offvalue=False, command=self.set_flags)
        backwards_checkbox.grid(row=1, column=2, columnspan=1)

        self.thru_flag = tk.BooleanVar()
        thru_checkbox = tk.Checkbutton(self.frame, text="THRU", variable=self.thru_flag, onvalue=True, offvalue=False, command=self.set_flags)
        thru_checkbox.grid(row=1, column=3, columnspan=1)

        # pack frame
        self.frame.pack(side=tk.TOP)

        self.selected = False

        # bind mouse input to click_handler callback
        self.txt.bind("<Button-1>", self.click_handler)

    def click_handler(self, event):
        # if LMB click
        if event.num == 1:
            # toggle selected value and set movement name label color
            self.selected = not self.selected
            if self.selected:
                self.txt.configure(foreground="red")
            else:
                self.txt.configure(foreground="black")
            
            # toggle movement selected value and redraw movement
            self.movement.selected = not self.selected
            self.movement.clear(self.canvas)
            self.movement.draw(self.canvas)
    
    def set_flags(self):
        self.movement.options["flags"]["arms::ASYNC"] = self.async_flag.get()
        self.movement.options["flags"]["arms::ABSOLUTE"] = self.absolute_flag.get()
        self.movement.options["flags"]["arms::BACKWARDS"] = self.backwards_flag.get()
        self.movement.options["flags"]["arms::THRU"] = self.thru_flag.get()