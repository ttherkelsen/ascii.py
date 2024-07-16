class Colours:
    def __init__(self, *colours):
        self.colours = tuple([ Colours.to_memoryview(t) for t in colours ])

    def __hash__(self):
        return hash(self.colours)

    def __getitem__(self, i):
        return self.colours[i]
    
    @staticmethod
    def to_memoryview(colour):
        # FIXME: Don't assume a colour is defined as "#rrggbbaa", could be (r, g, b, a)
        return memoryview(bytes((
            int(colour[1:3], 16),
            int(colour[3:5], 16),
            int(colour[5:7], 16),
            int(colour[7:], 16),
            )))
