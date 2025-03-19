import game as Game


def humanTurn(game:Game):
    print(f"Discard card: {game.getDeck().getDiscardCard()}")
    print(game.players[0])
    inp = input("Do you want to draw a [n]ew card or draw from the [d]iscard pile? ")
    while inp not in ['n', 'N', 'd', 'D']:
        inp = input("Do you want to draw a [n]ew card or draw from the [d]iscard pile? ")

    # If player wants a new card from deck.
    if inp in ['n', 'N']:
        card = game.getDeck().draw()
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
            game.getDeck().setDiscardCard(oldCard)
            game.players[0].swapCard(card, row, col)

        # If player wants to discard new card and reveal hidden card.
        else:
            coords = input("Type the coordinates of the card to replace ([row].[col]). ")
            # TODO: needs error handling
            row, col = map(int, coords.split("."))
            game.players[0].revealCard(row, col)
    # If player wants to use previously discarded card and swap out with existing card
    else:
        card = game.getDeck().getDiscardCard()
        coords = input(f"Type the coordinates of the card to replace ([row].[col]). ")
        # TODO: needs error handling
        row, col = map(int, coords.split("."))
        oldCard = game.players[0].getCard(row, col)
        game.getDeck().setDiscardCard(oldCard)
        game.players[0].swapCard(card, row, col)

    game.players[0].discard_column()    # Checks to see if there is a matching column to discard.
    print(game.players[0])



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

    

    while not game.isGameOver:         # TODO: check if game is over
        if int(game.getCurPlayer()) == 0: # While the player is not a bot
            humanTurn(game)
            game.nextPlayer()
        else:
            game.getCurPlayer().makeMove()
            game.nextPlayer()

    inp = input("Do you want to play again? [Y/n] ")
    while inp not in ['y', 'Y', 'n', 'N', '']:
        inp = input("Do you want to play again? [Y/n] ")
    if inp in ['n', 'N']:
        break   # End Program