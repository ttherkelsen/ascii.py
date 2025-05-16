from .font import Font
from .colours import Colours
from .cell import Cell
from .classes import PixelPosition, Size

from pyscript import web, ffi
import js

#FIXME: Destroy method?

class Surface:
    def __init__(self, js_id_or_div, font_name, size, init=None, pos=None):
        if isinstance(js_id_or_div, str):
            self.parent_div = web.page.find(f"#{js_id_or_div}")[0]
        else:
            self.parent_div = js_id_or_div
        self.js_id_or_div = js_id_or_div
        self.font_name = font_name
        self.size = size
        self.font = Font.load(font_name)
        self.pos = pos

        self.create_dom_elements()
        if init is None:
            self.colour_fill("#000000")
        else:
            self.fill(init)

    @property
    def pixel_width(self):
        return self.size.w * self.font.width

    @property
    def pixel_height(self):
        return self.size.h * self.font.height

    def create_dom_elements(self):
        # Create div and canvas tag and add it to the self.parent_div element
        canvas = web.canvas(
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
            
        self.div = web.div(canvas, style=style)
        self.parent_div.append(self.div)
        
        # Keep local proxy of canvas 2d context
        self.ctx = canvas._dom_element.getContext("2d")

    def add_child(self, bbox, init=None, font_name=None):
        if font_name is None:
            font_name = self.font_name
        child = Surface(
            self.div, font_name, bbox.to_size(), init,
            bbox.to_position().to_pixels(Size(self.font.width, self.font.height))
        )
        return child
        
    def colour_fill(self, colour):
        # FIXME: Fill canvas with colour
        pass
        
    def fill(self, cell):
        glyph = self.font.render_glyph(cell)
        for y in range(self.size.h):
            for x in range(self.size.w):
                self.ctx.putImageData(glyph, x*self.font.width, y*self.font.height)

    def write(self, cell, x, y):
        glyph = self.font.render_glyph(cell)
        self.ctx.putImageData(glyph, x*self.font.width, y*self.font.height)
    
    
