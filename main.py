                                  # CODE FOR THE 'TURTLES WAR ZONE'
                                  #     ASSIGNMENT-1
                                  #  ARTIFICIAL INTELLIGENT
                                  # (BY :
                                  #       1.ABHISHEK SAH (B15CS001).
                                  #       2.AKASH GUPTA  (B15CS003).
                                  # )
#
#
# gui imports and othe used modules inclusion
import random
from copy import deepcopy
import pygame # import pygame package fo interface
# interface developed using pygame

from pygame.locals import *
from sys import exit

#------>>>>>CORE VARIABLES USED IN DEVELOPING THE GAME ####
#EVERY VARIABLES DEFINED ARE HAVING THE COMMENTS RELATED TO THEIR PERSPECTIVE USE IN CODE


#GAME related
best_move = () # best move for the player as determined by strategy
black, white = (), () # black and white players

# gui variables
background_image_filename = 'background.jpg' # image for the background
fps = 5 # framerate of the scene (to save cpu time)
window_size = (256,256) # size of board in pixels
pause = 3
start = True
title = 'TURTLES WAR ZONE'
board_size = 8
left = 1
selected = (0, 1)
board = 0

turn = 'white' # keep track of whose turn it is
move_limit = [150, 0] # move limit for each game (declares game as draw otherwise)

######################## CLASSES ########################
class Piece(object):
    def __init__(self, color, king):
        self.color = color
        self.king = king
# def negascout(board, ply, alpha, beta, player):
#     global best_move
#
#     # find out ply depth for player
#     ply_depth = 0
#     if player != 'black': ply_depth = white.ply_depth
#     else: ply_depth = black.ply_depth
#
class Player(object):
    def __init__(self, type, color, strategy, ply_depth):
        self.type = type
        self.color = color
        self.strategy = strategy
        self.ply_depth = ply_depth


######################## INITIALIZE ########################

# FUNCTION will initialize board with all the pieces
def init_board():
    global move_limit
    move_limit[1] = 0
    result = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-1, -1, -1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1]
    ]

    # ALL PIECES ARE DEFINED TO BE KING SO THAT THEY CAN MOVE ANY WHERE IN THE BOARD
    # UP AND DOWN ,LEFT AND RIGHT
    # EVEN DIAGONAL MOVES ARE ALLOWED

    for m in range(8):
        for n in range(8):
            if (result[m][n] == 1):
                piece = Piece('black', False) # basic black piece
                result[m][n] = piece
            elif (result[m][n] == -1):
                piece = Piece('white', False) # basic white piece
                result[m][n] = piece
    return result

# initialize players
def init_player(type, color, strategy, ply_depth):
    return Player(type, color, strategy, ply_depth)

######################## FUNCTIONS ########################

# will return array with available moves to the player on board
def POSSIBLE_MOVES(board, player):
    moves = []
    for m in range(8):
        for n in range(8):
            if board[m][n] != 0 and board[m][n].color == player: # for all the players pieces...
                # ...check for jumps moves first
                if can_jump([m, n], [m+1, n+1], [m+2, n+2], board) == True: moves.append([m, n, m+2, n+2])
                if can_jump([m, n], [m-1, n+1], [m-2, n+2], board) == True: moves.append([m, n, m-2, n+2])
                if can_jump([m, n], [m+1, n-1], [m+2, n-2], board) == True: moves.append([m, n, m+2, n-2])
                if can_jump([m, n], [m-1, n-1], [m-2, n-2], board) == True: moves.append([m, n, m-2, n-2])
                if can_jump([m, n], [m, n + 1], [m, n + 2], board) == True: moves.append([m, n, m, n + 2])
                if can_jump([m, n], [m , n - 1], [m , n - 2], board) == True: moves.append([m, n, m, n - 2])
                if can_jump([m, n], [m + 1, n], [m + 2, n], board) == True: moves.append([m, n, m + 2, n])
                if can_jump([m, n], [m - 1, n ], [m - 2, n ], board) == True: moves.append([m, n, m - 2, n])

    if player=='white' or len(moves)==0: #len(moves) == 0: # HERE IT CAN MOVE TO ANY DIRECTION
        # ...check for regular moves
        for m in range(8):
            for n in range(8):			#MOVE CHANGE
                if board[m][n] != 0 and board[m][n].color == player: # for all the players pieces...
                    if can_move([m, n], [m+1, n+1], board) == True: moves.append([m, n, m+1, n+1])
                    if can_move([m, n], [m-1, n+1], board) == True: moves.append([m, n, m-1, n+1])
                    if can_move([m, n], [m+1, n-1], board) == True: moves.append([m, n, m+1, n-1])
                    if can_move([m, n], [m-1, n-1], board) == True: moves.append([m, n, m-1, n-1])
                    # if can_move([m, n], [m , n+1], board) == True: moves.append([m, n, m, n+1 ])
                    # if can_move([m, n], [m, n-1], board) == True: moves.append([m, n, m , n - 1])
                    # if can_move([m, n], [m -1, n], board) == True: moves.append([m, n, m - 1, n ])
                    # if can_move([m, n], [m + 1, n], board) == True: moves.append([m, n, m + 1, n])

    return moves # return the list with available jumps or moves

