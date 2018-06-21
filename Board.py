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

    def blit(self):
        self.screen.blit(self.image, self.rectangle)

    def get_width(self):
        return self.width