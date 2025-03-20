from player import Player
from deck import Deck
import random

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
        order_to_select = [ [3,0], [2,0], [1,0], 
                            [3,1], [2,1], [1,1],
                            [3,2], [2,2], [1,2],
                            [0,2], [0,1]]
        
    def makeMove(self, deck:Deck) -> bool: # Returns True if eveal round starts
        discardValue = deck.discard_card
        unseenAmt = self.getUnseenAmt()

        # If there is a column that can be cancelled out
        if (col := self.isColumnCancellable(discardValue)) != -1:
            self.cancelColumn(deck, col)      # Cancel out the column
            if col == len(self.hand_seen):    # Fixes ord_to_select if column was not on end
                for coord in self.order_to_select:
                    if coord[0] > col:
                        coord[0] -= 1
            return False    # Do not start eval round

        # If there is one unseen card left and discard would make score 0 or less
        elif (unseenAmt == 1) and ((self.getSeenScore() + discardValue) < 1):
            oldCard = self.swapCard(discardValue, 0, 0)   # swap discard with (0,0)
            deck.discard(oldCard)
            return True     # start eval round

        # If there is at most 1 card revealed and discard is 4 or less
        elif (unseenAmt > 10) and (discardValue < 5):
            col, row = self.order_to_select.pop(0)      
            oldCard = self.swapCard(discardValue)                 # Swap discard with first position available in "ord_to_select"
            deck.discard(oldCard)
            return False    # Do not start eval round
        
        # If discard is a decent valued card
        elif discardValue < 5:
            col, row = self.order_to_select.pop(0)
            oldCard = self.swapCard(discardValue, col, row)   # Swap discard with first position available in "ord_to_select"
            deck.discard(oldCard)
            return False    # Do not start eval round
        

        newCard = deck.draw()
        # If there is a column that can be cancelled out
        if (col := self.isColumnCancellable(newCard)) != -1:
            self.cancelColumn(deck, col)      # Cancel out the column
            if col == len(self.hand_seen):    # Fixes ord_to_select if column was not on end
                for coord in self.order_to_select:
                    if coord[0] > col:
                        coord[0] -= 1
            return False    # Do not start eval round
        
        # If there is one unseen card left and discard would make score 0 or less
        elif (unseenAmt == 1) and ((self.getSeenScore() + newCard) < 1):
            oldCard = self.swapCard(newCard, 0, 0)   # swap discard with (0,0)
            deck.discard(oldCard)
            return True     # start eval round

        # If discard is a decent valued card
        elif newCard < 5:
            col, row = self.order_to_select.pop(0)      
            oldCard = self.swapCard(newCard)                 # Swap discard with first position available in "ord_to_select"
            deck.discard(oldCard)
            return False    # Do not start eval round
        
        # If not on last unseen card.
        elif unseenAmt > 1:
            deck.discard(newCard)
            col, row = self.order_to_select.pop(0)
            self.revealCard(col, row)
            return False    # Do not start eval round
        
        else:
            deck.discard(newCard)
            return False    # Do not start eval round