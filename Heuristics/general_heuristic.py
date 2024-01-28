import sys
from gameState import GameState
from cell import Cell
from globals import *
from typing import List
from pieceCollection import *


def general_heuristic(state: GameState) -> int:
    score = 0
    player_color = state.player_turn
    first_importance = [state.board.left_diagonal, state.board.right_diagonal,
                        [Position(0, 0), Position(0, 1), Position(0, 2)],
                        [Position(0, 0), Position(1, 0), Position(2, 0)],
                        [Position(2, 0), Position(2, 1), Position(2, 2)],
                        [Position(0, 2), Position(1, 2), Position(2, 2)]]

    second_importance = [[Position(0, 1), Position(1, 1), Position(2, 1)],
                         [Position(1, 0), Position(1, 1), Position(1, 2)]]
    result = state.board.is_game_finished()
    if result:  # a player won
        # has winner
        if result[1] == player_color:
            return sys.maxsize
        elif result[1] != player_color:
            return -sys.maxsize

    else:  # game not finished
        for line in state.board.lines:
            whites, blacks = state.board.count_colors_on_line(line)
            if blacks == whites == 0:
                score += 0
            elif blacks == 0:
                score += get_score_of_line_with_one_color(player_color, WHITE, line, state)
            elif whites == 0:
                score += get_score_of_line_with_one_color(player_color, BLACK, line, state)
            else:  # there are blacks and whites in line
                score += get_score_of_line_with_2_colors(player_color, line, state)
            
    
        for line in first_importance:
            score += get_score_for_line(player_color, line, state, 20)
        for line in second_importance:
            score += get_score_for_line(player_color, line, state, 5)


    return score


def get_score_of_line_with_one_color(player_color: str, line_color: str, line: List[Cell], state: GameState) -> int:
    score = 0
    for location in line:
        cell = state.board.get_cell(location)
        if cell.is_empty():
            score += 100
        else:
            # Make the scoring less aggressive at lower depths
            score += cell.top().size * 200

    if player_color == line_color:
        return score
    return -score


def get_score_of_line_with_2_colors(player_color: str, line: List[Cell], state: GameState) -> int:
    score = 0
    min_opponent_size = LARGE
    for location in line:
        cell = state.board.get_cell(location)
        if not cell.is_empty():
            if cell.getCurrentColor != player_color and cell.top().size < min_opponent_size:
                min_opponent_size = cell.top().size

            if cell.getCurrentColor == player_color:
                # Make the scoring less aggressive at lower depths
                score += cell.top().size * 200
            else:
                # Make the scoring less aggressive at lower depths
                score -= cell.top().size * 200

    for stack in state.board.stacks[player_color]:
        if (not stack.is_empty()) and stack.top().size > min_opponent_size:
            return score
    return 0


def get_score_for_line(player_color: str, line: List[Position], state: GameState, coefficient: int) -> int:
    score = 0
    for location in line:
        cell = state.board.get_cell(location)
        if cell.is_empty():
            score += 5
        elif cell.getCurrentColor == player_color:
            score += cell.top().size * coefficient
            if is_middle(location):
                score += 500
            elif is_corner(location=cell.position):
                score += 200

        elif cell.getCurrentColor != player_color:
            score -= cell.top().size * coefficient
            if is_middle(location):
                score -= 500
            elif is_corner(location=cell.position):
                score -= 200

    return score

def is_corner(location: Position) -> bool:
    if location.row == 0 and location.col == 0:
        return True
    elif location.row == 2 and location.col == 0:
        return True
    elif location.row == 0 and location.col == 2:
        return True
    elif location.row == 2 and location.col == 2:
        return True
    return False


def is_middle(location: Position) -> bool:
    if location.row == 1 and location.col == 1:
        return True
    return False
