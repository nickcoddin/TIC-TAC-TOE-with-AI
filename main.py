import pygame, sys
from gameLogic import *
from consts import SQR_SIZE

create_screen()

def main():
    game = Game()
    board = game.board
    ai = game.ai

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                if event.key == pygame.K_g:
                    game.change_gamemode()

                if event.key == pygame.K_0:
                    ai.level = 0
                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                click_row = mouseY // SQR_SIZE
                click_col = mouseX // SQR_SIZE
                if game.board.available_square(click_row, click_col) and game.running:
                    game.make_move(click_row,click_col)
                    if game.over():
                        game.running =False


        if game.game_mode == "single" and game.player == ai.player and game.running:
            pygame.display.update()
            click_row, click_col = ai.eval(board)
            game.make_move(click_row, click_col)
            if game.over():
                game.running = False

        pygame.display.update()



main()

