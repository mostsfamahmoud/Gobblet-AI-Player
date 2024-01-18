import abc
from GameComponents.gameState import GameState
from GameComponents.pieceCollection import PieceMovement


class Player:

    @abc.abstractmethod
    def get_name(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def get_move(self, state: GameState) -> PieceMovement:
        raise NotImplemented
