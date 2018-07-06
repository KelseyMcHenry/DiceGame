import pygame
from random import randint
from Settings import SettingsPackage
import Settings
from random import choice
from Sprite import Piece
from Sprite import HalfBoard
from Sprite import FullBoard
from Sprite import Done


# TODO : refactor sprite list to be an object with sublists based on object type so you can pull just pieces, etc.
# TODO : make all measurements relative to size of screen / define them in terms of settings, do math to check in Settings
# TODO : add resize event listeners

# TODO : icon
# TODO : 3d roll rendering?
# TODO : menu
# TODO : attack animation?
# TODO : damage animation
# TODO : Minimax AI
# TODO : local multiplayer
# TODO : online multiplayer
#    TODO : chat
# TODO Settings menu
#    TODO : RBG Color picker
#    TODO : skins
#    TODO : background skins
# TODO : stats tracker


def clear_screen(pygame_screen, master_sprite_list, settings_package):
    pygame_screen.fill(settings_package[Settings.BACKGROUND_COLOR_RGB])
    for sprite_to_be_moved in master_sprite_list:
        sprite_to_be_moved.set_screen_pos((-500, -500))
    refresh_screen(pygame_screen, master_sprite_list, settings_package)


def clear_off_dead_pieces(master_sprite_list):
    board_list = [spr for spr in sprites if type(spr).__name__ == 'FullBoard']
    if len(board_list) > 0:
        board_reference = board_list[0]
        for candidate_piece in [spr for spr in master_sprite_list if type(spr).__name__ == "Piece"]:
            if candidate_piece.get_health() == 0:
                master_sprite_list.remove(candidate_piece)
                board_reference.remove_piece(sprite)


def refresh_screen(pygame_screen, master_sprite_list, settings_package):
    clear_off_dead_pieces(master_sprite_list)
    pygame_screen.fill(settings_package[Settings.BACKGROUND_COLOR_RGB])
    for sprite in master_sprite_list:
        sprite.blit()
        if type(spr).__name__ == "FullBoard":
            sprite.run_highlights((0, 255, 0))
        elif type(spr).__name__ == "Piece":
            if sprite.is_highlighted():
                sprite.highlight(settings_package[Settings.HIGHLIGHT_COLOR_RGB],
                                 settings_package[Settings.HIGHLIGHT_THICKNESS])

    pygame.display.flip()


def banner_print(print_value):
    while len(print_value) < 80:
        print_value = '-' + print_value + '-'
    print(print_value)


# ------------ pull settings from file ----------------------
banner_print('Initializing Settings')
settings = SettingsPackage()
# Settings Package
SP = settings.get_package()

sprites = list()

# ------------ init pygame screen --------------------------
banner_print('Initializing Pygame')
pygame.init()
banner_print('Initializing Font')
pygame.font.init()
my_font = pygame.font.SysFont(SP[Settings.FONT], int(SP[Settings.FONT_SIZE]))
banner_print('Setting Screen resolution')
screen = pygame.display.set_mode(SP[Settings.RESOLUTION])

pygame.display.set_caption(SP[Settings.GAME_NAME])
screen.fill(SP[Settings.BACKGROUND_COLOR_RGB])
banner_print('Setting screen background color')
piece_size = int(SP[Settings.PIECE_SIZE_PX])

# -------------- roll the dice -----------------------------

# PLAYER IS TEAM 1
# AI IS TEAM 2

banner_print('Rolling the dice for Player 1')

team_1_pieces = list()
piece_index = 0
for sides, count in SP[Settings.PIECE_RANK_AND_COUNT].items():
    for i in range(1, count + 1):
        piece = Piece(screen, piece_size, piece_size, (piece_size * piece_index, 0), sides, SP[Settings.TEAM_1_NAME], SP[Settings.TEAM_1_RGB])
        team_1_pieces.append(piece)
        sprites.append(piece)
        piece_index += 1
sum_team_1_pieces = sum([piece.get_health() for piece in team_1_pieces])


banner_print('Player one got a result of : ')
for sprite in sprites:
    if sprite.get_team() == SP[Settings.TEAM_1_NAME]:
        print(sprite)
print('sum total: ' + str(sum_team_1_pieces))

banner_print("Displaying Player 1's pieces")
refresh_screen(screen, sprites, SP)

banner_print('Rolling the dice for AI opponent')
team_2_pieces = list()
piece_index = 0
for sides, count in SP[Settings.PIECE_RANK_AND_COUNT].items():
    for i in range(1, count + 1):
        piece = Piece(screen, piece_size, piece_size, (-500, -500), sides, SP[Settings.TEAM_2_NAME], SP[Settings.TEAM_2_RGB])
        team_2_pieces.append(piece)
        sprites.append(piece)
        piece_index += 1
