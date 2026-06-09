from graphics import *
import settings
import pygame

def board(light_sq, dark_sq):
    win = GraphWin("Game", 600, 600)

    win.setCoords(0, 0, 8, 8)  # tels the window that bottom left is 0,0 and top right is 8,8
    for row in range(8):
        for col in range(8):
            po1 = Point(col, row)
            po2 = Point(col + 1, row + 1)  # adds one to the value of x and y
            square = Rectangle(po1, po2)
            square.draw(win)

            if (row + col) % 2 == 0:  # tile checker pattern
                square.setFill(dark_sq)
                square.setOutline(dark_sq)

            else:
                square.setFill(light_sq)
                square.setOutline(light_sq)

    return win

def pieces(win, board, white_piece, black_piece):
    # creates an empty 8x8 grid to hold our pieces
    graphic_pieces = [[None for _ in range(8)] for _ in range(8)]

    for row_index, row in enumerate(board):
        for col_index, value in enumerate(row):
            # find the center of the 1x1 grid square
            x_center = col_index + 0.5
            y_center = (7 - row_index) + 0.5

            if value == 1:  # red pieces
                piece = Circle(Point(x_center, y_center), 0.4)
                piece.setFill(white_piece)
                piece.setOutline("white")  # white outline
                piece.draw(win)
                # store the circle object at the matching list coordinates
                graphic_pieces[row_index][col_index] = piece

            elif value == 2:  # same thing for black pieces
                piece = Circle(Point(x_center, y_center), 0.4)
                piece.setFill(black_piece)
                piece.setOutline("white")
                piece.draw(win)
                graphic_pieces[row_index][col_index] = piece

    return graphic_pieces


# helper function to get all available jumps for a player to enforce forced capture rules
def get_all_available_jumps(board, turn):
    jumps = []
    # loop through entire board to find player pieces
    for row in range(8):
        for col in range(8):
            val = board[row][col]
            # check if piece belongs to current player (1/3 for red, 2/4 for black)
            is_player_piece = False
            if turn == 1 and (val == 1 or val == 3):
                is_player_piece = True
            elif turn == 2 and (val == 2 or val == 4):
                is_player_piece = True

            if is_player_piece:
                # find jumps for this specific piece
                piece_jumps = get_piece_jumps(board, row, col, val, turn)
                jumps.extend(piece_jumps)
    return jumps

# helper function to check all 4 diagonal directions for a single piece's valid jumps
def get_piece_jumps(board, row, col, val, turn):
    jumps = []
    # determine allowed directions based on piece type
    directions = []
    if val == 3 or val == 4:  # kings go any direction
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # fixed typo here
    elif val == 1:  # red regular goes up matrix (decreasing row index)
        directions = [(-1, -1), (-1, 1)]
    elif val == 2:  # black regular goes down matrix (increasing row index)
        directions = [(1, -1), (1, 1)]

    for dr, dc in directions:
        mid_row = row + dr
        mid_col = col + dc
        end_row = row + 2 * dr
        end_col = col + 2 * dc

        # make sure landing coordinates stay on the 8x8 board bounds
        if 0 <= end_row < 8 and 0 <= end_col < 8:
            mid_val = board[mid_row][mid_col]
            end_val = board[end_row][end_col]

            # check if middle piece is an enemy
            is_enemy = False
            if turn == 1 and (mid_val == 2 or mid_val == 4):
                is_enemy = True
            elif turn == 2 and (mid_val == 1 or mid_val == 3):
                is_enemy = True

            # if middle is enemy and landing spot is empty, it is a valid jump path
            if is_enemy and end_val == 0:
                jumps.append((row, col, end_row, end_col))
    return jumps


# resets outline to normal state depending on if the piece is a king or normal piece
def reset_piece_outline(piece, val):
    if val == 3 or val == 4:
        piece.setOutline("gold")
        piece.setWidth(4)
    else:
        piece.setOutline("white")
        piece.setWidth(1)

# stores all currently drawn move indicator dots
possible_move_dots = []

def clear_possible_moves():
    global possible_move_dots

    for dot in possible_move_dots:
        try:
            dot.undraw()
        except:
            pass

    possible_move_dots.clear()

