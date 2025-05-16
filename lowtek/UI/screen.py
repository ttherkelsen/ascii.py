import .utils

# Important note: Screen is not a component -- you cannot have a screen
# inside a screen; it will always be the top node of your UI hierarchy.
# Screen's purpose is to define a discrete area of the browser window
# to be used for Components and to capture and forward HTML DOM events
# (mouse and keyboard) to the UI.

class Screen:
    def __init__(self, size, jsid, theme, ui):
        self.size = size
        self.jsid = jsid
        self.theme = theme
        self.ui = ui
        
        self.ui.update_screen(self)
        self.surface = Surface(jsid, size, theme.font_name, Cell(self.theme.background, self.theme.colours.text))
        self.layout_required = True

    def layout(self):
        self.ui.layout_hint(self.size)
        self.ui.layout_done(self.surface, self.size.to_bbox())
        
    def render(self):
        if self.layout_required:
            self.layout()
            
        self.ui.render()
