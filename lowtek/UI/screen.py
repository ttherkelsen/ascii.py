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
        self.rerender = False

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
