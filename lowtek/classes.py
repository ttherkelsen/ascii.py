# Various utlity and helper classes which are too small to justify having their
# own file

class Rect:
    def __init__(self, nesw=0, n=0, e=0, s=0, w=0):
        if nesw:
            # Special case, Rect(int > 0) == all sides of rectangle
            n = e = s = w = nesw
        self.n = n
        self.e = e
        self.s = s
        self.w = w


class Size:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def __add__(self, other):
        if other is not Size:
            return NotImplemented

        return Size(self.w + other.w, self.h + other.h)

    def __sub__(self, other):
        if other is not Size:
            return NotImplemented

        return Size(abs(self.w - other.w), abs(self.h - other.h))

    
    def expand(self, rect):
        self.w += rect.e + rect.w
        self.h += rect.n + rect.s

    def expand_1(self, rect):
        self.w += (rect.e and 1) + (rect.w and 1)
        self.h += (rect.n and 1) + (rect.s and 1)

    def to_bbox(self, x=0, y=0):
        return BBox(x, y, self.w, self.h)
        

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_pixels(self, pixelsize):
        return PixelPosition(self.x * pixelsize.w, self.y * pixelsize.h)
    
PixelPosition = Position

class BBox:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def to_size(self):
        return Size(self.w, self.h)

    def to_position(self):
        return Position(self.x, self.y)
    
