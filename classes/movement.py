import pygame as pg
import math as m
import copy
from classes.converter import Converter as c


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

class Slider(pg.sprite.Sprite):
    def __init__(self, size, center_line, color, position_percent):
        self.padding = size[0]/8
        self.color = color
        self.position = position_percent / 100 * (size[0]-2*self.padding) # 0 to 100 representing the current length of the slider
        self.value = self.position / (size[0]-2*self.padding) * 100
        self.center_line = center_line
        self.width = size[0]
        self.height = size[1]
        self.original_original_image = pg.Surface(size, pg.SRCALPHA)
        self.original_image = copy.copy(self.original_original_image)

    def set_image(self, pos=None):
        self.position = self.position if pos==None else pos - self.rel_x - self.padding
        self.value = self.position / (self.width -2*self.padding) * 100
        self.original_image = copy.copy(self.original_original_image)
        if self.center_line:
            pg.draw.line(self.original_image, self.color, (self.padding, self.height/2), (self.width-self.padding, self.height/2),1)
        else:
            pg.draw.rect(self.original_image, self.color, (0,0,self.width, self.height), 2)
        pg.draw.circle(self.original_image, self.color, (self.padding+self.position, self.height/2), self.height/2)
        self.image = self.original_image

    def draw(self, w, pos):
        w.blit(self.image, pos)
        self.rel_x = pos[0]
        self.rect = self.image.get_rect(
            center=(pos[0]+self.width/2, pos[1]+self.height/2)
        )

    def collides(self, pos):
        if self.rect.collidepoint(pos):
            if pos[0] < self.rel_x+self.padding:
                self.set_image(self.rel_x+self.padding)
            elif pos[0] > self.rel_x + self.width - self.padding:
                self.set_image(self.rel_x+self.width-self.padding)
            else:
                self.set_image(pos[0])

            print("collides")
            return True
        return False

class Button(pg.sprite.Sprite):
    def __init__(self, size, outline_color, background_color, selected_render, selected, name):
        self.oc = outline_color
        self.bg = background_color
        self.name = name
        self.width = size[0]
        self.height = size[1]
        self.selected = selected
        self.selected_render = selected_render
        self.original_image = pg.Surface(size, pg.SRCALPHA)
        
    def set_image(self, rel_pos):
        self.rel_pos = rel_pos
        pg.draw.rect(self.original_image, self.bg, (0,0, self.width, self.height))
        if self.selected:
            self.original_image.blit(self.selected_render, (8,0))
        pg.draw.rect(self.original_image, self.oc, (0,0,self.width, self.height), 2)
        self.image = self.original_image

    def draw(self, w, pos):
        w.blit(self.image, (pos[0]+self.rel_pos[0], pos[1]+self.rel_pos[1]))
        self.rect = self.image.get_rect(
            center=(
                pos[0]+self.rel_pos[0]+self.width/2, 
                pos[1]+self.rel_pos[1]+self.height/2
            )
        )

    def clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.selected = not self.selected
            return True
        return False
    
