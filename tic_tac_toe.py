#!/bin/python3
"""
The board and stuffies
"""
import random
import sys
import numpy as np
import pygame
import config
from math import inf
from time import sleep
import torch

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
        self.scores = {'X': -10,
                       'O': 10,
                       'draw': 5,
                       ' ': 0}
        self.winner = ' '
        self.winner_x = 0
        self.winner_o = 0
        self.draws = 0
        self.D_in, self.H, self.D_out = 9, 20, 9
        self.model = torch.nn.Sequential(
                torch.nn.Linear(self.D_in, self.H),
                torch.nn.ReLU(),
                torch.nn.Linear(self.H, self.D_out),
        )
        self.loss_fn = torch.nn.MSELoss(reduction='sum')
        self.learning_rate = 1e4
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)

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
                self.winner = self.data[0][0]
                return 1
        if self.data[1][0] != ' ':
            if self.data[1][0] == self.data[1][1] == self.data[1][2]:
                self.winner = self.data[1][0]
                return 1
        if self.data[2][0] != ' ':
            if (self.data[2][0] == self.data[2][1] == self.data[2][2] or
                    self.data[2][0] == self.data[1][1] == self.data[0][2]):
                self.winner = self.data[2][0]
                return 1
        if self.data[0][1] != ' ':
            if self.data[0][1] == self.data[1][1] == self.data[2][1]:
                self.winner = self.data[0][1]
                return 1
        if self.data[0][2] != ' ':
            if self.data[0][2] == self.data[1][2] == self.data[2][2]:
                self.winner = self.data[0][2]
                return 1
        if self.check_draw() == 1:
            self.winner = 'draw'
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

    def random_opp(self):
        done = 0
        while not done:
            if self.winner != ' ':
                done = 1
            row = random.randint(0, 2)
            col = random.randint(0, 2)
            if self.data[row][col] == ' ':
                self.data[row][col] = 'O'
                done = 1

    def translate_board(self):
        liste = []
        for (i, row) in enumerate(self.data):
            for (j, col) in enumerate(row):
                if col == ' ':
                    liste.append(0)
                elif col == 'X':
                    liste.append(-1)
                elif col == 'O':
                    liste.append(1)
        return liste

    def nn_opp(self):
        x = self.translate_board()
        matrix = np.array(x)
        x = torch.Tensor(matrix)

        move = self.nn_opptimised()

        if move[0] == -1:
            print("error")
            sys.exit(-1)

        y = self.translate_board()
        matrix = np.array(y)
        y = torch.Tensor(matrix)

        self.data[move[0]][move[1]] = ' '

        for t in range(100000):
            y_pred = self.model(x)

            loss = self.loss_fn(y_pred, y)
            print(t, loss.item())

            if loss.item() < 0.1:
                break

            self.optimizer.zero_grad()

            loss.backward()

            self.optimizer.step()

    def nn_opptimised(self):
        best_score = -inf
        # if self.data[1][1] == ' ':
            # self.data[1][1] = 'X'
            # return
        move = (-1, -1)
        for (i, row) in enumerate(self.data):
            for (j, col) in enumerate(row):
                if col == ' ':
                    self.data[i][j] = 'O'
                    score = self.minimax(0, False, (i, j))
                    self.winner = ' '
                    self.data[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        #print(move, best_score)
        self.data[move[0]][move[1]] = 'O'
        return move

    def optimized_opp(self):
        best_score = inf
        # if self.data[1][1] == ' ':
            # self.data[1][1] = 'X'
            # return
        for (i, row) in enumerate(self.data):
            for (j, col) in enumerate(row):
                if col == ' ':
                    self.data[i][j] = 'X'
                    score = self.minimax(0, True, (i, j))
                    self.winner = ' '
                    self.data[i][j] = ' '
                    if score < best_score:
                        best_score = score
                        move = (i, j)
        #print(move, best_score)
        self.data[move[0]][move[1]] = 'X'

    def print_evaluation(self, level, move):
        print("|", sep=' ', end=' ')
        for i in range(level):
            print("-", end =' ')
        print(self.scores[self.winner] + level, self.winner, move)

    def minimax(self, depth, is_maximizing, move):
        if self.check_victor() == 1 or self.check_draw() == 1 or depth > 3:
            #self.print_evaluation(depth, move)
            return self.scores[self.winner] + depth
        if is_maximizing:
            best_score = -inf
            for (i, row) in enumerate(self.data):
                for (j, col) in enumerate(row):
                    if col == ' ':
                        self.data[i][j] = 'O'
                        score = self.minimax(depth + 1, False, (i, j))
                        self.winner = ' '
                        self.data[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = inf
            for (i, row) in enumerate(self.data):
                for (j, col) in enumerate(row):
                    if col == ' ':
                        self.data[i][j] = 'X'
                        score = self.minimax(depth + 1, True, (i, j))
                        self.winner = ' '
                        self.data[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score

    def reset_board(self):
        self.data = np.full((3, 3), ' ')
        self.winner = ' '

    def check_state(self):
        if self.check_draw() == 1:
            print('Draw!')
            self.draws += 1
            self.reset_board()
            #sleep(1)
            return 1
        if self.winner != ' ':
            if self.winner == 'X':
                self.winner_x += 1
                print('The winner is', self.winner, "winrate:", self.winner_x / (self.winner_x + self.winner_o + self.draws), "games:", (self.winner_x + self.winner_o + self.draws))
            else:
                self.winner_o += 1
                print('The winner is', self.winner, "winrate:", self.winner_o / (self.winner_x + self.winner_o + self.draws), "games:", (self.winner_x + self.winner_o + self.draws))
            self.reset_board()
            #sleep(1)
            return 1
        return 0

    def run(self):
        #for (i, row) in enumerate(self.data):
            #for (j, col) in enumerate(row):
                #self.data[i][j] = random.choice(['X', 'O'])
                #print(i, j, col)

        while True:
            self.clock.tick(config.FPS)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    print('Exiting...')
                    sys.exit(0)

            self.nn_opp()
            self.random_opp()
            self.check_victor()

            self.board()
            pygame.display.update()

            if self.check_state() == 1:
                continue

            self.optimized_opp()
            self.check_victor()

            self.board()
            pygame.display.update()
            self.nn_opp()

            if self.check_state() == 1:
                continue

if __name__ == '__main__':
    Tic_tac_toe().run()
