# constants
SCREEN_HEIGHT = 600

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
