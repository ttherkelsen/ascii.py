from .component import Component
from .cell import Cells

class Label(Component):
    """A single-line string of text with no wrapping functionality."""
    def __init__(self, text, **component):
        super().__init__(**component)
        self.text = text
        # FIXME: Support passing an array of cells in text argument?
        # FIXME: Trigger re-layout if text is changed

    def render(self):
        return super().render(Cells.from_str(text, self._screen.theme.colours.text)) if self.dirty else []
