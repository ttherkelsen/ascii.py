from lowtek.surface import Surface
from lowtek import UI
from lowtek.classes import BBox, Size
from lowtek.cell import Cell

import js

def run(*args):
    theme = UI.LightTheme()
    screen = UI.Screen(
        surface = Surface('canvas', 'ucs_9x15', Size(80, 40)),
        theme = theme,
    )
    screen.set_ui( # FIXME: Ugly hack, figure out a way to do this better
        UI.Frame(
            layout = UI.layout.Absolute(),
            children =[ UI.Fill(Cell(theme.background, theme.colours.background)) ],
        ),
        UI.Frame(
            bbox = BBox(6, 6, 10, 10),
            layout = UI.layout.Absolute(),
            children=[ UI.Fill(Cell("b", theme.colours.text)) ],
        ),
        UI.Frame(
            bbox = BBox(3, 3, 10, 10),
            layout = UI.layout.Absolute(),
            children=[ UI.Fill(Cell("a", theme.colours.text)) ],
        ),
    )
    screen.render()
    screen.ui[1].children[0].update("cell", Cell("z", theme.colours.text))
    screen.render()

js.addEventListener('py:all-done', run)
