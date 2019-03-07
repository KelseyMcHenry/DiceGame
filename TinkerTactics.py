import pygame
from random import randint
from Settings import SettingsPackage
import Settings
from random import choice
from Sprite import Piece
from Sprite import HalfBoard
from Sprite import FullBoard
from Sprite import Button
from Sprite import HeartCoin
from SpriteContainer import SpriteContainer
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from copy import deepcopy
import codecs
import graphviz
from graphviz import render
from subprocess import CalledProcessError
import cProfile

# TODO : make all measurements relative to size of screen / define them in terms of settings, do math to check in Settings
# TODO : add resize event listeners

# TODO : icon
# TODO : 3d roll rendering?
# TODO : main menu
# TODO : attack animation?
# TODO : damage animation
# TODO : Minimax AI?
# TODO : local multiplayer
# TODO : online multiplayer
#    TODO : chat
# TODO Settings menu
#    TODO : RBG Color picker
#    TODO : skins
#    TODO : background skins
# TODO : stats tracker

# ======================================= GLOBAL OBJECTS / SETTING SETUP ===============================================
# AI Tree
minimax_tree = Node("Initial")
node_storage = list()
# User defined Settings
SP = SettingsPackage().get_package()
# Master Sprite list used for rendering
master_sprite_list = SpriteContainer()
# Setting Setup
pygame.font.init()
my_font = pygame.font.SysFont(SP[Settings.FONT], SP[Settings.FONT_SIZE])
piece_size = SP[Settings.PIECE_SIZE_PX]
screen = pygame.display.set_mode(SP[Settings.RESOLUTION])


# ============================================== AI FUNCTIONS ==========================================================
def value_func(simplified_board_state, team):
    # possibly factor in standard deviation of health of pieces, factor in avg / median?
    # good enough for time being

    # TODO: CORRECT MINIMAX ALGORITHM, IMPLEMENT ALPHA BETA PRUNING : https://www.youtube.com/watch?v=l-hh51ncgDI
    sum_value = 0
    num_pieces = 0
    for row in simplified_board_state:
        for cell in row:
            if cell and cell[0][1] != team:
                if cell[0][0] > 0:
                    num_pieces += 1
                    sum_value += cell[0][0]
    if num_pieces <= 1:
        return -1000000
    if num_pieces > 5:
        raise ValueError(f"num of pieces exceeded 5 ... number was {num_pieces}")
    return sum_value * num_pieces


def ai_decision(simplified_board_state, team, board):
    pieces = []
    for row in simplified_board_state:
        for piece in row:
            if piece is not None and piece.get_team() == team:
                pieces.append(piece)
    all_possible_moves = []
    for p in pieces:
        moves = board.all_possible_moves(p.get_position()[0], p.get_position()[1], p.get_health())
        for m in moves:
            simulated_board = simulate_move(simplified_board_state, p, m)
            all_possible_moves.append((p, m, value_func(simulated_board, team)))

    banner_print("all possible moves")
    all_possible_moves.sort(key=lambda value: value[2])
    legible_list_print(all_possible_moves)
    return all_possible_moves[0][0], all_possible_moves[0][1]


def simulate_move(model, piece, pos):
    temp_model = [[None for _ in range(0, 5)] for _ in range(0, 6)]
    for row_index in range(len(model)):
        for column_index in range(len(model[0])):
            p = model[row_index][column_index]
            if model[row_index][column_index] and p is not piece:
                temp_model[row_index][column_index] = [p.get_health(), p.get_team()]

    temp_model[pos[0]][pos[1]] = [piece.get_health(), piece.get_team()]
    attacks = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for attack in attacks:
        try:
            temp = temp_model[pos[0] + attack[0]][pos[1] + attack[1]]
            if temp and temp[1] != piece.get_team():
                temp[0] = temp[0] - 1
        except IndexError:
            pass

    return temp_model


def minimax_make_decision(node):
    children = node.children
    min_node = None
    min = 1000000000
    for child in children:
        str_val = child.name
        fitness = int(str_val[str_val.index('= ') + 1:])
        if fitness < min:
            min = fitness
            min_node = child

    if len(min_node.children) == 0:
        return min_node
    else:
        return minimax_make_decision(min_node)


