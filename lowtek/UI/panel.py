from .container import Container
from lowtek.classes import BBox

class Panel(Container):
    """
    The Panel is the only component that can go in the root of Screen.
    
    Each panel is absolutely positioned and sized within the size of
    the surface.  Layout is run on each panel independently of every
    other panel.  Each panel is stacked on top of each other, with the
    last panel in the list being the topmost panel.
    
    Panels can be marked as modal in which case all input controls will
    only go to the topmost modal panel.  
    
    Window is a panel with user interactive controls for things like
    moving and resizing the window (if not disabled intentionally)
    """
    def __init__(
            self, /, *,
            bbox,
            **container,
    ):
        super().__init__(**container)
        self.bbox = bbox

    def layout_hint(self, size):
        super().layout_hint(self.bbox.to_size())

    def layout_done(self, bbox):
        super().layout_done(self.bbox)
        self._update_composite()

    def _update_composite(self):
        self._composite = self.bbox.to_composite()
        
    def move(self, pos):
        self.bbox += pos # FIXME: Check for out of bounds?  Or should this be done in calling screen?
        self._update_composite()
        super().move(pos)
