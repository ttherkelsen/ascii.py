from .panel import Panel
from lowtek.classes import BBox
from lowtek.colours import Colours
from lowtek.const import Cards
from lowtek.glyphs import GLYPHS

CARDTEMPLATE = {
    'chars': {
        'a': GLYPHS['B rr '],
        'b': GLYPHS['B  rr'],
        'c': GLYPHS['Brr  '],
        'a': GLYPHS['Br  r'],
        '-': GLYPHS['B s s'],
        '|': GLYPHS['Bs s '],
        'x': 0x2591,
    },
    'colours': {
        'red': '#ff0000ff',
        'black': '#000000ff',
        'back': '#c03030ff',
        'card': '#ffffffff',
    },
    'face': [
        "a-------b",
        "|vV    s|",
        "|V 111  |",
        "|  222  |",
        "|  333  |",
        "|  444  |",
        "|  555  |",
        "|  666 v|",
        "|s    vV|",
        "c-------d",
    ],
    'back': [
        "a-------b",
        "|xxxxxxx|",
        "|xxxxxxx|",
        "|xxxxxxx|",
        "|xxxxxxx|",
        "|xxxxxxx|",
        "|xxxxxxx|",
        "|xxxxxxx|",
        "|xxxxxxx|",
        "c-------d",
    ]
    Cards.ACE: [
        '   ',
        '   ',
        ' s ',
        '   ',
        '   ',
        '   ',
    ],
    Cards.TWO: [
        '   ',
        ' s ',
        '   ',
        '   ',
        ' s ',
        '   ',
    ],
    Cards.THREE: [
        '   ',
        ' s ',
        '   ',
        ' s ',
        '   ',
        ' s ',
    ],
    Cards.FOUR: [
        '   ',
        's s',
        '   ',
        '   ',
        's s',
        '   ',
    ],
    Cards.FIVE: [
        's s',
        '   ',
        ' s ',
        '   ',
        's s',
        '   ',
    ],
    Cards.SIX: [
        's s',
        '   ',
        's s',
        '   ',
        's s',
        '   ',
    ],
    Cards.SEVEN: [
        's s',
        ' s ',
        's s',
        '   ',
        's s',
        '   ',
    ],
}

CARD

class Card(Panel): #FIXME: Should extend Window not Panel
    def __init__(
            self, /, *,
            pos,
            face,
            style = Cards.STYLE_A,
    ):
        self.pos = pos
        self.face = face
        self.style = style
        super().__init__(bbox=BBox(pos, self.get_card_size()))

    def get_card_size(self):
        
