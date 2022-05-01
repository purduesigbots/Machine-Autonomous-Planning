# import statements
from abc import abstractmethod
from classes.converter import Converter as c
from classes.constants import DARK_MODE_BG, DARK_MODE_FG, LIGHT_MODE_BG, LIGHT_MODE_FG, SELECTED_COLOR
import tkinter as tk
import math

# Movement class encapsulates code associated with linear movements
class Movement:

    def __init__(self, owner, index, name):
        # initialize variables
        self.owner = owner
        self.index = index
        self.name = name
        self.options = {
            "speed": 100,
            "flags": {
                "arms::ASYNC": False,
                "arms::RELATIVE": False,
                "arms::REVERSE": False,
                "arms::THRU": False,
            }
        }

        self.selected = False
    
    # handles mouse click input for movement
    @abstractmethod
    def click_handler(self, event):
        pass

    # clear arrow from canvas
    @abstractmethod
    def clear(self):
        pass

    # draw arrow on canvas
    @abstractmethod
    def draw(self):
        pass
    
    # set the speed to val
    def set_speed(self, val):
        self.options["speed"] = val
    
    # get name as comment
    def get_name_as_cmt(self):
        return f'// {self.name}\n'
    
    # get string for exporting to script
    @abstractmethod
    def to_string(self):
        pass

# Linear class encapsulates code associated specifically with linear movements
class Linear(Movement):

    def __init__(self, owner, index, name, start, end, line_ref):
        # call super
        super().__init__(owner, index, name)

        # initialize variables
        self.start = start
        self.end = end
        self.line_ref = line_ref

        # bind click handler to line_ref tag
        self.owner.canvas.tag_bind(self.line_ref, "<Button-1>", self.click_handler)
    
    # handles mouse click input for movement
    def click_handler(self, event):
        # if the movement is selected and the canvas is not editing
        if self.selected and self.owner.editing_movement == 0:
            # calculate distances from both end points
            dist_from_end = math.sqrt((self.end[0] - event.x) ** 2 + (self.end[1] - event.y) ** 2)
            dist_from_start = math.sqrt((self.start[0] - event.x) ** 2 + (self.start[1] - event.y) ** 2)
            
            # based on distances, switch to editing end or start
            if dist_from_end <= dist_from_start:
                self.owner.editing_movement = 2
            else:
                self.owner.editing_movement = -2

            # set index and clear current line
            self.owner.editing_index = self.index
            self.clear()

    # clear arrow from canvas
    def clear(self):
        self.owner.canvas.delete(self.line_ref)

    # draw arrow on canvas
    def draw(self):
        line_fill = "green" if self.selected else "lime"
        self.line_ref = self.owner.canvas.create_line(self.start[0], self.start[1], self.end[0], self.end[1], 
                                     fill=line_fill, width=5, arrow=tk.LAST, arrowshape=(8, 10, 8))
        
        # rebind click handler
        self.owner.canvas.tag_bind(self.line_ref, "<Button-1>", self.click_handler)
    
    # get string for exporting to script
    def to_string(self):
        joined_flags = " | ".join([f for f in self.options["flags"] if self.options["flags"][f]])
        return f'chassis::move({{{{{c.convert_x(self.end[0])}, {c.convert_y(self.end[1])}}}}}, {self.options["speed"]}{", " + joined_flags if len(joined_flags) > 0 else ""});\n'