sum_team_2_pieces = sum([piece.get_health() for piece in team_2_pieces])


banner_print('AI got a result of : ')
for sprite in sprites:
    if sprite.get_team() == SP[Settings.TEAM_2_NAME]:
        print(sprite)
print('sum total: ' + str(sum_team_2_pieces))


# -------------------- contest values --------------------------

goes_first = '?'
goes_second = '?'
max_val = max(sum_team_1_pieces, sum_team_2_pieces)
diff = max_val - min(sum_team_1_pieces, sum_team_2_pieces)
if sum_team_1_pieces > sum_team_2_pieces:
    goes_first = SP[Settings.TEAM_1_NAME]
elif sum_team_2_pieces > sum_team_1_pieces:
    goes_first = SP[Settings.TEAM_2_NAME]
elif randint(0, 1) == 0:
    goes_first = SP[Settings.TEAM_2_NAME]
else:
    goes_first = SP[Settings.TEAM_1_NAME]


if goes_first == SP[Settings.TEAM_1_NAME]:
    goes_second = SP[Settings.TEAM_2_NAME]
else:
    goes_second = SP[Settings.TEAM_1_NAME]

# TODO: make onscreen text notification sprite objects
if sum_team_2_pieces == sum_team_1_pieces:
    banner_print(goes_first + ' is going first, they have won the coin flip; the sum score is tied at ' + str(max_val))
    # text_surface = my_font.render(goes_first + ' is going first, they have won the coin flip; the sum score is tied at ' + str(max_val), False, (0, 0, 0))
    # screen.blit(text_surface, (0, (team_2_pieces.index(piece) + len(team_2_pieces) + 2) * 12))
else:
    banner_print(goes_first + ' is going first with a sum score of ' + str(max_val) + '.')
    banner_print(goes_second + ' will be able to distribute the difference of ' + str(diff) + ' as they see fit.')

    # text_surface = my_font.render(goes_first + ' is going first with a sum score of ' + str(max_val) + '.', False, (0, 0, 0))
    # screen.blit(text_surface, (10, (piece_size * 2)))

    # text_surface = my_font.render(goes_second + ' will be able to distribute the difference of ' + str(diff) + ' as they see fit.', False, (0, 0, 0))
    # screen.blit(text_surface, (10, (piece_size * 2) + 12))

refresh_screen(screen, sprites, SP)

if goes_second == SP[Settings.TEAM_1_NAME]:
    banner_print("Player 1 is going second, letting them increment their pieces")
    # player interaction with the board, incrementing their pieces
    while True:
        events = pygame.event.get()
        # prevents spamming of re-render
        if len(events) > 0:
            for event in events:
                # X BUTTON
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [s for s in sprites if s.image_rectangle.collidepoint(pos)]
                    if len(clicked_sprites) > 0:
                        clicked_piece = clicked_sprites[0]
                        if diff > 0:
                            if event.button == 1 and clicked_piece.increment_health():
                                # LEFT CLICK - increment health of piece
                                diff -= 1
                            elif event.button == 3 and clicked_piece.decrement_health():
                                # RIGHT CLICK - decrement health of piece
                                diff += 1
            if diff == 0:
                break
            refresh_screen(screen, sprites, SP)
    banner_print('Player one got a result of : ')
    for sprite in sprites:
        if sprite.get_team() == SP[Settings.TEAM_1_NAME]:
            print(sprite)
else:
    while diff > 0:
        for sprite in [sp for sp in sprites if type(sp).__name__ == "Piece" and sp.get_team() == SP[Settings.TEAM_2_NAME]]:
            if diff > 0 and sprite.increment_health():
                diff -= 1
    banner_print('AI got a result of : ')
    for sprite in sprites:
        if sprite.get_team() == SP[Settings.TEAM_2_NAME]:
            print(sprite)

    refresh_screen(screen, sprites, SP)

banner_print("Setting up Player 1's half of the board to let them arrange their pieces")
clear_screen(screen, sprites, SP)

# setup player 1's half of the board
team_1_half_board = HalfBoard(75, screen, (0, 0))
sprites.append(team_1_half_board)

piece_sprites = [spr for spr in sprites if type(spr).__name__ == "Piece"]
for index, sprite in enumerate(piece_sprites):
    if sprite.get_team() == SP[Settings.TEAM_1_NAME]:
        sprite.set_screen_pos((((piece_size + 10) * index) + team_1_half_board.get_width() + 5, 0))

