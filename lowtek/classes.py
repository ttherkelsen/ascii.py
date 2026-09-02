# Various utlity and helper classes which are too small to justify having their
# own file

import copy

from . import const
from . import cell
from .glyphs import GLYPHS

class Core:
    def clone(self):
        return copy.copy(self)

class Callback(Core):
    def __init__(self, name, func, *args, **kwargs):
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self, *args, **kwargs):
        return self.func(*(args + self.args), **(self.kwargs | kwargs))
    
class Frame(Core):
    def __init__(
            self,
            nesw=None,
            n=None, e=None, s=None, w=None,
            order='nswe',
    ):
        if nesw:
            n = e = s = w = nesw

        self.n = n
        self.e = e
        self.s = s
        self.w = w
        self.order = order

    def __iter__(self):
        for d in self.order:
            value = getattr(self, d)
            if value:
                yield value
        
    def is_before(self, dirs):
        return self.order.index(dirs[0]) < self.order.index(dirs[1])
        
    def update_offsets(self, bbox):
        # FIXME: Can this be simplified/generalised?
        if self.n and self.n.offset is None:
            b = BBox(x=0, y=0, w=bbox.w, h=self.n.hint)
            if self.w and self.is_before("wn"):
                b += Position(x=self.w.hint, y=0)
                b -= Size(w=self.w.hint, h=0)
            if self.e and self.is_before("en"):
                b -= Size(w=self.e.hint, h=0)
            self.n.offset = b
        if self.s and self.s.offset is None:
            b = BBox(x=0, y=bbox.h-self.s.hint, w=bbox.w, h=self.s.hint)
            if self.w and self.is_before("ws"):
                b += Position(x=self.w.hint, y=0)
                b -= Size(w=self.w.hint, h=0)
            if self.e and self.is_before("es"):
                b -= Size(w=self.e.hint, h=0)
            self.s.offset = b
        if self.w and self.w.offset is None:
            b = BBox(x=0, y=0, w=self.w.hint, h=bbox.h)
            if self.n and self.is_before("nw"):
                b += Position(x=0, y=self.n.hint)
                b -= Size(w=0, h=self.n.hint)
            if self.s and self.is_before("sw"):
                b -= Size(w=0, h=self.s.hint)
            self.w.offset = b
        if self.e and self.e.offset is None:
            b = BBox(x=bbox.w-self.e.hint, y=0, w=self.e.hint, h=bbox.h)
            if self.n and self.is_before("ne"):
                b += Position(x=0, y=self.n.hint)
                b -= Size(w=0, h=self.n.hint)
            if self.s and self.is_before("se"):
                b -= Size(w=0, h=self.s.hint)
            self.e.offset = b
        
    def layout_done(self, bbox, theme):
        clone = self.clone()
        for d in "nesw":
            if value := getattr(self, d):
                match value:
                    case int():
                        setattr(clone, d, cell.CellHint(cell.Cell(theme.margin, theme.colours.margin), value))
                    case str():
                        setattr(clone, d, cell.CellHint(cell.Cell(value, theme.colours.margin), 1))
                    case cell.Cell():
                        setattr(clone, d, cell.CellHint(value, 1))
                    case cell.CellHint():
                        pass
                    case _:
                        raise TypeError(f'illegal type for Frame.{d} ({value=})')
        clone.update_offsets(bbox)
        return clone
        
    def to_hint(self, dirs):
        total = 0
        for d in dirs:
            value = getattr(self, d)
            if value is not None:
                match value:
                    case int():
                        total += value
                    case str():
                        total += 1
                    case cell.CellHint():
                        total += value.hint
                    case _:
                        raise TypeError(f'illegal type for Frame.{d} ({value=})')
        return total


    def to_position(self):
        return Position(x=self.to_hint('w'), y=self.to_hint('n'))
    
    def to_size(self):
        return Size(w=self.to_hint("ew"), h=self.to_hint("ns"))

    @classmethod
    def from_int(cls, num):
        return cls(nesw=num)

    @classmethod
    def from_str(cls, dirs, order="nesw"):
        if len(dirs) == 1:
            return cls(nesw=dirs)
        return cls(**dict(zip(order, dirs)))

Margin = Frame
Padding = Frame

