from .font2 import Font
from .colours import Colours
from .cell import Cell

from pyscript.web import dom, elements
from pyscript import ffi
import js

#FIXME: Destroy method?

class Surface:
    def __init__(self, js_id_or_div, font_name, width, height, init=None):
        if isinstance(js_id_or_div, str):
            self.div = dom.find(f"#{js_id_or_div}")[0]
        else:
            self.div = js_id_or_div
        self.js_id_or_div = js_id_or_div
        self.font_name = font_name
        self.width = width
        self.height = height
        self.font = Font.load(font_name)

        self.create_canvas_element()
        if init is None:
            self.colour_fill("#000000")
        else:
            self.fill(init)

    @property
    def pixel_width(self):
        return self.width * self.font.width

    @property
    def pixel_height(self):
        return self.height * self.font.height

    def create_canvas_element(self):
        # Create canvas tag and add it to the self.div element
        canvas = elements.canvas(
            style = {
                'width': f"{self.pixel_width}px",
                'height': f"{self.pixel_height}px"
            }
        )
        canvas._dom_element.width = self.pixel_width
        canvas._dom_element.height = self.pixel_height
        self.div.append(canvas)
        
        # Keep local proxy of canvas 2d context
        self.ctx = canvas._dom_element.getContext("2d")

    def colour_fill(self, colour):
        # FIXME: Fill canvas with colour
        pass
        
    def fill(self, cell):
        glyph = self.font.render_glyph(cell)
        for y in range(self.height):
            for x in range(self.width):
                self.ctx.putImageData(glyph, x*self.font.width, y*self.font.height)

    def write(self, cell, x, y):
        glyph = self.font.render_glyph(cell)
        self.ctx.putImageData(glyph, x*self.font.width, y*self.font.height)
    
