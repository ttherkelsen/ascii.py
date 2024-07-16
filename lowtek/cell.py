class Cell:
    def __init__(self, glyph, colours):
        self.glyph = glyph if isinstance(glyph, int) else ord(glyph)
        self.colours = colours

