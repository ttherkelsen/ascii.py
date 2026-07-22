from .component import Component
from ..cell import CellUpdateBBoxFill

class Fill(Component):
    """A component that expands to fill the entire available space with a single glyph."""
    def __init__(self, cell, **component):
        super().__init__(**component)
        self.cell = cell

    def update_cell(self, value):
        self.cells.main.cells = value
        self.cells.main.dirty = True
        
    # FIXME: Support borders etc
    def layout_hint(self, size):
        return size

    def layout_done(self, bbox):
        self.cells.main = CellUpdateBBoxFill(self.cell, bbox)

    
        
