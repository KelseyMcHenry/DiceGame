
from random import randint
import pygame
from PIL import Image
from Settings import Settings


class Piece:
    team = 'n/a'
    sides = 0
    health = 0
    pos = (-1, -1)
    highlighted = False

    def __init__(self, sides, team, screen, width, height, screen_pos, color):
        self.team = team
        self.sides = sides
        self.health = randint(1, sides)
        self.initial_health = self.health

        # screen related information
        self.color = color
        self.screen_pos = screen_pos

        pil_img = Image.open(r'C:\Users\d5ffpr\PycharmProjects\TinkerTactics\sprites' + '\\d' + str(self.sides) + '_' + str(self.health) + '.png')
        pil_img = pil_img.convert("RGBA")
        pixel_data = pil_img.load()
        for y in range(pil_img.size[1]):
            for x in range(pil_img.size[0]):
                # TODO : NICE TO HAVE: color the number black to contrast if they chose a light color, maybe outline it in black
                if pixel_data[x, y] == (0, 0, 0, 255):
                    pixel_data[x, y] = (color[0], color[1], color[2], 255)

        self.image = pygame.image.frombuffer(pil_img.tobytes(), pil_img.size, pil_img.mode)

        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rectangle = self.image.get_rect()
        self.screen = screen
        self.screen_rectangle = screen.get_rect()

        # start all the pieces at the position specified by screen_pos
        self.rectangle.topleft = screen_pos

    def __str__(self):
        return str({'sides': self.sides, 'health': self.health, 'position': self.pos, 'team': self.team})

    def get_health(self):
        return self.health

    def damage(self):
        if self.health > 0:
            self.health -= 1
            if self.health > 0:
                self.update_image()
            return True
        return False

    def is_dead(self):
        return self.health <= 0

    def move(self, newpos):
        self.pos = newpos

    def set_screen_pos(self, newpos):
        self.rectangle.topleft = newpos
        self.screen_pos = newpos

    def get_pos(self):
        return self.pos

    def get_team(self):
        return self.team

    def get_sides(self):
        return self.sides

    def blit(self):
        self.screen.blit(self.image, self.rectangle)

    def increment_health(self):
        if self.health < self.sides:
            self.health += 1
            self.update_image()
            return True
        return False

    def decrement_health(self):
        if self.health > self.initial_health:
            self.health -= 1
            self.update_image()
            return True
        return False

    def update_image(self):
        pil_img = Image.open(
            r'C:\Users\d5ffpr\PycharmProjects\TinkerTactics\sprites' + '\\d' + str(self.sides) + '_' + str(
                self.health) + '.png')
        pil_img = pil_img.convert("RGBA")
        pixel_data = pil_img.load()
        for y in range(pil_img.size[1]):
            for x in range(pil_img.size[0]):
                # TODO : NICE TO HAVE: color the number black to contrast if they chose a light color, maybe outline it in black
                if pixel_data[x, y] == (0, 0, 0, 255):
                    pixel_data[x, y] = (self.color[0], self.color[1], self.color[2], 255)

        self.image = pygame.image.frombuffer(pil_img.tobytes(), pil_img.size, pil_img.mode)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rectangle = self.image.get_rect()
        self.rectangle.topleft = self.screen_pos

    def get_rect(self):
        return self.rectangle

    def highlight(self, color):
        pygame.draw.rect(self.screen, color, self.rectangle, 5)
        self.highlighted = True

    def is_highlighted(self):
        return self.highlighted

    def clear_highlight(self):
        setting = Settings()
        s = setting.vals()
        self.highlight(s['background_color_RGB'])
        self.highlighted = False

    def get_screen_pos(self):
        return self.screen_pos

