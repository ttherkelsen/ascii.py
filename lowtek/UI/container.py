from .component import Component
from .layout.row import Row

class Container(Component):
    """
    The Container is a special Component whose only job is to
    contain other components.  Containers always use a layout manager
    (defaults to the Rows layout) and it is this manager which will
    handle all layout logic.
    """
    def __init__(self, children=None, layout=Row(), **component):
        super().__init__(**component)
        self.children = children if children is not None else []
        self.layout = layout

    def update_screen(self, screen):
        super().update_screen(screen)
        for child in self.children:
            child._screen = screen

    def layout_hint(self, size):
        # FIXME: Take decorations (border, padding, margin) into account
        csize = self.layout.hint(size - self.component_size, self.children)
        return csize + self.component_size

    def layout_done(self, parent_surface, bbox):
        # FIXME: Take decorations into account
        self.surface = parent_surface.add_child(bbox)
        self.layout.done(self.surface, bbox, self.children)
