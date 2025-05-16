from enum import Enum, auto, IntFlag
from .cell import CellsCollection
from lowtek import const
from lowtek.classes import Rect, Size

class Component:
    """Every UI component should have Component as (one of) its base class(es)."""
    def __init__(
            /, self, *,
            align   = const.Align.LEFT, # horizontal alignment of component
            valign  = const.Align.TOP,  # vertical alignment of component
            border  = None,             # should a border be drawn around the component?
            title   = None,             # should a title be displayed at the top of the component?
            margin  = None,             # Exterior space around component
            padding = None,             # Interior space around component content
            sizing  = const.Sizing.MAX, # How should component size itself (MAX/MIN)
    ):
        self.align = align
        self.valign = valign
        self.border = border
        self.title = title
        self.margin = margin
        self.padding = padding
        self.cells = CellsCollection()


    def update_screen(self, screen):
        self._screen = screen

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
    
        
    def layout_hint(self, size):
        """
        Called from parent component (usually a Container) with the max width & height that the
        component is allowed.

        Return a Size object:
        - h(eight) & w(idth) is the minimum size the component can have without truncating its
          content and/or using scrollbars
        """
        return Size(w=self.cells.main.w, h=self.cells.main.h) + self.component_size

        
    def layout_done(self, bbox):
        """
        Called from parent component (usually a Container) with the bounding box (x, y, width and height,
        usually x = y = 0) that this component must render inside.

        Things like applying (v)align, truncating, adding scrollbars, etc happen in this step.
        """
        # Fixme: Scrollbar support, for now always just truncate
        self._bbox = bbox
        theme = self._screen.theme
        size = Size(w=self.cells.main.w, h=self.cells.main.h)
        if self.padding:
            self.cells.translate_all(x=self.padding.w, y=self.padding.n)
            size.expand(self.padding)
            self.cells.padding = Cells.frame(
                size=size,
                rect=self.padding,
                char=theme.background,
                colours=theme.colours.padding,
            )
        if self.border:
            self.cells.translate_all(x=self.border.w and 1, y=self.border.n and 1)
            size.expand_1(self.border)
            self.cells.border = Cells.border(
                size=size,
                rect=self.border,
                colours=theme.colours.border,
            )
        if self.margin:
            self.cells.translate_all(x=self.margin.w, y=self.margin.n)
            size.expand(self.margin)
            self.cells.margin = Cells.frame(
                size=size,
                rect=self.margin,
                char=theme.background,
                colours=theme.colours.margin,
            )


    def render(self):
        pass


