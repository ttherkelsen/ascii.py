from lowtek.surface import Surface
from lowtek import UI
from lowtek.classes import BBox, Size, Position
from lowtek.cell import Cell
from lowtek.glyphs import GLYPHS
from lowtek.colours import Colours

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
                fill = Cell(theme.background, theme.colours.background),
            ),
            UI.Panel(
                bbox = BBox(6, 6, 10, 10),
                layout = UI.layout.Absolute(),
                fill = Cell(theme.panel_background, theme.colours.panel_background),
                children=[
                    UI.Picture(
                        imagedata = [
                            '0000000000',
                            '1111111111',
                            '2222222222',
                            '3333333333',
                            '4444444444',
                            '5555555555',
                            '6666666666',
                            '7777777777',
                            '8888888888',
                            '9999999999',
                        ],
                        palette = {
                            '0' : GLYPHS['GS0'],
                            '1' : GLYPHS['GS1'],
                            '2' : GLYPHS['GS2'],
                            '3' : GLYPHS['GS3'],
                            '4' : GLYPHS['GS4'],
                            '5' : ("5", None, "#ffffffff"),
                            '6' : ("6", "#ff0000ff", None),
                            '7' : ("7", "#ff0000ff", "#ffffffff"),
                            '8' : (ord('8'), "#ff0000ff", "#ffffffff"),
                            '9' : Cell("9", Colours("#ff0000ff", "#ffffffff")),
                        },
                    ),
                ],
            ),
        ],
    )
    screen.render()

js.addEventListener('py:all-done', run)
