import sys
from typing import List

from gameState import GameState
from pieceCollection import *

# This function calculates a heuristic score for a given game state.
# The score is calculated based on the positions of the pieces on the board.
def corners_heuristic(state: GameState) -> int:
    heuristic_score = 0
    current_player_color = state.player_turn

    # Positions of first importance are diagonals and edges.
    primary_positions = [state.board.left_diagonal, state.board.right_diagonal,
                        [Position(0, 0), Position(0, 1), Position(0, 2)],
                        [Position(0, 0), Position(1, 0), Position(2, 0)],
                        [Position(2, 0), Position(2, 1), Position(2, 2)],
                        [Position(0, 2), Position(1, 2), Position(2, 2)]]

    # Positions of second importance are the middle row and column.
    secondary_positions = [[Position(0, 1), Position(1, 1), Position(2, 1)],
                         [Position(1, 0), Position(1, 1), Position(1, 2)]]

    game_result = state.board.is_game_over()
    if game_result:  # a player won or draw
        # has winner
        if game_result[1] == current_player_color:
            heuristic_score += sys.maxsize
        elif game_result[1] != current_player_color:
            heuristic_score -= sys.maxsize

    else:  # game not finished
        # Calculate score for positions of first importance.
        for line in primary_positions:
            heuristic_score += get_score_for_line(current_player_color, line, state, 20)
        # Calculate score for positions of second importance.
        for line in secondary_positions:
            heuristic_score += get_score_for_line(current_player_color, line, state, 5)

    return heuristic_score

# This function calculates the score for a given line (row, column or diagonal).
def get_score_for_line(player_color: str, line: List[Position], state: GameState, score_multiplier: int) -> int:
    score = 0
    for location in line:
        cell = state.board.retrieve_cell_at_position(location)
        if cell.is_stack_empty():
            score += 5
        elif cell.getCurrentColor == player_color:
            score += cell.top().size * score_multiplier
            if is_middle_position(location):
                score += 500
            elif is_corner_position(position=cell.position):
                score += 200

        elif cell.getCurrentColor != player_color:
            score -= cell.top().size * score_multiplier
            if is_middle_position(location):
                score -= 500
            elif is_corner_position(position=cell.position):
                score -= 200

    return score

# This function checks if a given position is a corner.
def is_corner_position(position: Position) -> bool:
    if position.row == 0 and position.col == 0:
        return True
    elif position.row == 2 and position.col == 0:
        return True
    elif position.row == 0 and position.col == 2:
        return True
    elif position.row == 2 and position.col == 2:
        return True
    return False

# This function checks if a given position is the middle of the board.
def is_middle_position(location: Position) -> bool:
    if location.row == 1 and location.col == 1:
        return True
    return False