def can_jump(a, via, b, board):
    if b[0] < 0 or b[0] > 7 or b[1] < 0 or b[1] > 7:
        return False
    if board[b[0]][b[1]] != 0: return False
    if board[via[0]][via[1]] == 0: return False
    if board[a[0]][a[1]].color == 'white':
        if board[via[0]][via[1]].color != 'black': return False # only jump blacks
        return True # jump is possible
    if board[a[0]][a[1]].color == 'black':
        if board[via[0]][via[1]].color != 'white': return False # only jump whites
        return True # jump is possible

# will return true if the move is legal
def can_move(a, b, board):
    # is destination off board?
    if b[0] < 0 or b[0] > 7 or b[1] < 0 or b[1] > 7:
        return False
    # does destination contain a piece already?
    if board[b[0]][b[1]] != 0: return False
    return True;
    # for white piece (not king)
    # if board[a[0]][a[1]].king == False and board[a[0]][a[1]].color == 'white':
    #     if b[0] > a[0]: return True #return False # only move up
    #     return True # move is possible
    # # for black piece
    # if board[a[0]][a[1]].king == False and board[a[0]][a[1]].color == 'black':
    #     if b[0] < a[0]: return True # only move down
    #     return True # move is possible
    # # for kings
    # if board[a[0]][a[1]].king == True: return True # move is possible


# make a move on a board, assuming it's legit
def make_move(a, b, board):
    board[b[0]][b[1]] = board[a[0]][a[1]] # make the move
    board[a[0]][a[1]] = 0 # delete the source
    
    # check if we made a king
    # if b[0] == 0 and board[b[0]][b[1]].color == 'white': board[b[0]][b[1]].king = True
    # if b[0] == 7 and board[b[0]][b[1]].color == 'black': board[b[0]][b[1]].king = True
    if abs(a[0] - b[0]) == 2 or abs(a[1]-b[1])==2: # we made a jump...
        board[(a[0]+b[0])/2][(a[1]+b[1])/2] =board[b[0]][b[1]] # DELETE the jumped piece /
                                                #HERE RATHER THAN DELETION WE HAVE TO CONVERT THE JUMPED PLAYER INTO OUR TEAM
        #board[(a[0] + b[0]) / 2][(a[1] + b[1]) / 2] = board[a[0]][a[1]]
	# board[a[0]][a[1]]=0;
    ######################## CORE FUNCTIONS ########################

