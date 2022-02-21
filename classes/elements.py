import pygame as pg
import math as m

class Ring(pg.sprite.Sprite):
    def __init__(self, p, r=6):
        super().__init__()
        self.pos = p
        self.original_image = pg.Surface((r*2,r*2), pg.SRCALPHA)
        pg.draw.circle(self.original_image, (80,0,20), (r,r), r, int(r/2))
        self.image = self.original_image

class Platform(pg.sprite.Sprite):
    def __init__(self, p, size, width=5):
        super().__init__()
        self.pos = p
        self.original_image = pg.Surface(size, pg.SRCALPHA)
        pg.draw.rect(self.original_image, (180, 0, 0), (0, 0, size[0], size[1]), width)
        self.image=self.original_image

class Goal(pg.sprite.Sprite):
    def __init__(self, p, radius, color, n_branches):
        super().__init__()
        size = [radius*2, radius*2]
        self.pos = p
        self.color = color
        self.original_image = pg.Surface(size, pg.SRCALPHA)
        pg.draw.polygon(self.original_image, self.color, [
            (size[0]/2 + size[0]/2 * m.cos(2 * m.pi * i / 7), size[0]/2 +size[0]/2 * m.sin(2 * m.pi * i / 7))
            for i in range(7)
        ])
        width=5
        if n_branches > 0:
            pg.draw.line(self.original_image, (130,130,130), (0+width,size[1]/2),(size[0]-width, size[1]/2) , width)
        if n_branches > 1:
            pg.draw.line(self.original_image, (130,130,130), (size[0]/2,0+width),(size[0]/2, size[1]-width) , width)
        pg.draw.circle(self.original_image, (50,50,50), (size[0]/2, size[1]/2), 3)

        self.image = self.original_image

