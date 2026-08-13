from .component import Component
from .. import cell 
from ..classes import Size, Position, BBox
from ..glyphs import WIDE

# FIXME: This component should probably be generalised into Table component
class GlyphPage(Component):
    SIZE = Size(w=32+15+3+6, h=16+15+1+2)
    POS = Position(x=6, y=1)
    
    """Display the specified unicode page of glyphs."""
    def __init__(
            self, /, *,
            page,
            font,
            **component,
    ):
        super().__init__(**component)
        self.page = page
        self.font = font

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
                cells=cell.str2cells(f"{(self.page % 0xffff00)>>8:04x}yx", self.theme.colours.text),
                pos=bbox.to_position()),
            cell.Row(
                cells=cell.str2cells("  ".join([ f"{t:x}" for t in range(16) ]), self.theme.colours.text),
                pos=bbox.to_position() + Position(8, 0),
                ),
            cell.BBox(
                cells=cell.str2cells("  ".join([ f"{t:x}x" for t in range(16) ]), self.theme.colours.text),
                bbox=BBox(0, 0, 2, 31) + bbox.to_position() + Position(4, 2),
                ),
        ]
        + [
            cell.Row(
                cells=cell.ints2cells(
                    [
                        ( self.page+u*16+t if self.page+u*16+t in self.font.glyphs else 32,
                          self.page+u*16+t+WIDE if self.page+u*16+t+WIDE in self.font.glyphs else 32,
                          32 )
                        for t in range(16)
                    ],
                    self.theme.colours.text
                ),
                pos=bbox.to_position() + Position(8, u*2+2),
            )
            for u in range(16)
        ]
        )
        super().layout_done(bbox)
