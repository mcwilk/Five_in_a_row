import numpy as np
import pygame
import sys


# CONSTANTS:
PLAYER_1 = 1
PLAYER_2 = 2

XMARK = 'X'
OMARK = 'O'

BOARD_SIZE = 8
FIELD_SIZE = 50
INFO_ROW_SIZE = 50
MARGIN = 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

TIE = 'Tie game!'


# FUNCTIONS:
def empty_board():
    '''Function creates an empty matrix for a board'''

    board = np.zeros((BOARD_SIZE, BOARD_SIZE))
    moves = []
    
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            moves.append((y, x))
   
    return board, moves


def possible_moves(board, moves):
    '''Function specifies all possible moves'''

    poss_moves = []
    for item in moves:
        if board[item[0]][item[1]] == 0:
            poss_moves.append(item)

    return poss_moves


def user_turn(event, board, moves):
    '''Function reads user's move'''

    poss_moves = possible_moves(board, moves)
    move = False

    while not move:
        posx = event.pos[0]
        posy = event.pos[1]
        x = posx // FIELD_SIZE
        y = posy // FIELD_SIZE
        move = (y, x)

    return move


def change_turn(turn):
    '''Function changes a turn'''
    
    if turn == 1:
        return 2
    else:
        return 1


def is_winner(board, turn):
    '''Function checks if there is a winner'''

    # check if there is vertical winner:
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE - 4):
            if board[x][y] == board[x][y+1] == board[x][y+2] == board[x][y+3] == board[x][y+4] == turn:
                winner = turn
                return winner

    # check if there is horizontal winner:
    for x in range(BOARD_SIZE - 4):
        for y in range(BOARD_SIZE):
            if board[x][y] == board[x+1][y] == board[x+2][y] == board[x+3][y] == board[x+4][y] == turn:
                winner = turn
                return winner

    # check if there is a diagonal winner:
    ## negative (\\\):
    for x in range(BOARD_SIZE - 4):
        for y in range(BOARD_SIZE - 4):
            if board[x][y] == board[x+1][y+1] == board[x+2][y+2] == board[x+3][y+3] == board[x+4][y+4] == turn:
                winner = turn
                return winner

    ## positive (///):
    for x in range(BOARD_SIZE - 4):
        for y in range(4, BOARD_SIZE):
            if board[x][y] == board[x+1][y-1] == board[x+2][y-2] == board[x+3][y-3] == board[x+4][y-4] == turn:
                winner = turn
                return winner

    # check if it is a tie game:
    if 0 not in board:
        winner = TIE
        return winner


def draw_board(board, screen, mainFont):
    '''Function draws a board'''
    
    for x in range(BOARD_SIZE):

        for y in range(BOARD_SIZE):
            pygame.draw.rect(screen, WHITE, (x * FIELD_SIZE, y * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE), MARGIN)
            
            if board[y][x] == 0:
                pygame.draw.rect(screen, WHITE, (x * FIELD_SIZE, y * FIELD_SIZE, FIELD_SIZE, FIELD_SIZE), 2)
            elif board[y][x] == 1:
                mark_X(board, screen, mainFont, x, y)
            else:
                mark_O(board, screen, mainFont, x, y)

    pygame.display.update()


def centerXY(x, y):
    '''Function returns position for mark after mouse button click'''

    centerX = (x * FIELD_SIZE) + 8
    centerY = (y * FIELD_SIZE)

    return centerX, centerY


def mark_X(board, screen, mainFont, x, y):
    '''Function draws X mark on the board'''

    centerX, centerY = centerXY(x, y)
    mark = mainFont.render(XMARK, 1, RED)
    screen.blit(mark, (centerX, centerY))


def mark_O(board, screen, mainFont, x, y):
    '''Function draws O mark on the board'''

    centerX, centerY = centerXY(x, y)
    mark = mainFont.render(OMARK, 2, YELLOW)
    screen.blit(mark, (centerX, centerY))


def final_result(winner):
    '''Function returns final result statement'''

    if winner == 1:
        statement = "Player 1 wins!"
    elif winner == 2:
        statement = "Player 2 wins!"
    else:
        statement = "It's a tie game!"

    return statement


def draw_result(screen, statement, infoFont):
    '''Function draws final result statement'''

    result_info = infoFont.render(statement, 1, GREEN)
    screen.blit(result_info, (100, BOARD_SIZE * FIELD_SIZE + 10))


def main():
    '''Main program'''

    player_1_score = 0
    player_2_score = 0
    tie_score = 0
    turn = PLAYER_1
    result = False

    width = BOARD_SIZE * FIELD_SIZE
    height = width + INFO_ROW_SIZE
    window_size = (width, height)
    board, moves = empty_board()

    pygame.init()
    pygame.display.set_caption('Five in a row')

    mainFont = pygame.font.SysFont('Arial', 45)
    smallFont = pygame.font.SysFont('Arial', 25)
    infoFont = pygame.font.SysFont('Arial', 30)
    screen = pygame.display.set_mode(window_size)

    draw_board(board, screen, mainFont)
    
    pygame.display.update()

    # Print empty board:
    print(board)

    # 3. When game is still in progress:
    while not result:

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Ask Player_1 for input
                if turn == PLAYER_1:
                    move = user_turn(event, board, moves)
                    board[move[0]][move[1]] = turn
                    winner = is_winner(board, turn)

                # Ask Player_2 for input
                else:
                    move = user_turn(event, board, moves)
                    board[move[0]][move[1]] = turn
                    winner = is_winner(board, turn)
                
                # Update board
                draw_board(board, screen, mainFont)
                print(board)

                # Check if there is a winner
                if winner:
                    result = True
                    break
                else:
                    turn = change_turn(turn)

    statement = final_result(winner)
    draw_result(screen, statement, infoFont)
    draw_board(board, screen, mainFont)
    pygame.time.wait(25000)


if __name__ == '__main__':
    main()