def minimax_populate_tree(board_state, team, current_depth, max_depth, parent):
    # first call, root = minimax_tree

    pieces = []
    print(current_depth)

    for row_index in range(len(board_state)):
        for column_index in range(len(board_state[0])):
            p = board_state[row_index][column_index]
            if p and p[0][1] == team:
                pieces.append(p)

    for piece in pieces:
        # piece[1] = position tuple
        # piece[0][0] = health
        # piece[0][1] = team
        moves = minimax_all_possible_moves(board_state, piece[1], piece[0][0])
        for move in moves:
            # simulate the move
            simulated_board = minimax_simulate_move(board_state, piece, move)
            # evaluate how good the move is
            fitness = value_func(simulated_board, team)
            # store the information about the move into the tree
            temp_node = Node(str(piece[0][1]) + str(piece[0][0]) + ' ' + str(piece[1][0]) + ', ' + str(piece[1][1]) + ' to ' + str(move[0]) + ', ' + str(move[1]) + ' = ' + str(fitness), parent=parent)
            node_storage.append(temp_node)

            # flip the team we are evaluating for the next call
            if team == SP[Settings.TEAM_1_NAME]:
                new_team = SP[Settings.TEAM_2_NAME]
            else:
                new_team = SP[Settings.TEAM_1_NAME]

            # depth-first recursion
            if current_depth < max_depth and fitness > 0:
                minimax_populate_tree(simulated_board, new_team, current_depth + 1, max_depth, temp_node)


def minimax_all_possible_moves(board_state, piece_pos, piece_health):
    result = list()
    x = piece_pos[0]
    y = piece_pos[1]
    try:
        if x < 0 or y < 0:
            return result
        if board_state:
            # if the spot is empty and the piece is out of moves, return that position as valid
            if board_state[x][y] is None and piece_health == 0:
                result.append((x, y))
                return result
            # if there is another piece in the spot where the piece runs out of moves, do not return that value
            elif board_state[x][y] is not None and piece_health == 0:
                return result
    # if the moves go out of bounds, throw it out
    except IndexError:
        return result

    result.extend(minimax_all_possible_moves(board_state, (x, y - 1), piece_health - 1))
    result.extend(minimax_all_possible_moves(board_state, (x, y + 1), piece_health - 1))
    result.extend(minimax_all_possible_moves(board_state, (x - 1, y), piece_health - 1))
    result.extend(minimax_all_possible_moves(board_state, (x + 1, y), piece_health - 1))

    return list(set(result))


def minimax_simulate_move(model, piece, move):
    # piece[1] = position tuple
    # piece[0][0] = health
    # piece[0][1] = team
    model_copy = deepcopy(model)
    piece_copy = deepcopy(piece)
    model_copy[piece_copy[1][0]][piece_copy[1][1]] = None
    model_copy[move[0]][move[1]] = piece_copy
    piece_copy[1][0] = move[0]
    piece_copy[1][1] = move[1]

    attacks = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for attack in attacks:
        try:
            temp = model_copy[move[0] + attack[0]][move[1] + attack[1]]
            if temp and temp[0][1] != piece[0][1]:
                model_copy[move[0] + attack[0]][move[1] + attack[1]][0][0] -= 1
                if model_copy[move[0] + attack[0]][move[1] + attack[1]][0][0] == 0:
                    model_copy[move[0] + attack[0]][move[1] + attack[1]] = None
        except IndexError:
            pass

    return model_copy


# =========================================== UI / Rendering functions =================================================
# moves all sprites off the screen and fills the background again, then re-renders the screen
def clear_screen():
    for sprite_to_be_moved in master_sprite_list.get_all():
        sprite_to_be_moved.set_screen_pos((SP[Settings.RESOLUTION][0] * -1, SP[Settings.RESOLUTION][1] * -1))
    refresh_screen()


# removes any pieces from the board model and master_sprite_list that are dead
def clear_off_dead_pieces():
    board_list = master_sprite_list.get_subset("FullBoard")
    if board_list and len(board_list) > 0:
        board_reference = board_list[0]
        for candidate_piece in master_sprite_list.get_subset("Piece"):
            if candidate_piece.is_dead():
                master_sprite_list.remove(candidate_piece)
                board_reference.remove_piece(candidate_piece)


