from lowtek.font import Font
from lowtek.cell import Cell
from lowtek.colours import Colours
import js
from pyscript import ffi

font = Font.load("ucs_9x15")

js.console.log(ffi.to_js(font.depth))
js.console.log(ffi.to_js(font.render_glyph(Cell("a", Colours("#000000ff", "#ff0000ff")))))

