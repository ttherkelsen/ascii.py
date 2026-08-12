from .component import Component
from .. import cell 
from ..classes import Size, Position

# FIXME: This component should probably be generalised into Table component
class GlyphPage(Component):
    SIZE = Size(w=16+15+3+4, h=16+15+1+2)
    POS = Position(x=4, y=1)
    
    """Display the specified unicode page of glyphs."""
    def __init__(
            self, /, *,
            page,
            **component,
    ):
        super().__init__(**component)
        self.page = page

    def layout_hint(self, size):
        return self.SIZE

    def layout_done(self, bbox):
        self.cells['main'] = cell.CellUpdates([
            cell.CrossLD(
                pos=bbox.to_position(),
                size=self.SIZE,
                colours=self.theme.colours.border,
                center=self.POS),
            cell.Row(
                cells=cell.str2cells(f"{(self.page % 0xff00)>>8:x}yx", self.theme.colours.text),
                pos=bbox.to_position()),
            cell.Row(
                cells=cell.str2cells(" ".join([ f"{t:x}" for t in range(16) ]), self.theme.colours.text),
                pos=bbox.to_position() + Position(6, 0),
                ),
            cell.Column(
                cells=cell.str2cells(" ".join([ f"{t:x}" for t in range(16) ]), self.theme.colours.text),
                pos=bbox.to_position() + Position(3, 2),
                ),
        ] + [
            cell.Row(
                cells=cell.str2cells(
                    " ".join([ chr(self.page+u*16+t) for t in range(16) ]), self.theme.colours.text
                ),
                pos=bbox.to_position() + Position(6, u*2+2),
            )
            for u in range(16)
        ])
        super().layout_done(bbox)
