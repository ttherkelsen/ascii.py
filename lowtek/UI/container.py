from .component import Component
from .layout.row import Row
from .. import cell

class Container(Component):
    """
    The Container is a special Component whose only job is to
    contain other components.  Containers always use a layout manager
    (defaults to the Rows layout) and it is this manager which will
    handle all layout logic.
    """
    def __init__(
            self, /, *,
            children = None, # List of child components
            layout   = None, # Layout manager, defaults to Row()
            **component,
    ):
        super().__init__(**component)
        self.children = children if children is not None else []
        self.layout = layout or Row()

    def set_name_cache(self, cache):
        super().set_name_cache(cache)
        for child in self.children:
            child.set_name_cache(cache)
        
    def update_theme(self, theme, lazy=False):
        self.theme = theme
            
        for child in self.children:
            child.update("theme", theme, lazy)
            
    def layout_hint(self, size):
        psize = super().layout_hint(size)
        csize = self.layout.hint(size - psize, self.children)
        return csize + psize

    def layout_done(self, bbox):
        pbbox = super().layout_done(bbox)
        self.layout.done(pbbox, self.children)

    def move(self, pos, relative=True):
        super().move(pos, relative)
        for c in self.children:
            c.move(pos, relative)
        
    def render(self, all=False):
        yield from super().render(all)
        for child in self.children:
            yield from child.render(all)

    
    def get_mouse_tracking(self):
        tracking = super().get_mouse_tracking()
        for child in self.children:
            tracking |= child.get_mouse_tracking() # Children mouse tracking override container tracking
        return tracking
