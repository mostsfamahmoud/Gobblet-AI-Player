import gui
from Players.player import Player
from gameState import GameState
from time import sleep
from globals import *
from pieceCollection import PieceAction, Position


class HumanPlayer(Player):
    """
    Human controlled agent
    """

    def __init__(self):
        self.name = HUMAN  # Assigns the name "HUMAN" to the agent

    def get_name(self) -> str:
        return self.name  # Returns the name of the agent

    def determine_best_action(self, state: GameState) -> PieceAction:

        valid_actions = state.get_legal_actions()  # Retrieves legal actions from the game state

        while True:  # Loops until a valid action is obtained
            # Gets the source and destination tuples from the GUI (user clicks)
            src_tuple, dest_tuple = gui.get_clicks()

            # Checks if source or destination tuples are missing, continues the loop if so
            if src_tuple is None or dest_tuple is None:
                continue

            # Unpacks information from source tuple
            src_is_outside, src_index, src_color = src_tuple
            dest_is_outside, dest_index, dest_color = dest_tuple

            # Creates a piece object from the source information
            piece_position = Position(OUTSIDE, OUTSIDE)  # Default position

            # Checks if the source is outside (on the board's edge)
            if src_is_outside:
                stack_index = src_index
                src_piece = state.board.color_stacks[src_color][stack_index].top()
            else:  # Inside the board
                cell_index = src_index
                row, col = int(cell_index / GRID_DIMENSION), (cell_index % GRID_DIMENSION)
                piece_position = Position(row, col)
                src_piece = state.board.retrieve_cell_at_position(piece_position).top()

            if src_piece is None:
                continue  # Continues if the source piece is not found or invalid

            # Checks if the destination is outside (outside the board)
            if dest_is_outside:
                continue  # Continues if the destination is outside the board
            else:  # Inside the board
                cell_index = dest_index
                row, col = int(cell_index / GRID_DIMENSION), (cell_index % GRID_DIMENSION)

            # Creates a new action with the source and destination positions
            new_action = PieceAction(src_piece, piece_position, Position(row, col))

            # Checks if the new action is legal, if so, returns it
            if new_action in valid_actions:
                return new_action

            sleep(0.5)  # Adds a small delay before the next iteration to prevent rapid clicking
