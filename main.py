# import statements
import tkinter as tk
from classes.screen import Window
from PIL import Image, ImageTk
from classes.constants import SCREEN_HEIGHT, SCREEN_WIDTH

# create window
root = tk.Tk()

# set window title and size
root.title("Machine Autonomous Planner v0.1")
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

Window(root, can)

# start main loop
root.mainloop()