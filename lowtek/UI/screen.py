from .component import Component
from ..cell import CellGrid

# Important note: Screen is not a component -- you cannot have a screen
# inside a screen; it will always be the top node of your UI hierarchy.
# Screen's purpose is to define a discrete area of the browser window
# to be used for Components and to capture and forward HTML DOM events
# (mouse and keyboard) to the UI.
# UI must be a list of Panel (or its descendants) objects.

class Screen:
    def __init__(self, surface, theme):
        self.surface = surface
        self.theme = theme
        self.ui = []

        Component._screen = self
        self.cells = CellGrid(size=self.size)
        self.layout_required = True

    def set_ui(self, *panels):
        self.ui = panels
        
    @property
    def size(self):
        return self.surface.size
        
    def layout(self):
        for panel in self.ui:
            panel.layout_hint(self.surface.size)
            panel.layout_done(self.surface.size.to_bbox())
        self.layout_required = False
        
    def render(self):
        if self.layout_required:
            self.layout()

        # FIXME: It should be possible to move part of this to the layout phase?
        composite = set()
        for panel in self.ui[::-1]:
            updated = 0
            update = panel.render()
            for cp in update.crop(composite): # Remove cells that overlap with previously rendered panels
                self.cells.update(cp)
                updated += 1
            #print(updated, "cells updated")
            composite |= panel.bbox.to_composite()

        self.surface.update(self.cells.get_dirty())
