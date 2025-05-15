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

    def expand(self, rect):
        self.w += rect.e + rect.w
        self.h += rect.n + rect.s

    def expand_1(self, rect):
        self.w += (rect.e and 1) + (rect.w and 1)
        self.h += (rect.n and 1) + (rect.s and 1)


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        
class BBox:
    def __init__(self, x=0, y=0, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
