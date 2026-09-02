from ..cell import CellGrid
from ..classes import Position
from ..const import Mouse

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
            ui,
            mouse = Mouse.NONE,
    ):
        self.surface = surface
        self.theme = theme
        self.ui = ui
        self.mouse = mouse
        self.names = {}

        self.update_ui()
        self.update_layers(lazy=True)
        
        self.cells = CellGrid(size=self.size)
        self.layout_required = True
        self.prevcursor = None
        self.prevcomponent = None

        # FIXME: Make keyboard interaction work
        #js.addEventListener('keydown', self.js_event_keydown)
        #js.addEventListener('keyup', self.js_event_keyup)

        if mouse & Mouse.ENABLE:
            self.surface.canvas.addEventListener('mouseenter', self.js_event_mouseenter)
            self.surface.canvas.addEventListener('mouseleave', self.js_event_mouseleave)
            self.surface.canvas.addEventListener('mousemove', self.js_event_mousemove)
        

    @property
    def size(self):
        return self.surface.size

    def update_ui(self):
        for panel in self.ui:
            panel.update("theme", self.theme, lazy=True)
            panel.set_name_cache(self.names)

    def update_layers(self, lazy=False):
        layer = 0
        for panel in self.ui:
            panel.update("layer", layer, lazy=lazy)
            layer = panel.layer + 1

        self.ui.sort(key=lambda x: x.layer)

    def update(self, cname, name, value, lazy=False):
        if self.names[cname].update(name, value, lazy):
            self.layout_required = True # FIXME: Only the panel that contained the changed component needs re-layout

    def js_event_keydown(self, event):
        event.stopPropagation();
        
    def js_event_keyup(self, event):
        event.stopPropagation();

    def js_event_mouseenter(self, event):
        # Nothing to do here -- we don't register cell position here
        event.stopPropagation();

    def js_event_mousemove(self, event):
        event.stopPropagation();
        
        pos = Position(
            x = event.offsetX // self.surface.font.width,
            y = event.offsetY // self.surface.font.height,
        )

        t = pos.to_tuple()
        if self.prevcursor != pos:
            if self.prevcursor is not None:
                if t in self.mouse_tracking:
                    if (comp := self.mouse_tracking[t]) != self.prevcomponent:
                        if self.prevcomponent is not None:
                            self.event_component_mouseleave(self.prevcomponent)
                        self.prevcomponent = comp
                        self.event_component_mouseenter(self.prevcomponent)
                    self.event_component_mousemove(self.prevcomponent, pos)
                elif self.prevcomponent is not None:
                    self.event_component_mouseleave(self.prevcomponent)
                    self.prevcomponent = None
                self.event_cell_mouseleave(self.prevcursor)
            self.event_cell_mouseenter(pos)
            self.prevcursor = pos
            
    def js_event_mouseleave(self, event):
        event.stopPropagation();
        
        if self.prevcursor is not None:
            self.event_cell_mouseleave(self.prevcursor)
            self.prevcursor = None
            if self.prevcomponent is not None:
                self.event_component_mouseleave(self.prevcomponent)
                self.prevcomponent = None

    def event_cell_mouseenter(self, pos):
        #print("event_cell_mouseenter", pos)
        pass
        
    def event_cell_mouseleave(self, pos):
        #print("event_cell_mouseleave", pos)
        pass

    def event_component_mouseenter(self, component):
        component.mouse_enter()

    def event_component_mouseleave(self, component):
        component.mouse_exit()

    def event_component_mousemove(self, component, pos):
        component.mouse_over(pos)
    
    def shift_layer(self, cname, layer):
        # See FIXMEs in move()
        panel = self.names[cname]
        panel.update('layer', layer)
        idx = self.ui.index(panel)
        del self.ui[idx]
        self.ui.insert(layer, panel)
        self.update_layers()
        self.render(True)
            
    def move_panel(self, cname, pos, relative=True):
        # FIXME: Should this error if the found component is not a Panel (or subclass thereof)?
        self.names[cname].move(pos, relative)

        # FIXME: This could be optimised so that instead of rendering the entire component hierarchy, instead
        # we do:
        # 1 - Move bbox from old position to new position in CellGrid
        # 2 - Find out which panels overlap with the gap left between the old and new position
        # 3 - render only the parts of components that fit in the gap
        self.render(True)
            
    def layout(self):
        if self.mouse & Mouse.ENABLE:
            self.mouse_tracking = {}
            
        for panel in self.ui[::-1]:
            panel.layout_hint(self.surface.size)
            panel.layout_done(self.surface.size.to_bbox())
            if self.mouse & Mouse.ENABLE:
                self.mouse_tracking = panel.get_mouse_tracking() | self.mouse_tracking
        self.layout_required = False
        
    def render(self, all=False):
        if self.layout_required:
            self.layout()

        # FIXME: It should be possible to move part of this to the layout phase?
        composite = set()
        for panel in self.ui[::-1]:
            if panel.hidden:
                continue
            for cu in panel.render(all):
                for cp in cu:
                    # Remove cells that overlap with previously rendered panels
                    if cp.to_tuple() not in composite:
                        self.cells.update(cp)
            composite |= panel._composite # Minor optimisation
            
        self.surface.update(self.cells)
