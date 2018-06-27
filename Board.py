import pygame
from PIL import Image


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
        self.board_model = board_model_top.extend(board_model_bottom)

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