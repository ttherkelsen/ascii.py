from lowtek.surface import Surface
from lowtek import UI
from lowtek.classes import BBox, Size, Position
from lowtek.cell import Cell
from lowtek.colours import Colours
from lowtek.const import Mouse

import js

def mouse_exit(comp):
    comp.find('x').update("text", "??")
    comp.find('y').update("text", "??")
    screen.render()

def mouse_over(comp, pos):
    comp.find('x').update("text", f"{pos.x:2d}")
    comp.find('y').update("text", f"{pos.y:2d}")
    screen.render()

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
                    UI.Label(text="X:", bbox=BBox(0, 0, 2, 1)),
                    UI.Label(text="??", name="x", bbox=BBox(3, 0, 3, 1)),
                    UI.Label(text="Y:", bbox=BBox(0, 1, 2, 1)),
                    UI.Label(text="??", name="y", bbox=BBox(3, 1, 3, 1)),
                ],
                callbacks = {
                    'mouse_over': mouse_over,
                    'mouse_exit': mouse_exit,
                },
            ),
        ],
        mouse = Mouse.FULL,
    )
    
    screen.render()
    

js.addEventListener('py:all-done', run)
