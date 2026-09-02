from lowtek.surface import Surface
from lowtek import UI
from lowtek.classes import BBox, Size, Position, Callback
from lowtek.cell import Cell
from lowtek.colours import Colours
from lowtek.const import Mouse

import js

def mouse_exit(comp, x, y):
    comp.find(x).update("text", "??")
    comp.find(y).update("text", "??")
    screen.render()

def mouse_over(comp, pos, x, y):
    comp.find(x).update("text", f"{pos.x:2d}")
    comp.find(y).update("text", f"{pos.y:2d}")
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
                    UI.Label(text="??", name="x1", bbox=BBox(3, 0, 3, 1)),
                    UI.Label(text="Y:", bbox=BBox(0, 1, 2, 1)),
                    UI.Label(text="??", name="y1", bbox=BBox(3, 1, 3, 1)),
                ],
                callbacks = [
                    Callback('mouse_over', mouse_over, 'x1', 'y1'),
                    Callback('mouse_exit', mouse_exit, 'x1', 'y1'),
                ],
            ),
            UI.Panel(
                bbox = BBox(30, 5, 20, 10),
                margin = 1,
                layout = UI.layout.Absolute(),
                fill = Cell(theme.panel_background, Colours('#c0f0c0ff', '#333333ff')),
                tracked = True,
                children=[
                    UI.Label(text="X:", bbox=BBox(0, 0, 2, 1)),
                    UI.Label(text="??", name="x2", bbox=BBox(3, 0, 3, 1)),
                    UI.Label(text="Y:", bbox=BBox(0, 1, 2, 1)),
                    UI.Label(text="??", name="y2", bbox=BBox(3, 1, 3, 1)),
                ],
                callbacks = [
                    Callback('mouse_over', mouse_over, 'x2', 'y2'),
                    Callback('mouse_exit', mouse_exit, 'x2', 'y2'),
                ],
            ),
        ],
        mouse = Mouse.FULL,
    )
    
    screen.render()
    

js.addEventListener('py:all-done', run)
