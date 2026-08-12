from lowtek.surface import Surface
from lowtek import UI
from lowtek.classes import BBox, Size, Position
from lowtek.cell import Cell

import js

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
                children =[ UI.Fill(cell=Cell(theme.background, theme.colours.background)) ],
            ),
            UI.Panel(
                bbox = BBox(6, 6, 10, 10),
                layout = UI.layout.Absolute(),
                children=[ UI.Fill(cell=Cell("b", theme.colours.text), name='fill') ],
            ),
            UI.Panel(
                bbox = BBox(3, 3, 10, 10),
                layout = UI.layout.Absolute(),
                children=[ UI.Fill(cell=Cell("a", theme.colours.text)) ],
            ),
            UI.Panel(
                bbox = BBox(20, 0, 10, 10),
                layout = UI.layout.Absolute(),
                fill = Cell(theme.panel_background, theme.colours.text),
                children=[ UI.Fill(cell=Cell("a", theme.colours.text), bbox=BBox(1, 1, 3, 3)) ],
            ),
            UI.Panel(
                name = 'd',
                bbox = BBox(35, 10, 5, 5),
                layout = UI.layout.Absolute(),
                fill = Cell("d", theme.colours.text),
            ),
        ],
    )
    screen.render()
    screen.update("fill", "cell", Cell("z", theme.colours.text))
    screen.render()
    screen.move("d", Position(x=-5, y=-2))
    screen.render()

js.addEventListener('py:all-done', run)
