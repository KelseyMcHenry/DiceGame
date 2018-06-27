import Piece
import pygame
from PIL import Image
import PIL.ImageOps
from random import randint
from Settings import Settings
from Board import HalfBoard
from Board import FullBoard
from NavButton import Done


# TODO : break up into more methods
# TODO : make all measurements relative to size of screen
# TODO : add resize event listeners

# TODO : icon
# TODO : 3d roll rendering?
# TODO : menu
# TODO : placement
# TODO : board joining
# TODO : gameplay
#    TODO : attack animation?
#    TODO : damage animation
# TODO : AI
# TODO : local multiplayer
# TODO : online multiplayer
#    TODO : chat
# TODO Settings menu
#    TODO : RBG Color picker
#    TODO : skins
#    TODO : background skins
# TODO : stats tracker


def clear_screen(pygame_screen, sprite_list, settings):
    pygame_screen.fill(settings['background_color_RGB'])
    for sprite in sprite_list:
        sprite.set_screen_pos((-500, -500))
    refresh_screen(pygame_screen, sprite_list, settings)


def refresh_screen(pygame_screen, sprite_list, settings):
    pygame_screen.fill(settings['background_color_RGB'])
    for sprite in [spr for spr in sprite_list if type(spr).__name__ != "Piece"]:
        sprite.blit()
    for sprite in [spr for spr in sprite_list if type(spr).__name__ == "Piece"]:
        sprite.blit()
        if sprite.is_highlighted():
            sprite.highlight((255, 255, 0))
    pygame.display.flip()


# ------------ pull settings from file ----------------------
settings = Settings()
s = settings.vals()

sprites = list()

# ------------ init pygame screen --------------------------
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont(s['font'], int(s['font_size']))
screen = pygame.display.set_mode(s['resolution'])

pygame.display.set_caption(s['name'])
screen.fill(s['background_color_RGB'])

# -------------- roll the dice -----------------------------

# PLAYER IS TEAM 1
# AI IS TEAM 2

team_1_pieces = list()
piece_index = 0
for sides, count in s['piece_rank_and_count'].items():
    for i in range(1, count + 1):
        piece = Piece.Piece(sides, s['team_1_color_name'], screen, 75, 75, (75 * piece_index, 0), s['team_1_color_RGB'])
        team_1_pieces.append(piece)
        sprites.append(piece)
        piece_index += 1

for sprite in sprites:
    print(sprite)

refresh_screen(screen, sprites, s)

team_2_pieces = list()
piece_index = 0
for sides, count in s['piece_rank_and_count'].items():
    for i in range(1, count + 1):
        piece = Piece.Piece(sides, s['team_2_color_name'], screen, 75, 75, (75 * piece_index, 75), s['team_2_color_RGB'])
        team_2_pieces.append(piece)
        sprites.append(piece)
        piece_index += 1

# -------------------- contest values --------------------------

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
    screen.blit(text_surface, (10, (75 * 2)))

    text_surface = my_font.render(goes_second + ' will be able to distribute the difference of ' + str(diff) + ' as they see fit.', False, (0, 0, 0))
    screen.blit(text_surface, (10, (75 * 2) + 12))

pygame.display.flip()

if goes_second == s['team_1_color_name']:
    #player interaction with the board, incrementing their pieces
    while True:
        events = pygame.event.get()
        if len(events) > 0:
            for event in events:
                # X BUTTON
                if event.type == pygame.QUIT:
                    exit()
                # LEFT CLICK - increment health of piece
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [s for s in sprites if s.rectangle.collidepoint(pos)]
                    for sprite in clicked_sprites:
                        if diff > 0:
                            if sprite.increment_health():
                                diff -= 1
                                sprite.blit()
                # RIGHT CLICK - undo increment
                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [s for s in sprites if s.rectangle.collidepoint(pos)]
                    for sprite in clicked_sprites:
                        if diff > 0:
                            if sprite.decrement_health():
                                diff += 1
                                sprite.blit()
        if diff == 0:
            print('done!')
            for sprite in sprites:
                print(sprite)
            break

        pygame.display.flip()
else:
    # AI increments their pieces in secret, let the player look at their dice for a couple seconds
    pygame.display.flip()
    AI


clear_screen(screen, sprites, s)
pygame.display.flip()

team_1_half_board = HalfBoard(75, screen, (0, 0))
team_1_half_board.blit()
sprites.append(team_1_half_board)
pygame.display.flip()

