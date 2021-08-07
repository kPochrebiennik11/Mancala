from random import randint
from time import sleep
import pygame
from random import choice
import numpy as np
import math
from copy import deepcopy
from timeit import default_timer as timer

class Bucket:
    def __init__(self, indx, rectangle):
        self.stones = 4
        self.index = indx
        self.rect = rectangle
        if indx < 7:
            self.opposite_index = indx + (6 - indx) * 2
        else:
            self.opposite_index = (indx + (13 - indx) * 2) % 14

    def __str__(self):
        return f' |{self.stones}| '


class Board:
    MOVES_NUMBER = 0
    DEPTH = 3

    def __init__(self):
        global screen
        self.buckets = [Bucket(i, pygame.Rect(20, 30, 60, 60)) for i in range(14)]
        self.buckets[13].stones = 0
        self.buckets[6].stones = 0
        self.is_max_turn = True

    def print_board(self):
        print('|     |  ', end='')
        for i in range(12, 6, -1):
            print(self.buckets[i], end='')
        print('|     |')
        print(f'|  {self.buckets[13].stones}  |\t\t\t\t\t\t\t\t   ', end='')
        print(f'|  {self.buckets[6].stones}  |')
        print('|     |  ', end='')
        for i in range(6):
            print(self.buckets[i], end='')
        print('|     |  ', end='\n\n')

    def make_a_move(self, index):
        current_index = index
        number_of_stones = self.buckets[current_index].stones
        self.buckets[current_index].stones = 0
        for i in range(number_of_stones):
            current_index += 1
            self.buckets[current_index % 14].stones += 1
        if self.buckets[current_index % 14].stones == 1:
            self.beating(index, current_index % 14)
        self.is_max_turn = not self.is_max_turn

    def did_game_end(self):
        return all(0 == self.buckets[i].stones for i in range(6)) or all(0 == self.buckets[i].stones for i in range(7, 13))

    def extra_turn(self, index):
        if self.is_max_turn and index == 6:
            return True
        if not self.is_max_turn and index == 13:
            return True

    def bucket_to_stone_numbers(self):
        return list(map(lambda bucket: bucket.stones, self.buckets))

    def sum_remaining_points(self):
        for b in self.buckets[0:6]:
            print(b.stones, end='  ')
        print('-----')
        for b in self.buckets[7:13]:
            print(b.stones, end='  ')
        self.buckets[6].stones += np.sum(list(map(lambda bucket: bucket.stones, self.buckets[0:6])))
        self.buckets[13].stones += np.sum(list(map(lambda bucket: bucket.stones, self.buckets[7:13])))
        for b in self.buckets[0:5]:
            b.stones = 0
        for b in self.buckets[7:12]:
            b.stones = 0

    def beating(self, first_index, last_index):
        if self.is_max_turn:
            if 0 <= first_index <= 5 and 0 <= last_index <= 5:
                opposite_index = self.buckets[last_index].opposite_index
                self.buckets[6].stones += self.buckets[opposite_index].stones
                self.buckets[opposite_index].stones = 0
        else:
            if 7 <= first_index <= 12 and 7 <= last_index <= 12:
                opposite_index = self.buckets[last_index].opposite_index
                self.buckets[13].stones += self.buckets[opposite_index].stones
                self.buckets[opposite_index].stones = 0

    def who_won(self):
        print('Maximazing player number of moves : ' + str(Board.MOVES_NUMBER))
        print('Stones for maximazing player: ' + str(self.buckets[6].stones))
        print('Stones for minimazing player: ' + str(self.buckets[13].stones))
        if self.buckets[6].stones == self.buckets[13].stones:
            print('DRAW')
            return self.buckets[6].stones, self.buckets[13].stones, self.buckets[6].stones - self.buckets[13].stones
        if self.buckets[6].stones > self.buckets[13].stones:
            print('Maximazing player won by ' + str(self.buckets[6].stones - self.buckets[13].stones))
            return self.buckets[6].stones,  self.buckets[13].stones, self.buckets[6].stones - self.buckets[13].stones
        print('Minimazing player won by ' + str(self.buckets[13].stones - self.buckets[6].stones))
        return self.buckets[6].stones,  self.buckets[13].stones, self.buckets[6].stones - self.buckets[13].stones

    def evaluate_board(self):
        max_player_sum = 0
        min_player_sum = 0
        weights = [1, 1, 1, 1, 1, 1, 1]
        for i in range(7):
            max_player_sum += weights[i] * self.buckets[i].stones
        for i in range(7, 14):
            min_player_sum += weights[i - 7] * self.buckets[i].stones
        return max_player_sum - min_player_sum

    def evaluate_board2(self):
        max_player_sum = 0
        min_player_sum = 0
        weights = [1, 1, 1, 1, 1, 1, 500]
        for i in range(7):
            max_player_sum += weights[i] * self.buckets[i].stones
        for i in range(7, 14):
            min_player_sum += weights[i - 7] * self.buckets[i].stones
        return max_player_sum - min_player_sum

    def evaluate_board3(self):
        max_player_sum = 0
        min_player_sum = 0
        weights = [0, 0, 0, 0, 0, 0, 100]
        for i in range(7):
            max_player_sum += weights[i] * self.buckets[i].stones
        for i in range(7, 14):
            min_player_sum += weights[i - 7] * self.buckets[i].stones
        return max_player_sum - min_player_sum

    def evaluate_board4(self):
        max_player_sum = 0
        min_player_sum = 0
        weights = [1, 1, 1, 2, 2, 3, 4]
        for i in range(7):
            max_player_sum += weights[i] * self.buckets[i].stones * -10
        for i in range(7, 14):
            min_player_sum += weights[i - 7] * self.buckets[i].stones * 100
        return min_player_sum - max_player_sum

    def possible_moves_for_max(self):
        temp = []
        for i in range(6):
            if self.buckets[i].stones > 0:
                temp.append(i)
        return temp

    def possible_moves_for_min(self):
        temp = []
        for i in range(7, 13):
            if self.buckets[i].stones > 0:
                temp.append(i)
        return temp

    def make_random_move(self):
        if self.is_max_turn:
            bucket_index = choice(self.possible_moves_for_max())
            self.make_a_move(bucket_index)
            return bucket_index
        else:
            bucket_index = choice(self.possible_moves_for_min())
            self.make_a_move(bucket_index)
            return bucket_index

    def make_best_move_min(self, depth, eval_function):
        best_index = -1
        min = math.inf
        for move in self.possible_moves_for_min():
            new_board = deepcopy(self)
            new_board.make_a_move(move)
            temp_min = board.minimax_alpha_beta(new_board, depth, False, -math.inf, math.inf, eval_function)
            if temp_min < min:
                min = temp_min
                best_index = move
        self.make_a_move(best_index)
        return best_index

    def make_best_move_max(self, depth, eval_function):
        Board.MOVES_NUMBER += 1
        best_index = -1
        max = -math.inf
        for move in self.possible_moves_for_max():
            new_board = deepcopy(self)
            new_board.make_a_move(move)
            temp_max = board.minimax_alpha_beta(new_board, depth, True, -math.inf, math.inf, eval_function)
            if temp_max > max:
                max = temp_max
                best_index = move
        self.make_a_move(best_index)
        return best_index

    def make_best_move(self, depth_for_max, depth_for_min):
        best_index = -1
        if self.is_max_turn:
            max = -math.inf
            for move in self.possible_moves_for_max():
                new_board = deepcopy(self)
                new_board.make_a_move(move)
                temp_max = board.minimax(new_board, depth_for_max, True)
                if temp_max > max:
                    max = temp_max
                    best_index = move
        else:
            min = math.inf
            for move in self.possible_moves_for_min():
                new_board = deepcopy(self)
                new_board.make_a_move(move)
                temp_min = board.minimax(new_board, depth_for_min, False)
                if temp_min < min:
                    min = temp_min
                    best_index = move
        self.make_a_move(best_index)
        return best_index

    def minimax(self, board, depth, is_max_turn):
        if depth == 0 or board.did_game_end():
            return board.evaluate_board()
        if is_max_turn:
            maxEval = -math.inf
            for move in board.possible_moves_for_max():
                new_board = deepcopy(board)
                new_board.make_a_move(move)
                eval = self.minimax(new_board, depth - 1, False)
                if eval > maxEval:
                    if board.buckets[move].stones > 0:
                        Board.max_next_index = move
                maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = math.inf
            for move in board.possible_moves_for_min():
                new_board = deepcopy(board)
                new_board.make_a_move(move)
                eval = self.minimax(new_board, depth - 1, True)
                if eval < minEval:
                    if board.buckets[move].stones > 0:
                        Board.min_next_index = move
                minEval = min(minEval, eval)
            return minEval

    def minimax_alpha_beta(self, board_passed, depth, is_max_turn, alpha, beta, choose_eval_func):
        if depth == 0 or board_passed.did_game_end():
            if choose_eval_func == 1:
                return board_passed.evaluate_board()
            if choose_eval_func == 2:
                return board_passed.evaluate_board2()
            if choose_eval_func == 3:
                return board_passed.evaluate_board3()
            if choose_eval_func == 4:
                return board_passed.evaluate_board4()
        if is_max_turn:
            maxEval = -math.inf
            for move in board.possible_moves_for_max():
                new_board = deepcopy(board_passed)
                new_board.make_a_move(move)
                eval = self.minimax_alpha_beta(new_board, depth - 1, False, alpha, beta, choose_eval_func)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = math.inf
            for move in board.possible_moves_for_min():
                new_board = deepcopy(board_passed)
                new_board.make_a_move(move)
                eval = self.minimax_alpha_beta(new_board, depth - 1, True, alpha, beta, choose_eval_func)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval


pygame.init()
width = 900
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Mancala')
font = pygame.font.Font('freesansbold.ttf', 15)
bucket_color = (255, 0, 0)
well_color = (47, 79, 79)
highlight_color = (212, 175, 55)
background_color = (220, 220, 220)
surface = None
board = Board()


def render_text(surf, x_position, y_position, bucket_index):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, 15)
    text_surface = font.render(str(board.buckets[bucket_index].stones), False, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x_position + 30, y_position + 20)
    surf.blit(text_surface, text_rect)


def draw_rectangles(surf, last_b_index):
    x = 150
    y1 = 200
    y2 = 100
    highlight_last_bucket = lambda x: highlight_color if x == last_b_index else bucket_color
    for i in range(6):
        board.buckets[i].rect = pygame.draw.rect(screen, highlight_last_bucket(i), pygame.Rect(x, y1, 60, 60), x, y1)
        render_text(surf, x, y1, i)
        board.buckets[12 - i].rect = pygame.draw.rect(screen, highlight_last_bucket(12 - i), pygame.Rect(x, y2, 60, 60), x, y2)
        render_text(surf, x, y2, 12 - i)
        x += 100
    board.buckets[6].rect = pygame.draw.rect(screen, well_color, pygame.Rect(800, 130, 60, 100), 100, 100)
    render_text(surf, 800, 150, 6)
    board.buckets[13].rect = pygame.draw.rect(screen, well_color, pygame.Rect(20, 130, 60, 100), 100, 100)
    render_text(surf, 20, 150, 13)