# Linear class encapsulates code associated specifically with angular movements
class Angular(Movement):

    def __init__(self, owner, index, name, origin, start_angle, extent, line_ref):
        # call super
        super().__init__(owner, index, name)

        # initialize variables
        self.origin = origin
        self.start_angle = start_angle
        self.extent = extent
        self.line_ref = line_ref

        # bind click handler to line_ref tag
        self.owner.canvas.tag_bind(self.line_ref, "<Button-1>", self.click_handler)
    
    # handles mouse click input for movement
    def click_handler(self, event):
        # if the movement is selected and the canvas is not editing
        if self.selected and self.owner.editing_movement == 0:
            self.owner.editing_movement = 2

            # set index and clear current line
            self.owner.editing_index = self.index
            self.clear()

    # clear arrow from canvas
    def clear(self):
        self.owner.canvas.delete(self.line_ref)

    # draw arrow on canvas
    def draw(self):
        line_fill = "red" if self.selected else "magenta"
        self.line_ref = self.owner.canvas.create_arc(self.origin[0] - 20, self.origin[1] - 20, self.origin[0] + 20, self.origin[1] + 20,
                                     outline=line_fill, start=self.start_angle, extent=self.extent, width=5, style=tk.ARC)
        
        # rebind click handler
        self.owner.canvas.tag_bind(self.line_ref, "<Button-1>", self.click_handler)
    
    # get string for exporting to script
    def to_string(self):
        joined_flags = " | ".join([f for f in self.options["flags"] if self.options["flags"][f]])
        return f'chassis::turn({round(self.start_angle + self.extent, 2)}, {self.options["speed"]}{", " + joined_flags if len(joined_flags) > 0 else ""});\n'

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

        # create reverse flag variable and checkbutton
        self.reverse_flag = tk.BooleanVar()
        self.reverse_checkbox = tk.Checkbutton(self.frame, text="REVERSE", variable=self.reverse_flag, onvalue=True, offvalue=False, command=self.set_flags)
        self.reverse_checkbox.grid(row=1, column=2, columnspan=1)

        # if imported movement has reverse flag, set to true
        if "arms::REVERSE" in flags:
            self.reverse_flag.set(True)
            self.reverse_checkbox.select()

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

        # add delete button
        self.delete_button = tk.Button(self.frame, text="DELETE MOVEMENT", fg="red", command=self.destroy)

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
        self.movement.options["flags"]["arms::REVERSE"] = self.reverse_flag.get()
        self.movement.options["flags"]["arms::THRU"] = self.thru_flag.get()
    
    # select sidebar and movement
    def select(self):
        self.selected = True
        self.txt.configure(fg=SELECTED_COLOR)

        # add delete button
        self.delete_button = tk.Button(self.frame, text="DELETE MOVEMENT", fg="red", command=self.destroy)
        self.delete_button.grid(row=2, column=0, columnspan=4)

        # toggle movement selected value and redraw movement
        self.movement.selected = True
        self.movement.clear()
        self.movement.draw()

    # deselect sidebar and movement
    def deselect(self):
        self.selected = False
        self.txt.configure(fg=DARK_MODE_FG if self.owner.darkmode.get() else LIGHT_MODE_FG)

        self.delete_button.destroy()

        # toggle movement selected value and redraw movement
        self.movement.selected = False
        self.movement.clear()
        self.movement.draw()
    
    # delete self and corresponding movement and remove from Window
    def destroy(self):
        self.owner.remove_movement(self.movement)
        self.owner.remove_sidebar_group(self)
    
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
            self.reverse_checkbox.configure(bg=DARK_MODE_BG)
            self.reverse_checkbox.configure(fg=DARK_MODE_FG)
            self.reverse_checkbox.configure(selectcolor=DARK_MODE_BG)
            self.reverse_checkbox.configure(activebackground=DARK_MODE_BG)
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
            self.reverse_checkbox.configure(bg=LIGHT_MODE_BG)
            self.reverse_checkbox.configure(fg=LIGHT_MODE_FG)
            self.reverse_checkbox.configure(selectcolor=LIGHT_MODE_BG)
            self.reverse_checkbox.configure(activebackground=LIGHT_MODE_BG)
            self.thru_checkbox.configure(bg=LIGHT_MODE_BG)
            self.thru_checkbox.configure(fg=LIGHT_MODE_FG)
            self.thru_checkbox.configure(selectcolor=LIGHT_MODE_BG)
            self.thru_checkbox.configure(activebackground=LIGHT_MODE_BG)