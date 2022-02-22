NUM_ROWS = 6
NUM_COLS = 7

def make_new_game(r, c):
    # create new empty game (list)
    # repeat r times (number of rows)
    #   create a new row with c empty strings
    #   add that row to the game
    # return the game
    nl = []
    for i in range(r):
        row = [""] * c
        nl.append(row)
    return nl

def get_winner(game, n):
    pass

def is_draw(game):
    pass

def place_piece(game, col, value):
    pass
