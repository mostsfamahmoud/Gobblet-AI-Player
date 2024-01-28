import abc
from GameComponents.gameState import GameState
from GameComponents.pieceCollection import PieceMovement


class Player:

#function to get the name of the player
    @abc.abstractmethod
    def get_name(self) -> str:
        raise NotImplemented

#function to get the player move on the board
    @abc.abstractmethod
    def get_move(self, state: GameState) -> PieceMovement:
        raise NotImplemented
