# Colors that can be used to color blocks.

BLACK   = 30
RED     = 31
GREEN   = 32
YELLOW  = 33
BLUE    = 34
MAGENTA = 35
CYAN    = 36
WHITE   = 37

ALL_COLORS = [BLACK,RED,GREEN,YELLOW,BLUE,MAGENTA,CYAN,WHITE]

def is_proper_color(color):
    """
       Check whether the given color is a proper color.
       - True if the given color is one of the colors defined above.
       ASSUMPTIONS
       - None
    """
    return color in ALL_COLORS

def get_random_color():
    """
        Return a random color.
    """
    import random
    return random.choice(ALL_COLORS)

def get_color_name(color):
    """
       Return the name for the given color.
       - The function returns the name for the color as used in the GUI.
       ASSUMPTIONS
       - The given color is a proper color.
    """
    assert is_proper_color(color)
    if color == BLACK:
        return "black"
    elif color == RED:
        return "red"
    elif color == GREEN:
        return "green"
    elif color == YELLOW:
        return "yellow"
    elif color == BLUE:
        return "blue"
    elif color == MAGENTA:
        return "magenta"
    elif color == CYAN:
        return "cyan"
    elif color == WHITE:
        return "white"


