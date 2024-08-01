from lowtek.surface import Surface
from lowtek import UI
import js

def run(*args):
    screen = UI.Screen(
        surface = Surface('canvas', 'ucs_9x15', 80, 40),
        theme = UI.LightTheme(),
        ui = UI.RowContainer(
            children = [
                UI.Label( text = "Row 1" ),
                UI.Label( text = "Row 23" ),
                UI.Label( text = "Row 35555" ),
                UI.Label( text = "Row 4" ),
            ],
        ),
    )
    screen.render()


js.addEventListener('py:all-done', run)
