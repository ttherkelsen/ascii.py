class Location:
    def __init__(
            self, *, /,
            bbox,
            name = None,
            collection = None,    # Collection() -- the element in this location
            empty = None,         # Picture() component to use if collection is empty
