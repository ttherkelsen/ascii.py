from lowtek.surface import Surface
from lowtek import UI
import js

def run(*args):
    screen = UI.Screen(
        size = Size(80, 40),
        jsid = 'canvas',
        theme = UI.LightTheme(),
        ui = UI.Container(
            layout = UI.layout.Rows()
            children = [
                UI.Label(text = "Row 1"),
                UI.Label(text = "Row 23"),
                UI.Label(text = "Row 35555"),
                UI.Label(text = "Row 4"),
            ],
        ),
    )
    screen.render()


js.addEventListener('py:all-done', run)
