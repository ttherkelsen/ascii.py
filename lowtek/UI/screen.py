import .utils

# Important note: Screen is not a component -- you cannot have a screen
# inside a screen; it will always be the top node of your UI hierarchy.
# Screen's purposes is to act as a bridge between Components (that know
# nothing about how things are rendered graphically) and a Surface (which
# only knows how to render things graphically).
# This abstraction exists so that it is possible to replace both
# Component and Surface with other systems without (for example using a
# surface that uses HTML DOM instead of Canvas2D) having to redo the
# entire application.

class Screen:
    def __init__(self, surface, theme, ui):
        self.surface = surface
        self.theme = theme
        self.ui = ui

        self.surface.set_event_callback(self)
        self.init()

    def surface_event(self, event, data):
        if self.ui.mouse_event(event, data):
            # Mouse event caused a component to change, do another render cycle
            self.render()

    def init(self):
        self.cells = [
            Cell(self.theme.background, self.theme.colours.text) for t in range(self.surface.width * self.surface.height)
        ]
        self.render_cells()

    def render_cells(self):
        # FIXME: This should be generalised/optimised to only render the parts of
        # the screen that actually changed, not the entire screen
        self.surface.write_cells(0, 0, self.cells)

    def update_cells(self, update):
        x = update.x
        y = update.y

        if 0 > x > self.surface.width or 0 > y > self.surface.height:
            utils.debug("update_cells called with illegal x or y", x, y)
            return

        ox = x
        for cell in update.cells:
            self.cells[y * self.surface.width + x] = cell
            x += 1
            if ((ox - x) == update.w):
                x = ox;
                y += 1

    def render(self):
        for update in self.ui.render(self.surface.width, self.surface.height, self.theme):
            self.update_cells(update)
        self.render_cells()
