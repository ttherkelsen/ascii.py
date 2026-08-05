from .component import Component
from .layout.row import Row
from ..cell import CellUpdates

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
        
    def layout_hint(self, size):
        # FIXME: Take decorations (border, padding, margin) into account
        csize = self.layout.hint(size - self.component_size, self.children)
        return csize + self.component_size

    def layout_done(self, bbox):
        self.layout.done(bbox, self.children)
        self.cells.main = CellUpdates([ t.render() for t in self.children ])
        super().layout_done(bbox)

    
