from player import Player
# from game import Game
from deck import Deck

"""
Notes:
* getMaxCard() does not take into account if the column has two cards of same value
* shouldPickDiscard() does not use discard to lower (for example) a 12 to an 7.
    It will see that the card is above 6 and opt not to use it.
* 
"""

class Bot(Player):
    def __init__(self, id:int):
        super().__init__(id)

    def makeMove(self, deck:Deck) -> bool:      # Returns if eval round starts
        # Should the bot use the card on the discard pile?
        discardCard = deck.discard_card
        if self.shouldUseDiscard(discardCard):
            col, row = self.pickCardToSwap(discardCard)
            oldCard = self.swapCard(discardCard, col, row)
            deck.discard(oldCard)
            print(f"Bot {self.id} decided to swap the discard card ({discardCard}) with his {oldCard}.")
            return False

        # Should the bot use the card drawn from deck?
        newCard = deck.draw()
        if self.shouldUseNew(newCard):
            col, row = self.pickCardToSwap(newCard)
            oldCard = self.swapCard(newCard, col, row)
            deck.discard(oldCard)
            print(f"Bot {self.id} decided to swap the New Card ({newCard}) with his {oldCard}.")
            return False
        deck.discard(newCard)
        print(f"Bot {self.id} decided to discard the new card ({newCard}).")

        # If there is 1 unseen card left
        if self.getUnseenCards == 1:
            # start eval round if current sum is < 4  TODO: Could be smarter
            if self.currentSum < 4:
                self.turnCard()
                print(f"Bot {self.id} decided to start the Evaluation Round.")
                return True
            return False
        
        # Turn Card over
        self.turnCard()
        print(f"Bot {self.id} decided to turn over a card.")
        return False
    
    def turnCard(self):
        # Turns the first found unseen card.  TODO: Could be smarter
        for col in range(0, len(self.hand_seen)):
            for row in range(0, len(col)):
                if self.hand_seen[col][row] == 13:
                    self.revealCard(col, row)

    def currentSum(self) -> int:
        total = 0
        for col in self.hand_seen:
            for card in col:
                total += card
        return total

    def checkColumns(self, card:int) -> tuple[int, int]:
        for col in range(0, len(self.hand_seen)):
            matches = 0
            for row in range(0, len(col)):
                seen_card = self.hand_seen[col][row]
                if seen_card == card:
                    matches += 1
            if matches == 2:
                return (col, row)
        return (13, 13)

    def getMaxCard(self, card:int) -> tuple[int, int]:
        maxCard = -2
        maxCoords = (13, 13)
        for col in range(0, len(self.hand_seen)):
            for row in range(0, len(col)):
                seen_card = self.hand_seen[col][row]
                if seen_card > maxCard and seen_card != 13:
                    maxCard = seen_card
                    maxCoords = (col, row)
        return maxCoords
    
    def pickCardToSwap(self, cardToUse:int) -> tuple[int, int]:
        col, row = self.checkColumns(cardToUse)
        if col != 13 and row != 13:
            return (col, row)

        return self.getMaxCard(cardToUse)

    def shouldUseDiscard(self, discardCard:int) -> bool:
        col, row = self.checkColumns(discardCard)
        if col != 13 and row != 13:     # is there a column that can be completed?
            return True
        elif discardCard < 7:           # is the card below 7
            return True
        else:
            return False

    def shouldUseNew(self, newCard:int) -> bool:
        return self.shouldUseDiscard(newCard)