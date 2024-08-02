from types import SimpleNamespace
from ..colours import Colours

class Theme:
    pass

class LightTheme(Theme):
    def __init__(self):
        self.colours = SimpleNamespace(
            text = Colours("#c0c0c0ff", "#333333ff"),
            padding = Colours("#c0c0c0ff", "#333333ff"),
            margin = Colours("#c0c0c0ff", "#333333ff"),
            border = Colours("#c0c0c0ff", "#333333ff"),
            button = Colours("#30c030ff", "#000000ff"),
            button_hover = Colours("#30c0c0ff", "#000000ff"),
            )
        self.background = " "

        
class DarkTheme(Theme):
    def __init__(self):
        self.colours = SimpleNamespace(
            text = Colours("#000000ff", "#f0f0f0ff"),
            padding = Colours("#000000ff", "#f0f0f0ff"),
            margin = Colours("#000000ff", "#f0f0f0ff"),
            border = Colours("#000000ff", "#f0f0f0ff"), 
            button = Colours("#30c030ff", "#000000ff"),
            button_hover = Colours("#30c0c0ff", "#000000ff"),
            )
        self.background = " "

