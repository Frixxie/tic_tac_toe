#!/bin/python3
"""
The board and stuffies
"""
import random
import sys
import numpy as np
import pygame
import config

class Tic_tac_toe():
    """
    Organizer
    """
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((config.SCREEN_X, config.SCREEN_Y), 0, 32)

        self.data = np.full((3, 3), ' ')
        self.pos_xo = {(0, 0):(round(config.SCREEN_X / 6), round(config.SCREEN_Y / 6)),
                       (0, 1):(round(config.SCREEN_X / 2), round(config.SCREEN_Y / 6)),
                       (0, 2):(round(config.SCREEN_X / 6 * 5), round(config.SCREEN_Y / 6)),
                       (1, 0):(round(config.SCREEN_X / 6), round(config.SCREEN_Y / 2)),
                       (1, 1):(round(config.SCREEN_X / 2), round(config.SCREEN_Y / 2)),
                       (1, 2):(round(config.SCREEN_X / 6 * 5), round(config.SCREEN_Y / 2)),
                       (2, 0):(round(config.SCREEN_X / 6), round(config.SCREEN_Y / 6 * 5)),
                       (2, 1):(round(config.SCREEN_X / 2), round(config.SCREEN_Y / 6 * 5)),
                       (2, 2):(round(config.SCREEN_X / 6 * 5), round(config.SCREEN_Y / 6 * 5))}
        self.winner = ' '

    def board(self):
        pygame.draw.rect(self.screen, (26, 26, 26),
                         pygame.Rect(0, 0, config.SCREEN_X, config.SCREEN_Y))
        pygame.draw.line(self.screen, (255, 255, 255),
                         (config.SCREEN_X / 3, 0), (config.SCREEN_X / 3, config.SCREEN_Y))
        pygame.draw.line(self.screen, (255, 255, 255),
                         (config.SCREEN_X / 3 * 2, 0), (config.SCREEN_X / 3 * 2, config.SCREEN_Y))
        pygame.draw.line(self.screen, (255, 255, 255),
                         (0, config.SCREEN_Y / 3), (config.SCREEN_X, config.SCREEN_Y / 3))
        pygame.draw.line(self.screen, (255, 255, 255),
                         (0, config.SCREEN_Y / 3 * 2), (config.SCREEN_X, config.SCREEN_Y / 3 * 2))

        for (i, row) in enumerate(self.data):
            print(row)
            for (j, col) in enumerate(row):
                if col == 'O':
                    pygame.draw.circle(self.screen, (255, 255, 255),
                                       self.pos_xo[(i, j)], 45)
                    pygame.draw.circle(self.screen, (26, 26, 26),
                                       self.pos_xo[(i, j)], 44)
                if col == 'X':
                    self.draw_cross(self.pos_xo[(i, j)])

    def draw_cross(self, pos):
        pygame.draw.line(self.screen, (255, 255, 255),
                         (pos[0] - 40, pos[1] - 40), ((pos[0] + 40, pos[1] + 40)))
        pygame.draw.line(self.screen, (255, 255, 255),
                         (pos[0] - 40, pos[1] + 40), ((pos[0] + 40, pos[1] - 40)))

    def check_victor(self):
        if self.data[0][0] != ' ':
            if (self.data[0][0] == self.data[0][1] == self.data[0][2] or
                    self.data[0][0] == self.data[1][0] == self.data[2][0] or
                    self.data[0][0] == self.data[1][1] == self.data[2][2]):
                return 1
        if self.data[1][0] != ' ':
            if self.data[1][0] == self.data[1][1] == self.data[1][2]:
                return 1
        if self.data[2][0] != ' ':
            if (self.data[2][0] == self.data[2][1] == self.data[2][2] or
                    self.data[2][0] == self.data[1][1] == self.data[0][2]):
                return 1
        if self.data[0][1] != ' ':
            if self.data[0][1] == self.data[1][1] == self.data[2][1]:
                return 1
        if self.data[0][2] != ' ':
            if self.data[0][2] == self.data[1][2] == self.data[2][2]:
                return 1
        return 0

    def check_draw(self):
        for row in self.data:
            for col in row:
                if col == ' ':
                    return 0
        return 1

    def player_one(self):
        done = 0
        while done == 0:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    print('Exiting...')
                    sys.exit(0)
            keys = pygame.key.get_pressed()

            if self.winner != ' ':
                done = 1

            if keys[pygame.K_1]:
                if self.data[0][0] == ' ':
                    self.data[0][0] = 'O'
                    done = 1
                    print('kake')
            if keys[pygame.K_2]:
                if self.data[0][1] == ' ':
                    self.data[0][1] = 'O'
                    done = 1
            if keys[pygame.K_3]:
                if self.data[0][2] == ' ':
                    self.data[0][2] = 'O'
                    done = 1
            if keys[pygame.K_4]:
                if self.data[1][0] == ' ':
                    self.data[1][0] = 'O'
                    done = 1
            if keys[pygame.K_5]:
                if self.data[1][1] == ' ':
                    self.data[1][1] = 'O'
                    done = 1
            if keys[pygame.K_6]:
                if self.data[1][2] == ' ':
                    self.data[1][2] = 'O'
                    done = 1
            if keys[pygame.K_7]:
                if self.data[2][0] == ' ':
                    self.data[2][0] = 'O'
                    done = 1
            if keys[pygame.K_8]:
                if self.data[2][1] == ' ':
                    self.data[2][1] = 'O'
                    done = 1
            if keys[pygame.K_9]:
                if self.data[2][2] == ' ':
                    self.data[2][2] = 'O'
                    done = 1

    def random_opp(self, i):
        done = 0
        while done == 0:
            if self.winner != ' ' or i == 8 or i == 9:
                done = 1 
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            if self.data[row][col] == ' ':
                self.data[row][col] = 'X'
                done = 1


    def run(self):
        #for (i, row) in enumerate(self.data):
            #for (j, col) in enumerate(row):
                #self.data[i][j] = random.choice(['X', 'O'])
                #print(i, j, col)
        turn = 0

        while True:
            self.clock.tick(config.FPS)

            self.board()
            pygame.display.update()

            if self.winner != ' ':
                print('The winner is', self.winner)
                sys.exit(0)

            if self.check_draw() == 1:
                print('Draw!')

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    print('Exiting...')
                    sys.exit(0)

            self.player_one()
            turn += 1
            print(turn, self.winner)
            if self.check_victor() == 1 and self.winner == ' ':
                self.winner = 'O'

            self.random_opp(turn)
            turn += 1
            print(turn, self.winner)
            if self.check_victor() == 1 and self.winner == ' ':
                self.winner = 'X'
            

if __name__ == '__main__':
    Tic_tac_toe().run()
