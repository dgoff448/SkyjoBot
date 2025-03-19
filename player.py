

class Player:
    def __init__(self, id:int):
        self.id = id
        self.hand_actual = []
        self.hand_seen = [[13,13,13],[13,13,13],[13,13,13],[13,13,13]]
        self.score = 0

    def setHand(self, hand:list[list[int]]):
        self.hand_actual = hand

    def swapCard(self, card:int, row:int, col:int) -> int:
        oldCard = self.hand_actual[row][col]
        self.hand_actual[row][col] = card
        self.revealCard(row, col)
        return oldCard

    def revealCard(self, row:int, col:int):
        self.hand_seen[row][col] = self.hand_actual[row][col]

    def discard_column(self):
        for col in self.hand_actual:
            if (col[0] == col[1]) and (col[1] == col[2]):
                ind = self.hand_actual.index(col)
                self.hand_seen.pop(ind)
                self.hand_actual.pop(ind)

    def setScore(self):
        for col in self.hand_actual:
            for card in col:
                self.score += card

    def getScore(self) -> int:
        return self.score
    
    def getCard(self, row:int, col:int) -> int:
        return self.hand_actual[row][col]
    
    def getID(self) -> int:
        return self.id
    
    def getUnseenCards(self) -> int:
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
