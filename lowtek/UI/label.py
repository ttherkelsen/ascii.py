from .component import Component
from .. import cell
from ..classes import Size

class Label(Component):
    """A single-line string of text with no wrapping functionality."""
    def __init__(
            self, /, *,
            text,
            **component
    ):
        super().__init__(**component)
        self.text = text

    def update_text(self, value, lazy=False):
        oldlen = len(self.text)
        self.text = value
        if oldlen == len(self.text):
            self.cells['main'].cells = cell.str2cells(self.text, self.theme.colours.text)
            return False
        return True

    def layout_hint(self, size):
        return super().layout_hint(size) + Size(w=len(self.text), h=1)

    def layout_done(self, bbox):
        bbox = super().layout_done(bbox)
        self.cells['main'] = cell.Row(
            cells=cell.str2cells(self.text, self.theme.colours.text),
            pos=bbox.to_position())
