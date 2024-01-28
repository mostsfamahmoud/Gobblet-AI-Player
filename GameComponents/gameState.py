from typing import Union, List
from gameBoard import GameBoard
from globals import *
from pieceCollection import PieceAction


class GameState:
    def __init__(self, player_turn: str, board: Union[GameBoard, None] = None):
        # Initialize a State object with a board and the player's turn
        self.player_turn = player_turn  # Same as it's Color

        # Create a deep copy of the provided board to avoid shared references
        # If no board is provided, create a new Board instance
        self.board = board.clone() if board else GameBoard()

    def is_end_of_game(self) -> bool:
        # Check if the current state represents a terminal state (end of the game)
        if self.board.is_game_over():
            return True
        return False

    def get_legal_actions(self) -> List[PieceAction]:
        # Retrieve all legal actions for the current player's turn from the board
        return self.board.get_legal_actions(self.player_turn)

    def make_action(self, action: PieceAction):
        # Apply a given action to the board
        self.board.perform_piece_action(action)

    def create_successor(self, action: PieceAction) -> 'GameState':
        # Generate a successor State by applying the given action
        next_player_turn = BLACK if self.player_turn == WHITE else WHITE

        # Create a new GameState with the next player's turn and a copy of the current board
        successor_state = GameState(next_player_turn, self.board)

        # Apply the action to the copied board
        successor_state.make_action(action)
        return successor_state
