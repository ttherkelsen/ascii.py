from ..UI.screen import Screen

class Table(Screen):
    def __init__(
            self, *, /,
    ):
        # A table has:
        # - Menu / title bar on the top
        # - Background filled with a single cell or brushed with a Picture
        # - Status line on the bottom
        # - A number of locations
        #   - each location has a size and position
        # - The size of the Table is determined from the locations
        
