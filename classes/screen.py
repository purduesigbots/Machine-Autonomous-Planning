# import statements
from classes.movement import Movement, SidebarGroup
from classes.converter import Converter as c
import tkinter as tk
from tkinter import ttk
import os

# constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

class Window:

    def __init__(self, root, canvas):
        self.creating_movement = False
        self.start_point = (0, 0)
        self.end_point = (0, 0)
        self.root = root
        self.canvas = canvas
        self.temp_line = None
        self.movements = []

        self.mainmenu = tk.Menu(self.root)
        self.mainmenu.add_command(label = "Import")
        self.mainmenu.add_command(label = "Export", command=self.export_script)
        self.mainmenu.add_command(label = "Clear", command= self.clear)
        self.mainmenu.add_command(label = "Exit", command= root.destroy)

        self.root.config(menu=self.mainmenu)

        self.sidebar_canvas = tk.Canvas(root, width=SCREEN_WIDTH-SCREEN_HEIGHT, height=SCREEN_HEIGHT)
        v = ttk.Scrollbar(self.root, orient="vertical", command=self.sidebar_canvas.yview)
        self.sidebar = ttk.Frame(self.sidebar_canvas, width=SCREEN_WIDTH-SCREEN_HEIGHT, height=SCREEN_HEIGHT)
        self.sidebar.bind("<Configure>", lambda e: self.sidebar_canvas.configure(
            scrollregion=self.sidebar_canvas.bbox("all")
        ))
        self.sidebar_canvas.create_window((0, 0), anchor=tk.NW, window=self.sidebar)
        self.sidebar_canvas.configure(yscrollcommand=v.set)

        self.sidebar_canvas.place(anchor=tk.NW, x=SCREEN_HEIGHT, y=0)
        v.pack(side="right", fill="y")

        # bind keyboard input to key_handler callback
        self.root.bind("<Key>", self.key_handler)
        # bind mouse button input to click_handler callback
        self.canvas.bind("<Button>", self.click_handler)
        # bind mouse motion input to motion_handler callback
        self.canvas.bind("<Motion>", self.motion_handler)

    def key_handler(self, event):
        if self.creating_movement and event.keysym == "Escape":
            self.creating_movement = False
            self.canvas.delete(self.temp_line)
            self.start_point = (0, 0)
            self.end_point = (0, 0)

    # mouse click input handler
    def click_handler(self, event):
        # if mouse click is on field
        if event.x < SCREEN_HEIGHT:
            # convert to inches on field
            # bottom left of field is (0, 0)
            field_x = event.x / SCREEN_HEIGHT * 24.0 * 6
            field_y = (600 - event.y) / SCREEN_HEIGHT * 24.0 * 6

            # if this is first click
            if not self.creating_movement:
                # set creating movement to true and store starting point
                self.creating_movement = True
                self.start_point = (event.x, event.y)
            # if not first click
            else:
                # set creating movement to false and store end point
                self.end_point = (event.x, event.y)

                # create line between start and end point
                line_ref = self.canvas.create_line(self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1], 
                                     fill="lime", width=5, arrow=tk.LAST, arrowshape=(8, 10, 8))
                
                m = Movement(self.start_point, self.end_point, line_ref, name="Movement {}".format(len(self.movements) + 1))
                s = SidebarGroup(m, self.sidebar, self.canvas)

                self.movements.append(m)
                
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
            f.write(
                f'odom::reset({{{c.convert_x(self.movements[0].start[0])}, {c.convert_y(self.movements[0].start[1])}}});\n')
        for m in self.movements:
            f.write(m.to_string())
        f.close()
    
    # clear the field
    def clear(self):
        for m in self.movements:
            self.canvas.delete(m.line_ref)
        self.movements = []

        self.sidebar_canvas.delete("all")
        self.sidebar = ttk.Frame(self.sidebar_canvas, width=SCREEN_WIDTH-SCREEN_HEIGHT, height=SCREEN_HEIGHT)
        self.sidebar.bind("<Configure>", lambda e: self.sidebar_canvas.configure(
            scrollregion=self.sidebar_canvas.bbox("all")
        ))
        self.sidebar_canvas.create_window((0, 0), anchor=tk.NW, window=self.sidebar)
