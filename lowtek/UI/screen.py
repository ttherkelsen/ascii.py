from ..cell import CellGrid

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

        self.update_theme()
        
        self.cells = CellGrid(size=self.size)
        self.layout_required = True

    @property
    def size(self):
        return self.surface.size
    
    def get_names(self):
        names = {}
        for panel in self.ui:
            names |= panel.get_names()
        return names
        
    def update_theme(self):
        for panel in self.ui:
            panel.update("theme", self.theme, lazy=True)

    def update(self, cname, name, value, lazy=False):
        if self.names[cname].update(name, value, lazy):
            self.layout_required = True # FIXME: Only the panel that contained the changed component needs re-layout

    def move(self, cname, pos):
        print(self.names[cname].bbox)
        self.names[cname].bbox += pos
        print(self.names[cname].bbox)
        self.layout_required = True
        
            
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
            update = panel.render()
            for cp in update.crop(composite): # Remove cells that overlap with previously rendered panels
                self.cells.update(cp)
            composite |= panel._composite # Minor optimisation

        self.surface.update(self.cells.get_dirty())
