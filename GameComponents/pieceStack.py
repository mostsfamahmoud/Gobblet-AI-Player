from typing import Union, List
from GameComponents.pieceCollection import Piece


class PieceStack:

    # Here, pieces is annotated with Union[None, List[Piece]],
    # meaning it can either be None or a list of Piece objects.
    def __init__(self, pieces: Union[None, List[Piece]] = None):
        # Initialize the PiecesStack with a list of pieces or an empty list if None is provided
        self.pieces = pieces if pieces else []

    def get_size(self) -> int:
        # Return the number of pieces in the stack
        return len(self.pieces)

    def is_empty(self) -> bool:
        # Check if the stack is empty
        return not bool(self.pieces)

    def top(self) -> Union[None, Piece]:
        # Return the top piece of the stack if the stack is not empty
        if not self.is_empty():
            return self.pieces[-1]  # Accessing the last element in the list (top of the stack)
        return None

    def is_addition_valid(self, piece: Piece) -> bool:
        # Check if adding a piece on top of the stack is valid
        top_piece = self.top()

        # New piece can be added if the stack is empty or this new piece is larger
        # Otherwise, adding the piece is not valid
        return not top_piece or piece.size > top_piece.size

    def add(self, newPiece: Piece) -> bool:
        # Add a piece to the stack if the addition is valid
        if self.is_addition_valid(newPiece):
            self.pieces.append(newPiece)
            return True
        return False

    def pop(self) -> None:
        # Remove the top piece from the stack if the stack is not empty
        if self.pieces:
            self.pieces.pop()


if __name__ == "__main__":
    # Test or example code specific to PieceStack when run directly

    # Initialize an empty PieceStack
    stack = PieceStack()

    # Create instances of Piece
    piece1 = Piece(size=2, color='red', stack_index=0)
    piece2 = Piece(size=3, color='blue', stack_index=1)

    # Add pieces to the stack
    stack.add(piece1)
    stack.add(piece2)

    # Check the size of the stack
    print(stack.get_size())  # This should print 2

    # Check the top piece in the stack
    print(stack.top())  # This should print the details of piece2

    # Remove the top piece from the stack
    stack.pop()

    # Check the size of the updated stack after removal
    print(stack.get_size())  # This should print 1

    # Check the top piece in the updated stack
    print(stack.top())  # This should print the details of piece1
