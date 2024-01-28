# Import necessary classes and variables from other modules
from globals import *
# Constants: NONE = None, OUTSIDE = -1

class Position:
    # Initialize constructor with row and column
    def __init__(self, row: int, col: int):
        # Assign row and column attributes to the Location object
        self.row = row
        self.col = col

    # Check if the location is considered 'outside'
    def is_outside(self) -> bool:
        # Determine if the row value matches the constant for 'outside'
        return self.row == OUTSIDE  # OUTSIDE is a global variable set to -1

    # Define equality comparison for two locations
    def __eq__(self, other) -> bool:
        # Check if both the row and column of two locations are equal
        return isinstance(other, Position) and self.row == other.row and self.col == other.col

    # Return a string representation of the current location {row / column}
    def __repr__(self):
        # Display the row and column values in a formatted string
        return f'({self.row},{self.col})'


"""
# Example of Usage (CLASS Position)

loc1 = Position(2, 4)
loc2 = Position(2, 4)
loc3 = Position(3, 5)

print(loc1 == loc2)  # Output: True - loc1 and loc2 have the same row and column values
print(loc1 == loc3)  # Output: False - loc1 and loc3 have different row or column values

loc = Position(3, 5)
print(repr(loc))  # Output: '(3,5)' - repr() returns a string representing the object
print(loc)  # Output: '(3,5)' - when directly printing the object, __repr__ is called
"""


# Class representing a game piece
class Piece:
    # Initialize piece parameters: size, color, and stack index
    def __init__(self, size: int, color: str, stack_index: int = NONE):
        # Assign size, color, and stack index to the Piece object
        self.size = size
        self.color = color
        self.stack_index = stack_index
        # Initialize the piece's location as an outside location using the Position class
        self.position = Position(row=OUTSIDE, col=OUTSIDE)

    # Getters for properties
    def getSize(self):
        return self.size

    def getColor(self):
        return self.color

    def getStackIndex(self):
        return self.stack_index

    def getPosition(self):
        return self.position

    # Setters for some properties
    def setSize(self, size):
        self.size = size

    def setPosition(self, new_position):
        self.position = new_position

    # Compare two pieces for equality based on their size, color, location, and stack index
    def __eq__(self, other):
        return (
                isinstance(other, Piece)
                and self.size == other.size
                and self.color == other.color
                and self.position == other.position
                and self.stack_index == other.stack_index
        )

    def __repr__(self):
        return (
            f"Piece(size={self.size}, color='{self.color}', stack_index={self.stack_index}, position={self.position})"
        )

"""
# Example of Usage (CLASS Piece)

# Create instances of Piece
piece1 = Piece(size=2, color='red', stack_index=0)
piece2 = Piece(size=2, color='red', stack_index=0)

# Check if two pieces are equal
if piece1 == piece2:
    print("These pieces are equal.")
else:
    print("These pieces are not equal.")

piece1.setSize(3)
print(piece1.getSize())  # Output: 3

new_position = Position(row=5, col=10)
piece1.setPosition(new_position)
print(piece1.getPosition())  # Output: (5,10)
"""


class PieceAction:
    def __init__(self, piece: Piece, source: Position, destination: Position):
        # Initialize an action with a piece, source, and destination positions
        self.piece = piece  # Private attribute for Piece object
        self.src = source  # Private attribute for source Position object
        self.dest = destination  # Private attribute for destination Position object

    # Getters for attributes
    def getPiece(self):
        return self.piece

    def getSource(self):
        return self.src

    def getDestination(self):
        return self.dest

    # Setters for attributes
    def setPiece(self, piece):
        self.piece = piece

    def setSource(self, source):
        self.src = source

    def setDestination(self, destination):
        self.dest = destination

    def __eq__(self, other):
        # Override the equality comparison for two Action objects
        return (
                isinstance(other, PieceAction)
                and self.piece == other.piece
                and self.src == other.src
                and self.dest == other.dest
        )


if __name__ == "__main__":
    # Test or example code specific to PieceCollection when run directly

    # Create instances of Piece and Position
    piece1 = Piece(size=2, color='red', stack_index=0)
    source_position = Position(row=1, col=1)
    destination_position = Position(row=2, col=2)

    # Create a PieceAction instance
    action1 = PieceAction(piece1, source_position, destination_position)

    # Get attributes using getters
    print(action1.getPiece())  # The String Representation of the Piece
    print(action1.getSource())  # Output: (1, 1)
    print(action1.getDestination())  # Output: (2, 2)

    # Create another Piece and Position
    piece2 = Piece(size=3, color='blue', stack_index=1)
    new_source_position = Position(row=3, col=3)
    new_destination_position = Position(row=4, col=4)

    # Set attributes using setters
    action1.setPiece(piece2)
    action1.setSource(new_source_position)
    action1.setDestination(new_destination_position)

    # Get the updated attributes using getters
    print(action1.getPiece())  # Output: The String Representation of the Piece
    print(action1.getSource())  # Output: (3, 3)
    print(action1.getDestination())  # Output: (4, 4)
