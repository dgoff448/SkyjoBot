import random

class Deck:

    def __init__(self):
        self.cards = []
        self.card_counts = {"-2":5, "-1":10, "0":15, "1":10, "2":10,
                             "3":10, "4":10, "5":10, "6":10, "7":10,
                            "8":10, "9":10, "10":10, "11":10, "12":10}
        self.discard_card = 13

        for i in range(-2, 13):
            for j in range(0, self.card_counts[str(i)]):
                self.cards.append(i)

    def draw(self) -> int:
        card = self.cards.pop(random.randint(0, len(self.cards)-1))
        self.card_counts[str(card)] -= 1
        return card
    
    def discard(self, card:int):
        self.discard_card = card
    
    def getDiscardCard(self) -> int:
        return self.discard_card
