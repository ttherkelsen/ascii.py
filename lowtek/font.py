import pickle, os.path
import js
from pyscript import ffi

FONT_PATH = "./resource/font/"

class Font:
    cache = {} # shared amongst all instances
    
    def __init__(self, name, width, height, depth, glyphs, unknown=0):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.glyphs = glyphs
        self.unknown = unknown


    @property
    def size(self):
        return self.width * self.height * 4

    @property
    def xsize(self):
        return self.width * 4

        
    @classmethod
    def load(cls, name):
        with open(os.path.join(FONT_PATH, f"{name}.pickle"), "rb") as FD:
            data = pickle.load(FD)
        return cls(*data)
    

    def render_glyph(self, cell):
        # FIXME: Instead of one block of bytes, return rows of bytes
        glyph = cell.glyph if cell.glyph in self.glyphs else self.unknown
        
        if cell.colours in self.cache.setdefault(self.name, {}).setdefault(glyph, {}):
            return self.cache[self.name][glyph][cell.colours]
        
        bitmap = self.glyphs[cell.glyph]
        pixels = memoryview(bytearray(self.size))
        bitmask = (self.depth << 1) - 1
        
        for y in range(self.height):
            row = bitmap[y]
            for x in range(self.width):
                colour = cell.colours[row & bitmask]

                pos = y*self.width*4 + (self.width - x - 1)*4
                pixels[pos:pos+4] = colour
                row >>= self.depth

        data = js.Uint8ClampedArray.new(ffi.to_js(pixels))
        image_data = js.ImageData.new(data, self.width, self.height)
                
        self.cache[self.name][glyph][cell.colours] = image_data
        return image_data
    
