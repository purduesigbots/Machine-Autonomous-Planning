from hashlib import new
from classes.screen import Screen
from classes.movement import Movement, Sidebar
from classes.parser import Parser
import pygame as pg


'''
Keybinds for various functions of program
'''

keybinds = {
    "NEW_MOVEMENT": pg.K_m,  # Press M to make a new line
    "CANCEL_MOVEMENT": pg.K_ESCAPE,  # Press escape to cancel a line placement
    "SIDEBAR_DOWN": pg.K_DOWN, # Press down to move down on the sidebar view
    "SIDEBAR_UP": pg.K_UP, # Press up to move up on the sidebar view
    "RESET": pg.K_r, # Press R to clear the screen of movements
    "EXPORT": pg.K_e,  # press e to export the script
    "IMPORT": pg.K_i
}
selected = None
use_dark_mode = False

s = Screen(dark=use_dark_mode)
prevmouse = [False,False,False]


new_click = {} # Store if a key has a new button down
for k in keybinds.keys():
    new_click[k] = False
previous = {} # Store if the keybind was previously pressed
for k in keybinds.keys():
    previous[k] = False
current = {} # Store if the keybind is currently pressed
for k in keybinds.keys():
    current[k] = False



while True:
    clicked = pg.mouse.get_pressed()
    pos = pg.mouse.get_pos()
    keys = pg.key.get_pressed()


    '''
    Update screen with new mouse clicks
    '''
    if clicked[0]:
        s.slider_drag(pos)
        if not prevmouse[0]:
            
            if pos[0] > s.field_width:
                if selected:
                    s.remove_move()
            s.sidebar_clicks(pos)
            selected = None
    
    '''
    Get new keyboard clicks
    '''
    for k in current.keys():
        current[k] = keys[keybinds[k]] # Get current value of each keybind
    
    for k in new_click.keys():
        new_click[k] = current[k] and not previous[k] # Detect if it was a new keypress (True)

    '''
    Make keybinds do their functions
    '''

    # Reset screen
    if new_click["RESET"]:
        s.reset() 

    # Create a new movement if one does not exist. Uses 'NEW_MOVEMENT' or mouse press on field
    if not selected and (new_click["NEW_MOVEMENT"] or (clicked[0] and not prevmouse[0] and pos[0] <= s.field_width)):
        selected = Movement(
            name=f'Movement {len(s.movements)+1}', # Set movement name to 'Movement ' and which number movement it is
            prev=(
                # Connect new line to previous line if it exists. Use cursor position if it doesn't exist
                s.movements[len(s.movements)-1] if len(s.movements) else Movement(endpoint=pos))
        )
        s.add_move(selected) # Add the movement to the screen

    # Cancel a move if you are currently placing one. Uses 'CANCEL_MOVEMENT' or left click
    elif selected and (new_click["CANCEL_MOVEMENT"] or clicked[2] and not prevmouse[2]):
        selected = None
        s.remove_move() # Remove move from the screen

    # Move selected movement's endpoint to current mouse position
    if selected and pos[0] <= s.field_width:
        selected.update(endpoint=pos, bg=s.bg, tc=s.tc) 
        s.edit_move(selected) # Update movement with endpoint and screen's color theme


    
    # Move the sidebar up or down from the arrow keys
    if new_click["SIDEBAR_DOWN"]:
        s.move_sidebar(1)
    elif new_click["SIDEBAR_UP"]:
        s.move_sidebar(-1)
    
    # Export the script to usable ARMS code
    if new_click["EXPORT"]:
        Parser(s.movements).export_script()
    
    # Import the generated script
    if new_click["IMPORT"]:
        # Reset our screen
        s.reset()

        # Get a list of movements from the script file
        imported_moves = Parser().import_script()

        # Add each movement to the screen
        for m in imported_moves:
            s.add_move(m)

    # Make the X button actually close the program
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    '''
    Update previous values to current values
    '''
    prevmouse = clicked # Set previous mouse click to current click
    for k in previous.keys():
        previous[k] = current[k] # Set previous press to current press
    
    
    s.update(5) # Update screen on 5ms loop
