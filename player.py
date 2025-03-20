from deck import Deck

class Player:
    def __init__(self, id:int):
        self.id = id
        self.hand_actual = []
        self.hand_seen = [[13,13,13],[13,13,13],[13,13,13],[13,13,13]]
        self.score = 0

    def setHand(self, hand:list[list[int]]):
        self.hand_actual = hand

    def swapCard(self, card:int, col:int, row:int) -> int:
        oldCard = self.hand_actual[col][row]
        self.hand_actual[col][row] = card
        self.revealCard(col, row)
        return oldCard

    def revealCard(self, col:int, row:int):
        self.hand_seen[col][row] = self.hand_actual[col][row]

    def isColumnCancellable(self, discardValue:int) -> int:
        for i in range(0, len(self.hand_seen)):
            col = self.hand_seen[i]
            matches = 0
            for j in range(0, len(col)):
                if col[j] == discardValue:
                    matches += 1
            if matches == 2:
                return i
        return -1       # Returns if no column to cancel

    def cancelColumn(self, deck:Deck, col:int):
        cc = self.hand_seen[col]
        a, b, c = cc[0], cc[1], cc[2]
        dCard = c
        if a!=b and b==c:
            dCard = a
        elif a!=b and a==c:
            dCard = b
        self.hand_seen.pop(col)
        deck.discard(dCard)
        
    def setScore(self):
        for col in self.hand_actual:
            for card in col:
                self.score += card

    def getSeenScore(self) -> int:
        seen_score = 0
        for col in self.hand_seen:
            for card in col:
                if card != 13:
                    seen_score += card
        return seen_score
    
    def getCard(self, col:int, row:int) -> int:
        return self.hand_actual[col][row]

    def getUnseenAmt(self) -> int:
        unseen = 0
        for col in self.hand_seen:
            for card in col:
                if card == 13:
                    unseen += 1
        return unseen
    
    def __str__(self) -> str:
        output = ""
        cols = len(self.hand_seen)
        for j in range(0, 3):
            for i in range(0, cols):
                card = self.hand_seen[i][j]
                if card == 13:
                    card = "--"
                output += f"{card}\t"
            output += "\n"
        return output
    
    def __int__(self) -> int:
        return self.id
