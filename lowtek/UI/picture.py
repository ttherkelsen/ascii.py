from .component import Component
from .. import cell
from ..classes import Size

class Picture(Component):
    """A 2d picture with characters translated according to the given palette."""
    def __init__(
            self, /, *,
            imagedata,
            palette,
            colours = None,
            **component,
    ):
        super().__init__(**component)
        self.imagedata = imagedata
        self.palette = palette
        self.colours = colours

    def layout_hint(self, size):
        return super().layout_hint(size) + Size(w=len(self.imagedata[0]), h=len(self.imagedata))

    def layout_done(self, bbox):
        bbox = super().layout_done(bbox)
        self.cells['main'] = cell.Image(
            imagedata=self.imagedata,
            palette=self.palette,
            colours=self.colours or self.theme.colours.panel_background,
            pos=bbox.to_position(),
        )