def display_objects_update(bucket_index):
    draw_rectangles(screen, bucket_index)
    pygame.display.update()


last_bukcet_index = -1


def play_game_player_AI(event):
    global last_bukcet_index
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        for i in range(len(board.buckets)):
            if board.buckets[i].rect.collidepoint(x, y):
                board.make_a_move(i)
                display_objects_update(i)
        sleep(1)
        if last_bukcet_index == - 1:
            last_bukcet_index = board.make_random_move()
        else:
            last_bukcet_index = board.make_best_move()


def play_game_AI_AI(event):
    global last_bukcet_index
    global running
    if event.type == pygame.QUIT:
        running = False
    if board.did_game_end():
        running = False
        return
    #x, y = event.pos
    if last_bukcet_index == - 1:
        last_bukcet_index = board.make_random_move()
        display_objects_update(last_bukcet_index)
        sleep(0.1)
        last_bukcet_index = board.make_random_move()
        display_objects_update(last_bukcet_index)
        sleep(0.1)
    else:
        last_bukcet_index = board.make_best_move_max(7, 3)
        display_objects_update(last_bukcet_index)
        sleep(0.1)
        last_bukcet_index = board.make_best_move_min(4, 1)
        display_objects_update(last_bukcet_index)
        sleep(0.1)

    # if event.type == pygame.MOUSEBUTTONDOWN:

# measures = []
# for j in range(7):
#     temp = []
#     for i in range(10):
#         board_temp = Board()
#         start = timer()
#         board_temp.make_best_move(j, j)
#         stop = timer()
#         temp.append((stop-start))
#     measures.append(np.average(temp))
# print(measures)

scores = []



running = True
while running:
    screen.fill(background_color)
    for event in pygame.event.get():
        play_game_AI_AI(event)
        pygame.event.pump()
    display_objects_update(last_bukcet_index)

board.sum_remaining_points()
scores.append(board.who_won())
# board = Board()
# Board.MOVES_NUMBER = 0

print(scores)

pygame.quit()