# will evaluate board for a player
def evaluate(game, player):
    def simple_score(game, player):
        black, white = 0, 0 # keep track of score
        for m in range(8):
            for n in range(8):
                if (game[m][n] != 0 and game[m][n].color == 'black'):
                    if game[m][n].king == False: black += 100
                    else: black += 175
                elif (game[m][n] != 0 and game[m][n].color == 'white'):
                    if game[m][n].king == False: white += 100
                    else: white += 175
        if player != 'black': return white-black
        else: return black-white
    def piece_rank(game, player):
        black, white = 0, 0 # keep track of score
        for m in range(8):
            for n in range(8):
                if (game[m][n] != 0 and game[m][n].color == 'black'): # select black pieces on board
                    if game[m][n].king != True: # not for kings
                        black = black + (m*m)
                elif (game[m][n] != 0 and game[m][n].color == 'white'): # select white pieces on board
                    if game[m][n].king != True: # not for kings
                        white = white + ((7-m)*(7-m))
        if player != 'black': return white-black
        else: return black-white
    def edge_king(game, player):
        black, white = 0, 0 # keep track of score
        for m in range(8):
            if (game[m][0] != 0 and game[m][0].king != False):
                if game[m][0].color != 'white': black += -25
                else: white += -25
            if (game[m][7] != 0 and game[m][7].king != False):
                if game[m][7].color != 'white': black += -25
                else: white += -25
        if player != 'black': return white-black
        else: return black-white

    multi = random.uniform(0.97, 1.03) # will add +/- 3 percent to the score to make things more unpredictable

    return (simple_score(game, player) + piece_rank(game, player) + edge_king(game, player)) * 1

# have we killed the opponent already?
def end_game(board):
    black, white = 0, 0 # keep track of score
    for m in range(8):
        for n in range(8):
            if board[m][n] != 0:
                if board[m][n].color == 'black': black += 1 # we see a black piece
                else: white += 1 # we see a white piece

    return black, white

#                 return alpha # beta cut-off
#         ''' b := alpha+1 '''
#         b = alpha+1 # set new null window
#     ''' return alpha '''
#     if ply == 0: best_move = (moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]) # save the move
#     return alpha
#
# ''' http://en.wikipedia.org/wiki/Negamax '''
# ''' function negamax(node, depth, alpha, beta) '''
# def negamax(board, ply, alpha, beta, player):
#     global best_move
#
# will generate possible moves and board states until a given depth
# ''' http://en.wikipedia.org/wiki/Minimax '''
''' function minimax(node, depth) '''
def minimax(board, player, ply):
    global best_move
    ply_depth = 0
    if player != 'black': ply_depth = white.ply_depth
    else: ply_depth = black.ply_depth
    end = end_game(board)
    if ply >= ply_depth or end[0] == 0 or end[1] == 0: # are we still playing?
        ''' return the heuristic value of node '''
        score = evaluate(board, player) # return evaluation of board as we have reached final ply or end state
        return score
    if player != turn: 
        beta = +10000
        moves = POSSIBLE_MOVES(board, player) # get the available moves for player
        for i in range(len(moves)):
            new_board = deepcopy(board)
            make_move((moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]), new_board)
            if player == 'black': player = 'white'
            else: player = 'black'

            temp_beta = minimax(new_board, player, ply+1)
            if temp_beta < beta:
                beta = temp_beta 
        return beta
    else:
        alpha = -10000
        moves = POSSIBLE_MOVES(board, player)
        for i in range(len(moves)):
            new_board = deepcopy(board)
            make_move((moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]), new_board) # make move on new board
            if player == 'black': player = 'white'
            else: player = 'black'
            temp_alpha = minimax(new_board, player, ply+1)
            if temp_alpha > alpha:
                alpha = temp_alpha # take the highest alpha
                if ply == 0: best_move = (moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]) # save the move as it's our turn
        return alpha
