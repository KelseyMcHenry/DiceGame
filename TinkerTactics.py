import Piece
import pygame
from PIL import Image
import PIL.ImageOps
from random import randint
from Settings import Settings

# TODO : use dice-icons.png as a base to make a set of bmp sprites
# TODO possibly makes sense to make some sort of array/dict thing that holds items on screen and their positions


# TODO : menu
# TODO : redistribution
# TODO : placement
# TODO : board joining
# TODO : gameplay
# TODO : AI
# TODO : local multiplayer
# TODO : online multiplayer?


# ------------ setup settings ----------------------
settings = Settings()
s = settings.vals()

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont(s['font'], int(s['font_size']))
screen = pygame.display.set_mode(s['resolution'])

screen_entities = {}

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
        piece_index += 1

team_2_pieces = list()
piece_index = 0
for sides, count in s['piece_rank_and_count'].items():
    for i in range(1, count + 1):
        piece = Piece.Piece(sides, s['team_2_color_name'], screen, 75, 75, (75 * piece_index, 75), s['team_2_color_RGB'])
        team_2_pieces.append(piece)
        piece.blit()
        piece_index += 1


pygame.display.flip()

while True:
    pass


# rendering  -------------------- contest --------------------------

sum_team_1_pieces = sum([piece.get_health() for piece in team_1_pieces])
sum_team_2_pieces = sum([piece.get_health() for piece in team_2_pieces])

goes_first = '?'
goes_second = '?'
max_val = max(sum_team_1_pieces, sum_team_2_pieces)
diff = max_val - min(sum_team_1_pieces, sum_team_2_pieces)
if sum_team_1_pieces > sum_team_2_pieces:
    goes_first = s['team_1_color']
elif sum_team_2_pieces > sum_team_1_pieces:
    goes_first = s['team_2_color']
elif randint(0, 1) == 0:
    goes_first = s['team_2_color']
else:
    goes_first = s['team_1_color']


if goes_first == s['team_1_color']:
    goes_second = s['team_2_color']
else:
    goes_second = s['team_1_color']


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
    pass

# while True:
#     events = pygame.event.get()
#     if len(events) > 0:
#         print(events)
#     for event in events:
#         if event.type == pygame.QUIT:
#             exit()
#
#     pygame.display.flip()