# refreshes the background color, removes dead pieces, updates the display with all sprites in the master
# sprite list, and runs highlights overtop of everything after it is done
def refresh_screen():
    clear_off_dead_pieces()
    screen.fill(SP[Settings.BACKGROUND_COLOR_RGB])
    for full_board in master_sprite_list.get_subset("FullBoard"):
        full_board.blit()
        full_board.run_highlights(SP[Settings.POSS_MOVES_COLOR_RGB], SP[Settings.POSS_MOVES_THICKNESS])
    for half_board in master_sprite_list.get_subset("HalfBoard"):
        half_board.blit()
    for coin in master_sprite_list.get_subset("HeartCoin"):
        coin.blit()
    for button in master_sprite_list.get_subset("Button"):
        button.blit()
    for piece in master_sprite_list.get_subset("Piece"):
        piece.blit()
        if piece.is_highlighted():
            piece.highlight(SP[Settings.HIGHLIGHT_COLOR_RGB],
                            SP[Settings.HIGHLIGHT_THICKNESS])
    pygame.display.flip()

# ======================================= Console helper functions ====================================================
# prints to the console and fills extra space on left and right with hyphens
def banner_print(print_value):
    while len(print_value) < 120:
        print_value = '-' + print_value + '-'
    if len(print_value) % 2 == 0:
        print_value = print_value + '-'
    print(print_value)


def legible_list_print(list_to_print):
    for item in list_to_print:
        print(item)


# ======================================== Gameplay functions ==========================================================
def roll_dice(team_name, team_color, hide=False):
    team_pieces = list()
    piece_index = 0
    for sides, count in SP[Settings.PIECE_RANK_AND_COUNT].items():
        for i in range(1, count + 1):
            if not hide:
                piece = Piece(screen, piece_size, piece_size, (piece_size * piece_index, 0), sides, team_name, team_color)
            else:
                piece = Piece(screen, piece_size, piece_size, (SP[Settings.RESOLUTION][0] * -1, SP[Settings.RESOLUTION][1] * -1), sides, team_name, team_color)
            team_pieces.append(piece)
            master_sprite_list.add(piece)
            piece_index += 1
    sum_team_pieces = sum([piece.get_health() for piece in team_pieces])
    return team_pieces, sum_team_pieces


def print_pieces(team_name, sum_team_pieces):
    banner_print(team_name + ' got a result of : ')
    for sprite in master_sprite_list.get_subset("Piece"):
        if sprite.get_team() == team_name:
            print(sprite)
    print('sum total: ' + str(sum_team_pieces))


def who_goes_first(sum_team_1_pieces, sum_team_2_pieces, team_1_name, team_2_name):
    goes_first = '?'
    goes_second = '?'
    max_val = max(sum_team_1_pieces, sum_team_2_pieces)
    diff = max_val - min(sum_team_1_pieces, sum_team_2_pieces)
    if sum_team_1_pieces > sum_team_2_pieces:
        goes_first = team_1_name
    elif sum_team_2_pieces > sum_team_1_pieces:
        goes_first = team_2_name
    elif randint(0, 1) == 0:
        goes_first = team_2_name
    else:
        goes_first = team_1_name

    if goes_first == team_1_name:
        goes_second = team_2_name
    else:
        goes_second = team_1_name

    if sum_team_2_pieces == sum_team_1_pieces:
        banner_print(
            goes_first + ' is going first, they have won the coin flip; the sum score is tied at ' + str(max_val))
    else:
        banner_print(goes_first + ' is going first with a sum score of ' + str(max_val) + '.')
        banner_print(goes_second + ' will be able to distribute the difference of ' + str(diff) + ' as they see fit.')

    return goes_first, goes_second, diff


