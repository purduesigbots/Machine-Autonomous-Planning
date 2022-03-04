from classes.constants import SCREEN_HEIGHT

class Converter:

    def convert_x(x):
        # rescale x to inches
        x /= SCREEN_HEIGHT
        x *= 144

        # round to nearest  10th of an inch
        return round(x, 1)

    def convert_y(y):
        # rescale y to inches
        y /= SCREEN_HEIGHT
        y *= 144

        # move origin from top left to bottom left
        y = 144 - y

        # round to nearest 10th of an inch
        return round(y, 1)

    def convert_x_reverse(x):
        # rescale inches to x
        x /= 144
        x *= SCREEN_HEIGHT

        # Return rounded value
        return round(x, 0)

    def convert_y_reverse(y):
        # move origin to top left
        y = 144 - y

        # rescale inches to y
        y /= 144
        y *= SCREEN_HEIGHT

        # Return rounded value
        return round(y,0)