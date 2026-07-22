from lowtek.surface import Surface
from lowtek.cell import Cell, CellUpdateBBox
from lowtek.colours import Colours
from lowtek.classes import Size, BBox

import js
import time

def run(*args):
    a = time.time()
    s = Surface('canvas', 'ucs_9x15', Size(80, 40), Cell(".", Colours("#ccccccff", "#111111ff")))
    #s = Surface('canvas', 'ucs_9x15', Size(80, 40), 'red')
    #s = Surface('canvas', 'ucs_9x15', Size(80, 40))
    #s = Surface('canvas', 'ucs_9x15', Size(80, 40), '#00000020')  # Alpha
    #s = Surface('canvas', 'ucs_9x15', Size(80, 40), '#000000')

    s.update(CellUpdateBBox([ Cell("a", Colours("#2222ccff", "#22ccccff")) ]*12, BBox(x=3, y=3, w=4, h=3)))
    
    b = time.time()
    js.console.log(b - a)


js.addEventListener('py:all-done', run)
