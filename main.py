import game as Game
from player import Player

def humanTurn(game:Game):
    print(f"Discard card: {game.deck.discard_card}")
    print(game.players[0])
    inp = input("Do you want to draw a [n]ew card or draw from the [d]iscard pile? ")
    while inp not in ['n', 'N', 'd', 'D']:
        inp = input("Do you want to draw a [n]ew card or draw from the [d]iscard pile? ")

    # If player wants a new card from deck.
    if inp in ['n', 'N']:
        card = game.deck.draw()
        print(f"\nYour new card is {card}.")
        inp = input("Do you want to [s]wap the new card with one of yours or [d]iscard the new card and flip your own? ")
        while inp not in ['s', 'S', 'd', 'D']:
            inp = input("Do you want to [s]wap the new card with one of yours or [d]iscard the new card and flip your own? ")

        # If player wants to swap card for existing card
        if inp in ['s', 'S']:
            coords = input("Type the coordinates of the card to replace ([row].[col]). ")
            # TODO: needs error handling
            row, col = map(int, coords.split("."))
            oldCard = game.players[0].getCard(row, col)
            game.deck.discard(oldCard)
            game.players[0].swapCard(card, row, col)

        # If player wants to discard new card and reveal hidden card.
        else:
            coords = input("Type the coordinates of the card to replace ([row].[col]). ")
            # TODO: needs error handling
            row, col = map(int, coords.split("."))
            game.players[0].revealCard(row, col)
    # If player wants to use previously discarded card and swap out with existing card
    else:
        card = game.deck.discard_card
        coords = input(f"Type the coordinates of the card to replace ([row].[col]). ")
        # TODO: needs error handling
        row, col = map(int, coords.split("."))
        oldCard = game.players[0].getCard(row, col)
        game.deck.discard(oldCard)
        game.players[0].swapCard(card, row, col)

    game.players[0].humanColumnCancel()    # Checks to see if there is a matching column to discard.


# Main Start ************************************************************************************************

print("Welcome to Python SkyJo!")
while(True):
    inp = input("Do you want to play a game? [Y/n]")
    if inp in ['n', 'no', 'No', 'N']:
        print("Goodbye!")
        break

    # Getting amount of players
    player_count = input("How many players? ")
    while (not player_count.isnumeric()):
        player_count = input("How many players? (Enter a number from 1-8) ")

    # Initializing Game
    game = Game.Game(int(player_count))

    
    # Regular Rounds
    while not game.evalRound:         # check if eval round has started
        if int(game.curPlayer.id) == 0: # While the player is not a bot
            humanTurn(game)
        else:
            if game.curPlayer.makeMove(game.deck):
                game.startEvalRound(game.curPlayer)
            print(f"Bot {game.curPlayer.id}'s hand:\n{game.curPlayer}\n")
        game.nextPlayer()

    # Evaluation Round
    while game.curPlayer != game.evalPlayer:  # Checks if everyone has had their last turn
        if int(game.curPlayer) == 0:
            humanTurn(game)
        else:
            game.curPlayer.makeMove(game.deck)
            print(f"Bot {game.curPlayer.id}'s hand:\n{game.curPlayer}\n")
        game.curPlayer.setScore()
        game.nextPlayer()

    # Display scores and show winner.
    minScore = 145  # Highest possible score would be 144 (12x12) (if there were even 12-12s)
    winningPlayer = Player.Player(-1)
    scores = game.getScores()
    for i in range(0, len(scores)):
        print(f"Player {i}: {scores[i]}")
        if scores[i] < minScore:
            minScore = scores[i]
            winningPlayer = game.players[i]
        print("")
    print(f"Player {winningPlayer.id} is the Winner!\n")
    
    
    

    inp = input("Do you want to play again? [Y/n] ")
    while inp not in ['y', 'Y', 'n', 'N', '']:
        inp = input("Do you want to play again? [Y/n] ")
    if inp in ['n', 'N']:
        break   # End Program