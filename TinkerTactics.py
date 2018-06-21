import Piece
import pygame
from PIL import Image
import PIL.ImageOps
from random import randint
from Settings import Settings
from Board import HalfBoard



# TODO : define clear board function which sets positions on all pieces to somewhere off the board



# TODO : menu
# TODO : placement
# TODO : board joining
# TODO : gameplay
# TODO : AI
# TODO : local multiplayer
# TODO : online multiplayer?


# ------------ setup settings ----------------------
settings = Settings()
s = settings.vals()

sprites = list()

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont(s['font'], int(s['font_size']))
screen = pygame.display.set_mode(s['resolution'])

pygame.display.set_caption(s['name'])
screen.fill(s['background_color_RGB'])

# rendering  -------------------- rolling --------------------------

team_1_pieces = list()
piece_index = 0
for sides, count in s['piece_rank_and_count'].items():
    for i in range(1, count + 1):
        piece = Piece.Piece(sides, s['team_1_color_name'], screen, 75, 75, (75 * piece_index, 0), s['team_1_color_RGB'])
        team_1_pieces.append(piece)
        piece.blit()
        sprites.append(piece)
        piece_index += 1

team_2_pieces = list()
piece_index = 0
for sides, count in s['piece_rank_and_count'].items():
    for i in range(1, count + 1):
        piece = Piece.Piece(sides, s['team_2_color_name'], screen, 75, 75, (75 * piece_index, 75), s['team_2_color_RGB'])
        team_2_pieces.append(piece)
        piece.blit()
        sprites.append(piece)
        piece_index += 1

for sprite in sprites:
    print(sprite)

pygame.display.flip()


# rendering  -------------------- contest --------------------------

sum_team_1_pieces = sum([piece.get_health() for piece in team_1_pieces])
sum_team_2_pieces = sum([piece.get_health() for piece in team_2_pieces])

goes_first = '?'
goes_second = '?'
max_val = max(sum_team_1_pieces, sum_team_2_pieces)
diff = max_val - min(sum_team_1_pieces, sum_team_2_pieces)
if sum_team_1_pieces > sum_team_2_pieces:
    goes_first = s['team_1_color_name']
elif sum_team_2_pieces > sum_team_1_pieces:
    goes_first = s['team_2_color_name']
elif randint(0, 1) == 0:
    goes_first = s['team_2_color_name']
else:
    goes_first = s['team_1_color_name']


if goes_first == s['team_1_color_name']:
    goes_second = s['team_2_color_name']
else:
    goes_second = s['team_1_color_name']


if sum_team_2_pieces == sum_team_1_pieces:
    # rendering  -------------------- coin flip --------------------------
    print(goes_first + ' is going first, they have won the coin flip; the sum score is tied at ' + str(max_val))
    text_surface = my_font.render(goes_first + ' is going first, they have won the coin flip; the sum score is tied at ' + str(max_val), False, (0, 0, 0))
    screen.blit(text_surface, (0, (team_2_pieces.index(piece) + len(team_2_pieces) + 2) * 12))
else:
    print(goes_first + ' is going first with a sum score of ' + str(max_val) + '.')
    print(goes_second + ' will be able to distribute the difference of ' + str(diff) + ' as they see fit.')

    text_surface = my_font.render(goes_first + ' is going first with a sum score of ' + str(max_val) + '.', False, (0, 0, 0))
    screen.blit(text_surface, (0, (75 * 2)))

    text_surface = my_font.render(goes_second + ' will be able to distribute the difference of ' + str(diff) + ' as they see fit.', False, (0, 0, 0))
    screen.blit(text_surface, (0, (75 * 2) + 12))
    # rendering  -------------------- redistribution --------------------------

pygame.display.flip()

while True:
    events = pygame.event.get()
    if len(events) > 0:
        # print(events)
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in sprites if s.rectangle.collidepoint(pos)]
                for sprite in clicked_sprites:
                    if sprite.get_team() == goes_second and diff > 0:
                        sprite.increment_health()
                        diff -= 1
                        sprite.blit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in sprites if s.rectangle.collidepoint(pos)]
                for sprite in clicked_sprites:
                    if sprite.get_team() == goes_second and diff > 0:
                        sprite.decrement_health()
                        diff += 1
                        sprite.blit()
    if diff == 0:
        print('done!')
        for sprite in sprites:
            print(sprite)
        break

    pygame.display.flip()


screen.fill(s['background_color_RGB'])
pygame.display.flip()

board = HalfBoard(75, screen, (0, 0))
board.blit()
sprites.append(board)
pygame.display.flip()
print(board.get_width())

piece_sprites = [spr for spr in sprites if type(spr).__name__ == "Piece"]
print(piece_sprites)
for index, sprite in enumerate(piece_sprites):
    if sprite.get_team() == s['team_1_color_name']:
        sprite.set_screen_pos((((75 + 10)* index) + board.get_width() + 5, 0))
        sprite.blit()

pygame.display.flip()


while True:
    events = pygame.event.get()
    if len(events) > 0:
        # print(events)
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in sprites if s.rectangle.collidepoint(pos)]
                temp_sprite = None
                for sprite in clicked_sprites:
                    if type(sprite).__name__ == "Piece":
                        temp_sprite = sprite
                        sprite.highlight((255, 255, 0))
                        sprite.blit()
                for sprite in sprites:
                    if type(sprite).__name__ == "Piece" and sprite.is_highlighted() and sprite is not temp_sprite:
                        sprite.clear_highlight()
                        sprite.blit()
                pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in sprites if s.rectangle.collidepoint(pos)]
                for sprite in clicked_sprites:
                    if type(sprite).__name__ == "Piece" and sprite.is_highlighted():
                        sprite.clear_highlight()
                        sprite.blit()
                pygame.display.flip()
