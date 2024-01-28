import sys
from gameState import GameState
from cell import Cell
from globals import *
from typing import List
from pieceCollection import *

# This function calculates a heuristic score for a given game state.
def general_heuristic(state: GameState) -> int:
    total_score = 0
    current_player_color = state.player_turn  # Get the color of the current player

    # Define positions of first importance (diagonals and edges)
    primary_positions = [state.board.left_diagonal, state.board.right_diagonal,
                        [Position(0, 0), Position(0, 1), Position(0, 2)],
                        [Position(0, 0), Position(1, 0), Position(2, 0)],
                        [Position(2, 0), Position(2, 1), Position(2, 2)],
                        [Position(0, 2), Position(1, 2), Position(2, 2)]]

    # Define positions of second importance (middle row and column)
    secondary_positions = [[Position(0, 1), Position(1, 1), Position(2, 1)],
                         [Position(1, 0), Position(1, 1), Position(1, 2)]]

    # Check if the game has finished
    game_result = state.board.is_game_over()
    if game_result:  # a player won
        # has winner
        if game_result[1] == current_player_color:  # If the current player won
            return sys.maxsize
        elif game_result[1] != current_player_color:  # If the opponent won
            return -sys.maxsize

    else:  # game not finished
        # Calculate score for each line on the board
        for line in state.board.lines:
            whites, blacks = state.board.count_piece_colors_on_line(line)
            if blacks == whites == 0:  # If the line is empty
                total_score += 0
            elif blacks == 0:  # If the line only contains white pieces
                total_score += calculate_single_color_line_score(current_player_color, WHITE, line, state)
            elif whites == 0:  # If the line only contains black pieces
                total_score += calculate_single_color_line_score(current_player_color, BLACK, line, state)
            else:  # there are blacks and whites in line
                total_score += calculate_dual_color_line_score(current_player_color, line, state)

        # Calculate score for positions of first importance
        for line in primary_positions:
            total_score += get_score_for_line(current_player_color, line, state, 20)
        # Calculate score for positions of second importance
        for line in secondary_positions:
            total_score += get_score_for_line(current_player_color, line, state, 5)

    return total_score

# This function calculates the score for a line that only contains one color
def calculate_single_color_line_score(player_color: str, line_color: str, line: List[Cell], state: GameState) -> int:
    score = 0
    for position in line:
        cell = state.board.retrieve_cell_at_position(position)
        if cell.is_stack_empty():  # If the cell is empty
            score += 100
        else:  # If the cell contains a piece
            # Make the scoring less aggressive at lower depths
            score += cell.top().size * 200

    if player_color == line_color:  # If the line color is the same as the player color
        return score
    return -score  # If the line color is not the same as the player color

# This function calculates the score for a line that contains both colors
def calculate_dual_color_line_score(player_color: str, line: List[Cell], state: GameState) -> int:
    score = 0
    minimum_opponent_piece_size = LARGE
    for location in line:
        cell = state.board.retrieve_cell_at_position(location)
        if not cell.is_stack_empty():  # If the cell contains a piece
            if cell.getCurrentColor != player_color and cell.top().size < minimum_opponent_piece_size:
                minimum_opponent_piece_size = cell.top().size

            if cell.getCurrentColor == player_color:  # If the piece is the same color as the player
                # Make the scoring less aggressive at lower depths
                score += cell.top().size * 200
            else:  # If the piece is not the same color as the player
                # Make the scoring less aggressive at lower depths
                score -= cell.top().size * 200

    for stack in state.board.color_stacks[player_color]:
        if (not stack.is_empty()) and stack.top().size > minimum_opponent_piece_size:
            return score
    return 0

# This function calculates the score for a given line (row, column or diagonal)
def get_score_for_line(player_color: str, line: List[Position], state: GameState, score_multiplier: int) -> int:
    score = 0
    for location in line:
        cell = state.board.retrieve_cell_at_position(location)
        if cell.is_stack_empty():  # If the cell is empty
            score += 5
        elif cell.getCurrentColor == player_color:  # If the piece is the same color as the player
            score += cell.top().size * score_multiplier
            if is_middle_position(location):  # If the cell is in the middle of the board
                score += 500
            elif is_corner_position(location=cell.position):  # If the cell is in the corner of the board
                score += 200

        elif cell.getCurrentColor != player_color:  # If the piece is not the same color as the player
            score -= cell.top().size * score_multiplier
            if is_middle_position(location):  # If the cell is in the middle of the board
                score -= 500
            elif is_corner_position(location=cell.position):  # If the cell is in the corner of the board
                score -= 200

    return score

# This function checks if a given position is a corner
def is_corner_position(location: Position) -> bool:
    if location.row == 0 and location.col == 0:
        return True
    elif location.row == 2 and location.col == 0:
        return True
    elif location.row == 0 and location.col == 2:
        return True
    elif location.row == 2 and location.col == 2:
        return True
    return False

# This function checks if a given position is the middle of the board
def is_middle_position(location: Position) -> bool:
    if location.row == 1 and location.col == 1:
        return True
    return False