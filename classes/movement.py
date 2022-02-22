import pygame as pg
import math as m
from classes.coordinates import *


class Arrow(pg.sprite.Sprite):
    def __init__(self, start, endpoint, color):
        super().__init__()
        self.original_image = pg.Surface(
            (abs(endpoint[0]-start[0]), abs(endpoint[1]-start[1])), pg.SRCALPHA)
        self.color = color
        self.start = start
        self.endpoint = endpoint
        self.coordinates = [endpoint]
        self.clicked = False
        self.set_coordinates()

    def set_coordinates(self):
        '''
        Not proud of this code but it works

        Calculates the coordinates of the 3 points that makeup the
        the arrow based on which direction the movement goes in

        Math can probably be simplified but it works
        '''

        arr_t = 30  # Arrow's angle with the line
        arr_l = 20
        dx = self.endpoint[0] - self.start[0]
        dy = self.endpoint[1] - self.start[1]
        arr_t *= m.pi/180  # degrees to radians
        theta = m.pi/2 if not (dx == 0 and dy >= 0) else 3*m.pi/2
        try:
            theta = m.atan(dy/dx)
        except:
            a = 1  # Do nothing
            del a

        at1 = theta+arr_t
        at2 = theta-arr_t
        arrx = self.endpoint[0] - (1 if dx > 0 else -1)*arr_l * m.cos(at1)
        arry = self.endpoint[1] - (1 if dx > 0 else -1)*arr_l * m.sin(at1)
        arrx2 = self.endpoint[0] - (1 if dx > 0 else -1)*arr_l * m.cos(at2)
        arry2 = self.endpoint[1] - (1 if dx > 0 else -1)*arr_l * m.sin(at2)
        self.coordinates.append((arrx, arry))
        self.coordinates.append((arrx2, arry2))

    def draw(self, w):
        pg.draw.line(w, self.color, self.start, self.endpoint, 3)
        pg.draw.polygon(w, self.color, self.coordinates)


class Settings(pg.sprite.Sprite):
    def __init__(self, bg, tc, parent):
        super().__init__()
        self.parent = parent
        self.tc = tc
        self.bg = bg
        self.original_image = pg.Surface((400, 400), pg.SRCALPHA)
        self.rect = pg.Rect(350, 0, 50, 50)
        pg.draw.rect(self.original_image, bg, (0, 0, 400, 400))
        pg.draw.rect(self.original_image, tc, (0, 0, 400, 400), 5)
        pg.draw.rect(self.original_image, tc, self.rect, 5)
        self.original_image.blit(parent.sidebar.displayText, (15, 15))
        self.original_image.blit(parent.sidebar.posi, (15, 100))
        self.original_image.blit(parent.sidebar.posf, (15, 125))
        self.displaying = True
        self.image = self.original_image

    def show(self, w, pos):
        if self.displaying:
            w.blit(self.image, pos)

    def close(self, pos):
        return self.rect.collidepoint(pos)


class Sidebar(pg.sprite.Sprite):
    def __init__(self, name, start, endpoint, tc=(0, 0, 0)):
        self.name = name
        self.tc = tc
        self.start = start
        self.endpoint = endpoint
        self.width = 400
        self.height = 51
        self.original_image = pg.Surface(
            (self.width, self.height), pg.SRCALPHA)
        self.textfont = pg.font.SysFont("arial", 30)
        self.posfont = pg.font.SysFont("arial", 15)
        self.clicked = False
        self.set_text()

    def set_text(self):
        self.displayText = self.textfont.render(self.name, False, self.tc)
        self.posi = self.posfont.render(
            f'From: ({convert_x(self.start[0])} , {convert_y(self.start[1])})', False, self.tc)
        self.posf = self.posfont.render(
            f'To: ({convert_x(self.endpoint[0])} , {convert_y(self.endpoint[1])})', False, self.tc)
        self.original_image.blit(self.displayText, (10, 5))
        self.original_image.blit(self.posi, (220, 5))
        self.original_image.blit(self.posf, (240, 25))
        pg.draw.line(self.original_image, self.tc,
                     (0, self.height), (self.width, self.height), 4)
        self.image = self.original_image

    def draw(self, w, pos):
        w.blit(self.image, pos)
        self.rect = self.image.get_rect(
            center=(pos[0]+self.width/2, pos[1]+self.height/2))

    def collides(self, point):
        try:
            return True if self.rect.collidepoint(point) else False
        except:
            return False


class Movement():
    def __init__(self, name="Movement", move_type='drive', color=(50, 200, 50), tc=(0, 0, 0), bg=(0, 0, 0), prev=None, endpoint=(0, 0), start=None):
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
                "async": False,
                "absolute": False,
                "thru": False,
                "reverse": False,
            }
        }
        self.arrow = Arrow(self.start, self.endpoint, self.color)
        self.sidebar = Sidebar(self.name, self.start, self.endpoint)
        self.settings = Settings(self.bg, self.tc, self)

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

    def update_classes(self):
        self.arrow = Arrow(self.start, self.endpoint, self.color)
        self.sidebar = Sidebar(self.name, self.start, self.endpoint, self.tc)
        self.settings = Settings(self.bg, self.tc, self)

    def set_endpoint(self, p):
        self.endpoint = p
        self.arrow = Arrow(self.start, self.endpoint, self.color)
        self.sidebar = Sidebar(self.name, self.start, self.endpoint)
        self.settings = Settings(self.bg, self.tc, self)

    def is_clicked(self, pos):
        if self.sidebar.collides(pos):
            return True

    def toggle_settings(self, pos):
        self.sidebar.displaying = self.sidebar.collides(
            pos) or self.settings.close(pos)
        return self.sidebar.displaying

    def draw_arrow(self, w):
        self.arrow.draw(w)

    def draw_sidebar(self, w, p):
        self.sidebar.draw(w, p)

    def set_sidebar_color(self, bg, tc):
        self.tc = tc
        self.bg = bg
        self.sidebar = Sidebar(self.name, self.start, self.endpoint, tc)
        self.settings = Settings(self.bg, self.tc, self)

    def show_settings(self, w, pos):
        self.settings.show(w, pos)
