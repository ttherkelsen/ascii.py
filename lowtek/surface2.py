from .font2 import Font
from .colours import Colours
from .cell import Cell

from pyscript.web import dom, elements
from pyscript import ffi
import js

class Surface:
    def __init__(self, js_id, font_name, width, height, init=None):
        self.js_id = js_id
        self.font_name = font_name
        self.width = width
        self.height = height
        self.font = Font.load(font_name)
        self.pixels = memoryview(bytearray(self.font.size * self.width * self.height))

        init = init or Cell(" ", Colours("#000000ff", "#c0c0c0ff"))
        self.create_canvas_element()
        self.fill(init)
        #self.update_canvas()

    @property
    def pixel_width(self):
        return self.width * self.font.width

    @property
    def pixel_height(self):
        return self.height * self.font.height

    
    def create_canvas_element(self):
        # Create canvas tag and add it to the element with DOM id self.js_id
        div = dom.find(f"#{self.js_id}")[0]
        canvas = elements.canvas(
            style = {
                'width': f"{self.pixel_width}px",
                'height': f"{self.pixel_height}px"
            }
        )
        canvas._dom_element.width = self.pixel_width
        canvas._dom_element.height = self.pixel_height
        div.append(canvas)
        
        # Keep local proxy of canvas 2d context
        self.ctx = canvas._dom_element.getContext("2d")
        

    def update_canvas(self):
        data = js.Uint8ClampedArray.new(ffi.to_js(self.pixels))
        image_data = js.ImageData.new(data, self.pixel_width, self.pixel_height)
        self.ctx.putImageData(image_data, 0, 0)

        
    def fill(self, cell):
        glyph = self.font.render_glyph(cell)
        for y in range(self.height):
            for x in range(self.width):
                self.write(glyph, x, y)

    def write(self, glyph, x, y):
        self.ctx.drawImage(glyph, x*self.font.width, y*self.font.height)
    
