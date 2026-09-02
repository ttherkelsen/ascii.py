from .. import cell
from .. import const
from ..classes import Size, Margin, Padding, Border


class Component:
    """Every UI component should have Component as (one of) its base class(es)."""
    def __init__(
            self, /, *,
            align     = const.Align.LEFT, # horizontal alignment of component
            valign    = const.Align.TOP,  # vertical alignment of component
            border    = None,             # should a border be drawn around the component?
            margin    = None,             # Exterior space around component
            padding   = None,             # Interior space around component content
            sizing    = const.Sizing.MAX, # How should component size itself (MAX/MIN)
            bbox      = None,             # Used by some layout managers
            fill      = None,             # If specified, fill any cells not rendered by children with this cell
            theme     = None,             # Normally set during screen initialisation, but can be set manually
            name      = None,             # Name of the component, for easy access via Screen.update
            tracked   = None,             # Which cells are mouse tracked, see mouse_* methods below
            callbacks = None,             # Callback events (FIXME: better description)
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
        self.tracked = tracked
        self.callbacks = callbacks if callbacks is not None else {}
        
        self.cells = cell.CellUpdates()

    def find(self, name):
        return self._names[name]
        
    def update(self, name, value, lazy=False):
        if lazy and getattr(self, name, None) is not None:
            return False
        
        if (func := getattr(self, f'update_{name}', None)) is not None:
            return func(value, lazy)
        
        setattr(self, name, value)
        return True

    def set_name_cache(self, cache):
        self._names = cache
        if self.name is not None:
            self._names[self.name] = self
    
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

        if self.tracked:
            self._mouse_tracking = None
            
        return bbox

    def move(self, pos, relative=True):
        self.cells.move(pos, relative)
        
        if relative:
            self._bbox += pos
        else:
            self._bbox.set_position(pos)
            
        if self.tracked:
            self._mouse_tracking = None

        
    def render(self, all=False):
        if self.fill and "fill" not in self.cells:
            if composite := self.cells.fill(self._bbox):
                self.cells['fill'] = cell.Composite(cells=self.fill, composite=composite)

        if all:
            self.cells.set_dirty()
        yield from self.cells

    def get_mouse_tracking(self):
        if not self.tracked:
            return {}

        if self._mouse_tracking is None:
            if self.tracked is True:
                self._mouse_tracking = { t: self for t in self._bbox.to_composite() }
            else:
                self._mouse_tracking = { t: self for t in self.tracked }

        return self._mouse_tracking
        
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
        """
        if 'mouse_enter' in self.callbacks:
            return self.callbacks['mouse_enter'](self)

    def mouse_exit(self):
        """
        Called when the mouse enters a cell that is not one of the
        cells tracked by this component; or if the mouse leaves the
        associated screen altogether.
        """
        if 'mouse_exit' in self.callbacks:
            return self.callbacks['mouse_exit'](self)

    def mouse_over(self, pos):
        """
        Called with the component-relative position, when the
        mouse moves over a cells tracked by this component.
        """
        if 'mouse_over' in self.callbacks:
            return self.callbacks['mouse_over'](self, pos)

    def mouse_button_down(self, pos):
        ...

    def mouse_button_up(self, pos):
        ...

    def mouse_button_click(self, pos):
        ...
        
