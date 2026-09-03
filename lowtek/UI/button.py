from .component import Component
from .. import cell
from ..classes import Size

class Button(Component):
    """A button that can be clicked."""
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
            self.cells['main'].cells = cell.str2cells(self.text, self.theme.colours.button)
            return False
        return True

    def layout_hint(self, size):
        return super().layout_hint(size) + Size(w=len(self.text)+5, h=2)

    def layout_done(self, bbox):
        bbox = super().layout_done(bbox)
        self.cells['main'] = cell.Row(
            cells=cell.str2cells(f"  {self.text}  ", self.theme.colours.button),
            pos=bbox.to_position())
        self.cells['shadow'] = cell.DropShadow(
            size = Size(len(self.text)+4, 1),
            colours = self.theme.colours.shadow,
            pos=bbox.to_position(),
        )
        self.tracked = { (t+bbox.x, bbox.y) for t in range(len(self.text)+4) }

    def mouse_enter(self):
        self.cells['main'].cells = cell.str2cells(f"  {self.text}  ", self.theme.colours.button_hover)
        return True

    def mouse_exit(self):
        self.cells['main'].cells = cell.str2cells(f"  {self.text}  ", self.theme.colours.button)
        return True
