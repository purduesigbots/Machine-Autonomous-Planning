# import statements
from classes.movement import Movement, SidebarGroup
from classes.converter import Converter as c
from classes.constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE
import tkinter as tk
from tkinter import ttk
import sys
import os
from math import fmod

# Window class encapsulates main logic
class Window:

    def __init__(self, root, canvas):
        # initialize variables
        self.creating_movement = False
        self.start_point = (0, 0)
        self.end_point = (0, 0)
        self.root = root
        self.canvas = canvas
        self.temp_line = None
        self.movements = []
        self.sidebar_groups = []

        # create scrollable canvas for sidebar
        self.sidebar_canvas = tk.Canvas(root, width=SCREEN_WIDTH-SCREEN_HEIGHT, height=SCREEN_HEIGHT)
        v = ttk.Scrollbar(self.root, orient="vertical", command=self.sidebar_canvas.yview)
        self.sidebar = tk.Frame(self.sidebar_canvas, width=SCREEN_WIDTH-SCREEN_HEIGHT, height=SCREEN_HEIGHT)
        self.sidebar.bind("<Configure>", lambda e: self.sidebar_canvas.configure(
            scrollregion=self.sidebar_canvas.bbox("all")
        ))
        self.sidebar_canvas.create_window((0, 0), anchor=tk.NW, window=self.sidebar)
        self.sidebar_canvas.configure(yscrollcommand=v.set)

        self.sidebar_canvas.place(anchor=tk.NW, x=SCREEN_HEIGHT, y=0)
        v.pack(side="right", fill="y")

        # create variable to store which sidebar is selected at a time
        self.sidebar_selection_index = -1

        # create top menu bar
        mainmenu = tk.Menu(self.root, tearoff=False)

        # create file submenu
        file = tk.Menu(self.root, tearoff=False)

        # add import, export, clear
        file.add_command(label = "Import", command=self.import_script)
        file.add_command(label = "Export", command=self.export_script)
        file.add_command(label = "Clear", command= self.clear)

        # attach file submenu to main menu bar
        mainmenu.add_cascade(label = "File", menu=file)

        # create settings submenu
        settings = tk.Menu(self.root, tearoff=False)

        # add dark mode checkbutton
        self.darkmode = tk.BooleanVar()
        self.darkmode.set(True)
        settings.add_checkbutton(label="Dark Mode", onvalue=True, offvalue=False, variable=self.darkmode, state=tk.ACTIVE, command=self.set_darkmode)
        self.set_darkmode()

        # add toggle grid checkbutton
        self.grid = tk.BooleanVar()
        settings.add_checkbutton(label="Snap to Grid", onvalue=True, offvalue=False, variable=self.grid, command=self.set_grid)
        self.gridlines = []

        # attach settings submenu to main menu
        mainmenu.add_cascade(label = "Settings", menu=settings)

        # add exit to main menu
        mainmenu.add_command(label = "Exit", command= root.destroy)

        # attach main menu bar to root
        self.root.config(menu=mainmenu)

        # bind keyboard input to key_handler callback
        self.root.bind("<Key>", self.key_handler)
        # bind mouse button input to click_handler callback
        self.canvas.bind("<Button>", self.click_handler)
        # bind mouse motion input to motion_handler callback
        self.canvas.bind("<Motion>", self.motion_handler)
    
    # configure screen to use darkmode
    def set_darkmode(self):
        if self.darkmode.get():
            self.sidebar.configure(bg="black")
            self.sidebar_canvas.configure(bg="black")

            for s in self.sidebar_groups:
                s.adjust_theme()
        else:
            self.sidebar.configure(bg="white")
            self.sidebar_canvas.configure(bg="white")

            for s in self.sidebar_groups:
                s.adjust_theme()
    
    # display grid and force snap to grid
    def set_grid(self):
        if self.grid.get():
            n = SCREEN_HEIGHT / 6.0 / 24.0 * GRID_SIZE
            while n < SCREEN_HEIGHT:
                line1 = self.canvas.create_line(n, 0, n, SCREEN_HEIGHT, fill="#404040")
                line2 = self.canvas.create_line(0, n, SCREEN_HEIGHT, n, fill="#404040")
                self.gridlines.append(line1)
                self.gridlines.append(line2)
                n += SCREEN_HEIGHT / 6.0 / 24.0 * GRID_SIZE
        else:
            for g in self.gridlines:
                self.canvas.delete(g)
            self.gridlines.clear()

    # switch which sidebar group is selected
    def switch_selection(self, new_index):
        # if the current selected index exists, then deselect it
        if self.sidebar_selection_index != -1:
            self.sidebar_groups[self.sidebar_selection_index].deselect()
        
        # if the new index exists, then select it
        if new_index != -1:
            self.sidebar_groups[new_index].select()
        
        # replace the selected index
        self.sidebar_selection_index = new_index

    def key_handler(self, event):
        # if escape is hit, cancel the current movement
        if self.creating_movement and event.keysym == "Escape":
            self.creating_movement = False
            self.canvas.delete(self.temp_line)
            self.start_point = (0, 0)
            self.end_point = (0, 0)

    # mouse click input handler
    def click_handler(self, event):
        # if mouse click is on field
        if event.x < SCREEN_HEIGHT:

            # access x and y values
            x = event.x
            y = event.y

            # snap to grid functionality
            if self.grid.get():
                # find grid square size in pizels
                g = SCREEN_HEIGHT / 6 / 24 * GRID_SIZE
                print("g", g)

                # find position in interval and round to nearest grid point
                x_mod = fmod(x, g)
                print("x_mod", x_mod)
                if x_mod >= g / 2:
                    x = x - x_mod + g
                else:
                    x = x - x_mod
                print("x", x)

                y_mod = fmod(y, g)
                print("y_mod", y_mod)
                if y_mod >= g / 2:
                    y = y - y_mod + g
                else:
                    y = y - y_mod
                print("y", y)

            # if this is first click
            if not self.creating_movement:
                # set creating movement to true and store starting point
                self.creating_movement = True
                self.start_point = (x, y)
            # if not first click
            else:
                # set creating movement to false and store end point
                self.end_point = (x, y)

                # create line between start and end point
                line_ref = self.canvas.create_line(self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1], 
                                     fill="lime", width=5, arrow=tk.LAST, arrowshape=(8, 10, 8))
                
                m = Movement(self.start_point, self.end_point, line_ref, name="Movement {}".format(len(self.movements) + 1))
                s = SidebarGroup(m, self, len(self.sidebar_groups))

                self.movements.append(m)
                self.sidebar_groups.append(s)
                
                self.start_point = self.end_point
        # if mouse click is not on field
        else:
            print("Outside field")

    # mouse motion inpute handler
    def motion_handler(self, event):
        # if currently drawing a line
        if self.creating_movement:
            # delete the current temp line
            self.canvas.delete(self.temp_line)

            # create a new temp line between start point and current mouse position
            self.temp_line = self.canvas.create_line(self.start_point[0], self.start_point[1], event.x, event.y, 
                                               fill="lime", width=5, arrow=tk.LAST, arrowshape=(8, 10, 8))

    # Export path as cpp script
    def export_script(self):
        if not os.path.exists("output"):
            os.mkdir("output")
        f = open("output/script.cpp", "w")
        if(len(self.movements) > 0):
            f.write("// Reset odom\n")
            f.write(
                f'odom::reset({{{c.convert_x(self.movements[0].start[0])}, {c.convert_y(self.movements[0].start[1])}}});\n')
            f.write("\n")
        for m in self.movements:
            f.write(m.get_name_as_cmt())
            f.write(m.to_string())
            f.write("\n")
        f.close()
    
    # clear the field
    def clear(self):
        # clear all movements
        for m in self.movements:
            self.canvas.delete(m.line_ref)
        self.movements = []

        # clear out the sidebar canvas and recreate the scrollable frame
        self.sidebar_canvas.delete("all")
        self.sidebar = tk.Frame(self.sidebar_canvas, width=SCREEN_WIDTH-SCREEN_HEIGHT, height=SCREEN_HEIGHT)
        self.sidebar.bind("<Configure>", lambda e: self.sidebar_canvas.configure(
            scrollregion=self.sidebar_canvas.bbox("all")
        ))
        self.sidebar_canvas.create_window((0, 0), anchor=tk.NW, window=self.sidebar)

        # clear sidebar_groups vector
        self.sidebar_groups.clear()

        # set dark mode
        self.set_darkmode()

    def import_script(self):
        self.clear()

        # Check if the script.cpp file exists
        if not os.path.isfile(os.path.join("output","script.cpp")):
            try:
                os.mkdir("output")
            except:
                pass
            print("Please put script.cpp into the output directory")
            sys.exit()

        # Open the script
        f = open("output/script.cpp","r")

        start = None # Starting point based on odom::reset
        allLines = f.readlines() # Read the script

        for l in allLines:
            if "odom::reset" in l and start == None:
                # Get the start position with string indexing

                # Remove whitespace and get values between curly brackets
                data = "".join(l[l.index("{") : l.index("}")].split())[1:]
                dsplit = data.split(",")

                # Get start position
                start = (
                    c.convert_x_reverse(float(dsplit[0])), 
                    c.convert_y_reverse(float(dsplit[1]))
                )

            elif "chassis::move" in l:
                # Remove whitespace and get values between parenthesis
                data = "".join(l[l.index("(") : l.index(")")].split())

                # Get endpoint data of odom movement
                pos = data[data.index("{")+1 : data.index("}")].split(",")

                # Remove endpoint part from 'data'
                data = data[data.index("},")+2:]

                # Set the endpoint
                endpoint = (
                    c.convert_x_reverse(float(pos[0])), 
                    c.convert_y_reverse(float(pos[1]))
                )


                speed = 0

                # Check if there are any flags before fetching speed value
                if "," in data:

                    # Get the speed value and remove it from 'data'
                    speed = float(data[:data.index(",")])
                    data = data[data.index(",")+1:]
                else:
                    # Get the speed value and clear data
                    speed = float(data)
                    data = ""

                '''
                Create a new Movement based on:
                - Current number of movements
                - determined endpoint
                - determined startpoint
                - previous movement
                '''
                line_ref = self.canvas.create_line(start[0], start[1], endpoint[0], endpoint[1], 
                                     fill="lime", width=5, arrow=tk.LAST, arrowshape=(8, 10, 8))
                
                themove = Movement(start, self.end_point, line_ref, name = "Movement " + str(len(self.movements)+1))
                s = SidebarGroup(themove, self, len(self.sidebar_groups), speed=speed, flags=data)

                # Set the movements speed to the parsed speed
                themove.options["speed"] = speed

                # Set the movement's flags to the parsed flags
                for k in themove.options["flags"].keys():
                    if k in data:
                        themove.options["flags"][k] = True
                
                # Add the movement to our list of moves
                self.movements.append(themove)

                # Add the sidebar group to the list
                self.sidebar_groups.append(s)

                # Reset start to endpoint to chain movements
                start = endpoint

        