from enum import Enum, auto
from .classes import Rect
from argparse import Namespace

class Cell:
    def __init__(self, glyph, colours):
        self.glyph = glyph if isinstance(glyph, int) else ord(glyph)
        self.colours = colours

        
class CellUpdate:
    pass


class LineDrawing:
    """FIXME: Simplify this by turning it into a dict of frozenset keys:
    LD_CHARS = {
        frozenset("N"): 0x2551,
        frozenset("n"): 0x2502,
        ...etc...
    }
    That way you can get at the keys with LD_CHARS[frozenset("WEs")] and have
    easy support for single, double and single+double line drawing characters, and
    other characters could be used to support the other types of line drawing
    (dotted lines, fat lines, curved corners, etc)
    """
    LD_CHARS = (
        # Single
        #  0        1       2       3       4       5       6       7       8       9
        #  None     N       E       NE      W       NW      WE      NWE     S       NS
        ( 0x2573, 0x2502, 0x2500, 0x2514, 0x2500, 0x2518, 0x2500, 0x2534, 0x2502, 0x2502,
        #  10       11      12      13      14      15
        #  ES       NES     WS      NWS     WES     NESW
          0x250c, 0x251c, 0x2510, 0x2524, 0x252c, 0x253c ),
        
        # Double
        #  0        1       2       3       4       5       6       7       8       9
        #  None     N       E       NE      W       NW      WE      NWE     S       NS
        ( 0x2573, 0x2551, 0x2550, 0x2554, 0x2550, 0x255d, 0x2550, 0x2569, 0x2552, 0x2552,
        #  10       11      12      13      14      15
        #  ES       NES     WS      NWS     WES     NESW
          0x2554, 0x2560, 0x2557, 0x2563, 0x2566, 0x256c ),
    )
    N = 1
    E = 2
    W = 4
    S = 8
    
    @classmethod
    def get_char(cls, edges_open, char_type):
        o = 0
        for edge in edges_open:
            o |= getattr(cls, edge)
        return cls.LD_CHARS[char_type][0]


class CellsCollection:
    def __init__(self):
        self.updates = None

    @property
    def initialised(self):
        return self.cc is not None

    def get_cells(self):
        for k, v in self.__dict__.items():
            if not isinstance(v, Cells):
                continue
            yield v
    
    def add_cells(self, name, cells):
        if self.cc is None:
            self.cc = Namespace()
        setattr(self.cc, name, cells)


class CellsType(Enum):
    LINE = auto()  # A single line of cells (either horizontal or vertical)
    FRAME = auto() # A rectangular 
    BOX = auto()


class Cells:
    def __init__(self, cells, w=None, h=None, x=0, y=0, t=CellsType.BOX):
        # FIXME: Add checking for w and h based on what t is
        self.cells = cells
        self.w = w
        self.h = h
        self.x = 0
        self.y = 0
        self.t = t
        
        # set of (x, y) tuples of cell coordinates that have updates since last call to render
        # if None, means the cells have not been rendered yet and thus all cells need to be
        # rendered.  Empty set() means cells have been rendered at least once but have not
        # changed since last render and thus nothing needs to be rendered.
        self.updates = None


    def translate(self, x=0, y=0):
        self.x += x
        self.y += y
        

    def truncate(self, w, h):
        # FIXME
        if h < self.h:
            del self.cells[h:]
            self.h = h

        if w < self.w:
            for row in cells:
                del row[w:]
            self.w = w


    def expand(self, rect, cell):
        self.w += rect.w + rect.e
        for row in self.cells:
            row[0:0] = [ cell ]*rect.w
            row.extend([ cell ]*rect.e)

        if rect.n:
            self.cells[0:0] = [ [ cell ]*self.w for t in range(rect.n) ]
        if rect.s:
            self.cells.extend([ [ cell ]*self.w for t in range(rect.s) ])
        self.h += rect.n + rect.s


    def add_border(self, rect, colours):
        # FIXME: This assumes full NESW border 
        self.expand(Rect(1), None)

        # Corners
        self.cells[0][0] = Cell(LineDrawing.get_char("SE", rect.t), colours)
        self.cells[0][-1] = Cell(LineDrawing.get_char("SW", rect.t), colours)
        self.cells[-1][0] = Cell(LineDrawing.get_char("NE", rect.t), colours)
        self.cells[-1][-1] = Cell(LineDrawing.get_char("NW", rect.t), colours)

        # Horizontal lines
        cell = Cell(LineDrawing.get_char("WE", rect.t), colours)
        self.cells[0][1:-1] = [ cell ]*(self.w - 2)
        self.cells[-1][1:-1] = [ cell ]*(self.w - 2)

        # Vertical lines
        cell = Cell(LineDrawing.get_char("NS", rect.t), colours)
        for row in range(self.h - 2):
            self[row+1][0] = self[row+1][-1] = cell
        

    def merge(self, other, x=0, y=0):
        for oy in range(other.h):
            for ox in range(other.w):
                self.cells[y+oy][x+ox] = other.cells[oy][ox]


    @classmethod
    def fill(cls, char, colours, w, h):
        return cls([ [ Cell(char, colours) for t in range(w) ] for u in range(h) ], w, h)
    

    @classmethod
    def frame(cls, size, rect, char, colours):
        pass
    
    @classmethod
    def from_str(cls, string, colours):
        # FIXME: Add support for newlines in string?
        return cls([ Cell(t, colours) for t in string ], len(string), 1)
