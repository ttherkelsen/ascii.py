from .picture import Picture
from lowtek.classes import BBox, Size, Position
from lowtek.colours import Colours
from lowtek.const import Cards, MouseButton
from lowtek.glyphs import GLYPHS

CARDTEMPLATE = {
    'size': Size(7, 7),
    'palette': {
        's': None, # Overwritten in layout_done,

        # Face
        'a': ( GLYPHS['B rr '], None, '#a0a0a0ff' ),
        'b': ( GLYPHS['B  rr'], None, '#a0a0a0ff' ),
        'c': ( GLYPHS['Brr  '], None, '#a0a0a0ff' ),
        'd': ( GLYPHS['Br  r'], None, '#a0a0a0ff' ),
        '_': ( GLYPHS['B r r'], None, '#a0a0a0ff' ),
        '-': ( GLYPHS['B r r'], None, '#a0a0a0ff' ),
        '>': ( GLYPHS['Br r '], None, '#a0a0a0ff' ),
        '<': ( GLYPHS['Br r '], None, '#a0a0a0ff' ),

        # Back
        'x': GLYPHS['Ds '],
        'I': GLYPHS['B rr '],
        'B': GLYPHS['B  rr'],
        'C': GLYPHS['Brr  '],
        'D': GLYPHS['Br  r'],
        'E': GLYPHS['B r r'],
        'F': GLYPHS['B r r'],
        'G': GLYPHS['Br r '],
        'H': GLYPHS['Br r '],
        
    },
    'colours': {
        Cards.CLUBS: Colours("#ffffffff", "#000000ff"),
        Cards.SPADES: Colours("#ffffffff", "#000000ff"),
        Cards.HEARTS: Colours("#ffffffff", "#ff0000ff"),
        Cards.DIAMONDS: Colours("#ffffffff", "#ff0000ff"),
        Cards.FACEDOWN: Colours("#ff0000ff", "#f0f0f0ff"),
    },

    'template': [
        'a_____b',
        '>svV  <',
        '>v    <',
        '>V   W<',
        '>    w<',
        '>  Wws<',
        'c-----d',
    ],
    Cards.FACEDOWN: [
        'IEEEEEB',
        'GxxxxxH',
        'GxxxxxH',
        'GxxxxxH',
        'GxxxxxH',
        'GxxxxxH',
        'CFFFFFD',
    ],
}

class Card(Picture):
    def __init__(
            self, /, *,
            face,
            movable = False,
            **component,
    ):
        self.face = face
        self.movable = movable
        self._highlight = False
        self._panel_pos = None
         
        picture = {
            'colours': CARDTEMPLATE['colours'][Cards.FACEDOWN] if face & Cards.MASK_FACEDOWN else CARDTEMPLATE['colours'][face & Cards.MASK_SUIT],
            'palette': {} | CARDTEMPLATE['palette'],
            'draggable': movable,
        }
        if (face & Cards.MASK_VALUE) in CARDTEMPLATE:
            picture['imagedata'] = CARDTEMPLATE[face & Cards.MASK_VALUE]
        elif (face & Cards.MASK_FACEDOWN):
            picture['imagedata'] = CARDTEMPLATE[Cards.FACEDOWN]
        else:
            match face & Cards.MASK_SUIT:
                case Cards.CLUBS:
                    picture['palette']['s'] = GLYPHS['Cc']
                case Cards.SPADES:
                    picture['palette']['s'] = GLYPHS['Cs']
                case Cards.DIAMONDS:
                    picture['palette']['s'] = GLYPHS['Cd']
                case Cards.HEARTS:
                    picture['palette']['s'] = GLYPHS['Ch']
                
            img = []
            for row in CARDTEMPLATE['template']:
                match face & Cards.MASK_VALUE:
                    case Cards.ACE:
                        row = row.replace('v', 'A').replace('V', ' ').replace('w', 'A').replace('W', ' ')
                    case n if Cards.TWO <= n <= Cards.NINE:
                        row = row.replace('v', str(n)).replace('V', ' ').replace('w', str(n)).replace('W', ' ')
                    case Cards.TEN:
                        row = row.replace('v', '1').replace('V', '0').replace('w', '0').replace('W', '1')
                    case Cards.JACK:
                        row = row.replace('v', 'J').replace('V', ' ').replace('w', 'J').replace('W', ' ')
                    case Cards.QUEEN:
                        row = row.replace('v', 'Q').replace('V', ' ').replace('w', 'Q').replace('W', ' ')
                    case Cards.KING:
                        row = row.replace('v', 'K').replace('V', ' ').replace('w', 'K').replace('W', ' ')
                img.append(row)
            picture['imagedata'] = img
                        
        super().__init__(**(component | picture))

    def highlight(self, state=True):
        if self._highlight == state:
            return

        if state:
            self.cells['main'].cells.filter(frame=1).colour(None, "#000000ff").apply()
        else:
            self.cells['main'].cells.filter(frame=1).colour(None, "#a0a0a0ff").apply()
        self._highlight = state

    def mouse_enter(self):
        if not self.movable:
            return False

        self.highlight(True)
        return True

    def mouse_drag_begin(self):
        print("mouse_drag_begin")
        self._panel_pos = self._parent.bbox.to_position()
        return False
    
    def mouse_drag_move(self, delta):
        self.find("__screen__").move_panel(self._parent.name, delta)
        return False

    def mouse_drag_end(self, forced=False): # If cursor moves out of screen forced=True
        if forced:
            self.find("__screen__").move_panel(self._parent.name, self._panel_pos, relative=False)
        return False
    
    def mouse_exit(self):
        if not self.movable:
            return False
        
        self.highlight(False)
        return True

