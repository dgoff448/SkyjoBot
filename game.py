import deck as Deck
import player as Player

class Game:
    def __init__(self, player_count):
        self.player_count = player_count
        self.players = []
        self.deck = Deck.Deck()
        self.curPlayer = Player.Player(-1)      # Later set to players[0]
        self.isGameOver = False
        self.evalRound = False
        self.evalPlayer:Player = Player.Player(-1)    # Player that started eval round

        # Initializing Players
        for i in range(0, player_count):
            player = Player.Player(i)
            self.makeHand(player)
            self.players.append(player)
        self.curPlayer = self.players[0]

        # Prime Discard Pile
        self.deck.discard(self.deck.draw())

    def startEvalRound(self, player:Player):
        self.evalRound = True
        self.evalPlayer = player

    def makeHand(self, player:Player):
        hand = []
        for i in range(0, 4):
            col = []
            for j in range(0, 3):
                col.append(self.deck.draw())
            hand.append(col)
        player.setHand(hand)

    def nextPlayer(self):
        self.curPlayer += 1
        if self.curPlayer > self.player_count - 1:
            self.curPlayer = 0

    def getScores(self) -> list[int]:
        scores = []
        for player in self.players:
            scores.append(player.score)
        return scores