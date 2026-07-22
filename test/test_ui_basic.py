from lowtek.surface import Surface
from lowtek import UI
import js

def run(*args):
    screen = UI.Screen(
        surface = Surface('canvas', 'ucs_9x15', Size(80, 40)),
        theme = UI.LightTheme(),
        ui = [
            UI.Window(
                title = "Test",
                position = Position(3, 3),
                size = Size(10, 10),
            )
        ],
    )
    screen.render()


js.addEventListener('py:all-done', run)
