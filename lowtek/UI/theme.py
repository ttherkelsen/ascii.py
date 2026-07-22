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
        )
        self.background = "."
        self.frame_background = " "
        self.font_name = "ucs_9x15"

        
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
        )
        self.background = "."
        self.frame_background = " "
        self.font_name = "ucs_9x15"

