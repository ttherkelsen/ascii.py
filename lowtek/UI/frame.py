from .container import Container
from lowtek.classes import BBox

class Frame(Container):
    """
    The Frame is the only component that can go in the root of Screen.
    
    Each frame is absolutely positioned and sized within the size of
    the surface.  Layout is run on each frame independently of every
    other frame.  Each frame is stacked on top of each other, with the
    last frame in the list being the topmost frame.
    
    Frames can be marked as modal in which case all input controls will
    only go to the topmost modal frame.  
    
    Window is a frame with user interactive controls for things like
    moving and resizing the window (if not disabled intentionally)
    """
    def __init__(self, bbox=None, **container):
        super().__init__(**container)
        self.bbox = bbox if bbox is not None else BBox(0, 0, self._screen.size.w, self._screen.size.h)

    def layout_hint(self, size):
        super().layout_hint(self.bbox.to_size())

    def layout_done(self, bbox):
        super().layout_done(self.bbox)
