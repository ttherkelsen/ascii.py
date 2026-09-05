from lowtek.surface import Surface
from lowtek import UI
from lowtek.classes import BBox, Size, Position, Callback
from lowtek.cell import Cell
from lowtek.colours import Colours
from lowtek.const import Mouse, State

import js

def button_click(component):
    print("BUTTON CLICKED")
    return False

def run(*args):
    global screen
    
    theme = UI.LightTheme()
    size = Size(80, 40)
    screen = UI.Screen(
        surface = Surface('canvas', 'ucs_9x15', size),
        theme = theme,
        ui = [
            UI.Panel(
                bbox = size.to_bbox(),
                layout = UI.layout.Absolute(),
                fill = Cell(theme.background, theme.colours.background),
            ),
            UI.Panel(
                bbox = BBox(20, 10, 20, 10),
                margin = 1,
                layout = UI.layout.Absolute(),
                fill = Cell(theme.panel_background, theme.colours.text),
                tracked = True,
                children=[
                    UI.Button(
                        text="Click Me", bbox=BBox(0, 0, 15, 4),
                        callbacks=[
                            Callback('button_click', button_click),
                        ],
                    ),
                ],
            ),
        ],
        mouse = Mouse.ENABLE | Mouse.NOCONTEXT,
    )
    
    screen.render()
    

js.addEventListener('py:all-done', run)
