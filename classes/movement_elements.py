import pygame as pg
import math as m
from classes.converter import Converter as c
from classes.settings import Settings

'''
Arrow Class:
    - Stores the arrow sprite to be drawn onto the screen
        - start and end points
        - color
'''
class Arrow(pg.sprite.Sprite):
    def __init__(self, start, endpoint, color):
        super().__init__() # Initialize pygame Sprite
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
            pass

        '''
        I cant really explain this math anymore but it pretty much decides
        which direction the arrow is facing, and then calculates 2 more points
        bassed on the endpoint that when connected will make a triangle facing
        the same direction as the line
        '''
        at1 = theta+arr_t
        at2 = theta-arr_t
        arrx = self.endpoint[0] - (1 if dx > 0 else -1)*arr_l * m.cos(at1)
        arry = self.endpoint[1] - (1 if dx > 0 else -1)*arr_l * m.sin(at1)
        arrx2 = self.endpoint[0] - (1 if dx > 0 else -1)*arr_l * m.cos(at2)
        arry2 = self.endpoint[1] - (1 if dx > 0 else -1)*arr_l * m.sin(at2)
        self.coordinates.append((arrx, arry))
        self.coordinates.append((arrx2, arry2))

    def draw(self, w):
        pg.draw.line(w, self.color, self.start, self.endpoint, 3) # Draw the line from start to end
        pg.draw.polygon(w, self.color, self.coordinates) # Draw the arrow tip at the end of the line



'''
Sidebar Class:
    - Contains information about movement
        - movement name
        - movement start and endpoint
    - Contains settings view for editing movement
'''
class Sidebar(pg.sprite.Sprite):
    def __init__(self, parent):
        self.parent = parent # Pass the movement into the sidebar

        # Get information from the parent
        self.name = parent.name
        self.tc = parent.tc
        self.bg = parent.bg
        self.start = parent.start
        self.endpoint = parent.endpoint
        self.width = 400
        self.height = 50

        # Make blank sprite as original image
        self.original_image = pg.Surface(
            (self.width, self.height), pg.SRCALPHA)

        # Create large and small font
        self.textfont = pg.font.SysFont("arial", 30)
        self.posfont = pg.font.SysFont("arial", 15)
        self.clicked = False
        self.display_settings = False

        # Initialize sidebar text and settings class
        self.set_text()
        self.settings = Settings(self)

    def set_text(self):

        # Render the movement's name in large font
        self.displayText = self.textfont.render(self.name, False, self.tc)

        # Render the movement's start and endpoint in small font
        self.posi = self.posfont.render(
            f'From: ({c.convert_x(self.start[0])} , {c.convert_y(self.start[1])})', False, self.tc)
        self.posf = self.posfont.render(
            f'To: ({c.convert_x(self.endpoint[0])} , {c.convert_y(self.endpoint[1])})', False, self.tc)

        # Draw everything onto the blank sprite
        self.original_image.blit(self.displayText, (10, 5))
        self.original_image.blit(self.posi, (220, 5))
        self.original_image.blit(self.posf, (240, 25))
        pg.draw.line(self.original_image, self.tc,
                     (0, 0), (self.width, 0), 4)

        # Set the image to be displayed equal to now modified sprite
        self.image = self.original_image

    def draw(self, w, pos):
        # Draw our sprite onto the main window at the designated position
        w.blit(self.image, pos)

        # Keep track of the amount of height we have drawn to make the sidebar clean
        toreturn = self.height

        # Get the rectangle hitbox position of the sidebar title
        self.rect = self.image.get_rect(
            center=(pos[0]+self.width/2, pos[1]+self.height/2))

        # Display the settings if it is enableds
        if self.display_settings:
            self.settings.draw(w, (pos[0], pos[1]+self.height))

            # Add the setting's height to our drawn height
            toreturn += self.settings.height
        return toreturn

    def close_settings(self):
        self.display_settings = False

    def collides(self, point):
        try:
            # Check collisions with the settings if they are enabled
            if self.display_settings:
                self.settings.check_button_presses(point)
                self.settings.check_slider_slide(point)

            # Check collision with the title bar
            if self.rect.collidepoint(point):
                return True
            return False
        except:
            return False
