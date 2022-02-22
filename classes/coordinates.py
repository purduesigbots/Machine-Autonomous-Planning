from classes.screen import height


def convert_x(x):
    # rescale x to inches
    x /= height
    x *= 144

    # round to nearest  10th of an inch
    return round(x, 1)


def convert_y(y):
    # rescale y to inches
    y /= height
    y *= 144

    # move origin from top left to bottom left
    y = 144 - y

    # round to nearest 10th of an inch
    return round(y, 1)
