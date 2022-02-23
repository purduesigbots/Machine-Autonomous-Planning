import pygame as pg
import math as m
import copy as copy

# Slider class that slides between values and returns a value between 0 and 100
class Slider(pg.sprite.Sprite):
    def __init__(self, size, center_line, color, position_percent):
        # Set values we need from the parameters
        self.padding = size[0]/8 # total padding is 1/4th of the slider's width
        self.color = color
        self.position = position_percent / 100 * (size[0]-2*self.padding) # Scale starting value to viewable slider width
        self.value = self.position / (size[0]-2*self.padding) * 100 # Scale slider width to 0-100 value
        self.center_line = center_line
        self.width = size[0]
        self.height = size[1]

        # Set original image to blank sprite at size
        self.original_original_image = pg.Surface(size, pg.SRCALPHA)
        self.original_image = copy.copy(self.original_original_image)


    def set_image(self, pos=None):
        # Get mouse position relative to slider line
        self.position = self.position if pos==None else pos - self.rel_x - self.padding
        # Get 0-100 value from mouse position
        self.value = self.position / (self.width -2*self.padding) * 100
        # Reset original image
        self.original_image = copy.copy(self.original_original_image)
        if self.center_line:
            # Draw 1 line for slider
            pg.draw.line(self.original_image, self.color, (self.padding, self.height/2), (self.width-self.padding, self.height/2),1)
        else:
            # Draw rectangle for slider
            pg.draw.rect(self.original_image, self.color, (0,0,self.width, self.height), 2)
        # Draw circle representing slider position
        pg.draw.circle(self.original_image, self.color, (self.padding+self.position, self.height/2), self.height/2)
        self.image = self.original_image

    def draw(self, w, pos):
        # Draw slider onto screen at point 'pos'
        w.blit(self.image, pos)
        # Get how far to the right of the screen we are at
        self.rel_x = pos[0]

        # Set the rectangle hitbox to where we were drawn
        self.rect = self.image.get_rect(
            center=(pos[0]+self.width/2, pos[1]+self.height/2)
        )

    def collides(self, pos):
        # Check if a click was on this element
        if self.rect.collidepoint(pos):
            # Shift up clicks on left padding and shift down clicks on right padding
            if pos[0] < self.rel_x+self.padding:
                self.set_image(self.rel_x+self.padding)
            elif pos[0] > self.rel_x + self.width - self.padding:
                self.set_image(self.rel_x+self.width-self.padding)
            else:
                self.set_image(pos[0])
            return True
        return False

# Button class that toggles between selected and not selected
class Button(pg.sprite.Sprite):
    def __init__(self, size, outline_color, background_color, selected_render, selected, name):
        # Get the values we need from the parameters
        self.oc = outline_color
        self.bg = background_color
        self.name = name
        self.width = size[0]
        self.height = size[1]
        self.selected = selected
        self.selected_render = selected_render

        # Set our image to a blank box
        self.original_image = pg.Surface(size, pg.SRCALPHA)
        
    def set_image(self, rel_pos):
        # Get mouse position relative to where we were drawn
        self.rel_pos = rel_pos
        # Fill our shape with background color
        pg.draw.rect(self.original_image, self.bg, (0,0, self.width, self.height))

        # Draw the selected render if we are selected
        if self.selected:
            self.original_image.blit(self.selected_render, (8,0))

        # Draw an outline to display where the box is
        pg.draw.rect(self.original_image, self.oc, (0,0,self.width, self.height), 2)

        # Set our display image equal to what we just made above
        self.image = self.original_image

    def draw(self, w, pos):
        # Draw ourselves onto the screen relative to where we are in the settings class
        w.blit(self.image, (pos[0]+self.rel_pos[0], pos[1]+self.rel_pos[1]))

        # Get our rectangle hitbox
        self.rect = self.image.get_rect(
            center=(
                pos[0]+self.rel_pos[0]+self.width/2, 
                pos[1]+self.rel_pos[1]+self.height/2
            )
        )

    def clicked(self, pos):
        if self.rect.collidepoint(pos):
            # Toggle if the mouse position is within our rectangle hitbox
            self.selected = not self.selected
            return True
        return False
    