done_button = Done(piece_size, screen, (10, team_1_half_board.get_height() + 10))
sprites.append(done_button)

refresh_screen(screen, sprites, SP)

banner_print('HalfBoard setup completed')
banner_print('Waiting for Player 1 to place their pieces')

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
                clicked_sprites = [s for s in sprites if s.image_rectangle.collidepoint(pos)]
                temp_sprite = None
                if len(clicked_sprites) == 1:
                    sprite = clicked_sprites[0]
                    if type(sprite).__name__ == "HalfBoard":
                        for spr in sprites:
                            if type(spr).__name__ == "Piece" and spr.is_highlighted():
                                pos = ((pos[0] // piece_size) * piece_size, (pos[1] // piece_size) * piece_size)
                                spr.clear_highlight()
                                spr.set_screen_pos(pos)
                                sprite.set_piece_in_model((pos[1] // piece_size), (pos[0] // piece_size), spr)
                    if type(sprite).__name__ == "Piece":
                        temp_sprite = sprite
                        sprite.highlight(SP[Settings.HIGHLIGHT_COLOR_RGB], SP[Settings.HIGHLIGHT_THICKNESS])
                        for spr in sprites:
                            if type(spr).__name__ == "Piece" and spr.is_highlighted() and spr is not temp_sprite:
                                spr.clear_highlight()
                    if type(sprite).__name__ == "Done":
                        sprite.set_screen_pos((-500, -500))
                        done = True
                elif len(clicked_sprites) == 2:
                    for sprite in clicked_sprites:
                        if type(sprite).__name__ == "Piece":
                            if swap_sprite and swap_sprite.is_highlighted():
                                swap_sprite_pos = swap_sprite.get_screen_pos()
                                pos = ((pos[0] // piece_size) * piece_size, (pos[1] // piece_size) * piece_size)
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
                                sprite.highlight(SP[Settings.HIGHLIGHT_COLOR_RGB], SP[Settings.HIGHLIGHT_THICKNESS])
                                swap_sprite = sprite
                                for spr in sprites:
                                    if type(spr).__name__ == "Piece" and spr.is_highlighted() and spr is not temp_sprite:
                                        spr.clear_highlight()
                        else:
                            for spr in sprites:
                                if type(spr).__name__ == "Piece" and spr.is_highlighted():
                                    sprite.set_piece_in_model((pos[1] // piece_size), (pos[0] // piece_size), spr)
            refresh_screen(screen, sprites, SP)
            # RIGHT CLICK
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in sprites if s.rectangle.collidepoint(pos)]
                for sprite in clicked_sprites:
                    if type(sprite).__name__ == "Piece" and sprite.is_highlighted():
                        sprite.clear_highlight()
                        sprite.blit()
                pygame.display.flip()

banner_print('Player 1 has placed their pieces')

banner_print('Setting up a HalfBoard for AI')
team_2_half_board = HalfBoard(piece_size, screen, (0, team_1_half_board.get_height()))
sprites.append(team_2_half_board)
done = False

for piece in team_2_pieces:
    done = False
    while not done:
        rand_x, rand_y = randint(1, 5) - 1, randint(1, 3) - 1
        if not team_2_half_board.get_piece_in_model(rand_y, rand_x):
            team_2_half_board.set_piece_in_model(rand_y, rand_x, piece)
            pos = (rand_x * piece_size), (rand_y * piece_size) + team_1_half_board.get_height()
            piece.set_screen_pos(pos)
            done = True

banner_print('AI has placed their pieces')

banner_print('Merging both HalfBoards into a FullBoard')
gameboard = FullBoard(piece_size, screen, (0, 0), team_1_half_board.board_model, team_2_half_board.board_model)
sprites.append(gameboard)
sprites.remove(team_1_half_board)
sprites.remove(team_2_half_board)
sprites.remove(done_button)

refresh_screen(screen, sprites, SP)
banner_print('Gameplay has begun')

turn_number = 0
done = False
while not done:
    events = pygame.event.get()
    if len(events) > 0:
        if (turn_number % 2 == 0 and goes_first == SP[Settings.TEAM_1_NAME]) or (turn_number % 2 == 1 and goes_second == SP[Settings.TEAM_1_NAME]):
            for event in events:
                # X BUTTON
                if event.type == pygame.QUIT:
                    exit()
                # LEFT CLICK
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    array_pos = (pos[1] // piece_size, pos[0] // piece_size)
                    clicked_sprites = [s for s in sprites if s.image_rectangle.collidepoint(pos)]
                    if len(clicked_sprites) == 1:
                        sprite = clicked_sprites[0]
                        if type(sprite).__name__ == "FullBoard":
                            for spr in sprites:
                                if type(spr).__name__ == "Piece" and spr.is_highlighted() and array_pos in poss_moves:
                                    banner_print('Player Move')
                                    print(spr)
                                    orig_pos = sprite.index_of_piece(spr)
                                    pos = ((pos[0] // piece_size) * piece_size, (pos[1] // piece_size) * piece_size)
                                    spr.clear_highlight()
                                    spr.set_screen_pos(pos)
                                    sprite.set_piece_in_model(array_pos[0], array_pos[1], spr)
                                    poss_moves = None
                                    print(str(orig_pos) + ' ---> ' + str(array_pos))

                                    # attack
                                    targets_damaged = sprite.piece_attack(spr)
                                    for target in targets_damaged:
                                        print(target)
                                    # turn ends
                                    turn_number += 1
                        sprite.clear_highlighted_cells()
                        temp_sprite = None
                    elif len(clicked_sprites) == 2:
                        for sprite in clicked_sprites:
                            if type(sprite).__name__ == "Piece" and sprite.get_team() == SP[Settings.TEAM_1_NAME]:
                                temp_sprite = sprite
                                sprite.highlight((255, 0, 0), 5)
                                for spr in sprites:
                                    if type(spr).__name__ == "Piece" and spr.is_highlighted() and spr is not temp_sprite:
                                        spr.clear_highlight()
                                    if type(spr).__name__ == "FullBoard":
                                        spr.clear_highlighted_cells()
                                        location = spr.index_of_piece(temp_sprite)
                                        # pass to a function in FullBoard which returns a list of all possible moves
                                        poss_moves = spr.all_possible_moves(location[0], location[1], temp_sprite.get_health())
                                        # print(str(location) + ', ' + str(temp_sprite.get_health()) + ' -->' + str(poss_moves))
                                        for x, y in poss_moves:
                                            spr.highlight_cell(x, y, (255, 255, 0))
                    elif len(clicked_sprites) == 0:
                        for spr in sprites:
                            if type(spr).__name__ == "Piece" and spr.is_highlighted():
                                spr.clear_highlight()
                                temp_sprite = None
                            if type(spr).__name__ == "FullBoard":
                                spr.clear_highlighted_cells()
                refresh_screen(screen, sprites, SP)
                # RIGHT CLICK
                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [s for s in sprites if s.image_rectangle.collidepoint(pos)]
                    for sprite in clicked_sprites:
                        if type(sprite).__name__ == "Piece" and sprite.is_highlighted():
                            sprite.clear_highlight()
                    refresh_screen(screen, sprites, SP)
        else:
            # AI's turn
            unmoved = True
            while unmoved:
                banner_print('AI Move')
                piece = choice([spr for spr in sprites if type(spr).__name__ == "Piece" and spr.get_team() == SP[Settings.TEAM_2_NAME]])
                print(piece)
                board = [spr for spr in sprites if type(spr).__name__ == 'FullBoard'][0]
                piece_location = board.index_of_piece(piece)

                possible_moves = board.all_possible_moves(piece_location[0], piece_location[1], piece.get_health())
                if len(possible_moves) == 0:
                    continue
                move = choice(possible_moves)
                print(str(piece_location) + ' ---> ' + str(move))
                piece.set_screen_pos((move[1] * piece_size, move[0] * piece_size))
                board.set_piece_in_model(move[0], move[1], piece)
                unmoved = False
                turn_number += 1
                targets_damaged = board.piece_attack(piece)
                for target in targets_damaged:
                    print(target)
            refresh_screen(screen, sprites, SP)
    count_team_1 = sum(1 for piece in [s for s in sprites if type(s).__name__ == "Piece" and s.get_team() == SP[Settings.TEAM_1_NAME]])
    count_team_2 = sum(1 for piece in [s for s in sprites if type(s).__name__ == "Piece" and s.get_team() == SP[Settings.TEAM_2_NAME]])
    if not (count_team_1 > 1 and count_team_2 > 1):
        done = True

refresh_screen(screen, sprites, SP)
if count_team_1 == 1:
    print("AI WINS")
    text_surface = my_font.render("AI WINS", False, (0, 0, 0))
    screen.blit(text_surface, (15, (piece_size * 7)))
else:
    print("PLAYER WINS")
    text_surface = my_font.render("PLAYER WINS", False, (0, 0, 0))
    screen.blit(text_surface, (15, (piece_size * 7)))
pygame.display.flip()
while True:
    events = pygame.event.get()
    if len(events) > 0:
        for event in events:
            # X BUTTON
            if event.type == pygame.QUIT:
                exit()