class Settings(pg.sprite.Sprite):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.tc = parent.tc
        self.bg = parent.bg
        self.width = 400
        self.height = 150
        self.original_image = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.rect = pg.Rect(350, 0, 50, 50)
        self.create_buttons()
        self.set_text()
        self.image = self.original_image
        
    def create_buttons(self):
        checked = self.parent.textfont.render("X", False, self.tc)
        self.async_button = Button((30,30), self.tc, self.bg, checked, self.parent.parent.options['flags']['arms::ASYNC'], 'async')
        self.thru_button = Button((30,30), self.tc, self.bg, checked, self.parent.parent.options['flags']['arms::THRU'], 'thru')
        self.backwards_button = Button((30,30), self.tc, self.bg, checked, self.parent.parent.options['flags']['arms::BACKWARDS'], 'back')
        self.absolute_button = Button((30,30), self.tc, self.bg, checked, self.parent.parent.options['flags']['arms::ABSOLUTE'], 'absolute')
        self.speed_slider = Slider((200,30), True, self.tc, self.parent.parent.options['speed'])

    def set_text(self):
        self.original_image = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.speed = self.parent.textfont.render(
            f'Speed: {self.parent.parent.options["speed"]}',
            False, self.tc
        )

        self.use_async = self.parent.textfont.render("ASYNC", False, self.tc)
        self.use_thru = self.parent.textfont.render("THRU", False, self.tc)
        self.use_absolute = self.parent.textfont.render("ABSOLUTE",False, self.tc)
        self.use_backwards = self.parent.textfont.render("BACKWARDS",False, self.tc)


        self.speed_slider.set_image()

        self.original_image.blit(self.speed, (self.speed_slider.width, 0))

        self.async_button.set_image((10,30))
        self.original_image.blit(self.use_async, (50, 30))

        self.thru_button.set_image((10,60))
        self.original_image.blit(self.use_thru, (50, 60))

        self.absolute_button.set_image((10,90))
        self.original_image.blit(self.use_absolute, (50, 90))

        self.backwards_button.set_image((10, 120))
        self.original_image.blit(self.use_backwards, (50, 120))

        self.image = self.original_image
        
    def update_settings(self):
        print("updated")
        print(self.speed_slider.value)
        self.parent.parent.options['speed'] = int(self.speed_slider.value)
        self.parent.parent.options['flags']['arms::ASYNC'] = self.async_button.selected
        self.parent.parent.options['flags']['arms::THRU'] = self.thru_button.selected
        self.parent.parent.options['flags']['arms::ABSOLUTE'] = self.absolute_button.selected
        self.parent.parent.options['flags']['arms::BACKWARDS'] = self.backwards_button.selected
        self.set_text()

    def check_button_presses(self,pos):
        buttons = [
            self.async_button,
            self.absolute_button,
            self.thru_button,
            self.backwards_button
        ]
        for b in buttons:
            if b.clicked(pos):
                b.set_image(b.rel_pos)
                self.update_settings()
                return True
        return False

    def check_slider_slide(self, pos):
        if self.speed_slider.collides(pos):
            self.update_settings()
            return True
        return False

    def draw(self, w, pos):
        w.blit(self.image, pos)
        self.async_button.draw(w, pos)
        self.thru_button.draw(w, pos)
        self.absolute_button.draw(w, pos)
        self.backwards_button.draw(w, pos)
        self.speed_slider.draw(w,pos)
        self.rect = self.image.get_rect(
            center=(pos[0]+self.width/2, pos[1]+self.height/2)
        )

    def close(self, pos):
        return self.rect.collidepoint(pos)

class Sidebar(pg.sprite.Sprite):
    def __init__(self, parent):
        self.parent = parent
        self.name = parent.name
        self.tc = parent.tc
        self.bg = parent.bg
        self.start = parent.start
        self.endpoint = parent.endpoint
        self.width = 400
        self.height = 50
        self.original_image = pg.Surface(
            (self.width, self.height), pg.SRCALPHA)
        self.textfont = pg.font.SysFont("arial", 30)
        self.posfont = pg.font.SysFont("arial", 15)
        self.clicked = False
        self.display_settings = False
        self.set_text()
        self.settings = Settings(self)

    def set_text(self):
        self.displayText = self.textfont.render(self.name, False, self.tc)
        self.posi = self.posfont.render(
            f'From: ({c.convert_x(self.start[0])} , {c.convert_y(self.start[1])})', False, self.tc)
        self.posf = self.posfont.render(
            f'To: ({c.convert_x(self.endpoint[0])} , {c.convert_y(self.endpoint[1])})', False, self.tc)
        self.original_image.blit(self.displayText, (10, 5))
        self.original_image.blit(self.posi, (220, 5))
        self.original_image.blit(self.posf, (240, 25))
        pg.draw.line(self.original_image, self.tc,
                     (0, 0), (self.width, 0), 4)
        self.image = self.original_image

    def draw(self, w, pos):
        w.blit(self.image, pos)
        toreturn = self.height
        self.rect = self.image.get_rect(
            center=(pos[0]+self.width/2, pos[1]+self.height/2))
        if self.display_settings:
            self.settings.draw(w, (pos[0], pos[1]+self.height))
            toreturn += self.settings.height
        return toreturn

    def collides(self, point):
        try:
            if self.display_settings:
                self.settings.check_button_presses(point)
                self.settings.check_slider_slide(point)
            if self.rect.collidepoint(point):
                return True
            return False
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

    def is_clicked(self, pos):
        if self.sidebar.collides(pos):
            return True

    def toggle_settings(self, pos):
        self.sidebar.displaying = self.sidebar.collides(
            pos)
        return self.sidebar.displaying

    def draw_arrow(self, w):
        self.arrow.draw(w)

    def draw_sidebar(self, w, p):
        return self.sidebar.draw(w, p)

    def set_sidebar_color(self, bg, tc):
        self.tc = tc
        self.bg = bg
        self.sidebar = Sidebar(self)

    def show_settings(self, w, pos):
        self.settings.show(w, pos)

    def sidebar_clicked(self, pos):
        if self.sidebar.collides(pos):
            self.sidebar.display_settings = not self.sidebar.display_settings
        return self.sidebar.display_settings

    def toString(self):
        joined_flags = " | ".join([f for f in self.options["flags"] if self.options["flags"][f]])
        return f'chassis::move({{{c.convert_x(self.endpoint[0])} , {c.convert_y(self.endpoint[1])}}}, {self.options["speed"]}{", " + joined_flags if len(joined_flags) > 0 else ""});\n'
