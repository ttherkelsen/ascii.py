from lowtek.surface import Surface
from lowtek import UI
from lowtek.classes import BBox, Size, Position
from lowtek.cell import Cell
from lowtek.const import Cards

import js, random

def run(*args):
    deck = []
    for suit in (Cards.HEARTS, Cards.DIAMONDS, Cards.CLUBS, Cards.SPADES):
        for value in range(13):
            deck.append(suit | Cards(value+1))
    random.shuffle(deck)
            
    cards = [
        UI.Panel(
            bbox = BBox(2, 2, 7, 7),
            layout = UI.layout.Absolute(),
            children = [ UI.Card(face=Cards.BACK | Cards.STYLE_DEFAULT) ],
        ),
    ]

    for row in range(7):
        bbox = BBox(2 + (row*8), 11 + (row*2), 7, 7)
        cards.append(
            UI.Panel(
                bbox = bbox,
                layout = UI.layout.Absolute(),
                children = [ UI.Card(face=deck.pop() | Cards.STYLE_DEFAULT) ],
            )
        )
        for column in range(6 - row):
            bbox = BBox(2 + ((row+column+1)*8), 11 + (row*2), 7, 7)
            cards.append(
                UI.Panel(
                    bbox = bbox,
                    layout = UI.layout.Absolute(),
                    children = [ UI.Card(face=Cards.BACK | Cards.STYLE_DEFAULT) ],
                )
            )
            
    
    theme = UI.LightTheme()
    size = Size(80, 40)
    screen = UI.Screen(
        surface = Surface('canvas', 'ucs_9x15', size),
        theme = theme,
        ui = [
            UI.Panel(
                bbox = size.to_bbox(),
                layout = UI.layout.Absolute(),
                fill = Cell(theme.background, theme.colours.background),
            ),
        ] + cards,
    )
    screen.render()

js.addEventListener('py:all-done', run)