def vs_ai():
    # -------------- roll the dice -----------------------------

    # PLAYER IS TEAM 1
    # AI IS TEAM 2

    # -------------- roll for Player ---------------------------
    banner_print('Rolling the dice for Player 1')
    team_1_pieces, sum_team_1_pieces = roll_dice(SP[Settings.TEAM_1_NAME], SP[Settings.TEAM_1_RGB])

    # -------------- print results of piece roll ---------------
    print_pieces(SP[Settings.TEAM_1_NAME], sum_team_1_pieces)

    # -------------- display results of roll -------------------
    banner_print("Displaying Player 1's pieces")
    refresh_screen()

    # ----------------- roll for AI ----------------------------
    banner_print('Rolling the dice for AI opponent')
    team_2_pieces, sum_team_2_pieces = roll_dice(SP[Settings.TEAM_2_NAME], SP[Settings.TEAM_2_RGB], hide=True)

    # --------- print results results of piece roll ------------
    print_pieces(SP[Settings.TEAM_2_NAME], sum_team_2_pieces)

    # ------------------ contest values ------------------------
    goes_first, goes_second, diff = who_goes_first(sum_team_1_pieces, sum_team_2_pieces, SP[Settings.TEAM_1_NAME], SP[Settings.TEAM_2_NAME])
    refresh_screen()

    if goes_second == SP[Settings.TEAM_1_NAME]:
        coin = HeartCoin(screen, piece_size, piece_size, (piece_size * 6, 0), diff, SP)
        master_sprite_list.add(coin)
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
                        clicked_sprites = [s for s in master_sprite_list.get_all() if
                                           s.image_rectangle.collidepoint(pos)]
                        if len(clicked_sprites) > 0:
                            clicked_piece = clicked_sprites[0]
                            if diff > 0:
                                if event.button == 1 and clicked_piece.increment_health():
                                    # LEFT CLICK - increment health of piece
                                    diff -= 1
                                    coin.decrement()
                                elif event.button == 3 and clicked_piece.decrement_health():
                                    # RIGHT CLICK - decrement health of piece
                                    diff += 1
                                    coin.increment()
                if diff == 0:
                    break
            refresh_screen()
        banner_print('Player one got a result of : ')
        master_sprite_list.remove(coin)
        for sprite in master_sprite_list.get_subset("Piece"):
            if sprite.get_team() == SP[Settings.TEAM_1_NAME]:
                print(sprite)
    else:
        # AI distributes the difference amongst their pieces evenly, from left to right until they are out of points to distribute
        while diff > 0:
            for sprite in [sp for sp in master_sprite_list.get_subset("Piece") if
                           sp.get_team() == SP[Settings.TEAM_2_NAME]]:
                if diff > 0 and sprite.increment_health():
                    diff -= 1
        banner_print('AI got a result of : ')
        for sprite in master_sprite_list.get_subset("Piece"):
            if sprite.get_team() == SP[Settings.TEAM_2_NAME]:
                print(sprite)

    refresh_screen()

    banner_print("Setting up Player 1's half of the board to let them arrange their pieces")
    # clears away remaining sprites after the distribution phase
    clear_screen()

    # setup player 1's half of the board
    team_1_half_board = HalfBoard(piece_size, screen, (0, 0))
    master_sprite_list.add(team_1_half_board)

    # place all of the Player's pieces so they can select and arrange them. Must specify screen position again because it
    # was put off the screen to refresh the screen earlier
    piece_sprites = master_sprite_list.get_subset("Piece")
    for index, sprite in enumerate(piece_sprites):
        if sprite.get_team() == SP[Settings.TEAM_1_NAME]:
            sprite.set_screen_pos((((piece_size + 10) * index) + team_1_half_board.get_width() + 5, 0))

    done_button = Button(100, 50, screen, (10, team_1_half_board.get_height() + 10), 'done', 'Done', SP)
    master_sprite_list.add(done_button)

    refresh_screen()

    banner_print('HalfBoard setup completed')
    banner_print('Waiting for Player 1 to place their pieces')

    # temporary sprite reference used when the Player wishes to swap 2 sprites
    swap_sprite = None
    # temporary sprite used to hold a reference to the selected piece when clearing highlights when a new piece is selected
    highlight_sprite = None

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
                    clicked_sprites = [s for s in master_sprite_list.get_all() if s.image_rectangle.collidepoint(pos)]
                    highlight_sprite = None
                    if len(clicked_sprites) == 1:
                        sprite = clicked_sprites[0]
                        # if the player is clicking only on the board, check to see if there is a highlighted piece to
                        # place, if there is, place it in the square they specified on screen, clear that piece's highlight,
                        # and place in the board model
                        if type(sprite).__name__ == "HalfBoard":
                            for spr in master_sprite_list.get_subset("Piece"):
                                if spr.is_highlighted():
                                    pos = ((pos[0] // piece_size) * piece_size, (pos[1] // piece_size) * piece_size)
                                    spr.clear_highlight()
                                    spr.set_screen_pos(pos)
                                    sprite.set_piece_in_model((pos[1] // piece_size), (pos[0] // piece_size), spr)
                        # if the player is clicking only on a piece, they must be selecting it. Store it in case they
                        # perform a swap in the next loop iteration, highlight it, and un-highlight any other pieces
                        # that might be highlighted.
                        if type(sprite).__name__ == "Piece":
                            highlight_sprite = sprite
                            sprite.highlight(SP[Settings.HIGHLIGHT_COLOR_RGB], SP[Settings.HIGHLIGHT_THICKNESS])
                            for spr in master_sprite_list.get_subset("Piece"):
                                if spr.is_highlighted() and spr is not highlight_sprite:
                                    spr.clear_highlight()
                        # if the player clicks the Done button, end the loop and throw the Done button off the board
                        if type(sprite).__name__ == "Button" and sprite.get_action() == 'done':
                            done = True
                            for p in master_sprite_list.get_subset("Piece"):
                                if p.get_position() == (-1, -1) and p.get_team() == SP[Settings.TEAM_1_NAME]:
                                    done = False
                                    break
                            if done:
                                sprite.set_screen_pos(
                                    (SP[Settings.RESOLUTION][0] * -1, SP[Settings.RESOLUTION][1] * -1))
                    elif len(clicked_sprites) == 2:
                        for sprite in clicked_sprites:
                            # when the player is clicking on both a Piece and another sprite, they must be clicking on
                            # a sprite already placed on the board...
                            if type(sprite).__name__ == "Piece":
                                # check to see if the player has selected a sprite in the last loop iteration and if so,
                                # place the swap sprite in the selected sprite's position, and put the selected sprite where
                                # the swap sprite was
                                if swap_sprite and swap_sprite.is_highlighted():
                                    swap_sprite_pos = swap_sprite.get_screen_pos()
                                    pos = ((pos[0] // piece_size) * piece_size, (pos[1] // piece_size) * piece_size)
                                    swap_sprite.clear_highlight()
                                    swap_sprite.set_screen_pos(pos)
                                    highlight_sprite = sprite
                                    sprite.set_screen_pos(swap_sprite_pos)
                                    for spr in master_sprite_list.get_subset("Piece"):
                                        if spr.is_highlighted() and spr is not highlight_sprite:
                                            spr.clear_highlight()
                                    swap_sprite = None
                                else:
                                    highlight_sprite = sprite
                                    sprite.highlight(SP[Settings.HIGHLIGHT_COLOR_RGB], SP[Settings.HIGHLIGHT_THICKNESS])
                                    swap_sprite = sprite
                                    for spr in master_sprite_list.get_subset("Piece"):
                                        if spr.is_highlighted() and spr is not highlight_sprite:
                                            spr.clear_highlight()
                            else:
                                for spr in master_sprite_list.get_subset("Piece"):
                                    if spr.is_highlighted():
                                        sprite.set_piece_in_model((pos[1] // piece_size), (pos[0] // piece_size), spr)
                refresh_screen()
                # RIGHT CLICK
                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [s for s in master_sprite_list.get_all() if s.image_rectangle.collidepoint(pos)]
                    for sprite in clicked_sprites:
                        if type(sprite).__name__ == "Piece" and sprite.is_highlighted():
                            sprite.clear_highlight()
                    refresh_screen()

    banner_print('Player 1 has placed their pieces')

    banner_print('Setting up a HalfBoard for AI')
    team_2_half_board = HalfBoard(piece_size, screen, (0, team_1_half_board.get_height()))
    master_sprite_list.add(team_2_half_board)
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
    master_sprite_list.add(gameboard)
    master_sprite_list.remove(team_1_half_board)
    master_sprite_list.remove(team_2_half_board)
    master_sprite_list.remove(done_button)

    refresh_screen()
    banner_print('Gameplay has begun')

    print(master_sprite_list)

    turn_number = 0
    done = False
    while not done:
        events = pygame.event.get()
        if len(events) > 0:
            if (turn_number % 2 == 0 and goes_first == SP[Settings.TEAM_1_NAME]) or (
                    turn_number % 2 == 1 and goes_second == SP[Settings.TEAM_1_NAME]):
                for event in events:
                    # X BUTTON
                    if event.type == pygame.QUIT:
                        exit()
                    # LEFT CLICK
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        array_pos = (pos[1] // piece_size, pos[0] // piece_size)
                        clicked_sprites = [s for s in master_sprite_list.get_all() if
                                           s.image_rectangle.collidepoint(pos)]
                        if len(clicked_sprites) == 1:
                            sprite = clicked_sprites[0]
                            if type(sprite).__name__ == "FullBoard":
                                for spr in master_sprite_list.get_subset("Piece"):
                                    if spr.is_highlighted() and array_pos in poss_moves:
                                        banner_print('Player Move')
                                        orig_pos = sprite.index_of_piece(spr)
                                        pos = ((pos[0] // piece_size) * piece_size, (pos[1] // piece_size) * piece_size)
                                        spr.clear_highlight()
                                        spr.set_screen_pos(pos)
                                        sprite.set_piece_in_model(array_pos[0], array_pos[1], spr)
                                        poss_moves = None
                                        print("MOVE: " + str(spr) + " : " + str(orig_pos) + ' ---> ' + str(array_pos))

                                        # attack
                                        targets_damaged = sprite.piece_attack(spr)
                                        for target in targets_damaged:
                                            print("DAMAGE: " + str(target))
                                        # turn ends
                                        turn_number += 1
                            sprite.clear_highlighted_cells()
                            highlight_sprite = None
                        elif len(clicked_sprites) == 2:
                            for sprite in clicked_sprites:
                                if type(sprite).__name__ == "Piece" and sprite.get_team() == SP[Settings.TEAM_1_NAME]:
                                    highlight_sprite = sprite
                                    sprite.highlight(SP[Settings.HIGHLIGHT_COLOR_RGB], SP[Settings.HIGHLIGHT_THICKNESS])
                                    for spr in master_sprite_list.get_subset("Piece"):
                                        if spr.is_highlighted() and spr is not highlight_sprite:
                                            spr.clear_highlight()
                                    for spr in master_sprite_list.get_subset("FullBoard"):
                                        spr.clear_highlighted_cells()
                                        location = spr.index_of_piece(highlight_sprite)
                                        # pass to a function in FullBoard which returns a list of all possible moves
                                        poss_moves = spr.all_possible_moves(location[0], location[1],
                                                                            highlight_sprite.get_health())
                                        # print(str(location) + ', ' + str(highlight_sprite.get_health()) + ' -->' + str(poss_moves))
                                        for x, y in poss_moves:
                                            spr.highlight_cell(x, y, SP[Settings.POSS_MOVES_COLOR_RGB],
                                                               SP[Settings.POSS_MOVES_THICKNESS])
                        elif len(clicked_sprites) == 0:
                            for spr in master_sprite_list.get_subset("Piece"):
                                if spr.is_highlighted():
                                    spr.clear_highlight()
                                    highlight_sprite = None
                            for spr in master_sprite_list.get_subset("FullBoard"):
                                spr.clear_highlighted_cells()
                    refresh_screen()
                    # RIGHT CLICK
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                        pos = pygame.mouse.get_pos()
                        clicked_sprites = [s for s in master_sprite_list.get_all() if
                                           s.image_rectangle.collidepoint(pos)]
                        for sprite in clicked_sprites:
                            if type(sprite).__name__ == "Piece" and sprite.is_highlighted():
                                sprite.clear_highlight()
                        refresh_screen()
            else:
                # AI's turn
                # currently random move
                unmoved = True
                while unmoved:
                    banner_print('AI Move')
                    board = master_sprite_list.get_subset("FullBoard")[0]
                    # piece = choice([spr for spr in sprites if type(spr).__name__ == "Piece" and spr.get_team() == SP[Settings.TEAM_2_NAME]])
                    # possible_moves = board.all_possible_moves(piece_location[0], piece_location[1], piece.get_health())
                    # if len(possible_moves) == 0:
                    #     continue
                    # move = choice(possible_moves)

                    global minimax_tree
                    minimax_tree = Node("Initial")
                    minimax_populate_tree(board.simple_board_state(), SP[Settings.TEAM_2_NAME], 0, 2, minimax_tree)
                    # with codecs.open("tree_output.txt", "w", "utf-8") as output_file:
                    #     for pre, fill, node in RenderTree(minimax_tree):
                    #         output_file.write(str(pre) + str(node.name) + '\n')
                    #
                    # DotExporter(minimax_tree).to_dotfile("output")
                    # render('dot', 'pdf', r"C:\Users\d5ffpr\PycharmProjects\TinkerTactics\output")
                    decision = minimax_make_decision(minimax_tree).__str__()
                    elements = decision.split("/")
                    move_str = elements[2]
                    piece_index_x = int(move_str[move_str.index(' ') + 1: move_str.index(',')])
                    piece_index_y = int(move_str[move_str.index(',') + 2: move_str.index(' to')])
                    piece = board.piece_at_index(piece_index_x, piece_index_y)
                    temp_move = move_str[move_str.index(' to ') + 4: move_str.index(' =')].split(',')
                    move = [int(s) for s in temp_move]

                    minimax_tree = Node("Initial")
                    node_storage.clear()

                    # piece, move = ai_decision(board.board_model, SP[Settings.TEAM_2_NAME], board)
                    piece_location = board.index_of_piece(piece)
                    print("MOVE: " + str(piece) + " : " + str(piece_location) + ' ---> ' + str(move))
                    piece.set_screen_pos((move[1] * piece_size, move[0] * piece_size))
                    board.set_piece_in_model(move[0], move[1], piece)
                    unmoved = False
                    turn_number += 1
                    targets_damaged = board.piece_attack(piece)
                    for target in targets_damaged:
                        print("DAMAGE: " + str(target))
                refresh_screen()

            # determine if the game is over
            count_team_1 = sum(1 for piece in [s for s in master_sprite_list.get_subset("Piece") if
                                               s.get_team() == SP[Settings.TEAM_1_NAME]])
            count_team_2 = sum(1 for piece in [s for s in master_sprite_list.get_subset("Piece") if
                                               s.get_team() == SP[Settings.TEAM_2_NAME]])
            if count_team_1 and count_team_2 and not (count_team_1 > 1 and count_team_2 > 1):
                done = True

    refresh_screen()
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


def main():
    # pull settings
    banner_print('Initializing Settings')
    # ------------ init pygame screen --------------------------
    banner_print('Initializing Pygame')
    pygame.init()
    banner_print('Initializing Font')
    banner_print('Setting Screen resolution')
    pygame.display.set_caption(SP[Settings.GAME_NAME])
    screen.fill(SP[Settings.BACKGROUND_COLOR_RGB])
    banner_print('Setting screen background color')

    # -------------- setup menu -----------------------
    banner_print('Menu setup')

    vs_ai_button = Button(150, 50, screen, (10, 10), 'VS AI', 'VS AI', SP)
    settings_button = Button(150, 50, screen, (10, 70), 'Settings', 'Settings', SP)
    master_sprite_list.add(vs_ai_button)
    master_sprite_list.add(settings_button)
    refresh_screen()

    selection = None
    while not selection:
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
                    clicked_sprites = [s for s in master_sprite_list.get_all() if s.image_rectangle.collidepoint(pos)]
                    if len(clicked_sprites) > 0:
                        clicked_button = clicked_sprites[0]
                        selection = clicked_button.get_action()
        refresh_screen()

    master_sprite_list.remove(vs_ai_button)
    master_sprite_list.remove(settings_button)

    if selection == 'VS AI':
        vs_ai()


cProfile.run('main()', 'stats.prof_file')
