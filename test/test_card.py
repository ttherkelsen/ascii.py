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
                fill = Cell(theme.panel_background, theme.colours.text),
            ),
            UI.Card(
                face = Cards.FIVE | Cards.CLUBS,
                pos = Position(x=5, y=5),
            )
        ],
    )
    screen.render()

js.addEventListener('py:all-done', run)
