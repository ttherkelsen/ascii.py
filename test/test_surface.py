from lowtek.surface import Surface
from lowtek.cell import Cell
from lowtek.colours import Colours
import js
from pyscript import ffi, when
import time

def run(*args):
    a = time.time()
    s = Surface('canvas', 'ucs_9x15', 80, 40, Cell("a", Colours("#c0c0c0ff", "#000000ff")))
    b = time.time()
    js.console.log(ffi.to_js(b - a))


js.addEventListener('py:all-done', run)
