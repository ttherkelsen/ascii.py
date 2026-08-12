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

    def update_theme(self, theme, lazy=False):
        self.theme = theme
            
        for child in self.children:
            child.update("theme", theme, lazy)

    def get_names(self):
        return { child.name: child for child in self.children + [ self ] if getattr(child, 'name', None) is not None }
            
    def layout_hint(self, size):
        psize = super().layout_hint(size)
        csize = self.layout.hint(size - psize, self.children)
        return csize + psize

    def layout_done(self, bbox):
        pbbox = super().layout_done(bbox)
        self.layout.done(pbbox, self.children)
        for idx, child in enumerate(self.children):
            self.cells[f"child_{idx}"] = child.render()

    
