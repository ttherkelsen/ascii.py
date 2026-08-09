from lowtek.surface import Surface
from lowtek import UI
from lowtek.classes import BBox, Size, Frame, FrameLD
from lowtek.cell import Cell, CellHint
from lowtek.colours import Colours
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
                fill = Cell(theme.background, theme.colours.background),
            ),
            UI.Panel(
                bbox = BBox(20, 3, 20, 20),
                layout = UI.layout.Absolute(),
                children = [
                    UI.Fill(
                        margin=Frame(
                            n=1,
                            s=CellHint(cell=Cell(" ", Colours("#c0ffc0ff", "#333333ff"))),
                            e=CellHint(cell=Cell(" ", Colours("#c0c0ffff", "#333333ff")), hint=2),
                            w=CellHint(cell=Cell("b", Colours("#c0c0c0ff", "#ffffffff")), hint=3),
                            order="wnes",
                        ),
                        padding=1,
                        border='r',
                        cell=Cell("a", Colours('#ffc0c0ff', '#333333ff')),
                    )
                ],
            ),
            UI.Panel(
                bbox = BBox(50, 5, 10, 10),
                layout = UI.layout.Absolute(),
                children = [
                    UI.Fill(
                        border=FrameLD(
                            n="s",
                        ),
                        cell=Cell("b", Colours('#ffc0c0ff', '#333333ff')),
                    )
                ],
            ),
        ],
    )
    screen.render()

js.addEventListener('py:all-done', run)
