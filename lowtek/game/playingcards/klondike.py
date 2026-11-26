from .playingcards import PlayingCardGame, Card

class KlondikeCardGame(PlayingCardGame):
    def __init__(self):
        super().__init__(
        areas = [
            CardPile(
                name = "drawpile",
                pos = Position(0, 0),
                faceup = False,
                cards = [
                ],
            ),
        ],
    )

    def valid_move(self, src, dst):
        pass


