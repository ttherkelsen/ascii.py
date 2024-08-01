from lowtek import UI
from lowtek.surface import Surface

class FontPage(UI.Container):
    def __init__(self, page):
        grid = [ [ """This should be the first row header""" ] ]
        for y in range(16):
            build = [ """This should be the left-side ..Y. number for each row""" ]
            for x in range(16):
                build.append(UI.Label(chr(page*256 + y*16 + x)))
            grid.append(build)
        super().__init__(
            padding = 1,
            layout = UI.Layout.Grid((17, 17)),
            align = UI.Align.CENTER,
            children = grid,
        )


class FontApp:
    def __init__(self):
        left_side = UI.Container(
            padding = 1,
            layout = UI.Layout.Grid((2, 3)),
            align = UI.Layout.Center,
            children = [
                [ UI.Label('Font Name:'), UI.DropDown(), ],
                # FIXME: Populate below based on the bit depth of the font
                [ UI.Label('Colour 1:'), UI.ColourChooser(), ],
                [ UI.Label('Colour 2:'), UI.ColourChooser(), ],
            ],
        )
        ui = UI.Container(
            border = UI.Component.DoubleLine,
            title = 'Font Viewer',
            layout = UI.Layout.Columns(weight='*,*'),
            width = UI.Component.Max,
            children = [ left_side, FontPage(0) ],
        )
        screen = UI.Screen(
            Surface('canvas', 'ucs_9x15', 80, 40),
            UI.DarkTheme(),
            ui,
        )
        screen.render()

    
