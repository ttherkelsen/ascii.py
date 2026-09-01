from lowtek.surface import Surface
from lowtek import UI
from lowtek.classes import BBox, Size, Position
from lowtek.cell import Cell
from lowtek.colours import Colours

import js

def mouseenter(screen, unused):
    screen.update('cursor', 'hidden', False)
    screen.render(True)

def mouseleave(screen, unused):
    screen.update('cursor', 'hidden', True)
    screen.update('x', "text", "??")
    screen.update('y', "text", "??")
    screen.render(True)

def mouseentercell(screen, pos):
    screen.update('x', "text", f"{pos.x:2d}")
    screen.update('y', "text", f"{pos.y:2d}")
    screen.move_panel('cursor', pos, relative=False)

def run(*args):
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
                children=[
                    UI.Label(text="X:", bbox=BBox(0, 0, 2, 1)),
                    UI.Label(text="??", name="x", bbox=BBox(3, 0, 3, 1)),
                    UI.Label(text="Y:", bbox=BBox(0, 1, 2, 1)),
                    UI.Label(text="??", name="y", bbox=BBox(3, 1, 3, 1)),
                ],
            ),
            UI.Panel(
                name = 'cursor',
                bbox = BBox(0, 0, 1, 1),
                hidden = True,
                layout = UI.layout.Absolute(),
                fill = Cell(" ", Colours("#ffff00ff", "#000000ff")),
            ),
        ],
    )
    screen.subscribe("mouseenter", mouseenter)
    screen.subscribe("mouseentercell", mouseentercell)
    screen.subscribe("mouseleave", mouseleave)
    
    screen.render()
    

js.addEventListener('py:all-done', run)