class Border(Frame):
    LD = {
        'n': 'B N N',
        's': 'B S S',
        'e': 'BE E ',
        'w': 'BW W ',
        'nw': 'B WN ',
        'ne': 'B  NE',
        'sw': 'BSW  ',
        'se': 'BS  E',
    }

    def dir2glyph(self, dir):
        temp = self.LD[dir]
        if len(dir) == 1:
            return GLYPHS[temp.replace(dir.upper(), getattr(self, dir))]

        if getattr(self, dir[0]) and getattr(self, dir[1]):
            temp = temp.replace(dir[0].upper(), getattr(self, dir[1]))
            temp = temp.replace(dir[1].upper(), getattr(self, dir[0]))
        elif getattr(self, dir[0]):
            temp = self.LD[dir[0]]
            temp = temp.replace(dir[0].upper(), getattr(self, dir[0]))
        else: # getattr(self, dir[1])
            temp = self.LD[dir[1]]
            temp = temp.replace(dir[1].upper(), getattr(self, dir[1]))
        return GLYPHS[temp]

    def is_before(self, dirs):
        return True
    
    def update_offsets(self, bbox):
        super().update_offsets(bbox)

        if self.n or self.w:
            self.nw.offset = BBox(x=0, y=0, w=1, h=1)

        if self.n or self.e:
            self.ne.offset = BBox(x=bbox.w-1, y=0, w=1, h=1)

        if self.s or self.w:
            self.sw.offset = BBox(x=0, y=bbox.h-1, w=1, h=1)

        if self.s or self.e:
            self.se.offset = BBox(x=bbox.w-1, y=bbox.h-1, w=1, h=1)

    
    def layout_done(self, bbox, theme):
        clone = self.clone()
        def set_value(d, value):
            match value:
                case str():
                    setattr(clone, d, cell.CellHint(cell.Cell(self.dir2glyph(d), theme.colours.margin), 1))
                case cell.Cell():
                    setattr(clone, d, cell.CellHint(value, 1))
                case cell.CellHint():
                    pass
                case _:
                    raise TypeError(f'illegal type for FrameLD.{d} ({value=})')
                
        for d in "nesw":
            if value := getattr(self, d):
                set_value(d, value)

        for d in ('nw', 'ne', 'sw', 'se'):
            if getattr(clone, d[0]) or getattr(clone, d[1]):
                set_value(d, d)
            else:
                setattr(clone, d, None)

        clone.update_offsets(bbox)
        clone.order = ('n', 'e', 's', 'w', 'nw', 'ne', 'sw', 'se')
        return clone
        
    @classmethod
    def from_str(cls, dirs):
        if len(dirs) == 1:
            return cls(nesw=dirs)
        return cls(**dict(zip(order, dirs)))

class Size(Core):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def __add__(self, other):
        if not isinstance(other, Size):
            return NotImplemented

        return Size(self.w + other.w, self.h + other.h)

    def __iadd__(self, other):
        if not isinstance(other, Size):
            return NotImplemented

        self.w += other.w
        self.h += other.h
        return self

    def __sub__(self, other):
        if not isinstance(other, Size):
            return NotImplemented

        return Size(abs(self.w - other.w), abs(self.h - other.h))

    def __isub__(self, other):
        if not isinstance(other, Size):
            return NotImplemented

        self.w -= other.w
        self.h -= other.h
        return self

    def to_center(self):
        return Position(x=self.w//2, y=self.h//2)
    
    def to_bbox(self, x=0, y=0):
        return BBox(x, y, self.w, self.h)
        

class Position(Core):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"<Position @ {id(self)} {self.x=} {self.y=}"
    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
            
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other):
        if not isinstance(other, Position):
            return NotImplemented

        return Position(self.x + other.x, self.y + other.y)
    
    def __iadd__(self, other):
        if not isinstance(other, Position):
            return NotImplemented

        self.x += other.x
        self.y += other.y
        return self
    
    def __sub__(self, other):
        if not isinstance(other, Position):
            return NotImplemented

        return Position(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        if not isinstance(other, Position):
            return NotImplemented

        self.x -= other.x
        self.y -= other.y
        return self

    def to_pixels(self, pixelsize):
        return PixelPosition(self.x * pixelsize.w, self.y * pixelsize.h)

    def to_tuple(self):
        return (self.x, self.y)
    

PixelPosition = Position

class BBox(Position, Size):
    def __init__(self, x, y, w, h):
        Position.__init__(self, x, y)
        Size.__init__(self, w, h)

    def __add__(self, other):
        match other:
            case Size():
                return BBox(self.x, self.y, self.w + other.w, self.h + other.h)
            case Position():
                return BBox(self.x + other.x, self.y + other.y, self.w, self.h)
            case _:
                return NotImplemented

    def __iadd__(self, other):
        match other:
            case Size():
                Size.__iadd__(self, other)
                return self
            case Position():
                Position.__iadd__(self, other)
                return self
            case _:
                return NotImplemented

    def __sub__(self, other):
        match other:
            case Size():
                return BBox(self.x, self.y, self.w - other.w, self.h - other.h)
            case Position():
                return BBox(self.x - other.x, self.y - other.y, self.w, self.h)
            case _:
                return NotImplemented
    
    def __isub__(self, other):
        match other:
            case Size():
                Size.__isub__(self, other)
                return self
            case Position():
                Position.__isub__(self, other)
                return self
            case _:
                return NotImplemented

    def set_position(self, pos):
        self.x = pos.x
        self.y = pos.y
            
    def __str__(self):
        return f"<BBox @ {id(self)} {self.x=} {self.y=} {self.w=} {self.h=}"
    __repr__ = __str__

    def to_size(self):
        return Size(self.w, self.h)

    def to_position(self):
        return Position(self.x, self.y)

    def to_composite(self):
        c = set()
        for y in range(self.h):
            for x in range(self.w):
                c.add(( self.x + x, self.y + y ))
        return c
    