class Settings(pg.sprite.Sprite):
    def __init__(self, parent):
        super().__init__() 
        # Get values we need from out parent class
        self.parent = parent
        self.tc = parent.tc
        self.bg = parent.bg
        self.width = 400
        self.height = 150

        # Create blank sprite
        self.original_image = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.rect = pg.Rect(350, 0, 50, 50)

        # Create buttons and slider
        self.create_buttons()
        self.set_text()
        self.image = self.original_image
        
    def create_buttons(self):

        # Render in an X to be used for pressed buttons 
        checked = self.parent.textfont.render("X", False, self.tc)

        # Create a button for each ARMS movement flag
        self.async_button = Button((30,30), self.tc, self.bg, checked, self.parent.parent.options['flags']['arms::ASYNC'], 'async')
        self.thru_button = Button((30,30), self.tc, self.bg, checked, self.parent.parent.options['flags']['arms::THRU'], 'thru')
        self.backwards_button = Button((30,30), self.tc, self.bg, checked, self.parent.parent.options['flags']['arms::BACKWARDS'], 'back')
        self.absolute_button = Button((30,30), self.tc, self.bg, checked, self.parent.parent.options['flags']['arms::ABSOLUTE'], 'absolute')
        
        # Create a slider for the movement's speed
        self.speed_slider = Slider((200,30), True, self.tc, self.parent.parent.options['speed'])

    def set_text(self):
        # Reset our image
        self.original_image = pg.Surface((self.width, self.height), pg.SRCALPHA)

        # Render our current speed
        self.speed = self.parent.textfont.render(
            f'Speed: {self.parent.parent.options["speed"]}',
            False, self.tc
        )

        # render in text to display which button does what
        self.use_async = self.parent.textfont.render("ASYNC", False, self.tc)
        self.use_thru = self.parent.textfont.render("THRU", False, self.tc)
        self.use_absolute = self.parent.textfont.render("ABSOLUTE",False, self.tc)
        self.use_backwards = self.parent.textfont.render("BACKWARDS",False, self.tc)

        # Update the slider image
        self.speed_slider.set_image()

        # Update our image with the speed text
        self.original_image.blit(self.speed, (self.speed_slider.width, 0))

        # Update async button and draw async button's text to our image
        self.async_button.set_image((10,30))
        self.original_image.blit(self.use_async, (50, 30))

        # Update thru button and draw button's text to our image
        self.thru_button.set_image((10,60))
        self.original_image.blit(self.use_thru, (50, 60))

        # Update absolute button and draw button's text to our image
        self.absolute_button.set_image((10,90))
        self.original_image.blit(self.use_absolute, (50, 90))

        # Update backwards button and draw button's text to our image
        self.backwards_button.set_image((10, 120))
        self.original_image.blit(self.use_backwards, (50, 120))

        # Set our display image to what we just drew
        self.image = self.original_image
        
    def update_settings(self):
        # Update the movement's (parent.parent) options with the values from the buttons and slider
        self.parent.parent.options['speed'] = int(self.speed_slider.value)
        self.parent.parent.options['flags']['arms::ASYNC'] = self.async_button.selected
        self.parent.parent.options['flags']['arms::THRU'] = self.thru_button.selected
        self.parent.parent.options['flags']['arms::ABSOLUTE'] = self.absolute_button.selected
        self.parent.parent.options['flags']['arms::BACKWARDS'] = self.backwards_button.selected

        # Update our image
        self.set_text()

    def check_button_presses(self,pos):
        buttons = [
            self.async_button,
            self.absolute_button,
            self.thru_button,
            self.backwards_button
        ]

        # Make each button check if it was clicked
        for b in buttons:
            if b.clicked(pos):
                # Toggle the button and redraw
                b.set_image(b.rel_pos)

                # Update the movement's settings
                self.update_settings()
                return True
        return False

    def check_slider_slide(self, pos):
        # Check collision with slider and automatically update slider position
        if self.speed_slider.collides(pos):
            # Update the movement's settings
            self.update_settings()
            return True
        return False

    def draw(self, w, pos):
        # Draw our image (mainly text) onto the screen
        w.blit(self.image, pos)
        
        # Draw the buttons onto the screen
        self.async_button.draw(w, pos)
        self.thru_button.draw(w, pos)
        self.absolute_button.draw(w, pos)
        self.backwards_button.draw(w, pos)

        # Draw the slider onto the screen
        self.speed_slider.draw(w,pos)

        # Get our hitbox rectangle
        self.rect = self.image.get_rect(
            center=(pos[0]+self.width/2, pos[1]+self.height/2)
        )
