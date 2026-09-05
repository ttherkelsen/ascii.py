from .component import Component
from .. import cell
from ..classes import Size, Position
from ..const import MouseButton, State

class Button(Component):
    """A button that can be clicked."""
    def __init__(
            self, /, *,
            text,
            state = State.UP,
            **component
    ):
        super().__init__(**component)
        self.text = text
        self.state = state

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
        self._button_bbox = bbox
        self.render_state()
        if not (self.state & State.DISABLED):
            self.tracked = { (t+bbox.x, bbox.y) for t in range(len(self.text)+4) }

    def render_text(self, colours, offset=None):
        pos = self._button_bbox.to_position()
        if offset:
            pos += offset
        self.cells['main'] = cell.Row(
            cells=cell.str2cells(f"  {self.text}  ", colours),
            pos=pos)

    def render_dropshadow(self, clear=False):
        if clear:
            self.cells['shadow'] = cell.Row(
                cells=cell.str2cells(" "*(len(self.text)+4), clear),
                pos=self._button_bbox.to_position() + Position(1, 1),
            )
            self.cells['clear'] = cell.Row(
                cells=cell.str2cells(" ", clear),
                pos=self._button_bbox.to_position(),
            )
        else:
            if 'clear' in self.cells:
                del self.cells['clear']
            self.cells['shadow'] = cell.DropShadow(
                size = Size(len(self.text)+4, 1),
                colours = self.theme.colours.shadow,
                pos=self._button_bbox.to_position(),
            )
            
    def render_state(self):
        if self.state & State.DISABLED:
            c = self.theme.colours.button_disabled
        elif self.state & State.HOVER:
            c = self.theme.colours.button_hover
        else:
            c = self.theme.colours.button

        if self.state & State.DOWN:
            self.render_text(c, offset=Position(1, 0))
            self.render_dropshadow(self.theme.colours.text)
        else:
            self.render_text(c)
            self.render_dropshadow()
                    
        
    def mouse_enter(self):
        if self.state & State.DISABLED:
            return False

        self.state |= State.HOVER
        self.cells['main'].cells = cell.str2cells(f"  {self.text}  ", self.theme.colours.button_hover)
        super().mouse_enter()
        return True

    def mouse_exit(self):
        if self.state & State.DISABLED:
            return False
        
        self.state &= ~State.HOVER
        self.cells['main'].cells = cell.str2cells(f"  {self.text}  ", self.theme.colours.button)
        super().mouse_exit()
        return True

    def mouse_button_down(self, button, pos):
        if self.state & State.DISABLED or button != MouseButton.LEFT:
            return False

        self.state |= State.DOWN
        self.render_state()
        super().mouse_button_down(button, pos)
        return True

    def mouse_button_up(self, button, pos):
        if self.state & State.DISABLED or button != MouseButton.LEFT:
            return False
        
        self.state &= ~State.DOWN
        self.render_state()
        super().mouse_button_up(button, pos)
        return True

    def mouse_button_click(self, button, pos):
        if self.state & State.DISABLED or button != MouseButton.LEFT:
            return False

        super().mouse_button_click(button, pos)
        if 'button_click' in self.callbacks:
            return self.callbacks['button_click'].run(self)
        return False
