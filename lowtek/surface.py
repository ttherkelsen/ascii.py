from .font import Font
from .colours import Colours
from .cell import Cell

from pyscript.web import dom, elements
from pyscript import ffi
import js

#FIXME: Destroy method?

class Surface:
    def __init__(self, js_id_or_div, font_name, width, height, init=None, pos=None):
        if isinstance(js_id_or_div, str):
            self.parent_div = dom.find(f"#{js_id_or_div}")[0]
        else:
            self.parent_div = js_id_or_div
        self.js_id_or_div = js_id_or_div
        self.font_name = font_name
        self.width = width
        self.height = height
        self.font = Font.load(font_name)
        self.pos = pos

        self.create_dom_elements()
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

    def create_dom_elements(self):
        # Create div and canvas tag and add it to the self.parent_div element
        canvas = elements.canvas(
            style = {
                'width': f"{self.pixel_width}px",
                'height': f"{self.pixel_height}px"
            }
        )
        canvas._dom_element.width = self.pixel_width
        canvas._dom_element.height = self.pixel_height
        
        style = {
            'width': f"{self.pixel_width}px",
            'height': f"{self.pixel_height}px",
            'z-index': '0',
        }
        if self.pos is None:
            style['position'] = 'relative'
        else:
            style['position'] = 'absolute'
            style['top'] = f"{self.pos.y}px"
            style['left'] = f"{self.pos.x}px"
            
        self.div = elements.div(style=style)
        self.div.append(canvas)
        self.parent_div.append(self.div)
        
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
    
