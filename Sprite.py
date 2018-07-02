from random import randint
import pygame
from PIL import Image
from Settings import Settings


class Sprite:

    def __init__(self, screen, width, height, screen_pos, sprite_path):
        self.screen = screen
        self.screen_pos = screen_pos
        self.width_px = width
        self.height_px = height
        self.sprite_path = sprite_path

        # open image in PIL, convert to RGBA
        pil_img = Image.open(self.sprite_path)
        pil_img = pil_img.convert("RGBA")
        self.image = pygame.image.frombuffer(pil_img.tobytes(), pil_img.size, pil_img.mode)

        # scale image
        self.image = pygame.transform.scale(self.image, (self.width_px, self.height_px))

        # set the image's position on the screen
        self.image_rectangle = self.image.get_rect()
        self.image_rectangle.topleft = self.screen_pos

    def get_screen_pos(self):
        return self.screen_pos

    def set_screen_pos(self, newpos):
        self.screen_pos = newpos
        self.image_rectangle.topleft = self.screen_pos

    def get_width(self):
        return self.width_px

    def get_height(self):
        return self.height_px

    def get_image_path(self):
        return self.sprite_path

    def set_image(self, image):
        self.image = image
        # update image rectangle and image's screen position
        self.image_rectangle = self.image.get_rect()
        self.image_rectangle.topleft = self.screen_pos

    def blit(self):
        self.screen.blit(self.image, self.image_rectangle)


class Piece(Sprite):

    def __init__(self, screen, width, height, screen_pos, sides, team, color):
        self.team = team
        self.sides = sides
        self.health = randint(1, sides)
        self.initial_health = self.health
        self.color = color
        self.array_pos = (-1, -1)
        self.highlighted = False

        # init parent properties
        sprite_path = r'C:\Users\d5ffpr\PycharmProjects\TinkerTactics\sprites\d' + str(self.sides) + '_' + str(self.health) + '.png'
        Sprite.__init__(self, screen, width, height, screen_pos, sprite_path)

        # recolor the sprite and update it
        pil_img = Image.open(self.sprite_path)
        pil_img = pil_img.convert("RGBA")
        pixel_data = pil_img.load()
        for y in range(pil_img.size[1]):
            for x in range(pil_img.size[0]):
                # TODO :if they chose a light color, outline it in black
                # TODO :if they chose a dark color, outline it in white
                # if pixel is not transparent background pixel...
                if pixel_data[x, y] == (0, 0, 0, 255):
                    pixel_data[x, y] = (self.color[0], self.color[1], self.color[2], 255)

        image = pygame.image.frombuffer(pil_img.tobytes(), pil_img.size, pil_img.mode)
        image = pygame.transform.scale(image, (self.width_px, self.height_px))
        self.set_image(image)

    def __str__(self):
        return str({'sides': self.sides, 'health': self.health, 'position': self.array_pos, 'team': self.team})

    def get_team(self):
        return self.team

    def get_sides(self):
        return self.sides

    def get_health(self):
        return self.health

    def get_initial_health(self):
        return self.initial_health

    def is_highlighted(self):
        return self.highlighted

    def increment_health(self):
        if self.health < self.sides:
            self.health += 1
            self.update_piece_image()
            return True
        return False

    def decrement_health(self):
        if self.health > self.initial_health:
            self.health -= 1
            self.update_piece_image()
            return True
        return False

    def damage(self):
        if self.health > 0:
            self.health -= 1
            if self.health > 0:
                self.update_piece_image()

    def update_piece_image(self):
        self.sprite_path = r'C:\Users\d5ffpr\PycharmProjects\TinkerTactics\sprites\d' + str(self.sides) + '_' + str(self.health) + '.png'
        pil_img = Image.open(self.sprite_path)
        pil_img = pil_img.convert("RGBA")
        pixel_data = pil_img.load()
        for y in range(pil_img.size[1]):
            for x in range(pil_img.size[0]):
                # TODO :if they chose a light color, outline it in black
                # TODO :if they chose a dark color, outline it in white
                # if pixel is not transparent background pixel...
                if pixel_data[x, y] == (0, 0, 0, 255):
                    pixel_data[x, y] = (self.color[0], self.color[1], self.color[2], 255)

        image = pygame.image.frombuffer(pil_img.tobytes(), pil_img.size, pil_img.mode)
        image = pygame.transform.scale(image, (self.width_px, self.height_px))
        self.set_image(image)

    def is_dead(self):
        return self.health <= 0

    def highlight(self, color, thickness):
        pygame.draw.rect(self.screen, color, self.image_rectangle, int(thickness))
        self.highlighted = True

    def clear_highlight(self):
        self.highlighted = False


class HalfBoard(Sprite):

    def __init__(self, cell_size, screen, screen_pos):
        Sprite.__init__(self, screen, 5 * cell_size, 3 * cell_size, screen_pos, r'C:\Users\d5ffpr\PycharmProjects\TinkerTactics\checkerboard3x5.png')

        self.width = 5 * cell_size
        self.height = 3 * cell_size

        # start all the pieces at the position specified by screen_pos
        self.board_model = [[None for _ in range(5)] for _ in range(3)]

    def __str__(self):
        return_s = ''
        for row in self.board_model:
            return_s += row
            return_s += '\n'
        return_s.strip()

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_piece_in_model(self, i, j, piece):
        for row in self.board_model:
            for piece_reference in row:
                if piece_reference is piece:
                    piece_reference = None
        self.board_model[i][j] = piece

    def get_piece_in_model(self, i, j):
        return self.board_model[i][j]


class Done(Sprite):

    def __init__(self, cell_size, screen, screen_pos):
        Sprite.__init__(self, screen, 2 * cell_size, cell_size, screen_pos, r'C:\Users\d5ffpr\PycharmProjects\TinkerTactics\sprites\done.png')

        self.width = 2 * cell_size
        self.height = cell_size


class FullBoard(Sprite):

    def __init__(self, cell_size, screen, screen_pos, board_model_top, board_model_bottom):
        Sprite.__init__(self, screen, 5 * cell_size, 6 * cell_size, screen_pos, r'C:\Users\d5ffpr\PycharmProjects\TinkerTactics\checkerboard6x5.png')

        self.width = 5 * cell_size
        self.height = 6 * cell_size

        self.board_model = [[None for _ in range(5)] for _ in range(6)]
        for i in range(0, 3):
            for j in range(0, 5):
                self.board_model[i][j] = board_model_top[i][j]
        for i in range(0, 3):
            for j in range(0, 5):
                self.board_model[i+3][j] = board_model_bottom[i][j]
        self.highlighted_cells = [[False for _ in range(5)] for _ in range(6)]

    def __str__(self):
        return_s = ''
        for row in self.board_model:
            return_s += str(row)
            return_s += '\n'
        return_s.strip()
        return return_s

    def remove_piece(self, piece):
        for width in range(0, 5):
            for height in range(0, 6):
                if self.board_model[height][width] is piece:
                    self.board_model[height][width] = None

    def set_piece_in_model(self, i, j, piece):
        self.remove_piece(piece)
        self.board_model[i][j] = piece

    def get_piece_in_model(self, i, j):
        try:
            ret_val = self.board_model[i][j]
            return ret_val
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




