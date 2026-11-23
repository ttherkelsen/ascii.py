import abc

from .classes import Position, Size
from .colours import Colours
from .glyphs import GLYPHS

class Cell:
    def __init__(self, glyph, colours):
        self.glyph = glyph if isinstance(glyph, int) else ord(glyph)
        self.colours = colours

    def inverse(self):
        return Cell(self.glyph, self.colours.inverse())

    def update_colours(self, *colours):
        return Cell(self.glyph, self.colours.update(*colours))

def str2cells(text, colours):
    return [ Cell(t, colours) for t in text ]

def ints2cells(ints, colours):
    cells = []
    for ii in ints:
        for i in ii:
            cells.append(Cell(i, colours))
    return cells

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

    def to_tuple(self):
        return (self.pos.x, self.pos.y)
        
class CellUpdate(abc.ABC):
    def __init__(self, cells, pos=None):
        self.cells = cells
        #self.dirty = True
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

    def set_dirty(self, state=True):
        self.dirty = state
        
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
                yield CellPosition(self.cells[idx], Position(self.bbox.x + xx, self.bbox.y + yy) + self.pos)
                idx += 1

class BBoxFill(BBox):
    def iter(self):
        for yy in range(self.bbox.h):
            for xx in range(self.bbox.w):
                yield CellPosition(self.cells, Position(self.bbox.x + xx, self.bbox.y + yy) + self.pos)

class CellCollection:
    def __init__(self, parent, size, cells=None):
        self.parent = parent
        self.size = size
        self.cells = cells or {}

    def __getitem__(self, pos):
        return self.cells[pos]
    
    def __setitem__(self, pos, cell):
        self.cells[pos] = cell

    def items(self):
        return self.cells.items()
        
    def clone(self, parent):
        return CellCollection(parent, self.size)
        
    def filter(self, frame=None):
        cc = self.clone(self)
        if frame:
            ps = set()
            for i in range(frame):
                for x in range(self.size.w):
                    ps.add(Position(x, i))
                    ps.add(Position(x, self.size.h - i - 1))
                for y in range(self.size.h):
                    ps.add(Position(i, y))
                    ps.add(Position(self.size.w - i - 1, y))
            cc.cells = { pos: self[pos] for pos in ps }
                
        return cc

    def inverse(self):
        for pos, cell in self.items():
            self[pos] = self[pos].inverse()
        return self

    def colour(self, *colours):
        for pos, cell in self.items():
            self[pos] = self[pos].update_colours(*colours)
        return self

    def apply(self):
        obj = self
        while True:
            obj = obj.parent
            if not isinstance(obj, CellCollection):
                break

        # obj is containing Grid object -- this could be expanded to all types of CellUpdate objects
        for pos, cell in self.cells.items():
            obj[pos] = cell
        

class Grid(CellUpdate):
    def __init__(self, imagedata, palette, colours, **cellupdate):
        self.imagedata = imagedata
        self.palette = palette
        self.colours = colours
        super().__init__(
            cells=self.render_cells(),
            **cellupdate,
        )

    def iter(self):
        if self.dirty is True:
            seq = self.cells.items()
        else:
            seq = self.dirty

        for pos, cell in seq:
            yield CellPosition(cell, pos + self.pos)

    def __setitem__(self, pos, cell):
        if self.dirty is True:
            pass
        elif self.dirty is False:
            self.dirty = [ (pos, cell) ]
        else:
            self.dirty.append((pos, cell))
        self.cells[pos] = cell

    def render_cells(self):
        cells = CellCollection(self, Size(len(self.imagedata[0]), len(self.imagedata)))
        for y, row in enumerate(self.imagedata):
            for x, col in enumerate(row):
                c = self.palette.get(col, col)
                match c:
                    case str():
                        cell = Cell(ord(c), self.colours)
                    case int():
                        cell = Cell(c, self.colours)
                    case tuple():
                        c, *colours = c
                        cell = Cell(c, self.colours.update(*colours))
                    case Cell():
                        cell = c
                    case _:
                        raise ValueError(f"Unknown palette type {c=}")
                cells[Position(x, y)] = cell
        return cells

        
        
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
            yield CellPosition(self.cells, Position(x, y) + self.pos)

class Frame(BBox):
    def __init__(self, frame, **bbox):
        super().__init__(cells=None, **bbox)
        self.frame = frame
        
    def iter(self):
        for d in self.frame:
            for y in range(d.offset.h):
                for x in range(d.offset.w):
                    yield CellPosition(d.cell, Position(self.bbox.x + d.offset.x + x, self.bbox.y + d.offset.y + y) + self.pos)

class DropShadow(CellUpdate):
    def __init__(self, size, colours, pos=None):
        super().__init__(cells=None, pos=pos)
        self.size = size
        self.dss = Cell(GLYPHS['DSs'], colours)
        self.dse = Cell(GLYPHS['DSe'], colours)

    def iter(self):
        for x in range(self.size.w):
            yield CellPosition(self.dss, Position(x + 1, self.size.h) + self.pos)
        yield CellPosition(self.dse, Position(self.size.w, self.size.h - 1) + self.pos)
                    
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
        self.cus = {}
        if childupdates is not None:
            for idx, c in enumerate(childupdates):
                self.cus[idx] = c

    def __iter__(self):
        return self.iter()
    
    def iter(self, all=False, dirty=None):
        for name, cu in self.cus.items():
            if isinstance(cu, CellUpdate) and (all or cu.dirty):
                yield cu
                if dirty is not None:
                    cu.set_dirty(dirty)
            elif isinstance(cu, CellUpdates):
                # FIXME: Should not be necessary to nest CellUpdates as you can just assign
                # to any value attribute you want?
                for cuu in cu:
                    yield cuu
                    if dirty is not None:
                        cuu.set_dirty(dirty)
                    
    def __getitem__(self, key):
        return self.cus[key]

    def __setitem__(self, key, value):
        self.cus[key] = value

    def __delitem__(self, key):
        del self.cus[key]

    def __contains__(self, key):
        return key in self.cus
                    
    def fill(self, bbox):
        composite = bbox.to_composite()
        for cu in self.iter(all=True, dirty=True):
            for cp in cu:
                 # We intentionally use remove because no component
                 # should ever render to any cell position more than
                 # once, so if it happens, we want this to catch it.
                composite.remove(cp.to_tuple())
        return composite

    def move(self, pos, relative=True):
        for cu in self.iter(all=True, dirty=True):
            if relative:
                cu.pos += pos
            else:
                cu.pos = pos
    
    def set_dirty(self, state=True):
        for cu in self.cus.values():
            cu.set_dirty(state)

class CellGrid:
    def __init__(self, size):
        self.size = size
        self.grid = [ [ None ]*size.w for t in range(size.h) ]
        self.dirty = []

    def __iter__(self):
        yield from self.dirty
        self.dirty = []
        
    def __getitem__(self, pos):
        if isinstance(pos, Position):
            return self.grid[pos.y][pos.x]
        return NotImplemented

    def update(self, cp):
        self.grid[cp.pos.y][cp.pos.x] = cp.cell
        self.dirty.append(cp)

    
