from typing import Union, List
from GameComponents.gameBoard import GameBoard
from globals import *
from GameComponents.pieceCollection import PieceMovement


class GameState:
    def __init__(self, player_turn: str, board: Union[GameBoard, None] = None):
        # Initialize a State object with a board and the player's turn
        self.player_turn = player_turn  # Same as it's Color

        # Create a deep copy of the provided board to avoid shared references
        # If no board is provided, create a new Board instance
        self.board = board.clone() if board else GameBoard()

    def is_terminal(self) -> bool:
        # Check if the current state represents a terminal state (end of the game)
        if self.board.is_game_finished():
            return True
        return False

    def get_legal_moves(self) -> List[PieceMovement]:
        # Retrieve all legal actions for the current player's turn from the board
        return self.board.get_legal_moves(self.player_turn)

    def make_movement(self, move: PieceMovement):
        # Apply a given move to the board
        self.board.move_piece(move)

    def create_successor(self, move: PieceMovement) -> 'GameState':
        # Generate a successor State by applying the given move
        next_player_turn = BLACK if self.player_turn == WHITE else WHITE

        # Create a new GameState with the next player's turn and a copy of the current board
        successor_state = GameState(next_player_turn, self.board)

        # Apply the move to the copied board
        successor_state.make_movement(move)
        return successor_state
