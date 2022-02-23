from classes.screen import Screen
from classes.movement import Movement
from classes.parser import Parser
import pygame as pg

'''
KEYBINDS FOR CERTAIN ACTIONS
'''
NEW_MOVEMENT = pg.K_m  # Press M to make a new line
CANCEL_MOVEMENT = pg.K_ESCAPE  # Press escape to cancel a line placement
SIDEBAR_DOWN = pg.K_DOWN
SIDEBAR_UP = pg.K_UP
RESET = pg.K_r
EXPORT = pg.K_e  # press e to export the script

selected = None
use_dark_mode = False

s = Screen(dark=use_dark_mode)
prevclick = False

while True:
    # Get mouse event informtion (clicked and position)
    clicked = pg.mouse.get_pressed()[0]
    pos = pg.mouse.get_pos()

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == RESET:
                s.reset()
            if not selected and event.key == NEW_MOVEMENT:
                selected = Movement(
                    name=f'Movement {len(s.movements)+1}',
                    prev=(s.movements[len(s.movements)-1]
                          if len(s.movements) else Movement(endpoint=pos))
                )
                selected.update(endpoint=pos)
                s.add_move(selected)
            elif selected and event.key == NEW_MOVEMENT:
                selected = None
            elif selected and event.key == CANCEL_MOVEMENT:
                selected = None
                s.remove_move()

            if event.key == SIDEBAR_DOWN:
                s.move_sidebar(1)
            elif event.key == SIDEBAR_UP:
                s.move_sidebar(-1)

            if event.key == EXPORT:
                Parser(s.movements).export_script()
        elif event.type == pg.QUIT:
            pg.quit()
            exit()

        if selected:
            if pos[0] <= s.field_width:
                selected.update(endpoint=pos, bg=s.bg, tc=s.tc)
                s.edit_move(selected)
        if clicked and not prevclick:
            if pos[0] > s.field_width:
                if selected:
                    s.remove_move()
                s.sidebar_clicks(pos)
            selected = None
        prevclick = clicked
    s.update(5)