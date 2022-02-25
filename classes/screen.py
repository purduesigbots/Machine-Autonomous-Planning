from turtle import window_height
import pygame as pg

width = 1000
height = 600

class Screen:
    pg.init()

    def __init__(self, dark=False):
        # Initialize a bunch of stuff that we need
        self.movements = []
        self.sidebar_start = 0
        # Setup our pygame window with the width and height at the very top
        self.window = pg.display.set_mode((width,height))
        self.width = width
        self.height = height
        self.field_width = self.height
        self.dark = dark
        self.movement_settings_display = None
        self.selected_sidebar = None
        self.lines = (50, 50, 50) if dark else (180, 180, 180)
        self.bg = (15, 15, 15) if dark else (235, 235, 235)
        self.tc = (70, 70, 70) if dark else (180, 180, 180)

        # Update ourself with a 50ms delay
        self.update(50)

    def draw_background(self):
        # Fill our window with our background
        self.window.fill(self.bg)

        # Load the field and add it to our window
        bg_image = pg.image.load('assets/field.png')
        bg_image = pg.transform.scale(bg_image, (self.height, self.height))
        self.window.blit(bg_image, bg_image.get_rect())

        # Split the field into 6 horizontal and vertical sections and draw lines
        # Helps us see the tiles easier
        split_height = self.height/6
        for i in range(6):
            sh = i*split_height
            pg.draw.line(self.window, self.lines, (sh, 0), (sh, self.height))
            pg.draw.line(self.window, self.lines, (0, sh), (self.height, sh))
        pg.draw.line(self.window, self.lines, (self.height, 0),
                     (self.height, self.height), 3)

    def draw_arrows(self):
        # Draw every movement's arrow onto the field
        for m in self.movements:
            m.draw_arrow(self.window)

    def draw_sidebar(self):
        # Determine which sidebars are visible, and draw only those sidebars
        self.visible_sidebars = []
        drawn_height = 0
        # Starting at our initial sidebar, iterate until the end of self.movements
        for m in range(self.sidebar_start, len(self.movements)):

            # If our drawn height exceeds the visible height escape
            if drawn_height >= self.height:
                break

            # Add this sidebar to the visible ones and draw it to the screen
            self.visible_sidebars.append(self.movements[m])
            drawn_height += self.movements[m].draw_sidebar(
                self.window, (self.field_width, drawn_height)
            )
        
    def update(self, dt):
        # Update our background, arrows, and sidebar
        self.draw_background()
        self.draw_arrows()
        self.draw_sidebar()

        # Wait a small amount of time and then update
        pg.time.delay(dt)
        pg.display.update()

    def move_sidebar(self, direction):
        # Move our sidebar view up or down 1 position
        new_start = self.sidebar_start + direction
        if new_start >= 0 and new_start < len(self.movements):
            self.sidebar_start = new_start

    def sidebar_clicks(self, pos):
        # Check which sidebar if any were clicked
        for m in range(len(self.movements)):
            # Reset every movement's color to the default arrow color
            self.movements[m].set_arrow_color((50, 200, 50))
            # Next iteration if the sidebar isn't visible
            if not self.movements[m] in self.visible_sidebars:
                continue

            # Check if this iteration was clicked
            if self.movements[m].sidebar_clicked(pos):
                # Check if a different sidebar was already open
                if not self.selected_sidebar==None and self.selected_sidebar != m:
                    # Close the already open sidebar and reset the arrow color
                    self.movements[self.selected_sidebar].close_sidebar()
                    self.movements[self.selected_sidebar].set_arrow_color((50,200,50))
                # Set the current iteration to the open sidebar and update the arrow color
                self.selected_sidebar = m
                self.movements[m].set_arrow_color((35, 100, 35))
                
    def slider_drag(self, pos):
        # Check if the mouse is sliding a slider and if it is, slide it
        for m in self.visible_sidebars:
            if m.sidebar.display_settings:
                m.sidebar.settings.check_slider_slide(pos)

    def add_move(self, m):
        # Add a movement to our list of movements
        m.update(bg=self.bg, tc=self.tc)
        self.movements.append(m)

    def edit_move(self, new_move, i=None):
        # Edit a move that is already in our movement's list
        if not len(self.movements):
            return # Return if our list is empty
        # Get an index value based on the input i
        v = len(self.movements)-1 if i == None else i

        # Update the parameter with our background and text color/foreground
        new_move.update(bg=self.bg, tc=self.tc)
        self.movements[v] = new_move # Set our movement list at index v to the modified parameter
        if i == None:
            return # Return if i was not specified (normal arrow drawing from main)

        # Check to make sure arrow we are modifying is not last arrow
        if i < len(self.movements)-1:
            # Edit the arrow after the arrow we just modified with updated information
            to_change = self.movements[i+1]
            to_change.update(start=new_move.endpoint, prev=new_move, bg=self.bg, tc=self.tc)
            self.movements[i+1] = to_change

    def remove_move(self, i=None):
        # Remove a movement from our list based on i
        i = len(self.movements)-1 if not i else i
        try:
            del self.movements[i]
        except:
            pass

    def reset(self):
        # Completely reset ourselves by calling __init__
        self.__init__(dark=self.dark)
