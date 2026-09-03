from lowtek.surface import Surface
from lowtek import UI
from lowtek.classes import BBox, Size
from lowtek.cell import Cell
from lowtek import utils

import js

def run(*args):
    size = Size(80, 40)
    theme = UI.LightTheme()

    #surface = Surface('canvas', 'unscii_full_8x16', size)
    #surface = Surface('canvas', 'unifont_all_8x16w', size)
    surface = Surface('canvas', 'ucs_9x15', size)

    screen = UI.Screen(
        theme = theme,
        surface = surface,
        ui = [
            UI.Panel(
                bbox = size.to_bbox(),
                layout = UI.layout.Absolute(),
                children =[ UI.Fill(cell=Cell(theme.background, theme.colours.background)) ],
            ),
            UI.Panel(
                bbox = BBox(12, 3, 56, 34),
                fill = Cell(theme.panel_background, theme.colours.panel_background),
                layout = UI.layout.Absolute(),
                children = [ UI.GlyphPage(page=0x2500, font=surface.font) ],
            ),
        ],
    )
    screen.render()

js.addEventListener('py:all-done', run)
