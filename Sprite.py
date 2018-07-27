from random import randint
import pygame
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from Settings import SettingsPackage
import Settings


class Sprite:

    def __init__(self, screen, width, height, screen_pos, sprite_filename):
        self.screen = screen
        self.screen_pos = screen_pos
        self.width_px = width
        self.height_px = height
        self.SP = SettingsPackage().get_package()
        self.sprite_directory_path = self.SP[Settings.PATH_TO_SPRITES]
        self.sprite_path = self.sprite_directory_path + sprite_filename

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

    def get_screen(self):
        return self.screen


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
        sprite_name = 'd' + str(self.sides) + '_' + str(self.health) + '.png'
        Sprite.__init__(self, screen, width, height, screen_pos, sprite_name)

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
        return f'hp: {self.health}/{self.sides}, pos: {self.array_pos}, team: {self.team}'

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

    def damage_no_screen_update(self):
        if self.health > 0:
            self.health -= 1

    def update_piece_image(self):
        self.sprite_path = self.sprite_directory_path + 'd' + str(self.sides) + '_' + str(self.health) + '.png'
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

    def set_position(self, position):
        self.array_pos = position

    def get_position(self):
        return self.array_pos

    def set_health(self, health):
        self.health = health


class HalfBoard(Sprite):

    def __init__(self, cell_size, screen, screen_pos):
        Sprite.__init__(self, screen, 5 * cell_size, 3 * cell_size, screen_pos, 'checkerboard3x5.png')

        self.width = 5 * cell_size
        self.height = 3 * cell_size

        # start all the pieces at the position specified by screen_pos
        self.board_model = [[None for _ in range(5)] for _ in range(3)]

    def __str__(self):
        max_item_size = 0
        for row in self.board_model:
            for item in row:
                if len(str(item)) > max_item_size:
                    max_item_size = len(str(item))
        return_s = ''
        for row in self.board_model:
            for item in row:
                difference = max_item_size - len(str(item))
                return_s += str(item)
                for _ in range(difference):
                    return_s += ' '
                if row.index(item) != (len(row) - 1):
                    return_s += ', '
            return_s += '\n'
        return_s.strip()
        return return_s

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
        piece.set_position((i, j))

    def get_piece_in_model(self, i, j):
        return self.board_model[i][j]