#
# ''' http://en.wikipedia.org/wiki/Negascout '''
# ''' function negascout(node, depth, alpha, beta) '''
# def negascout(board, ply, alpha, beta, player):
#     global best_move
#
#     # find out ply depth for player
#     ply_depth = 0
#     if player != 'black': ply_depth = white.ply_depth
#     else: ply_depth = black.ply_depth
#
#     end = end_game(board)
#
#     ''' if node is a terminal node or depth = 0 '''
#     if ply >= ply_depth or end[0] == 0 or end[1] == 0: # are we still playing?
#         ''' return the heuristic value of node '''
#         score = evaluate(board, player) # return evaluation of board as we have reached final ply or end state
#         return score
#     ''' b := beta '''
#     b = beta
#
#     ''' foreach child of node '''
#     moves = POSSIBLE_MOVES(board, player) # get the available moves for player
#     for i in range(len(moves)):
#         # create a deep copy of the board (otherwise pieces would be just references)
#         new_board = deepcopy(board)
#         make_move((moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]), new_board) # make move on new board
#
#         ''' alpha := -negascout (child, depth-1, -b, -alpha) '''
#         # ...make a switch of players
#         if player == 'black': player = 'white'
#         else: player = 'black'
#
#         alpha = -negascout(new_board, ply+1, -b, -alpha, player)
#         ''' if alpha >= beta '''
#         if alpha >= beta:
#             ''' return alpha '''
#             return alpha # beta cut-off
#         ''' if alpha >= b '''
#         if alpha >= b: # check if null-window failed high
#
#             ''' alpha := -negascout(child, depth-1, -beta, -alpha) '''
#             # ...make a switch of players
#             if player == 'black': player = 'white'
#             else: player = 'black'
#
#             alpha = -negascout(new_board, ply+1, -beta, -alpha, player) # full re-search
#             ''' if alpha >= beta '''
#             if alpha >= beta:
#                 ''' return alpha '''
#                 return alpha # beta cut-off
#         ''' b := alpha+1 '''
#         b = alpha+1 # set new null window
#     ''' return alpha '''
#     if ply == 0: best_move = (moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]) # save the move
#     return alpha
#
# ''' http://en.wikipedia.org/wiki/Negamax '''
# ''' function negamax(node, depth, alpha, beta) '''
# def negamax(board, ply, alpha, beta, player):
#     global best_move
#
#     # find out ply depth for player
#     ply_depth = 0
#     if player != 'black': ply_depth = white.ply_depth
#     else: ply_depth = black.ply_depth
#
#     end = end_game(board)
#
#     ''' if node is a terminal node or depth = 0 '''
#     if ply >= ply_depth or end[0] == 0 or end[1] == 0: # are we still playing?
#         ''' return the heuristic value of node '''
#         score = evaluate(board, player) # return evaluation of board as we have reached final ply or end state
#         return score
#
#     ''' else '''
#     ''' foreach child of node '''
#     moves = POSSIBLE_MOVES(board, player) # get the available moves for player
#     for i in range(len(moves)):
#         # create a deep copy of the board (otherwise pieces would be just references)
#         new_board = deepcopy(board)
#         make_move((moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]), new_board) # make move on new board
#
#         ''' alpha := max(alpha, -negamax(child, depth-1, -beta, -alpha)) '''
#         # ...make a switch of players
#         if player == 'black': player = 'white'
#         else: player = 'black'
#
#         temp_alpha = -negamax(new_board, ply+1, -beta, -alpha, player)
#         if temp_alpha >= alpha:
#             if ply == 0: best_move = (moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]) # save the move
#             alpha = temp_alpha
#
#         ''' {the following if statement constitutes alpha-beta pruning} '''
#         ''' if alpha>=beta '''
#         if alpha >= beta:
#             ''' return beta '''
#             if ply == 0: best_move = (moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]) # save the move
#             return beta
#     ''' return alpha '''
#     return alpha

# ''' http://www.ocf.berkeley.edu/~yosenl/extras/alphabeta/alphabeta.html '''
''' algorithm alpha-beta pruning(player,board,alpha,beta) '''
def alpha_beta(player, board, ply, alpha, beta):
    global best_move
    ply_depth = 0
    if player != 'black': ply_depth = white.ply_depth
    else: ply_depth = black.ply_depth
    end = end_game(board)
    if ply >= ply_depth or end[0] == 0 or end[1] == 0: # are we still playing?
        ''' return winner '''
        score = evaluate(board, player) 
        return score
    moves = POSSIBLE_MOVES(board, player) 
    if player == turn: 
        for i in range(len(moves)):
            new_board = deepcopy(board)
            make_move((moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]), new_board) 
            if player == 'black': player = 'white'
            else: player = 'black'
            score = alpha_beta(player, new_board, ply+1, alpha, beta)
            if score > alpha:
                if ply == 0: best_move = (moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]) # save the move
                alpha = score
            ''' if alpha >= beta then return alpha (cut off) '''
            if alpha >= beta:
                #if ply == 0: best_move = (moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]) # save the move
                return alpha
        return alpha

    else:
        for i in range(len(moves)):
            new_board = deepcopy(board)
            make_move((moves[i][0], moves[i][1]), (moves[i][2], moves[i][3]), new_board) # make move on new board
            if player == 'black': player = 'white'
            else: player = 'black'
            score = alpha_beta(player, new_board, ply+1, alpha, beta)
            if score < beta: beta = score
            if alpha >= beta: return beta
        return beta