def draw_possible_moves(win, available_jumps, start_row, start_col,
                        current_board, clicked_value,
                        req_jumps_enabled):

    global possible_move_dots

    clear_possible_moves()

    valid_destinations = []

    if clicked_value == 1:
        directions = [(-1, -1), (-1, 1)]

    elif clicked_value == 2:
        directions = [(1, -1), (1, 1)]

    elif clicked_value in (3, 4):
        directions = [
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)
        ]

    else:
        directions = []

    # -----------------------------------------
    # Forced captures enabled AND jumps exist on the board
    # -----------------------------------------
    if req_jumps_enabled and len(available_jumps) > 0:

        for jump in available_jumps:
            sr, sc, er, ec = jump

            print("Available jumps:", available_jumps)
            print("Selected piece:", start_row, start_col)

            if sr == start_row and sc == start_col:
                valid_destinations.append((er, ec))

    # -----------------------------------------
    # Forced captures disabled OR no jumps exist right now
    # Show normal steps (plus optional jumps if rule is disabled)
    # -----------------------------------------
    else:

        # Normal diagonal steps
        for dr, dc in directions:

            new_row = start_row + dr
            new_col = start_col + dc

            if (0 <= new_row < 8 and
                    0 <= new_col < 8 and
                    current_board[new_row][new_col] == 0):

                valid_destinations.append((new_row, new_col))

        # Only add optional jumps here if forced captures are turned off entirely
        if not req_jumps_enabled:
            piece_jumps = get_piece_jumps(
                current_board,
                start_row,
                start_col,
                clicked_value,
                1 if clicked_value in (1, 3) else 2
            )

            for _, _, jump_row, jump_col in piece_jumps:
                valid_destinations.append((jump_row, jump_col))

    # -----------------------------------------
    # Draw dots
    # -----------------------------------------
    for row, col in valid_destinations:

        x_center = col + 0.5
        y_center = (7 - row) + 0.5

        dot = Circle(Point(x_center, y_center), 0.15)
        dot.setFill("gray")
        dot.setOutline("gray")

        print("valid_destinations =", valid_destinations)

        dot.draw(win)

        possible_move_dots.append(dot)

