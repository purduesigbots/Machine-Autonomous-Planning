# import statements
import tkinter as tk
from PIL import Image, ImageTk

# constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# create window
root = tk.Tk()

# set window title and size
root.title("Visual Auton Generator v0.1")
root.geometry("{0}x{1}+50+0".format(SCREEN_WIDTH, SCREEN_HEIGHT))

# create field image from assets and resize
img = Image.open('assets/field.png')
img = img.resize((SCREEN_HEIGHT, SCREEN_HEIGHT))
field = ImageTk.PhotoImage(img)

# create canvas and display image
can = tk.Canvas(root, width=SCREEN_HEIGHT,
    height=SCREEN_HEIGHT)
can.place(anchor=tk.NW, x=0, y=0)
can.create_image(0, 0, anchor=tk.NW, image=field)

class Window:
    def __init__(self, root, canvas):
        self.creating_movement = False
        self.start_point = (0, 0)
        self.end_point = (0, 0)
        self.root = root
        self.canvas = canvas
        self.temp_line = None

w = Window(root, can)

# mouse click input handler
def click_handler(event):
    # if mouse click is on field
    if event.x < SCREEN_HEIGHT:
        # convert to inches on field
        # bottom left of field is (0, 0)
        field_x = event.x / SCREEN_HEIGHT * 24.0 * 6
        field_y = (600 - event.y) / SCREEN_HEIGHT * 24.0 * 6

        # if this is first click
        if not w.creating_movement:
            # set creating movement to true and store starting point
            w.creating_movement = True
            w.start_point = (event.x, event.y)
        # if not first click
        else:
            # set creating movement to false and store end point
            w.creating_movement = False
            w.end_point = (event.x, event.y)

            # create line between start and end point
            w.canvas.create_line(w.start_point[0], w.start_point[1], w.end_point[0], w.end_point[1], 
                                 fill="lime", width=5, arrow=tk.LAST, arrowshape=(8, 10, 8))
    # if mouse click is not on field
    else:
        print("Outside field")

# mouse motion inpute handler
def motion_handler(event):
    # if currently drawing a line
    if w.creating_movement:
        # delete the current temp line
        w.canvas.delete(w.temp_line)

        # create a new temp line between start point and current mouse position
        w.temp_line = w.canvas.create_line(w.start_point[0], w.start_point[1], event.x, event.y, 
                                           fill="lime", width=5, arrow=tk.LAST, arrowshape=(8, 10, 8))

# bind mouse button input to click_handler callback
w.root.bind("<Button>", click_handler)
# bind mouse motion input to motion_handler callback
w.root.bind("<Motion>", motion_handler)

# start main loop
w.root.mainloop()