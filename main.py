from classes.screen import Screen
from classes.movement import Movement
import pygame as pg


NEW_MOVEMENT = pg.K_m # Press M to make a new line
CANCEL_MOVEMENT = pg.K_ESCAPE # Press escape to cancel a line placement

selected = None
use_dark_mode = False

dat = input("Input Start Point (Example: 450, 550) : ")
dat = dat.replace(" ","")
split = dat.split(",")
x = float(split[0])
y = float(split[1])
s = Screen(dark=use_dark_mode)
while True:
    pos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type==pg.KEYDOWN:
            if not selected and event.key == NEW_MOVEMENT:
                selected = Movement(
                    name = f'Movement {len(s.movements)+1}',
                    prev=(s.movements[len(s.movements)-1] if len(s.movements) else Movement(endpoint=(x,y)))
                    )
                selected.set_endpoint(pos)
                s.add_move(selected)
            elif selected and event.key == CANCEL_MOVEMENT:
                selected=None
                s.remove_move()
        if selected:
            if pos[0] <= s.field_width:
                selected.set_endpoint(pos)
                s.edit_move(selected)
        if pg.mouse.get_pressed()[0]:
            if pos[0] > s.field_width:
                if selected:
                    s.remove_move()
                print(pos)
                s.check_clicks(pos)
            selected=None

    s.update(5)
