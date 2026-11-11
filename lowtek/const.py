# Various constants

from enum import Enum, auto, IntFlag, IntEnum

class Mouse(IntFlag):
    NONE = 0
    ENABLE = 1
    CURSOR = 2
    INVERSE = 4
    HIDE = 8
    NOCONTEXT = 16

    SHOW = 6
    FULL = 11
    FULLINVERSE = 13

class MouseButton(IntEnum):
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2
    BACK = 3
    FORWARD = 4

class State(IntFlag):
    UP = auto()
    DOWN = auto()
    HOVER = auto()
    DISABLED = auto()
    
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
    
class Cards(IntFlag):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    FACE_BACK = 14
    MASK_VALUE = 2**4 - 1

    CLUBS = 2**4
    DIAMONDS = 2**5
    SPADES = 2**6
    HEARTS = 2**7
    SUIT_BACK = 2**8
    MASK_SUIT = 2**4 | 2**5 | 2**6 | 2**7 | 2**8

    BACK = 14 + 2**8
    
    STYLE_DEFAULT = 2**16
    STYLE_A = 2**16
    MASK_STYLE = 2**16
