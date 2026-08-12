from .component import Component
from .. import cell

class Fill(Component):
    """A component that expands to fill the entire available space with a single glyph."""
    def __init__(
            self, /, *,
            cell,        # Mandatory -- the cell used to fill with
            **component,
    ):
        super().__init__(**component)
        self.cell = cell

    def update_cell(self, value, lazy=False):
        self.cells['main'].cells = value
        return False
        
    def layout_done(self, bbox):
        cbbox = super().layout_done(bbox)
        self.cells['main'] = cell.BBoxFill(cells=self.cell, bbox=cbbox)
        

    
        
