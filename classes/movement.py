# import statements
from classes.converter import Converter as c
from classes.constants import DARK_MODE_BG, DARK_MODE_FG, LIGHT_MODE_BG, LIGHT_MODE_FG, SELECTED_COLOR
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
                "arms::RELATIVE": False,
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
        line_fill = "green" if self.selected else "lime"
        self.line_ref = canvas.create_line(self.start[0], self.start[1], self.end[0], self.end[1], 
                                     fill=line_fill, width=5, arrow=tk.LAST, arrowshape=(8, 10, 8))
    
    # set the speed to val
    def set_speed(self, val):
        self.options["speed"] = val
    
    # toggle async value
    def toggle_async(self):
        self.options["flags"]["arms::ASYNC"] = not self.options["flags"]["arms::ASYNC"]
    
    # get name as comment
    def get_name_as_cmt(self):
        return f'// {self.name}\n'
    
    # get string for exporting to script
    def to_string(self):
        joined_flags = " | ".join([f for f in self.options["flags"] if self.options["flags"][f]])
        return f'chassis::move({{{c.convert_x(self.end[0])} , {c.convert_y(self.end[1])}}}, {self.options["speed"]}{", " + joined_flags if len(joined_flags) > 0 else ""});\n'

# SidebarGroup class encapsulates sidebar widget groups
class SidebarGroup:

    def __init__(self, movement, owner, index, speed=100, flags=""):
        # initialize variables
        self.movement = movement
        self.owner = owner
        self.index = index
        self.selected = False
        
        # create sub-frame
        self.frame = tk.Frame(self.owner.sidebar)

        # add movement name label
        self.txt = tk.Label(self.frame, text=self.movement.name, font=("Arial", 18))
        self.txt.grid(row=0, column=0, columnspan=2)

        # add speed label
        self.speed_txt = tk.Label(self.frame, text="Speed: ", font=("Arial", 12))
        self.speed_txt.grid(row=0, column=2, columnspan=1)

        # add speed slider
        self.slider = tk.Scale(self.frame, from_=0, to=100, orient="horizontal", command= lambda e: self.movement.set_speed(e))
        self.slider.set(speed)
        self.slider.grid(row=0, column=3, columnspan=2)

        # create async flag variable and checkbutton
        self.async_flag = tk.BooleanVar()
        self.async_checkbox = tk.Checkbutton(self.frame, text="ASYNC", variable=self.async_flag, onvalue=True, offvalue=False, command=self.set_flags)
        self.async_checkbox.grid(row=1, column=0, columnspan=1)

        # if imported movement has async flag, set to true
        if "arms::ASYNC" in flags:
            self.async_flag.set(True)
            self.async_checkbox.select()

        # create relative flag variable and checkbutton
        self.relative_flag = tk.BooleanVar()
        self.relative_checkbox = tk.Checkbutton(self.frame, text="RELATIVE", variable=self.relative_flag, onvalue=True, offvalue=False, command=self.set_flags)
        self.relative_checkbox.grid(row=1, column=1, columnspan=1)

        # if imported movement has relative flag, set to true
        if "arms::RELATIVE" in flags:
            self.relative_flag.set(True)
            self.relative_checkbox.select()

        # create backwards flag variable and checkbutton
        self.backwards_flag = tk.BooleanVar()
        self.backwards_checkbox = tk.Checkbutton(self.frame, text="BACKWARDS", variable=self.backwards_flag, onvalue=True, offvalue=False, command=self.set_flags)
        self.backwards_checkbox.grid(row=1, column=2, columnspan=1)

        # if imported movement has backwards flag, set to true
        if "arms::BACKWARDS" in flags:
            self.backwards_flag.set(True)
            self.backwards_checkbox.select()

        # create thru flag variable and checkbutton
        self.thru_flag = tk.BooleanVar()
        self.thru_checkbox = tk.Checkbutton(self.frame, text="THRU", variable=self.thru_flag, onvalue=True, offvalue=False, command=self.set_flags)
        self.thru_checkbox.grid(row=1, column=3, columnspan=1)

        # if imported movement has thru flag, set to true
        if "arms::THRU" in flags:
            self.thru_flag.set(True)
            self.thru_checkbox.select()

        # adjust theme at start
        self.adjust_theme()

        # pack frame
        self.frame.pack(side=tk.TOP)

        # bind mouse input to click_handler callback
        self.txt.bind("<Button-1>", self.click_handler)

    def click_handler(self, event):
        # if LMB click
        if event.num == 1:
            # if selected, then deselect
            if self.selected:
                self.owner.switch_selection(-1)
            else:
                self.owner.switch_selection(self.index)
    
    # set movement flags to stored flag variable values
    def set_flags(self):
        self.movement.options["flags"]["arms::ASYNC"] = self.async_flag.get()
        self.movement.options["flags"]["arms::RELATIVE"] = self.relative_flag.get()
        self.movement.options["flags"]["arms::BACKWARDS"] = self.backwards_flag.get()
        self.movement.options["flags"]["arms::THRU"] = self.thru_flag.get()
    
    # select sidebar and movement
    def select(self):
        self.selected = True
        self.txt.configure(fg=SELECTED_COLOR)

        # toggle movement selected value and redraw movement
        self.movement.selected = True
        self.movement.clear(self.owner.canvas)
        self.movement.draw(self.owner.canvas)

    # deselect sidebar and movement
    def deselect(self):
        self.selected = False
        self.txt.configure(fg=DARK_MODE_FG if self.owner.darkmode.get() else LIGHT_MODE_FG)

        # toggle movement selected value and redraw movement
        self.movement.selected = False
        self.movement.clear(self.owner.canvas)
        self.movement.draw(self.owner.canvas)
    
    # adjust dark mode vs light mode
    def adjust_theme(self):
        if self.owner.darkmode.get():
            self.frame.configure(bg=DARK_MODE_BG)
            self.txt.configure(bg=DARK_MODE_BG)
            self.txt.configure(fg=SELECTED_COLOR if self.selected else DARK_MODE_FG)
            self.speed_txt.configure(bg=DARK_MODE_BG)
            self.speed_txt.configure(fg=DARK_MODE_FG)
            self.slider.configure(bg=DARK_MODE_BG)
            self.slider.configure(fg=DARK_MODE_FG)
            self.async_checkbox.configure(bg=DARK_MODE_BG)
            self.async_checkbox.configure(fg=DARK_MODE_FG)
            self.async_checkbox.configure(selectcolor=DARK_MODE_BG)
            self.async_checkbox.configure(activebackground=DARK_MODE_BG)
            self.relative_checkbox.configure(bg=DARK_MODE_BG)
            self.relative_checkbox.configure(fg=DARK_MODE_FG)
            self.relative_checkbox.configure(selectcolor=DARK_MODE_BG)
            self.relative_checkbox.configure(activebackground=DARK_MODE_BG)
            self.backwards_checkbox.configure(bg=DARK_MODE_BG)
            self.backwards_checkbox.configure(fg=DARK_MODE_FG)
            self.backwards_checkbox.configure(selectcolor=DARK_MODE_BG)
            self.backwards_checkbox.configure(activebackground=DARK_MODE_BG)
            self.thru_checkbox.configure(bg=DARK_MODE_BG)
            self.thru_checkbox.configure(fg=DARK_MODE_FG)
            self.thru_checkbox.configure(selectcolor=DARK_MODE_BG)
            self.thru_checkbox.configure(activebackground=DARK_MODE_BG)
        else:
            self.frame.configure(bg=LIGHT_MODE_BG)
            self.txt.configure(bg=LIGHT_MODE_BG)
            self.txt.configure(fg=SELECTED_COLOR if self.selected else LIGHT_MODE_FG)
            self.speed_txt.configure(bg=LIGHT_MODE_BG)
            self.speed_txt.configure(fg=LIGHT_MODE_FG)
            self.slider.configure(bg=LIGHT_MODE_BG)
            self.slider.configure(fg=LIGHT_MODE_FG)
            self.async_checkbox.configure(bg=LIGHT_MODE_BG)
            self.async_checkbox.configure(fg=LIGHT_MODE_FG)
            self.async_checkbox.configure(selectcolor=LIGHT_MODE_BG)
            self.async_checkbox.configure(activebackground=LIGHT_MODE_BG)
            self.relative_checkbox.configure(bg=LIGHT_MODE_BG)
            self.relative_checkbox.configure(fg=LIGHT_MODE_FG)
            self.relative_checkbox.configure(selectcolor=LIGHT_MODE_BG)
            self.relative_checkbox.configure(activebackground=LIGHT_MODE_BG)
            self.backwards_checkbox.configure(bg=LIGHT_MODE_BG)
            self.backwards_checkbox.configure(fg=LIGHT_MODE_FG)
            self.backwards_checkbox.configure(selectcolor=LIGHT_MODE_BG)
            self.backwards_checkbox.configure(activebackground=LIGHT_MODE_BG)
            self.thru_checkbox.configure(bg=LIGHT_MODE_BG)
            self.thru_checkbox.configure(fg=LIGHT_MODE_FG)
            self.thru_checkbox.configure(selectcolor=LIGHT_MODE_BG)
            self.thru_checkbox.configure(activebackground=LIGHT_MODE_BG)