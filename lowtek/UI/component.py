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

        if self.fill and "component_fill" in self.cells:
            del self.cells['component_fill']
            
        return bbox


    def render(self):
        if self.fill and "component_fill" not in self.cells:
            if composite := self.cells.fill(self._bbox):
                self.cells['component_fill'] = cell.Composite(cells=self.fill, composite=composite)
            
        return self.cells

