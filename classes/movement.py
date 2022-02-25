import pygame as pg
import math as m
import copy
from classes.movement_elements import Arrow, Sidebar
from classes.converter import Converter as c

'''
Movement Class:
    - Stores the properties of the movement
        - Start and endpoint
        - Speed
        - Flags
    - Stores arrow sprite to be drawn onto field
    - Stores sidebar sprite to be drawn onto sidebar
'''
class Movement():
    def __init__(self, name="Movement", move_type='drive', color=(50, 200, 50), tc=(0, 0, 0), bg=(0, 0, 0), prev=None, endpoint=(0, 0), start=None):
        '''
        Initialize the movement's values based on parameters
        '''
        self.name = name
        self.type = move_type
        self.color = color
        self.prev = prev
        self.tc = tc
        self.bg = bg
        self.start = prev.endpoint if prev else (start if start else (0, 600))
        self.angle_i = prev.angle_i if prev else 0
        self.endpoint = endpoint
        self.options = {
            "speed": 100,
            "flags": {
                "arms::ASYNC": False,
                "arms::ABSOLUTE": False,
                "arms::BACKWARDS": False,
                "arms::THRU": False,
            }
        }

        # Generate arrow with this movement's properties
        self.arrow = Arrow(self.start, self.endpoint, self.color)

        # Generate sidebar and pass ourself into it as its parent
        self.sidebar = Sidebar(self)

    def update(self,  name=-333, move_type=-333, color=-333, tc=-333, bg=-333, prev=-333, endpoint=-333, start=-333):
        # Screw this function, would love to use self.__init__ but it was messing some other things up
        # Lots of ternary to decide on updating each property or not
        self.name = self.name if name == -333 else name
        self.type = self.type if move_type == -333 else move_type
        self.color = self.color if color == -333 else color
        self.tc = self.tc if tc == -333 else tc
        self.bg = self.bg if bg == -333 else bg
        self.prev = self.prev if prev == -333 else prev
        self.start = self.start if start == -333 else start
        self.endpoint = self.endpoint if endpoint == -333 else endpoint
        # update our classes with the new properties
        self.update_classes()

    def set_arrow_color(self, color):
        # Set our arrow's drawn color to what we want it as
        self.arrow.color = color

    def update_classes(self):
        # Update our classes after something called this.update()
        self.arrow = Arrow(self.start, self.endpoint, self.color)
        self.sidebar = Sidebar(self)

    def set_endpoint(self, p):
        # Set our endpoint
        self.endpoint = p
        self.update_classes

    def draw_arrow(self, w):
        # draw our arrow onto the screen
        self.arrow.draw(w)

    def draw_sidebar(self, w, p):
        # Draw our sidebar onto the screen
        return self.sidebar.draw(w, p)

    def sidebar_clicked(self, pos):
        # Modify our sidebar and stuff if it was clicked
        if self.sidebar.collides(pos):
            self.sidebar.display_settings = not self.sidebar.display_settings
        return self.sidebar.display_settings
    
    def close_sidebar(self):
        # Close the sidebar
        self.sidebar.close_settings()


    def toString(self):
        # Convert our movement's endpoint into a string for the script
        joined_flags = " | ".join([f for f in self.options["flags"] if self.options["flags"][f]])
        return f'chassis::move({{{c.convert_x(self.endpoint[0])} , {c.convert_y(self.endpoint[1])}}}, {self.options["speed"]}{", " + joined_flags if len(joined_flags) > 0 else ""});\n'
