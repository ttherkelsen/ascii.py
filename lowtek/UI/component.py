from enum import Enum, auto, IntFlag

class Component:
    """Every UI component should have Component as (one of) its base class(es)."""
    def __init__(
            /, self, *,
            align   = Align.LEFT, # horizontal alignment of component
            valign  = Align.TOP,  # vertical alignment of component
            border  = None,       # should a border be drawn around the component?
            title   = None,       # should a title be displayed at the top of the component?
            margin  = None,       # Exterior space around component
            padding = None,       # Interior space around component content
            sizing  = Sizing.MAX, # True/False; component takes up as much/little space as possible
    ):
        self.align = align
        self.valign = valign
        self.border = border
        self.title = title
        self.margin = margin
        self.padding = padding

    @property
    def component_size:
        """Return combined size of everything except component content cells (borders, margin, padding, etc)"""
        h = 0
        w = 0

        if self.border:
            if self.border.n:
                h += 1
            if self.border.s:
                h += 1
            if self.border.e:
                w += 1
            if self.border.w:
                w += 1

        if self.margin:
            h += self.margin.n + self.margin.s
            w += self.margin.e + self.margin.w

        if self.padding:
            h += self.padding.n + self.padding.s
            w += self.padding.e + self.padding.w

        return Size(w=w, h=h)
    
        
    def layout_hint(self, width, height):
        """
        Called from parent component (usually a Container) with the max width & height that the
        component is allowed.

        Return a Size object:
        - h(eight) & w(idth) is the minimum size the component can have without truncating its
          content and/or using scrollbars
        """
        return Size(w=self.cells.w, h=self.cells.h) + self.component_size

        
    def layout_done(self, bbox):
        """
        Called from parent component (usually a Container) with the bounding box (x, y, width and height)
        that this component must render inside.

        Things like applying (v)align, truncating, adding scrollbars, etc happen in this step.
        """
        # Fixme: Scrollbar support, for now always just truncate
        self._bbox = bbox
        theme = self._screen.theme
        if self.padding:
            self.cells.expand(self.padding, Cell(theme.background, theme.colours.padding))
        if self.border:
            self.cells.add_border(self.border, theme.colours.border)
        if self.margin:
            self.cells.expand(self.margin, Cell(theme.background, theme.colours.margin))

        


    def render(self):
        pass


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
    SINGLE = 0
    DOUBLE = 1
    

class Rect:
    def __init__(self, nesw=0, n=0, e=0, s=0, w=0, t=None):
        if nesw:
            # Special case, Rect(int > 0) == all sides of rectangle
            n = e = s = w = nesw
        self.n = n
        self.e = e
        self.s = s
        self.w = w
        self.t = t


class Size:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def __add__(self, other):
        if other is not Size:
            return NotImplemented

        return Size(self.w + other.w, self.h + other.h)

class BBox:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
