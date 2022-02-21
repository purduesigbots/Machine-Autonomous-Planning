import pygame as pg
from classes.elements import Ring, Platform, Goal

class Screen:
    pg.init()
    def __init__(self, size=(1000,600), dark=False):
        self.movements = []
        self.sidebar_start = 0
        self.window=pg.display.set_mode(size)
        self.width=size[0]
        self.height=size[1]
        self.field_width = self.height
        self.dark = dark
        self.movement_settings_display = None
        self.lines = (50,50,50) if dark else (180,180,180)
        self.bg = (15,15,15) if dark else (235,235,235)
        self.tc = (70,70,70) if dark else (180,180,180)
        self.update(50)

    '''
    This is just gonna be hardcoded elements placement to make the field look cleaner
    '''
    def draw_elements(self):
        ring_radius = 6
        goal_radius = 25

        rings = [
            Ring((50,50)),
            Ring((75,75)),
            Ring((100,100)),
            Ring((125,125)),
        ]

        goals = [
            Goal(
                (self.field_width/4- goal_radius,self.height/2- goal_radius), #Position
                goal_radius, #radius
                (246,190,0), #Color
                1 #Number of posts (0 for alliance, 1 for small neutral, 2 for tall neutral)
            ),
            Goal(
                (self.field_width/2 - goal_radius,self.height/2-goal_radius),
                goal_radius,
                (246,190,0),
                2
            ),
            Goal(
                (self.field_width*3/4 - goal_radius,self.height/2-goal_radius),
                goal_radius,
                (246,190,0),
                1
            ),
            Goal(
                (self.field_width/12 - goal_radius, self.height/4 -goal_radius),
                goal_radius,
                (25,25,220),
                0
            ),
            Goal(
                (self.field_width*11/12 - goal_radius, self.height*3/4 -goal_radius),
                goal_radius,
                (220,25,25),
                0
            ),
            Goal(
                (self.field_width/12 - goal_radius, self.height/4 -goal_radius),
                goal_radius,
                (25,25,220),
                0
            ),

        ]

        platforms = [
            Platform

        ]
        for g in goals:
            self.window.blit(g.image, g.pos)

        for r in rings:
            self.window.blit(r.image, r.pos)
        platform_width = 5
        pw = platform_width

        '''
        Red and Blue Platforms
        '''
        pg.draw.rect(self.window, (180, 0, 0), (self.field_width/3, 0, self.field_width/3, self.height/6))
        pg.draw.rect(self.window, self.bg, (self.field_width/3 + pw, pw, self.field_width/3 - 2*pw, self.height/6 - 2*pw))
        pg.draw.rect(self.window, (0, 0, 180), (self.field_width/3, self.height*5/6, self.field_width/3, self.height))
        pg.draw.rect(self.window, self.bg, (self.field_width/3 + pw, self.height*5/6+pw, self.field_width/3 - 2*pw, self.height/6 - 2*pw))

        '''
        RINGS
        '''
    def draw_settings(self):
        if self.movement_settings_display == None:
            return
        self.movements[self.movement_settings_display].show_settings(self.window, (self.field_width/6,self.height/6))

    def draw_background(self):
        self.window.fill(self.bg)
        split_height = self.height/6
        for i in range(6):
            sh = i*split_height
            pg.draw.line(self.window, self.lines, (sh,0), (sh,self.height))
            pg.draw.line(self.window, self.lines, (0,sh), (self.height,sh))
        pg.draw.line(self.window, self.lines, (self.height,0), (self.height,self.height),3)

    def update(self, dt):
        self.draw_background()
        self.draw_elements()

        l = len(self.movements)
        for m in range(l):
            self.movements[m].draw_arrow(self.window)
        for m in range(l if l<12 else 12):
            self.movements[m+self.sidebar_start].draw_sidebar(self.window, (self.field_width, m*self.height/12))
        self.draw_settings()
        pg.time.delay(dt)
        pg.display.update()

    def move_sidebar(self, direction):
        self.sidebar_start+=direction
        self.sidebar_start = 0 if self.sidebar_start < 0 else self.sidebar_start
        self.sidebar_start = len(self.movements)-12 if self.sidebar_start > len(self.movements)-12 else self.sidebar_start
        
    def check_clicks(self, pos):
        sidebar_clicks = []
        for m in self.movements:
            if m.is_clicked(pos):
                sidebar_clicks.append(int(m.name.split(" ")[1])-1)
        clicked = max(sidebar_clicks) if len(sidebar_clicks)>0 else None
        self.movement_settings_display = clicked if not self.movement_settings_display == clicked else None

    def add_move(self, m):
        m.set_sidebar_color(self.bg, self.tc)
        self.movements.append(m)

    def edit_move(self, new_move, i=None):
        i=len(self.movements)-1 if not i else i
        new_move.set_sidebar_color(self.bg, self.tc)
        self.movements[i]=new_move

    def remove_move(self, i=None):
        i=len(self.movements)-1 if not i else i
        del self.movements[i]

    def reset(self):
        self.__init__(size=(self.width,self.height),dark=self.dark)