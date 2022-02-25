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

    def draw_arrows(self):
        for m in self.movements:
            m.draw_arrow(self.window)

    def draw_sidebar(self):
        self.visible_sidebars = []
        drawn_height = 0
        for m in range(self.sidebar_start, len(self.movements)):
            if drawn_height >= self.height:
                break
            self.visible_sidebars.append(self.movements[m])
            drawn_height += self.movements[m].draw_sidebar(
                self.window, (self.field_width, drawn_height)
            )
        
    def update(self, dt):
        self.draw_background()
        self.draw_arrows()
        self.draw_sidebar()
        pg.time.delay(dt)
        pg.display.update()

    def move_sidebar(self, direction):
        new_start = self.sidebar_start + direction
        if new_start >= 0 and new_start < len(self.movements):
            self.sidebar_start = new_start

    def sidebar_clicks(self, pos):
        for m in self.visible_sidebars:
            m.set_arrow_color((50, 200, 50))
            if m.sidebar_clicked(pos):
                m.set_arrow_color((35, 100, 35))
                
    def slider_drag(self, pos):
        for m in self.visible_sidebars:
            if m.sidebar.display_settings:
                m.sidebar.settings.check_slider_slide(pos)

    def add_move(self, m):
        m.update(bg=self.bg, tc=self.tc)
        self.movements.append(m)

    def edit_move(self, new_move, i=None):
        if not len(self.movements):
            return
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
        self.__init__(dark=self.dark)
