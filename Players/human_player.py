import gui
from Players.player import Player
from GameComponents.gameState import GameState
from time import sleep
from globals import *
from GameComponents.pieceCollection import PieceMovement, Position


class HumanPlayer(Player):
    """
    Human controlled agent
    """

    def __init__(self):
        self.name = HUMAN  # Assigns the name "HUMAN" to the agent

    def get_name(self) -> str:
        return self.name  # Returns the name of the agent

    def get_move(self, state: GameState) -> PieceMovement:

        moves = state.get_legal_moves()  # Retrieves legal actions from the game state

        while True:  # Loops until a valid move is obtained
            # Gets the source and destination tuples from the GUI (user clicks)
            source_tuple, destination_tuple = gui.get_clicks()

            # Checks if source or destination tuples are missing, continues the loop if so
            if source_tuple is None or destination_tuple is None:
                continue

            # Unpacks information from source tuple
            is_source_outside, source_index, source_color = source_tuple

            # Unpacks information from destination tuple
            is_destination_outside, destination_index, destination_color = destination_tuple

            # Creates a Position object to store the current piece position
            piece_position = Position(OUTSIDE, OUTSIDE)  # Default position

            # Checks if the source is outside (on the board's edge)
            if is_source_outside:
                stack_index = source_index
                source_piece = state.board.stacks[source_color][stack_index].top()
            else:  # Inside the board
                cell_index = source_index
                row = int(cell_index / GRID_DIMENSION)
                col = (cell_index % GRID_DIMENSION)
                piece_position = Position(row, col)
                source_piece = state.board.get_cell(piece_position).top()

            if source_piece is None:
                continue  # Continues if the source piece is not found or invalid

            # Checks if the destination is outside (outside the board)
            if is_destination_outside:
                continue  # Continues if the destination is outside the board
            else:  # Inside the board
                cell_index = destination_index
                row = int(cell_index / GRID_DIMENSION)
                col = (cell_index % GRID_DIMENSION)
                destination_position = Position(row, col)

            # Creates a new move with the source and destination positions
            new_move = PieceMovement(source_piece, piece_position, destination_position)

            # Checks if the new move is legal, if so, returns it
            if new_move in moves:
                return new_move

            sleep(0.5)  # Adds a small delay before the next iteration to prevent rapid clicking
