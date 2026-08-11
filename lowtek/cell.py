import abc

from .classes import Position
from .glyphs import GLYPHS

class Cell:
    def __init__(self, glyph, colours):
        self.glyph = glyph if isinstance(glyph, int) else ord(glyph)
        self.colours = colours

def str2cells(text, colours):
    return [ Cell(t, colours) for t in text ]

class CellHint:
    def __init__(self, cell, hint=1, offset=None):
        self.cell = cell
        self.hint = hint
        self.offset = offset

class CellPosition:
    def __init__(self, cell, pos):
        self.cell = cell
        self.pos = pos

    def __str__(self):
        return f"CellPosition @ {id(self)} {self.cell=} {self.pos=}"
    __repr__ = __str__
        
class CellUpdate(abc.ABC):
    def __init__(self, cells, pos=None):
        self.cells = cells
        self.dirty = True
        self.pos = pos or Position(0, 0)

    @property
    def cells(self):
        return self._cells

    @cells.setter
    def cells(self, value):
        self._cells = value
        self.dirty = True
        
    def __iter__(self):
        if not self.dirty:
            return
        for cp in self.iter():
            yield cp
        self.dirty = False

    @abc.abstractmethod
    def iter(self):
        ... # Must be implemented in subclass

class BBox(CellUpdate):
    def __init__(self, bbox, **cellupdate):
        super().__init__(**cellupdate)
        self.bbox = bbox

    def iter(self):
        idx = 0
        for yy in range(self.bbox.h):
            for xx in range(self.bbox.w):
                yield CellPosition(self.cells[idx], Position(self.bbox.x + xx, self.bbox.y + yy))
                idx += 1

class BBoxFill(BBox):
    def iter(self):
        for yy in range(self.bbox.h):
            for xx in range(self.bbox.w):
                yield CellPosition(self.cells, Position(self.bbox.x + xx, self.bbox.y + yy))
        
class Row(CellUpdate):
    def iter(self):
        for idx, cell in enumerate(self.cells):
            yield CellPosition(self.cells[idx], Position(idx, 0) + self.pos)

class Column(CellUpdate):
    def iter(self):
        for idx, cell in enumerate(self.cells):
            yield CellPosition(self.cells[idx], Position(0, idx) + self.pos)
            
class Composite(CellUpdate):
    def __init__(self, composite, **cellupdate):
        super().__init__(**cellupdate)
        self.composite = composite

    def iter(self):
        for x, y in self.composite:
            yield CellPosition(self.cells, Position(x, y))

class Frame(BBox):
    def __init__(self, frame, **bbox):
        super().__init__(cells=None, **bbox)
        self.frame = frame
        
    def iter(self):
        for d in self.frame:
            for y in range(d.offset.h):
                for x in range(d.offset.w):
                    yield CellPosition(d.cell, Position(self.bbox.x + d.offset.x + x, self.bbox.y + d.offset.y + y))

class CrossLD(CellUpdate):
    def __init__(self, size, colours, center=None, pos=None):
        super().__init__(cells=None, pos=pos)
        self.size = size
        self.center = center or size.center()
        self.hline = Cell(GLYPHS['B s s'], colours)
        self.vline = Cell(GLYPHS['Bs s '], colours)
        self.cross = Cell(GLYPHS['Bssss'], colours)

    def iter(self):
        for x in range(self.size.w):
            if x != self.center.x:
                yield CellPosition(self.hline, Position(x, self.center.y) + self.pos)
        for y in range(self.size.h):
            if y != self.center.y:
                yield CellPosition(self.vline, Position(self.center.x, y) + self.pos)
        yield CellPosition(self.cross, Position(self.center.x, self.center.y) + self.pos)
            
class CellUpdates:
    def __init__(self, childupdates=None):
        if childupdates is not None:
            for idx, c in enumerate(childupdates):
                setattr(self, str(idx), c)
                
    def __iter__(self):
        for name, cu in self.__dict__.items():
            if isinstance(cu, CellUpdate) and cu.dirty:
                yield cu
            elif isinstance(cu, CellUpdates):
                # FIXME: Should not be necessary to nest CellUpdates as you can just assign
                # to any value attribute you want?
                for cuu in cu:
                    yield cuu

    def crop(self, composite):
        for cu in self:
            for cp in cu:
                if (cp.pos.x, cp.pos.y) not in composite:
                    yield cp

    def fill(self, bbox):
        composite = bbox.to_composite()
        for cu in self:
            for cp in cu:
                 # We intentionally use remove because no component
                 # should ever render to any cell position more than
                 # once, so if it happens, we want this to catch it.
                composite.remove((cp.x, cp.y))
            cu.dirty = True
        return composite
                    
    def dirty(self, state=True): # FIXME: Should this be a property instead?  If not should be renamed to set_dirty
        for cu in self:
            cu.dirty = state

class CellGrid:
    def __init__(self, size):
        self.size = size
        self.grid = [ [ None ]*size.w for t in range(size.h) ]
        self.dirty = []

    def get_dirty(self):
        for cp in self.dirty:
            yield cp
        self.dirty = []
        
    def update(self, cp):
        self.grid[cp.pos.y][cp.pos.x] = cp.cell
        self.dirty.append(cp)
