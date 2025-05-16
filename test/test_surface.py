from lowtek.surface import Surface
from lowtek.cell import Cell
from lowtek.colours import Colours
from lowtek.classes import Position, Size
import js
from pyscript import ffi, web
import time

def run(*args):
    a = time.time()
    s = Surface('canvas', 'ucs_9x15', Size(80, 40), Cell("a", Colours("#c0c0c0ff", "#000000ff")))
    cs = s.add_child('ucs_9x15', Size(10, 10), Position(20, 10), Cell(" ", Colours("#00000040", "#ffffffff")))
    cs = s.add_child('ucs_9x15', Size(10, 10), Position(30, 10), Cell("b", Colours("#000000ff", "#ffffffff")))
    b = time.time()
    js.console.log(ffi.to_js(b - a))


js.addEventListener('py:all-done', ffi.create_proxy(run))
#js.addEventListener('py:all-done', run)
