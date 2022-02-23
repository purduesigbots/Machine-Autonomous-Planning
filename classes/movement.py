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
        self.arrow = Arrow(self.start, self.endpoint, self.color)
        self.sidebar = Sidebar(self)

    def update(self,  name=-333, move_type=-333, color=-333, tc=-333, bg=-333, prev=-333, endpoint=-333, start=-333):
        self.name = self.name if name == -333 else name
        self.type = self.type if move_type == -333 else move_type
        self.color = self.color if color == -333 else color
        self.tc = self.tc if tc == -333 else tc
        self.bg = self.bg if bg == -333 else bg
        self.prev = self.prev if prev == -333 else prev
        self.start = self.start if start == -333 else start
        self.endpoint = self.endpoint if endpoint == -333 else endpoint
        self.update_classes()

    def set_arrow_color(self, color):
        self.arrow.color = color

    def update_classes(self):
        self.arrow = Arrow(self.start, self.endpoint, self.color)
        self.sidebar = Sidebar(self)

    def set_endpoint(self, p):
        self.endpoint = p
        self.arrow = Arrow(self.start, self.endpoint, self.color)
        self.sidebar = Sidebar(self)

    def draw_arrow(self, w):
        self.arrow.draw(w)

    def draw_sidebar(self, w, p):
        return self.sidebar.draw(w, p)

    def sidebar_clicked(self, pos):
        if self.sidebar.collides(pos):
            self.sidebar.display_settings = not self.sidebar.display_settings
        return self.sidebar.display_settings

    def toString(self):
        joined_flags = " | ".join([f for f in self.options["flags"] if self.options["flags"][f]])
        return f'chassis::move({{{c.convert_x(self.endpoint[0])} , {c.convert_y(self.endpoint[1])}}}, {self.options["speed"]}{", " + joined_flags if len(joined_flags) > 0 else ""});\n'
