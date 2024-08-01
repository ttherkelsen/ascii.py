from types import SimpleNamespace
from ..colours import Colours

class Theme:
    pass

class LightTheme(Theme):
    def __init__(self):
        self.colours = SimpleNamespace(
            text = Colours("#c0c0c0ff", "#333333ff"),
            button = Colours("#30c030ff", "#000000ff"),
            button_hover = Colours("#30c0c0ff", "#000000ff"),
            )
        self.border = 1
        self.shadow_offset = [ 2, 1 ]
        self.background = " "

        
class DarkTheme(Theme):
    def __init__(self):
        self.colours = SimpleNamespace(
            text = Colours("#000000ff", "#f0f0f0ff"),
            button = Colours("#30c030ff", "#000000ff"),
            button_hover = Colours("#30c0c0ff", "#000000ff"),
            )
        self.border = 1
        self.shadow_offset = [ 2, 1 ]
        self.background = " "

