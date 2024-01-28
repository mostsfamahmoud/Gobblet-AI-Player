from typing import Union
from pieceCollection import *
from pieceStack import PieceStack


class Cell:
    def __init__(self, cellStack: PieceStack = PieceStack(), cellPosition: Position = Position(OUTSIDE, OUTSIDE)):
        # Initialize a Cell with a stack of pieces (defaulting to an empty stack) and a Position (defaulting to outside)
        self.stack = cellStack
        self.position = cellPosition

    def is_stack_empty(self) -> bool:
        # Check if the cell's stack is empty
        return self.stack.is_stack_empty()

    def getCurrentColor(self) -> Union[str, None]:
        # Return the color of the top piece of the cell's stack (or None if the stack is empty)
        if self.is_stack_empty():
            return None
        return self.stack.top().getColor()

    def add(self, piece: Piece) -> bool:
        # Add a piece to the cell's stack and return True if successful, False otherwise
        return self.stack.add(piece)

    def top(self) -> Union[None, Piece]:
        # Return the top piece of the cell's stack (or None if the stack is empty)
        return self.stack.top()

    def pop(self):
        # Remove the top piece from the cell's stack
        self.stack.pop()


if __name__ == "__main__":
    # Test or example code specific to Cell when run directly

    # Create instances of Piece, PieceStack, and Position
    piece1 = Piece(size=2, color='red', stack_index=0)
    piece2 = Piece(size=3, color='blue', stack_index=1)
    piece3 = Piece(size=1, color='green', stack_index=2)
    stack = PieceStack()
    position = Position(2, 2)

    # Create a cell and perform operations
    cell = Cell(stack, position)

    # Check if the cell's stack is empty (should be True at this point)
    print(cell.is_stack_empty())

    # Add piece1 to the cell's stack
    cell.add(piece1)

    # Check the color of the top piece in the cell's stack
    print(cell.getCurrentColor())  # Output: 'red'

    # Add piece2 to the cell's stack
    cell.add(piece2)

    # Check the color of the top piece in the cell's stack
    print(cell.getCurrentColor())  # Output: 'blue'

    # Add piece3 to the cell's stack (Won't be added)
    cell.add(piece3)

    # Check the color of the top piece in the cell's stack
    print(cell.getCurrentColor())  # Output: 'blue'

    # Remove the top piece from the cell's stack
    cell.pop()

    # Check the color of the top piece in the cell's stack after popping
    print(cell.getCurrentColor())  # Output: 'red'
