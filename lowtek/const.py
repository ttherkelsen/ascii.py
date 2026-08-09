# Various constants

from enum import Enum, auto, IntFlag

class Align(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()
    STRETCH = auto()
    TOP = auto()
    MIDDLE = auto()
    BOTTOM = auto()

    
class Sizing(IntFlag):
    XMIN = 1
    XMAX = 2
    YMIN = 4
    YMAX = 8
    MIN = 5
    MAX = 10


class LineDrawing:
    NONE = ' '
    SINGLE = 's'
    DOUBLE = 'd'
    THICK = 't'
    ROUNDED = 'r'
    DOTTED3 = '3'
    DOTTED4 = '4'
    THICKDOTTED3 = '5'
    THICKDOTTED4 = '6'
    
