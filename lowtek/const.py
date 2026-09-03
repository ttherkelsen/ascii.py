# Various constants

from enum import Enum, auto, IntFlag

class Mouse(IntFlag):
    NONE = 0
    ENABLE = 1
    CURSOR = 2
    INVERSE = 4
    HIDE = 8

    SHOW = 6
    FULL = 11
    FULLINVERSE = 13

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
    DOTTED2 = '2'
    DOTTED3 = '3'
    DOTTED4 = '4'
    THICKDOTTED2 = '5'
    THICKDOTTED3 = '6'
    THICKDOTTED4 = '7'
    
