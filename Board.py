import pygame
from PIL import Image
from itertools import product


class HalfBoard:

    def __init__(self, cell_size, screen, screen_pos):
        self.image = pygame.image.load(r'C:\Users\d5ffpr\PycharmProjects\TinkerTactics\checkerboard3x5.png')

        self.width = 5 * cell_size
        self.height = 3 * cell_size
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rectangle = self.image.get_rect()
        self.screen = screen
        self.screen_rectangle = screen.get_rect()

        # start all the pieces at the position specified by screen_pos
        self.rectangle.topleft = screen_pos
        self.board_model = [[None for _ in range(5)] for _ in range(3)]

    def blit(self):
        self.screen.blit(self.image, self.rectangle)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_screen_pos(self, newpos):
        self.rectangle.topleft = newpos
        self.screen_pos = newpos

    def set_piece_in_model(self, x, y, piece):
        print(x, y)
        self.board_model[y][x] = piece

    def get_piece_in_model(self, x, y):
        return self.board_model[y][x]


class FullBoard:

    def __init__(self, cell_size, screen, screen_pos, board_model_top, board_model_bottom):
        self.image = pygame.image.load(r'C:\Users\d5ffpr\PycharmProjects\TinkerTactics\checkerboard6x5.png')

        self.width = 5 * cell_size
        self.height = 6 * cell_size
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rectangle = self.image.get_rect()
        self.screen = screen
        self.screen_rectangle = screen.get_rect()

        # start all the pieces at the position specified by screen_pos
        self.rectangle.topleft = screen_pos

        self.board_model = [[None for _ in range(5)] for _ in range(6)]
        for i in range(0, 3):
            for j in range(0, 5):
                self.board_model[i][j] = board_model_top[i][j]
        for i in range(0, 3):
            for j in range(0, 5):
                self.board_model[i+3][j] = board_model_bottom[i][j]
        self.highlighted_cells = [[False for _ in range(5)] for _ in range(6)]

    def blit(self):
        self.screen.blit(self.image, self.rectangle)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_screen_pos(self, newpos):
        self.rectangle.topleft = newpos
        self.screen_pos = newpos

    def set_piece_in_model(self, x, y, piece):
        loc = self.index_of_piece(piece)
        self.board_model[loc[0]][loc[1]] = None
        print(y, x)
        self.board_model[y][x] = piece

    def get_piece_in_model(self, x, y):
        try:
            return self.board_model[y][x]
        except IndexError:
            return None

    def highlight_cell(self, x, y, color):
        self.highlighted_cells[x][y] = True
        self.run_highlights(color)

    def run_highlights(self, color):
        for x in range(5):
            for y in range(6):
                if self.highlighted_cells[y][x]:
                    pygame.draw.rect(self.screen, color, (x * 75 + 5, y * 75 + 5, 75 - 10, 75 - 10), 5)

    def clear_highlighted_cells(self):
        for x in range(5):
            for y in range(6):
                self.highlighted_cells[y][x] = False

    def index_of_piece(self, piece):
        if piece is None:
            return -500, -500
        for i, x in enumerate(self.board_model):
            if piece in x:
                return i, x.index(piece)

    def all_possible_moves(self, x, y, health):
        result = list()
        try:
            if x < 0 or y < 0:
                return result

            if self.board_model[x][y] is None and health == 0:
                result.append((x, y))
                return result
            elif self.board_model[x][y] is not None and health == 0:
                return result
        except IndexError:
            return result

        result.extend(self.all_possible_moves(x, y - 1, health - 1))
        result.extend(self.all_possible_moves(x, y + 1, health - 1))
        result.extend(self.all_possible_moves(x - 1, y, health - 1))
        result.extend(self.all_possible_moves(x + 1, y, health - 1))

        return list(set(result))