class Button(Sprite):

    def __init__(self, width, height, screen, screen_pos, action, text, SP):
        Sprite.__init__(self, screen, width, height, screen_pos, 'done.png')
        self.action = action

        pil_img = Image.new('RGB', (width, height), color=(0, 0, 0))
        draw = ImageDraw.Draw(pil_img)
        font_size = height // 2
        draw.text((((width - (font_size * (3/5) * len(text))) // 2), (height - font_size) // 2), text, font=ImageFont.truetype(SP[Settings.FONT] + ".ttf", font_size), fill=(255, 255, 255))

        self.image = pygame.image.frombuffer(pil_img.tobytes(), pil_img.size, pil_img.mode)

    def get_action(self):
        return self.action


class FullBoard(Sprite):

    def __init__(self, cell_size, screen, screen_pos, board_model_top, board_model_bottom):
        Sprite.__init__(self, screen, 5 * cell_size, 6 * cell_size, screen_pos, 'checkerboard6x5.png')

        self.width = 5 * cell_size
        self.height = 6 * cell_size

        self.board_model = [[None for _ in range(5)] for _ in range(6)]
        for i in range(0, 3):
            for j in range(0, 5):
                self.board_model[i][j] = board_model_top[i][j]
        for i in range(0, 3):
            for j in range(0, 5):
                self.board_model[i+3][j] = board_model_bottom[i][j]
        for i in range(0, 6):
            for j in range(0, 5):
                if self.board_model[i][j] is not None:
                    self.board_model[i][j].set_position((i, j))

        self.highlighted_cells = [[False for _ in range(5)] for _ in range(6)]

    def __str__(self):
        max_item_size = 0
        for row in self.board_model:
            for item in row:
                if len(str(item)) > max_item_size:
                    max_item_size = len(str(item))
        return_s = ''
        for row in self.board_model:
            for item in row:
                difference = max_item_size - len(str(item))
                return_s += str(item)
                for _ in range(difference):
                    return_s += ' '
                if row.index(item) != (len(row) - 1):
                    return_s += ', '
            return_s += '\n'
        return_s.strip()
        return return_s

    def remove_piece(self, piece):
        found = False
        for width in range(0, 5):
            for height in range(0, 6):
                if self.board_model[height][width] is piece:
                    self.board_model[height][width] = None
                    found = True
        if not found:
            print("Not Found")
            print(self.board_model)
            print(piece)

    def set_piece_in_model(self, i, j, piece):
        self.remove_piece(piece)
        piece.set_position((i, j))
        self.board_model[i][j] = piece

    def get_piece_in_model(self, i, j):
        try:
            if i < 0 or j < 0:
                return None
            ret_val = self.board_model[i][j]
            return ret_val
        except IndexError:
            return None

    def highlight_cell(self, x, y, color, thickness):
        self.highlighted_cells[x][y] = True
        self.run_highlights(color, thickness)

    def run_highlights(self, color, thickness):
        piece_size = self.SP[Settings.PIECE_SIZE_PX]
        for x in range(5):
            for y in range(6):
                if self.highlighted_cells[y][x]:
                    pygame.draw.rect(self.screen,
                                     color,
                                     (x * piece_size + thickness,
                                      y * piece_size + thickness,
                                      piece_size - (2 * thickness),
                                      piece_size - (2 * thickness)),
                                     thickness)

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

    def all_possible_moves(self, x, y, health, simplified_board_state=None):
        result = list()
        try:
            if x < 0 or y < 0:
                return result
            if simplified_board_state:
                if simplified_board_state[x][y] is None and health == 0:
                    result.append((x, y))
                    return result
                elif simplified_board_state[x][y] is not None and health == 0:
                    return result
            else:
                if self.board_model[x][y] is None and health == 0:
                    result.append((x, y))
                    return result
                elif self.board_model[x][y] is not None and health == 0:
                    return result
        except IndexError:
            return result

        result.extend(self.all_possible_moves(x, y - 1, health - 1, simplified_board_state))
        result.extend(self.all_possible_moves(x, y + 1, health - 1, simplified_board_state))
        result.extend(self.all_possible_moves(x - 1, y, health - 1, simplified_board_state))
        result.extend(self.all_possible_moves(x + 1, y, health - 1, simplified_board_state))

        return list(set(result))

    def piece_attack(self, piece):
        piece_location = self.index_of_piece(piece)
        attack_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        targets = [item for item in [self.get_piece_in_model(piece_location[0] + x, piece_location[1] + y) for x, y in attack_directions] if item is not None]
        targets_damaged = []
        for target in targets:
            if target.get_team() != piece.get_team():
                target.damage()
                targets_damaged.append(target)
        return targets_damaged

    def simple_board_state(self):
        # piece[1] = position tuple
        # piece[0][0] = health
        # piece[0][1] = team
        temp_model = [[None for _ in range(0, 5)] for _ in range(0, 6)]
        for row_index in range(len(self.board_model)):
            for column_index in range(len(self.board_model[0])):
                p = self.board_model[row_index][column_index]
                if p:
                    temp_model[row_index][column_index] = [[p.get_health(), p.get_team()], list(p.get_position())]
        return temp_model


class HeartCoin(Sprite):

    def __init__(self, screen, width, height, screen_pos, value, SP):

        self.value = value
        self.SP = SP

        # init parent properties
        sprite_name = 'heart_coin.png'
        Sprite.__init__(self, screen, width, height, screen_pos, sprite_name)

        pil_img = Image.open(self.sprite_path)
        pil_img = pil_img.convert("RGBA")
        draw = ImageDraw.Draw(pil_img)
        font = ImageFont.truetype(SP[Settings.FONT] + ".ttf", 20)
        draw.text((width // 2,  height // 2), str(value), (0, 0, 0), font=font)

        image = pygame.image.frombuffer(pil_img.tobytes(), pil_img.size, pil_img.mode)
        image = pygame.transform.scale(image, (self.width_px, self.height_px))
        self.set_image(image)

    def __str__(self):
        return "Coin value: " + str(self.value)

    def decrement(self):
        self.value -= 1
        self.update_image()

    def increment(self):
        self.value += 1
        self.update_image()

    def get_value(self):
        return self.value

    def update_image(self):
        pil_img = Image.open(self.sprite_path)
        pil_img = pil_img.convert("RGBA")
        draw = ImageDraw.Draw(pil_img)
        font = ImageFont.truetype(self.SP[Settings.FONT] + ".ttf", 20)
        draw.text((self.width_px // 2, self.height_px // 2), str(self.value), (0, 0, 0), font=font)

        image = pygame.image.frombuffer(pil_img.tobytes(), pil_img.size, pil_img.mode)
        image = pygame.transform.scale(image, (self.width_px, self.height_px))
        self.set_image(image)