def start_game(saved_settings):
    try:
        current_turn = 1  # red goes first

        if saved_settings is None:
            saved_settings = {
                'show_moves': 0,
                'req_jumps': 0,
                'color': 0,
                'music': 0
            }
            print("No settings chosen. Loaded defaults!")

        show_moves_enabled = saved_settings.get('show_moves', 1)
        req_jumps_enabled = saved_settings.get('req_jumps', 1)

        color_choice = saved_settings.get('color', 1)

        current_colors = settings.preset_colors(color_choice+1 if color_choice != 0 else color_choice)

        light_sq = current_colors["light_square"]
        dark_sq = current_colors["dark_square"]
        white_piece = current_colors["w_piece"]
        black_piece = current_colors["b_piece"]

        game_board = board(light_sq, dark_sq)

        pygame.mixer.init()
        music_settings = saved_settings.get("music",1)
        track_to_play = settings.preset_music(music_settings)

        pygame.mixer.music.load(track_to_play)
        pygame.mixer.music.set_volume(0.4)  # Keep it cozy at 40% volume
        pygame.mixer.music.play(-1)
        print(f"Now playing: {track_to_play}") # music

        current_board = [
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0]
        ]

        # Capture the grid of pieces returned by the pieces function
        p_shapes = pieces(game_board, current_board, white_piece, black_piece)

        # track combo sequence variables
        in_combo = False
        combo_row = -1
        combo_col = -1

        # checks if red pieces (1, 3) and black pieces (2, 4) both exist in the matrix
        # if one doesn't then the loop exits
        while any(cell in (1, 3) for row in current_board for cell in row) and \
                any(cell in (2, 4) for row in current_board for cell in row):

            # find all available jumps on the board at the start of turn sequence
            if not in_combo:
                available_jumps = get_all_available_jumps(current_board, current_turn)
            else:
                # if in combo, only look at the piece currently performing jumps
                combo_piece_val = current_board[combo_row][combo_col]
                available_jumps = get_piece_jumps(current_board, combo_row, combo_col, combo_piece_val, current_turn)

                # if no more jumps are available for this piece, combo turn ends completely
                if not available_jumps:
                    in_combo = False
                    current_turn = 2 if current_turn == 1 else 1
                    continue

            print(f"Turn: Player {current_turn}. Forced Jumps Available: {len(available_jumps) > 0}")
            print("Click 1: Select a piece...")
            click1 = game_board.getMouse()
            start_col = int(click1.getX())
            start_row = int(click1.getY())
            matrix_start_row = 7 - start_row

            # block selection if locked into a combo with a specific piece
            if in_combo and (matrix_start_row != combo_row or start_col != combo_col):
                print("Must continue combo sequence with the highlighted piece!")
                continue

            clicked_value = current_board[matrix_start_row][start_col]

            if req_jumps_enabled and len(available_jumps) > 0:

                piece_can_jump = False

                for sr, sc, er, ec in available_jumps:
                    if sr == matrix_start_row and sc == start_col:
                        piece_can_jump = True
                        break

                if not piece_can_jump:
                    print("You must select a piece that can capture.")
                    continue

            # checks if they clicked their own piece or king (1/3 for red, 2/4 for black)
            is_valid_turn = False
            if current_turn == 1 and (clicked_value == 1 or clicked_value == 3):
                is_valid_turn = True
            elif current_turn == 2 and (clicked_value == 2 or clicked_value == 4):
                is_valid_turn = True

            if is_valid_turn:
                # highlight selected piece with a bold yellow outline
                selected_shape = p_shapes[matrix_start_row][start_col]
                selected_shape.setOutline("yellow")
                selected_shape.setWidth(4)

                if show_moves_enabled:
                    draw_possible_moves(
                        game_board,
                        available_jumps,
                        matrix_start_row,
                        start_col,
                        current_board,
                        clicked_value,
                        req_jumps_enabled
                    )

                print("Piece selected! Click 2: Choose where to move")

                # waits for the second click
                click2 = game_board.getMouse()

                clear_possible_moves()

                end_col = int(click2.getX())
                end_row = int(click2.getY())
                matrix_end_row = 7 - end_row

                col_diff = abs(end_col - start_col)  # finds the diagonals
                row_diff = abs(end_row - start_row)

                is_step = (col_diff == 1 and row_diff == 1)  # normal 1 space move
                is_jump = (col_diff == 2 and row_diff == 2)  # jump over a piece move

                # checks direction, kings can go anywhere but regular pieces go forward
                if clicked_value == 3 or clicked_value == 4:
                    direction_ok = True
                elif clicked_value == 1:
                    direction_ok = matrix_end_row < matrix_start_row
                elif clicked_value == 2:
                    direction_ok = matrix_end_row > matrix_start_row

                # check if the destination square is empty and direction is right
                if current_board[matrix_end_row][end_col] == 0 and direction_ok:
                    move_executed = False

                    # handle regular single step move (only if there are no forced jumps on board)
                    if is_step:
                        # only enforce forced captures if enabled
                        if req_jumps_enabled and len(available_jumps) > 0:
                            print("Illegal move! You are forced to capture an enemy piece.")
                            reset_piece_outline(selected_shape, clicked_value)
                            continue

                        current_board[matrix_end_row][end_col] = clicked_value
                        current_board[matrix_start_row][start_col] = 0
                        move_executed = True

                    # handle jumping over an enemy piece
                    elif is_jump:
                        # ensure this specific jump path is within our legal forced jump list
                        current_jump_action = (
                            matrix_start_row,
                            start_col,
                            matrix_end_row,
                            end_col
                        )

                        if req_jumps_enabled:

                            if current_jump_action not in available_jumps:
                                print("Illegal jump destination match failed!")
                                reset_piece_outline(selected_shape, clicked_value)
                                continue

                        else:

                            piece_jumps = get_piece_jumps(
                                current_board,
                                matrix_start_row,
                                start_col,
                                clicked_value,
                                current_turn
                            )

                            if current_jump_action not in piece_jumps:
                                print("Illegal jump destination match failed!")
                                reset_piece_outline(selected_shape, clicked_value)
                                continue

                        mid_row_pos = (matrix_start_row + matrix_end_row) // 2
                        mid_col_pos = (start_col + end_col) // 2

                        # clear enemy from matrix and screen
                        current_board[mid_row_pos][mid_col_pos] = 0
                        jumped_piece = p_shapes[mid_row_pos][mid_col_pos]
                        jumped_piece.undraw()
                        p_shapes[mid_row_pos][mid_col_pos] = None

                        # update jumping piece positions matrix
                        current_board[matrix_end_row][end_col] = clicked_value
                        current_board[matrix_start_row][start_col] = 0
                        move_executed = True

                    if move_executed:
                        # move the circle
                        # calculates distance to move (destination - start)
                        dx = end_col - start_col
                        dy = end_row - start_row

                        # grab the circle object from our shape grid and slide it
                        target_piece = p_shapes[matrix_start_row][start_col]
                        target_piece.move(dx, dy)

                        # king promotion check
                        is_promoted = False
                        if clicked_value == 1 and matrix_end_row == 0:  # red reached top
                            current_board[matrix_end_row][end_col] = 3  # 3 = red king
                            is_promoted = True
                        elif clicked_value == 2 and matrix_end_row == 7:  # black reached bottom
                            current_board[matrix_end_row][end_col] = 4  # 4 = black king
                            is_promoted = True

                        # update the matrix grid position
                        p_shapes[matrix_end_row][end_col] = target_piece
                        p_shapes[matrix_start_row][start_col] = None

                        # restore outline look after move completes
                        current_piece_value = current_board[matrix_end_row][end_col]
                        reset_piece_outline(target_piece, current_piece_value)

                        print("Moved")

                        # check for consecutive multi-jump paths
                        if is_jump and not is_promoted:
                            # look ahead for more available jumps from the new coordinate location
                            next_jumps = get_piece_jumps(current_board, matrix_end_row, end_col, current_piece_value,
                                                         current_turn)
                            if len(next_jumps) > 0:
                                in_combo = True
                                combo_row = matrix_end_row
                                combo_col = end_col
                                # re-highlight piece because it enters consecutive move phase immediately
                                target_piece.setOutline("yellow")
                                target_piece.setWidth(4)
                                clear_possible_moves()
                                print("Combo available! Must execute next jump path sequence.")
                                continue

                        # reset turn status back to normal flow state if no combos exist
                        in_combo = False
                        current_turn = 2 if current_turn == 1 else 1
                    else:
                        print("Illegal Move")
                        reset_piece_outline(selected_shape, clicked_value)
                else:
                    print("Occupied Square" if current_board[matrix_end_row][end_col] != 0 else "Illegal Move")
                    reset_piece_outline(selected_shape, clicked_value)
            else:
                print("Empty Square" if clicked_value == 0 else "Not Your Turn")

    except GraphicsError:
        print("Game Closed")