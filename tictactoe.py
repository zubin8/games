##########################
# Game graphic interface #
##########################

from tkinter import *
from random import *
from math import *
import time
import copy

SIZE = 500
GRID_LEN = 3

GRID_PADDING = max(1, 20 // GRID_LEN)
WHITE_COLOR = "#ffffff"
BLACK_COLOR = "#000000"
WIN_BACKGROUND_COLOR = "#dabbbb"
BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_DICT = {"":"#9e948a",
                         "O":"#eee4da",
                         "X":"#e4eeda"}
CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65" }
DEFAULT_CELL_COLOR = "#f9f6f2"
FONT = ("Verdana", max(1, 160 // GRID_LEN), "bold")
SCORE_FONT = ("Verdana", max(15, 80 // GRID_LEN), "bold")

class GameGrid(Frame):
    def __init__(self, logic):
        Frame.__init__(self)
        self.l = logic
        self.grid()
        self.master.title('Tic Tac Toe')
        self.players = ['X', 'O']
        self.grid_cells = []
        self.init_grid()
        self.init_info()
        self.restart_game()
        self.mainloop()

    def restart_game(self):
        self.is_game_over = False
        self.turn = 0
        self.game_state = self.l['make_new_game']()
        self.update_grid_cells()
        self.update_info()
        self.status_label.config(text='Turn', bg=WHITE_COLOR)

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid()

        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background,
                             bg=BACKGROUND_COLOR_DICT[""],
                             width=SIZE / GRID_LEN,
                             height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                t = Label(master=cell, text='', bg=BACKGROUND_COLOR_DICT[""], justify=CENTER, font=FONT, width=4, height=2)
                t.i = i
                t.j = j
                t.grid()
                t.bind("<Button-1>", lambda ev,t=t: self.update_round(t))
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def update_round(self, t):
        if self.is_game_over:
            self.restart_game()
            return
        current_player = self.players[self.turn%2]
        old_state = copy.deepcopy(self.game_state)
        self.game_state = self.l['add_value'](self.game_state, t.i, t.j, current_player)
        if old_state == self.game_state:
            return
        self.update_grid_cells()
        self.update_info()

    def init_info(self):
        self.turn = 0
        current_player = self.players[self.turn%2]
        info_container = Frame(self, width=SIZE, height=50)
        info_container.grid()

        player_label = Frame(info_container, bg=WHITE_COLOR, width=SIZE / 2, height=20)
        player_label.grid(row=0, column=0, columnspan=1, padx=GRID_PADDING, pady=GRID_PADDING)
        self.player_label = Label(master=player_label, text=current_player, fg=BLACK_COLOR, bg=WHITE_COLOR, justify=RIGHT, font=SCORE_FONT, width=10, height=1)
        self.player_label.pack()

        status_label = Frame(info_container, bg=WHITE_COLOR, width=SIZE / 2, height=20)
        status_label.grid(row=0, column=1, columnspan=1, padx=GRID_PADDING, pady=GRID_PADDING)
        self.status_label = Label(master=status_label, text="Turn", fg=BLACK_COLOR, bg=WHITE_COLOR, justify=RIGHT, font=SCORE_FONT, width=10, height=1)
        self.status_label.pack()

    def update_grid_cells(self):
        current_matrix = self.game_state
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                value = current_matrix[i][j]
                self.grid_cells[i][j].configure(text=value, fg=BLACK_COLOR, bg=BACKGROUND_COLOR_DICT[value])
        self.update_idletasks()

    def update_info(self):
        if self.l['get_winner'](self.game_state) is not None:
            self.is_game_over = True
            self.player_label.config(bg=WIN_BACKGROUND_COLOR)
            self.status_label.config(text='Won!', bg=WIN_BACKGROUND_COLOR)
            for i,j in self.get_winning_cells():
                self.grid_cells[i][j].configure(bg=WIN_BACKGROUND_COLOR)
        elif self.l['is_draw'](self.game_state):
            self.is_game_over = True
            self.player_label.config(text="Draw!", bg=WIN_BACKGROUND_COLOR)
            self.status_label.config(text='Draw!', bg=WIN_BACKGROUND_COLOR)
        else:
            self.turn += 1
            current_player = self.players[self.turn%2]
            self.player_label.config(text=current_player, bg=WHITE_COLOR)
            if self.turn % 2 == 0 and self.l.get('ai'):
                i, j = self.l['ai'](self.game_state)
                tile = self.grid_cells[i][j]
                self.update_round(tile)

    def get_winning_cells(self):
        game = self.game_state
        for i in range(3):
            if game[i][0] != '' and game[i][0] == game[i][1] == game[i][2]:
                return (i,0), (i,1), (i,2)
            if game[0][i] != '' and game[0][i] == game[1][i] == game[2][i]:
                return (0,i), (1,i), (2,i)
        if game[0][0] != '' and game[0][0] == game[1][1] == game[2][2]:
            return (0,0), (1,1), (2,2)
        if game[2][0] != '' and game[2][0] == game[1][1] == game[0][2]:
            return (2,0), (1,1), (0,2)
        return ()
            

def make_new_game():
    return [["" ,"" ,"" ],["" ,"" ,"" ],["" ,"" ,"" ]]

def add_value(game, i, j, value):
    if game[i][j]=="":
        game[i][j]=value
    return game

def get_winner(game):
    ''' return value if there are 3 in a row, unless it is an empty string '''
    if game[0][0]== game[1][1]==game[2][2] =="O" or \
        game[0][0]== game[0][1]==game[0][2] =="O" or \
         game[0][0]== game[1][0]==game[2][0] =="O" or \
          game[2][0]== game[2][1]==game[2][2] =="O" or \
           game[0][2]== game[1][2]==game[2][2] =="O" or \
            game[0][1]== game[1][1]==game[2][1] =="O" or \
             game[1][0]== game[1][1]==game[1][2] =="O" or \
              game[0][2]== game[1][1]==game[2][0] =="O":
        return "O"
    elif game[0][0]== game[1][1]==game[2][2] =="X" or \
          game[0][0]== game[0][1]==game[0][2] =="X" or \
           game[0][0]== game[1][0]==game[2][0] =="X" or \
            game[2][0]== game[2][1]==game[2][2] =="X" or \
             game[0][2]== game[1][2]==game[2][2] =="X" or \
              game[0][1]== game[1][1]==game[2][1] =="X" or \
               game[1][0]== game[1][1]==game[1][2] =="X" or \
                game[0][2]== game[1][1]==game[2][0] =="X":
        return "X"
def flattenlen(game):
    ns = ""
    for i in range(len(game)):
        for j in range(len(game)):
            ns += game[i][j]
    if len(ns) == 9:
        return True
    return False

def is_draw(game):
    if flattenlen(game) == True:
        return "Is draw"

from random import randint

def iT(game):
    '''
    go through every cell in the grid (every row/col)
        if cell is empty,
           try and put the x at that position
           then check if x wins:
              we need to put at this position
    put at random empty position
    '''
    for i in range(len(game)):
        for j in range(len(game[i])):
            if game[i][j] == "":
                game[i][j] = "X"
                if get_winner(game) == "X":
                    game[i][j] = ""
                    return (i,j)
                else:
                    game[i][j] = ""
                    
    for i in range(len(game)):
        for j in range(len(game[i])):
            if game[i][j] == "":
                game[i][j] = "O"
                if get_winner(game) == "O":
                    game[i][j] = ""
                    return (i,j)
                else:
                    game[i][j] = ""
    i = randint(0,2)
    j = randint(0,2)
    while game[i][j] != "":
        i = randint(0,2)
        j = randint(0,2)
    return (i,j)


gamegrid = GameGrid({
    'make_new_game': make_new_game,
    'add_value': add_value,
    'get_winner': get_winner,
    'is_draw': is_draw,
    'ai': iT,
})
