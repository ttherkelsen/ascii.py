from lowtek.surface import Surface
from lowtek import UI
from lowtek.classes import BBox, Size, Position
from lowtek.cell import Cell
from lowtek.const import Cards, Mouse

import js, random

def run(*args):
    theme = UI.LightTheme()
    size = Size(80, 40)
    deck = []
    for suit in (Cards.HEARTS, Cards.DIAMONDS, Cards.CLUBS, Cards.SPADES):
        for value in range(13):
            deck.append(suit | Cards(value+1))
    random.shuffle(deck)
            
    cards = [
        UI.Card(
            pos = Position(2, 2),
            face = deck.pop() | Cards.FACEDOWN | Cards.STYLE_DEFAULT,
        ),
    ]

    for row in range(7):
        pos = Position(2 + (row*8), 11 + (row*2))
        cards.append(
            UI.Card(
                pos = pos,
                face = deck.pop() | Cards.STYLE_DEFAULT,
                movable = True,
            )
        )
        for column in range(6 - row):
            pos = Position(2 + ((row+column+1)*8), 11 + (row*2))
            cards.append(
                UI.Card(
                    pos = pos,
                    face=deck.pop() | Cards.FACEDOWN | Cards.STYLE_DEFAULT,
                )
            )
            
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
        mouse = Mouse.ENABLE | Mouse.NOCONTEXT,
    )

    screen.render()


js.addEventListener('py:all-done', run)
