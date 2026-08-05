import abc

from .classes import Position
from .glyphs import GLYPHS

class Cell:
    def __init__(self, glyph, colours):
        self.glyph = glyph if isinstance(glyph, int) else ord(glyph)
        self.colours = colours

def str2cells(text, colours):
    return [ Cell(t, colours) for t in text ]
    

class CellPosition:
    def __init__(self, cell, x, y):
        self.cell = cell
        self.x = x
        self.y = y

    @classmethod
    def offset(cls, pos, cell, x, y):
        return cls(cell, pos.x + x, pos.y + y)
        
class CellUpdate(abc.ABC):
    def __init__(self, cells, pos=None):
        self.cells = cells
        self.dirty = True
        self.pos = pos or Position(0, 0)

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
                yield CellPosition(self.cells[idx], self.bbox.x + xx, self.bbox.y + yy)
                idx += 1

class BBoxFill(BBox):
    def iter(self):
        for yy in range(self.bbox.h):
            for xx in range(self.bbox.w):
                yield CellPosition(self.cells, self.bbox.x + xx, self.bbox.y + yy)
        
class Row(CellUpdate):
    def iter(self):
        for idx, cell in enumerate(self.cells):
            yield CellPosition.offset(self.pos, self.cells[idx], idx, 0)

class Column(CellUpdate):
    def iter(self):
        for idx, cell in enumerate(self.cells):
            yield CellPosition.offset(self.pos, self.cells[idx], 0, idx)
                
class Composite(CellUpdate):
    def __init__(self, composite, **cellupdate):
        super().__init__(**cellupdate)
        self.composite = composite

    def iter(self):
        for x, y in self.composite:
            yield CellPosition(self.cells, x, y)
        

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
                yield CellPosition.offset(self.pos, self.hline, x, self.center.y)
        for y in range(self.size.h):
            if y != self.center.y:
                yield CellPosition.offset(self.pos, self.vline, self.center.x, y)
        yield CellPosition.offset(self.pos, self.cross, self.center.x, self.center.y)
            
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
                if (cp.x, cp.y) not in composite:
                    yield cp

    def fill(self, bbox):
        composite = bbox.to_composite()
        for cu in self:
            for cp in cu:
                 # We intentionally use remove because no component
                 # should ever render to any cell position more than
                 # once.
                composite.remove((cp.x, cp.y))
            cu.dirty = True
        return composite
                    
    def dirty(self, state=True):
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
        self.grid[cp.y][cp.x] = cp.cell
        self.dirty.append(cp)
