from lowtek.surface import Surface
from lowtek import UI
from lowtek.classes import BBox, Size
from lowtek.cell import Cell
from lowtek import utils

import js

def run(*args):
    size = Size(80, 40)
    theme = UI.LightTheme()
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
                bbox = BBox(20, 3, 38, 34),
                #fill = Cell(theme.panel_background, theme.colours.panel_background),
                layout = UI.layout.Absolute(),
                #children = [ UI.GlyphPage(page=0x2500) ],
            ),
        ],
    )
    screen.render()

js.addEventListener('py:all-done', run)