piece_sprites = [spr for spr in sprites if type(spr).__name__ == "Piece"]
print(piece_sprites)
for index, sprite in enumerate(piece_sprites):
    if sprite.get_team() == s['team_1_color_name']:
        sprite.set_screen_pos((((75 + 10) * index) + team_1_half_board.get_width() + 5, 0))
        sprite.blit()

done_button = Done(75, screen, (10, team_1_half_board.get_height() + 10))
done_button.blit()
sprites.append(done_button)

pygame.display.flip()

swap_sprite = None

done = False
while not done:
    events = pygame.event.get()
    if len(events) > 0:
        # print(events)
        for event in events:
            # X BUTTON
            if event.type == pygame.QUIT:
                exit()
            # LEFT CLICK
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in sprites if s.rectangle.collidepoint(pos)]
                print(clicked_sprites)
                temp_sprite = None
                if len(clicked_sprites) == 1:
                    sprite = clicked_sprites[0]
                    if type(sprite).__name__ == "HalfBoard":
                        print('board click ')
                        for spr in sprites:
                            if type(spr).__name__ == "Piece" and spr.is_highlighted():
                                pos = ((pos[0] // 75) * 75, (pos[1] // 75) * 75)
                                spr.clear_highlight()
                                spr.set_screen_pos(pos)
                                sprite.set_piece_in_model((pos[0] // 75), (pos[1] // 75), spr)
                    if type(sprite).__name__ == "Piece":
                        print('piece click ')
                        temp_sprite = sprite
                        sprite.highlight((255, 255, 0))
                        for spr in sprites:
                            if type(spr).__name__ == "Piece" and spr.is_highlighted() and spr is not temp_sprite:
                                spr.clear_highlight()
                    if type(sprite).__name__ == "Done":
                        sprite.set_screen_pos((-500, -500))
                        done = True
                elif len(clicked_sprites) == 2:
                    for sprite in clicked_sprites:
                        if type(sprite).__name__ == "Piece":
                            print('piece click ')
                            if swap_sprite and swap_sprite.is_highlighted():
                                swap_sprite_pos = swap_sprite.get_screen_pos()
                                pos = ((pos[0] // 75) * 75, (pos[1] // 75) * 75)
                                swap_sprite.clear_highlight()
                                swap_sprite.set_screen_pos(pos)
                                temp_sprite = sprite
                                sprite.set_screen_pos(swap_sprite_pos)
                                for spr in sprites:
                                    if type(spr).__name__ == "Piece" and spr.is_highlighted() and spr is not temp_sprite:
                                        spr.clear_highlight()
                                swap_sprite = None
                            else:
                                temp_sprite = sprite
                                sprite.highlight((255, 255, 0))
                                swap_sprite = sprite
                                for spr in sprites:
                                    if type(spr).__name__ == "Piece" and spr.is_highlighted() and spr is not temp_sprite:
                                        spr.clear_highlight()
                        else:
                            for spr in sprites:
                                if type(spr).__name__ == "Piece" and spr.is_highlighted():
                                    sprite.set_piece_in_model((pos[0] // 75), (pos[1] // 75), spr)
            refresh_screen(screen, sprites, s)
            # RIGHT CLICK
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in sprites if s.rectangle.collidepoint(pos)]
                for sprite in clicked_sprites:
                    if type(sprite).__name__ == "Piece" and sprite.is_highlighted():
                        sprite.clear_highlight()
                        sprite.blit()
                pygame.display.flip()


team_2_half_board = HalfBoard(75, screen, (0, team_1_half_board.get_height()))
sprites.append(team_2_half_board)
done = False

for piece in team_2_pieces:
    done = False
    while not done:
        rand_x, rand_y = randint(1, 5) - 1, randint(1, 3) - 1
        if not team_2_half_board.get_piece_in_model(rand_x, rand_y):
            team_2_half_board.set_piece_in_model(rand_x, rand_y, piece)
            pos = (rand_x * 75), (rand_y * 75) + team_1_half_board.get_height()
            piece.set_screen_pos(pos)
            done = True

print(team_1_half_board.board_model)
print(team_2_half_board.board_model)

gameboard = FullBoard(75, screen, (0, 0), team_1_half_board.board_model, team_2_half_board.board_model)
sprites.append(gameboard)
sprites.remove(team_1_half_board)
sprites.remove(team_2_half_board)

refresh_screen(screen, sprites, s)

while True:
    pass