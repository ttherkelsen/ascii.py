from argparse import Namespace
from ..colours import Colours

class Theme:
    pass

class LightTheme(Theme):
    def __init__(self):
        self.colours = Namespace(
            text = Colours("#c0c0c0ff", "#333333ff"),
            padding = Colours("#c0c0c0ff", "#333333ff"),
            margin = Colours("#c0c0c0ff", "#333333ff"),
            border = Colours("#c0c0c0ff", "#333333ff"),
            button = Colours("#30c030ff", "#000000ff"),
            button_hover = Colours("#30c0c0ff", "#000000ff"),
            background = Colours("#a0a0a0ff", "#333333ff"),
            panel_background = Colours("#c0c0c0ff", "#333333ff"),
            mouse = Colours("#c0c0ff80", "#33333380"),
        )
        self.margin = " "
        self.padding = " "
        self.background = "."
        self.panel_background = " "
        self.font_name = "ucs_9x15"
        self.mouse = " " #"\u2591"

        
class DarkTheme(Theme):
    def __init__(self):
        self.colours = Namespace(
            text = Colours("#000000ff", "#f0f0f0ff"),
            padding = Colours("#000000ff", "#f0f0f0ff"),
            margin = Colours("#000000ff", "#f0f0f0ff"),
            border = Colours("#000000ff", "#f0f0f0ff"), 
            button = Colours("#30c030ff", "#000000ff"),
            button_hover = Colours("#30c0c0ff", "#000000ff"),
            background = Colours("#000000ff", "#c0c0c0ff"),
            panel_background = Colours("#000000ff", "#f0f0f0ff"),
            mouse = Colours("#00000080", "#f0f0f080"),
        )
        self.margin = " "
        self.padding = " "
        self.background = "."
        self.panel_background = " "
        self.font_name = "ucs_9x15"
        self.mouse = "\u2591"

