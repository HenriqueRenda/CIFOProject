# Importing required modules
import random
from copy import deepcopy

# The methods are described well inside report

# Method for detecting collision
def check_collision(board, tile_shape, offsets):
    for cy, row in enumerate(tile_shape):
        for cx, val in enumerate(row):
            if val == 0:
                continue
            try:
                if board[cy + offsets[1]][cx + offsets[0]]:
                    return True
            except IndexError:
                return True
    return False

# Method for rotating tile
def get_rotated_tile(tile):
    return list(zip(*reversed(tile)))

# Method for getting effective height
def get_effective_height(board, tile, offsets):
    offset_x, offset_y = offsets
    while not check_collision(board, tile, (offset_x, offset_y)):
        offset_y += 1
    return offset_y-1

# Method for getting board with tile
def get_board_with_tile(board, tile, offsets, flattened=False):
    # Make a copy
    board = deepcopy(board)
    # If flatten, change all numbers to 0/1
    if flattened:
        board = [[int(bool(val)) for val in row] for row in board]
    # Add current tile (do not flatten)
    for y, row in enumerate(tile):
        for x, val in enumerate(row):
            if val != 0:
                board[y + offsets[1]][x + offsets[0]] = val
    return board

# Utility method for calling get_board_with_tile
def get_future_board_with_tile(board, tile, offsets, flattened=False):
    return get_board_with_tile(board, tile, (offsets[0], get_effective_height(board, tile, offsets)), flattened)


# Method for getting height of each column
def get_col_heights(board):
    heights = [0] * 10
    cols = list(range(10))
    for neg_height, row in enumerate(board):
        for i, val in enumerate(row):
            if val == 0 or i not in cols:
                continue
            heights[i] = 24 - neg_height
            cols.remove(i)
    return heights


# Method for counting empty spaces below covers
def get_hole_count(board):
    holes = 0
    cols = [0] * 10
    for neg_height, row in enumerate(board):
        height = 24 - neg_height
        for i, val in enumerate(row):
            if val == 0 and cols[i] > height:
                holes += 1
                continue
            if val != 0 and cols[i] == 0:
                cols[i] = height
    return holes


# Method for getting the unevenness of the board
def get_bumpiness(board):
    bumpiness = 0
    heights = get_col_heights(board)
    for i in range(1, 10):
        bumpiness += abs(heights[i - 1] - heights[i])
    return bumpiness

# Method for getting number of lines cleared from the board
def get_board_and_lines_cleared(board):
    score_count = 0
    row = 0
    while True:
        if row >= len(board):
            break
        if 0 in board[row]:
            row += 1
            continue
        # Delete the "filled" row
        del board[row]
        # Insert empty row at top
        board.insert(0, [0] * 10)
        score_count += 1
    return board, score_count