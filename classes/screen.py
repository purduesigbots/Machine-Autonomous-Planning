from turtle import window_height
import pygame as pg

width = 1000
height = 600

class Screen:
    pg.init()

    def __init__(self, dark=False):
        self.movements = []
        self.sidebar_start = 0
        self.window = pg.display.set_mode((width,height))
        self.width = width
        self.height = height
        self.field_width = self.height
        self.dark = dark
        self.movement_settings_display = None
        self.lines = (50, 50, 50) if dark else (180, 180, 180)
        self.bg = (15, 15, 15) if dark else (235, 235, 235)
        self.tc = (70, 70, 70) if dark else (180, 180, 180)
        self.update(50)

    def draw_settings(self):
        if self.movement_settings_display == None:
            return
        self.movements[self.movement_settings_display].show_settings(
            self.window, (self.field_width/6, self.height/6))

    def draw_background(self):
        self.window.fill(self.bg)
        bg_image = pg.image.load('assets/field.png')
        bg_image = pg.transform.scale(bg_image, (self.height, self.height))
        self.window.blit(bg_image, bg_image.get_rect())
        split_height = self.height/6
        for i in range(6):
            sh = i*split_height
            pg.draw.line(self.window, self.lines, (sh, 0), (sh, self.height))
            pg.draw.line(self.window, self.lines, (0, sh), (self.height, sh))
        pg.draw.line(self.window, self.lines, (self.height, 0),
                     (self.height, self.height), 3)

    def update(self, dt):
        self.draw_background()

        l = len(self.movements)
        for m in range(l):
            self.movements[m].draw_arrow(self.window)
        for m in range(l if l < 12 else 12):
            self.movements[m+self.sidebar_start].draw_sidebar(
                self.window, (self.field_width, m*self.height/12))
        self.draw_settings()
        pg.time.delay(dt)
        pg.display.update()

    def move_sidebar(self, direction):
        self.sidebar_start += direction
        self.sidebar_start = 0 if self.sidebar_start < 0 else self.sidebar_start
        self.sidebar_start = len(
            self.movements)-12 if self.sidebar_start > len(self.movements)-12 else self.sidebar_start

    def check_clicks(self, pos):
        sidebar_clicks = []
        for m in self.movements:
            if m.toggle_settings(pos):
                sidebar_clicks.append(int(m.name.split(" ")[1])-1)
            m.update(color=(50, 200, 50))
        clicked = max(sidebar_clicks) if len(sidebar_clicks) > 0 else None
        if not clicked == None:
            self.movement_settings_display = clicked if not self.movement_settings_display == clicked else None
        if not self.movement_settings_display == None:
            self.movements[self.movement_settings_display].update(
                color=(35, 100, 35))
            self.movements[self.movement_settings_display].show_settings(
                self.window, (self.field_width/6, self.height/6))

    def add_move(self, m):
        m.update(bg=self.bg, tc=self.tc)
        self.movements.append(m)

    def edit_move(self, new_move, i=None):
        i = len(self.movements)-1 if not i else i
        new_move.update(bg=self.bg, tc=self.tc)
        self.movements[i] = new_move

    def remove_move(self, i=None):
        i = len(self.movements)-1 if not i else i
        try:
            del self.movements[i]
        except:
            pass

    def reset(self):
        self.__init__(size=(self.width, self.height), dark=self.dark)
