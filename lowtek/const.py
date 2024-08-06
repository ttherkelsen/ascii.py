# Various constants

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


class Border(Enum):
    SINGLE = auto()
    DOUBLE = auto()
    
