from ..cell import CellGrid
from ..classes import Position

import js

# Important note: Screen is not a component -- you cannot have a screen
# inside a screen; it will always be the top node of your UI hierarchy.
# Screen's purpose is to define a discrete area of the browser window
# to be used for Components and to capture and forward HTML DOM events
# (mouse and keyboard) to the UI.
# UI must be a list of Panel (or its descendants) objects.

class Screen:
    def __init__(
            self, /, *,
            surface,
            theme,
            ui
    ):
        self.surface = surface
        self.theme = theme
        self.ui = ui
        self.names = self.get_names()
        self.subscriptions = {}

        self.update_theme()
        self.update_layers(lazy=True)
        
        self.cells = CellGrid(size=self.size)
        self.layout_required = True

        js.addEventListener('keydown', self.event_keydown)
        js.addEventListener('keyup', self.event_keyup)

    @property
    def size(self):
        return self.surface.size

    def subscribe(self, name, callback):
         # FIXME: How to deal with multiple subs on same event?
        self.subscriptions.setdefault(name, []).append(callback)

    def check_subscriptions(self, name, event):
        if name in self.subscriptions:
            for cb in self.subscriptions[name]:
                cb(self, event)
        
    def get_names(self):
        names = {}
        for panel in self.ui:
            names |= panel.get_names()
        return names
        
    def update_theme(self):
        for panel in self.ui:
            panel.update("theme", self.theme, lazy=True)

    def update_layers(self, lazy=False):
        layer = 0
        for panel in self.ui:
            panel.update("layer", layer, lazy=lazy)
            layer = panel.layer + 1

        self.ui.sort(key=lambda x: x.layer)

    def update(self, cname, name, value, lazy=False):
        if self.names[cname].update(name, value, lazy):
            self.layout_required = True # FIXME: Only the panel that contained the changed component needs re-layout

    def event_keydown(self, event):
        #print(f"event_keydown {event.key=} {event.keyCode=} {event.charCode=} {event.code=}")
        self.check_subscriptions('keydown', event)
        event.stopPropagation();
        
    def event_keyup(self, event):
        #print(f"event_keyup {event.key=} {event.keyCode=} {event.charCode=} {event.code=}")
        event.stopPropagation();
            
    def shift_layer(self, cname, layer):
        # See FIXMEs in move()
        panel = self.names[cname]
        panel.update('layer', layer)
        idx = self.ui.index(panel)
        del self.ui[idx]
        self.ui.insert(layer, panel)
        self.update_layers()
        self.render(True)
            
    def move_panel(self, cname, pos):
        # FIXME: Should this error if the found component is not a Panel (or subclass thereof)?
        self.names[cname].move(pos)

        # FIXME: This could be optimised so that instead of rendering the entire component hierarchy, instead
        # we do:
        # 1 - Move bbox from old position to new position in CellGrid
        # 2 - Find out which panels overlap with the gap left between the old and new position
        # 3 - render only the parts of components that fit in the gap
        self.render(True)
            
    def layout(self):
        for panel in self.ui:
            panel.layout_hint(self.surface.size)
            panel.layout_done(self.surface.size.to_bbox())
        self.layout_required = False
        
    def render(self, all=False):
        if self.layout_required:
            self.layout()

        # FIXME: It should be possible to move part of this to the layout phase?
        composite = set()
        for panel in self.ui[::-1]:
            for cu in panel.render(all):
                for cp in cu:
                    # Remove cells that overlap with previously rendered panels
                    if cp.to_tuple() not in composite:
                        self.cells.update(cp)
            composite |= panel._composite # Minor optimisation
            
        self.surface.update(self.cells)
