class Absolute:
    """
    Place children according to the bbox specified for each of them.
    
    If you use this layout manager you must make sure none of the
    specified bbox'es overlap!

    If a child component does not specify a bbox, it will default to
    the entire size of the container.  This is useful for containers
    with only one child component.
    """
    def __init__(self):
        pass
    
    def hint(self, size, children):
        for c in children:
            c.layout_hint(c.bbox.to_size() if c.bbox else size)
        return size

    def done(self, bbox, children):
        for c in children:
            cbbox = c.bbox + bbox.to_position() if c.bbox else bbox
            c.layout_done(cbbox)
    