def end_turn():
    global turn 
    if turn != 'black':	turn = 'black'
    else: turn = 'white'
def cpu_play(player):
    global board, move_limit # global variables
    if player.strategy == 'minimax': alpha = minimax(board, player.color, 0)
    elif player.strategy == 'negascout': alpha = negascout(board, 0, -10000, +10000, player.color)
    elif player.strategy == 'negamax': alpha = negamax(board, 0, -10000, +10000, player.color)
    elif player.strategy == 'alpha-beta': alpha = alpha_beta(player.color, board, 0, -10000, +10000)
    if alpha == -10000: # no more moves available... all is lost
        if player.color == white: show_winner("black")
        else: show_winner("white")
    make_move(best_move[0], best_move[1], board) # make the move on board
    move_limit[1] += 1 # add to move limit
    end_turn()
def draw_piece(row, column, color, king):
    posX = ((window_size[0]/8)*column) - (window_size[0]/8)/2
    posY = ((window_size[1]/8)*row) - (window_size[1]/8)/2
    if color == 'black':
        border_color = (255, 255, 255)
        inner_color = (109,161,251)#(0, 0, 0)
    elif color == 'white':
        border_color = (0, 0, 0)
        inner_color = (236,63,26)#(255, 255, 255)
    pygame.draw.circle(screen, border_color, (posX, posY), 3)
    pygame.draw.circle(screen, inner_color, (posX, posY), 5)
def ply_check():
    global black, white
    if black.type != 'cpu': black.ply_depth = white.ply_depth
    elif white.type != 'cpu': white.ply_depth = black.ply_depth
def player_check():
    global black, white

    if black.type != 'cpu' or black.type != 'human': black.type = 'cpu'
    if white.type != 'cpu' or white.type != 'human': white.type = 'cpu'

    if black.ply_depth <0: black.ply_depth = 1
    if white.ply_depth <0: white.ply_depth = 1

    if black.color != 'black': black.color = 'black'
    if white.color != 'white': white.color = 'white'

    if black.strategy != 'minimax' or black.strategy != 'negascout':
        if black.strategy != 'negamax' or black.strategy != 'alpha-beta': black.strategy = 'alpha-beta'
    if white.strategy != 'minimax' or white.strategy != 'negascout':
        if white.strategy != 'negamax' or white.strategy != 'alpha-beta': white.strategy = 'alpha-beta'

# initialize the game with the proper difficulty level players and the boardfor the game
def game_init(difficulty):
    global black, white
    # if difficulty == 'hard':
    #     black = init_player('cpu', 'black', 'alpha-beta', 8) # init black player
    #     white = init_player('human', 'white', 'alpha-beta', 8) # init white player
    #     board = init_board()
    # elif difficulty == 'moderate':
    #     black = init_player('cpu', 'black', 'alpha-beta', 4) # init black player
    #     white = init_player('human', 'white', 'alpha-beta', 4) # init white player
    #     board = init_board()
    # easy difficult
    # else:
    black = init_player('cpu', 'black', 'alpha-beta', 1) # init black player
    white = init_player('human', 'white', 'alpha-beta', 1) # init white player
    board = init_board()

    return board

######################## GUI FUNCTIONS ########################

# show countdown on screen
def show_countdown(i):
    while i >= 0:
        tim = font_big.render(' '+repr(i)+' ', True, (255, 255, 255), (20, 160, 210)) # create message
        timRect = tim.get_rect() # create a rectangle
        timRect.centerx = screen.get_rect().centerx# center the rectangle
        timRect.centery = screen.get_rect().centery +50
        screen.blit(tim, timRect) # blit the text
        pygame.display.flip() # display scene from buffer
        i-=1
        pygame.time.wait(1000) # pause game for a second

