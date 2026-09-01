from .. import cell
from .. import const
from ..classes import Size, Margin, Padding, Border


class Component:
    """Every UI component should have Component as (one of) its base class(es)."""
    def __init__(
            self, /, *,
            align   = const.Align.LEFT, # horizontal alignment of component
            valign  = const.Align.TOP,  # vertical alignment of component
            border  = None,             # should a border be drawn around the component?
            margin  = None,             # Exterior space around component
            padding = None,             # Interior space around component content
            sizing  = const.Sizing.MAX, # How should component size itself (MAX/MIN)
            bbox    = None,             # Used by some layout managers
            fill    = None,             # If specified, fill any cells not rendered by children with this cell
            theme   = None,             # Normally set during screen initialisation, but can be set manually
            name    = None,             # Name of the component, for easy access via Screen.update
            tracked = None,             # Which cells are mouse tracked, see mouse_* methods below
    ):
        self.align = align
        self.valign = valign
        self.border = Border.from_str(border) if isinstance(border, str) else border
        self.margin = Margin.from_int(margin) if isinstance(margin, int) else margin
        self.padding = Padding.from_int(padding) if isinstance(padding, int) else padding
        self.sizing = sizing
        self.bbox = bbox
        self.fill = fill
        self.theme = theme
        self.name = name
        self.cells = cell.CellUpdates()

    def update(self, name, value, lazy=False):
        if lazy and getattr(self, name, None) is not None:
            return False
        
        if (func := getattr(self, f'update_{name}', None)) is not None:
            return func(value, lazy)
        
        setattr(self, name, value)
        return True

    def set_dirty(self, state=True):
        self.cells.set_dirty(state)
    
    def layout_hint(self, size):
        """
        Called from parent component (usually a Container) with the
        max width & height that the component is allowed.

        Return a Size object; the minimum size the component can have
        without truncating its content and/or using scrollbars.

        Each component should only account for its own size, and
        return the total of its own size and that of its parent
        component.
        """
        size = Size(0, 0)

        if self.border:
            size += self.border.to_size()
            
        if self.margin:
            size += self.margin.to_size()

        if self.padding:
            size += self.padding.to_size()
            
        return size

        
    def layout_done(self, bbox): 
        """
        Called from parent component (usually a Container) with
        the bounding box (x, y, width and height) that this component
        must render inside.

        Things like applying (v)align, truncating, adding scrollbars,
        etc happen in this step.
        """
        # Fixme: Scrollbar support, for now always just truncate
        self._bbox = bbox

        for decoration in ('padding', 'border', 'margin'): # Order is important!
            if dec := getattr(self, decoration):
                dec = dec.layout_done(bbox, self.theme)
                self.cells[decoration] = cell.Frame(bbox=bbox, frame=dec)
                bbox = bbox + dec.to_position() - dec.to_size()

        if self.fill and "fill" in self.cells:
            del self.cells['fill']

        return bbox

    def move(self, pos, relative=True):
        self.cells.move(pos, relative)

    def render(self, all=False):
        if self.fill and "fill" not in self.cells:
            if composite := self.cells.fill(self._bbox):
                self.cells['fill'] = cell.Composite(cells=self.fill, composite=composite)

        if all:
            self.cells.set_dirty()
        yield from self.cells

    def mouse_enter(self):
        """
        Called when the mouse enters one of the cells tracked by
        this component for the first time.

        The tracked attribute can be set to either True or a composite
        (set of (x, y) tuples).  If set to True, a composite will be generated as
        part of the layout workflow based on the min (top left corner) and max
        (bottom right corner) positions of rendered cells.
        
        While all components are tracked, if two (or more) components'
        tracked cells overlap, this method will only be called on the
        component in the top-most panel.
        
        This method should be overridden in a subclass; component
        intentionally does not implement any logic for this method.
        The same goes for all mouse_* methods.
        """
        ...

    def mouse_leave(self):
        """
        Called when the mouse enters a cell that is not one of the
        cells tracked by this component; or if the mouse leaves the
        associated screen altogether.
        """
        ...

    def mouse_move(self, pos):
        """
        Called with the component-relative position, when the
        mouse moves over a cells tracked by this component.
        """
        ...

    def mouse_button_down(self, pos):
        ...

    def mouse_button_up(self, pos):
        ...

    def mouse_button_click(self, pos):
        ...
        
