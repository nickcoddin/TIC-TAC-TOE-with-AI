import copy
import random
from consts import *
import pygame
import numpy as np

def create_screen():
    global screen
    pygame.display.set_caption("TIC-TAC-TOE")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BACKGROUND_COLOR)



class Board:

    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_squares = self.squares
        self.mark_square = 0

    def final_state(self, show = False):
        '''
        :return: 0 if there is no win
        :return: 1 if player 1  wins
        :return: 2 if player 2  wins
        '''

        # Vertical
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = O_COLOR if self.squares[1][col] == 2  else X_COLOR
                    sPos = (col * SQR_SIZE + SQR_SIZE//2, 20)
                    ePos = (col * SQR_SIZE + SQR_SIZE//2, HEIGHT - 20)

                    pygame.draw.line(screen, color, sPos, ePos, LINE_WIDTH)
                return self.squares[0][col]

        # Horizontal
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = O_COLOR if self.squares[row][1] == 2 else X_COLOR
                    sPos = (20, row * SQR_SIZE + SQR_SIZE // 2)
                    ePos = (WIDTH - 20, row * SQR_SIZE + SQR_SIZE // 2)

                    pygame.draw.line(screen, color, sPos, ePos, LINE_WIDTH)
                return self.squares[row][0]

        # Diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = O_COLOR if self.squares[1][1] == 2 else X_COLOR
                sPos = (20, 20)
                ePos = (WIDTH - 20, HEIGHT - 20)

                pygame.draw.line(screen, color, sPos, ePos, LINE_WIDTH)

            return self.squares[1][1]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = O_COLOR if self.squares[1][1] == 2 else X_COLOR
                sPos = (20, HEIGHT - 20)
                ePos = (WIDTH-20, 20)

                pygame.draw.line(screen, color, sPos, ePos, LINE_WIDTH)
            return self.squares[1][1]

        return 0


    def mark_sqr(self,row, col, player):
        self.squares[row][col] = player
        self.mark_square += 1

    def available_square(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_square(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.available_square(row, col):
                    empty_squares.append((row, col))
        return empty_squares

    def is_full(self):
        return self.mark_square == 9

    def is_empty(self):
        return self.mark_square == 0


class AI:
    def __init__(self, level = 1, player = 2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_squares = board.get_empty_square()
        idx = random.randrange(0, len(empty_squares))
        return empty_squares[idx]

    def minimax(self, board, maximizing):
        case = board.final_state()
        if case == 1:
            return 1, None
        if case == 2:
            return -1, None
        elif board.is_full():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_squares = board.get_empty_square()

            for (row, col) in empty_squares:
                new_board = copy.deepcopy(board)
                new_board.mark_sqr(row, col, 1)
                eval = self.minimax(new_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_squares = board.get_empty_square()

            for (row, col) in empty_squares:
                new_board = copy.deepcopy(board)
                new_board.mark_sqr(row, col, self.player)
                eval = self.minimax(new_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move



    def eval(self, main_board):
        if self.level == 0:
            eval = "Random"
            move = self.rnd(main_board)
        else:
            eval, move = self.minimax(main_board, False)

        print('AI has chosen to mark the square on position {} with an evaluation of : {}'.format(move, eval))
        return move


class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.game_mode = "single"  #multiplayer  vs singleplayer
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_figure(row, col)
        self.change_turn()

    def show_lines(self):

        screen.fill(BACKGROUND_COLOR)

        #Horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQR_SIZE), (WIDTH, SQR_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT-SQR_SIZE), (WIDTH, HEIGHT-SQR_SIZE), LINE_WIDTH)

        #Vertical
        pygame.draw.line(screen, LINE_COLOR, (SQR_SIZE, 0), (SQR_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH-SQR_SIZE, 0), (WIDTH-SQR_SIZE, HEIGHT), LINE_WIDTH)

    def draw_figure(self, row , col):
        if self.player == 1:
            start_pos = (col * SQR_SIZE + X_SPACE, row * SQR_SIZE + X_SPACE)
            end_pos = (col * SQR_SIZE + SQR_SIZE - X_SPACE, row * SQR_SIZE + SQR_SIZE - X_SPACE)
            pygame.draw.line(screen, X_COLOR, start_pos, end_pos, X_WIDTH)

            start_pos2 = (col * SQR_SIZE + X_SPACE, row * SQR_SIZE + SQR_SIZE - X_SPACE)
            end_pos2 = (col * SQR_SIZE + SQR_SIZE - X_SPACE, row * SQR_SIZE + X_SPACE)
            pygame.draw.line(screen, X_COLOR, start_pos2, end_pos2, X_WIDTH)

        elif self.player == 2:
            center = (col * SQR_SIZE + SQR_SIZE//2, row * SQR_SIZE + SQR_SIZE//2)
            pygame.draw.circle(screen, O_COLOR, center, O_RADIUS, O_WIDTH)


    def change_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
       if self.game_mode == "single":
           self.game_mode = "multi"
       else:
           self.game_mode = "single"

    def over(self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()

    def reset(self):
        self.__init__()