# show message for user on screen
def show_message(message):
    text = font.render(' ' + message + ' ', True, (255, 255, 255), (120, 195, 46))  # create message
    textRect = text.get_rect() 
    textRect.centerx = screen.get_rect().centerx  
    textRect.centery = screen.get_rect().centery
    screen.blit(text, textRect) 
def show_winner(winner):
    global board
    if winner == 'draw': show_message("draw ...")
    else: show_message(winner+' wins')
    pygame.display.flip()
    show_countdown(pause)
    board = init_board()
def mouse_click(pos):
    global selected, move_limit
    if (turn != 'black' and white.type != 'cpu') or (turn != 'white' and black.type != 'cpu'):
        column = pos[0]/(window_size[0]/board_size)
        row = pos[1]/(window_size[1]/board_size)
        if board[row][column] != 0 and board[row][column].color == turn:
            selected = row, column
        else:
            moves = POSSIBLE_MOVES(board, turn)
            for i in range(len(moves)):
                if selected[0] == moves[i][0] and selected[1] == moves[i][1]:
                    if row == moves[i][2] and column == moves[i][3]:
                        make_move(selected, (row, column), board) # make the move
                        move_limit[1] += 1 # add to move limit
                        end_turn() # end turn

######################## START OF GAME ########################

pygame.init()

board = game_init('easy')
        # INITIALISE PLAYERS AND BOARD FOR THE GAME
        #HERE WE CAN SELECT THE GAME DIFFICULTY AS PER USER REQUIREMENTS
ply_check() # make changes to player's ply if playing vs human

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption(title)
clock = pygame.time.Clock()

background = pygame.image.load(background_image_filename).convert()
font = pygame.font.Font('freesansbold.ttf', 11)
font_big = pygame.font.Font('freesansbold.ttf', 13)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == left:
            mouse_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                board = game_init('easy')
            if event.key == pygame.K_F2:
                board = game_init('moderate')
            if event.key == pygame.K_F3:
                board = game_init('hard')
    screen.blit(background, (0, 0))
    if (turn != 'black' and white.type == 'human') or (turn != 'white' and black.type == 'human'): show_message('YOUR TURN')
    else: show_message('CPU THINKING...')
    for m in range(8):
        for n in range(8):
            if board[m][n] != 0:
                draw_piece(m+1, n+1, board[m][n].color, board[m][n].king)
    if start == True:
        show_message(''+title)
        show_countdown(pause)
        start = False
    end = end_game(board)
    if end[1] == 0:	show_winner("black")
    elif end[0] == 0: show_winner("white")
    elif move_limit[0] == move_limit[1]: show_winner("draw")
    else: pygame.display.flip()
    if turn != 'black' and white.type == 'cpu': cpu_play(white)
    elif turn != 'white' and black.type == 'cpu': cpu_play(black)
clock.tick(fps)
# part of the screen
#     im=ImageGrab.grab(bbox=(1000,100,1400,600)) # X1,Y1,X2,Y2
#     # im.show()
#     im.save('1.png')
#     #image to text
    #     i= image_to_string(Image.open('1.png'))
    #     print ("i "+i)
    #     j=i.split("\n")
    #     for k in range(0,len(j)):
# 
# def negascout(board, ply, alpha, beta, player):
#     global best_move
#
#     # find out ply depth for player
#     ply_depth = 0
#     if player != 'black': ply_depth = white.ply_depth
#     else: ply_depth = black.ply_depth
#
#     print j[k]
#     ques=""
#     ans1=""
#     ans2=""
#     ans3=""
#     ans3=j[len(j)-1]
#     ans2=j[len(j)-3]
#     ans1=j[len(j)-5]
#     for k in range(0,len(j)-5):
#         ques+=j[k]+" "
#     print ques, ans1,ans2,ans3
#
#     webbrowser.open("https://www.google.co.in/search?q="+ques, new=2)
#    #