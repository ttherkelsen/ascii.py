from .font import Font

from pyscript import web

#FIXME: Destroy method?

class Surface:
    def __init__(self, js_id_or_div, font_name, size, init=None, zindex=0):
        self.js_id_or_div = js_id_or_div
        if isinstance(js_id_or_div, str):
            self.div = web.page.find(f"#{js_id_or_div}")[0]
        else:
            self.div = js_id_or_div
        self.font_name = font_name
        self.size = size
        self.font = Font.load(font_name)
        self.zindex = zindex

        self.create_dom_elements()
        match init:
            case None:
                pass
            case str():
                self.colour_fill(init)
            case _:
                self.fill(init)

    @property
    def pixel_width(self):
        return self.size.w * self.font.width

    @property
    def pixel_height(self):
        return self.size.h * self.font.height

    def create_overlay(self):
        return Surface(self.js_id_or_div, self.font_name, self.size, init="#00000000", zindex=self.zindex+1)

    def create_dom_elements(self):
        # Create div and canvas tag and add it to the self.parent_div element
        style = {
            'width': f"{self.pixel_width}px",
            'height': f"{self.pixel_height}px",
            'z-index': f"{self.zindex}",
        }
        if self.zindex > 0:
            style['position'] = 'absolute'
            style['left'] = '0px'
            style['cursor'] = 'none'
            
        canvas = web.canvas(style=style)
        canvas._dom_element.width = self.pixel_width
        canvas._dom_element.height = self.pixel_height

        if self.zindex == 0:
            self.div._dom_element.style = 'position: relative;'
        self.div.append(canvas)
        self.canvas = canvas
        
        # Keep local proxy of canvas 2d context
        self.ctx = canvas._dom_element.getContext("2d")

    def colour_fill(self, colour):
        self.ctx.fillStyle = colour;
        self.ctx.fillRect(0, 0, self.pixel_width, self.pixel_height);
        
    def fill(self, cell):
        glyph = self.font.render_glyph(cell)
        for y in range(self.size.h):
            for x in range(self.size.w):
                self.ctx.putImageData(glyph, x*self.font.width, y*self.font.height)

    def write(self, cell, x, y):
        glyph = self.font.render_glyph(cell)
        self.ctx.putImageData(glyph, x*self.font.width, y*self.font.height)
    
    def update(self, cu):
        for cp in cu:
            glyph = self.font.render_glyph(cp.cell)
            self.ctx.putImageData(glyph, cp.pos.x*self.font.width, cp.pos.y*self.font.height)
            
