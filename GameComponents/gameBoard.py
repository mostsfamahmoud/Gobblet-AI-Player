from copy import deepcopy
from typing import Tuple, List, Union
from GameComponents.cell import Cell
from GameComponents.pieceStack import PieceStack
from GameComponents.pieceCollection import *


class GameBoard:
    ############################ Board Initailization ##########################

    # Define positions for each row
    rows = [
        [Position(i, j) for j in range(GRID_DIMENSION)]  # Create Position objects for each column in a row
        for i in range(GRID_DIMENSION)  # Iterate through each row
    ]

    # Define positions for each column
    columns = [
        [Position(i, j) for i in range(GRID_DIMENSION)]  # Create Position objects for each row in a column
        for j in range(GRID_DIMENSION)  # Iterate through each column
    ]

    # Define positions for the left diagonal
    left_diagonal = [
        Position(i, i)  # Create Position objects with row and column both as 'i'
        for i in range(GRID_DIMENSION)  # Iterate from 0 to GRID_DIMENSION - 1
    ]

    # Define positions for the right diagonal
    right_diagonal = [
        Position(i, (GRID_DIMENSION - 1) - i)  # Create Position objects for the right diagonal
        for i in range(GRID_DIMENSION)  # Iterate from 0 to GRID_DIMENSION - 1
    ]

    # Combine all the different lines (left diagonal, right diagonal, rows, columns) into a single list
    lines = [left_diagonal, right_diagonal] + rows + columns

    def __init__(self):
        # Initialize the Board with stacks, cells, and pieces
        self.stacks = {color: [] for color in COLORS}  # Create a dictionary of empty lists for each color
        self.cells = []  # Initialize the cells list

        # Create stacks for each color and stack index with respective pieces
        for color in COLORS:
            for stack_index in range(STACKS_COUNT):
                # Create a PieceStack object
                stack = PieceStack()

                # Create pieces of various sizes for the current color and stack index, add to the stack
                for size in SIZES:
                    stack.add(Piece(size, color, stack_index))

                # Add the stack to the corresponding color in the stacks dictionary
                self.stacks[color].append(stack)

        # Create cells in a GRID_DIMENSION x GRID_DIMENSION grid
        for row in range(GRID_DIMENSION):
            rowCell = []

            for col in range(GRID_DIMENSION):
                # Create Cell objects and add to the cells list
                rowCell.append(Cell(PieceStack(), Position(row, col)))

            # Add the row of cells to the cells list to form the grid
            self.cells.append(rowCell)

    def clone(self):
        # Create a new instance of Board
        cloned_board = GameBoard()

        # Deep copy stacks dictionary
        cloned_board.stacks = {color: deepcopy(stack_list) for color, stack_list in self.stacks.items()}

        # Deep copy cells list
        cloned_board.cells = deepcopy(self.cells)

        return cloned_board

    ############################ Methods for Retrieving Information ##########################

    def get_cell(self, cellPosition: Position) -> Union[None, Cell]:
        # Get the cell at the specified location, return None if the location is outside the board
        if cellPosition.is_outside():
            return None

        return self.cells[cellPosition.row][cellPosition.col]

    def get_outside_pieces(self, pieceColor: str) -> List[Piece]:
        # Get the possible pieces outside the board for a given color
        stacks = self.stacks[pieceColor]

        outside_pieces = []
        for stack in stacks:
            if stack.top() is not None:
                outside_pieces.append(stack.top())

        return outside_pieces

    def get_inside_pieces(self, pieceColor: str) -> List[Piece]:
        # Get the possible pieces inside the board for a given color
        inside_pieces = []
        for row in self.cells:
            for cell in row:
                if cell.getCurrentColor() == pieceColor:
                    if cell.top() is not None:
                        inside_pieces.append(cell.top())

        return inside_pieces

    def get_all_pieces(self, pieceColor: str) -> List[Piece]:
        # Get all available pieces (both inside and outside) for a given color
        return self.get_outside_pieces(pieceColor) + self.get_inside_pieces(pieceColor)

    ############################ Methods for Game Logic and Checking Game State ##########################

    def count_line_colors(self, linePositions: List[Position]) -> Tuple[int, int]:
        # Tally the number of white and black pieces on a given line
        whites_count, blacks_count = 0, 0
        for position in linePositions:
            color = self.cells[position.row][position.col].getCurrentColor()
            if color == WHITE:
                whites_count += 1
            elif color == BLACK:
                blacks_count += 1

        return whites_count, blacks_count

    def check_for_win(self) -> Union[Tuple[bool, str, List[Position]], bool]:
        # Check for a win condition in any line
        for line in self.lines:
            whites_count, blacks_count = self.count_line_colors(line)
            if whites_count == GRID_DIMENSION:
                return True, WHITE, line
            elif blacks_count == GRID_DIMENSION:
                return True, BLACK, line

        return False

    def get_lines_of_cell(self, cell: Cell) -> List[List[Position]]:
        # Initialize an empty list to store lines that the cell belongs to
        cell_lines = []

        # Iterate through each line in the precomputed lines of the board
        for line in self.lines:
            # Check if the cell's position is part of the current line
            if cell.position in line:
                # If the cell is in this line, add this line to the list of lines the cell belongs to
                cell_lines.append(line)

        return cell_lines

    def is_move_legal(self, move: PieceMovement) -> bool:
        # Get source and destination cells, as well as the piece to move
        source_cell = self.get_cell(move.getSource())
        destination_cell = self.get_cell(move.getDestination())
        piece_to_move = move.getPiece()

        # Check if the source cell is outside and if there are no pieces in the corresponding stack
        if source_cell is None and len(self.stacks[move.piece.color][move.piece.stack_index].pieces) == 0:
            return False

        # If the source cell is not outside but is empty, the move is invalid
        if source_cell and source_cell.is_empty():
            return False

        # If the destination cell is outside, the move is invalid
        if destination_cell.position.is_outside():
            return False

        # If the destination cell is empty, the move is valid
        if destination_cell.is_empty():
            return True

        # If the destination cell is not empty, check if the piece can be placed on top
        if piece_to_move.getSize() > destination_cell.top().getSize():
            # If the source cell is not outside, the move is valid
            if source_cell:
                return True
            else:
                # Get all lines that the destination cell belongs to
                destination_cell_lines = self.get_lines_of_cell(destination_cell)

                # Iterate through lines involving the destination cell
                for line in destination_cell_lines:
                    # Count the number of pieces of each color in the line
                    whites, blacks = self.count_line_colors(line)

                    # Check if placing the piece completes a line for the respective color
                    if piece_to_move.color == WHITE and blacks == GRID_DIMENSION - 1:
                        return True  # Completed a line for the WHITE color
                    elif piece_to_move.color == BLACK and whites == GRID_DIMENSION - 1:
                        return True  # Completed a line for the BLACK color

        return False  # No valid move found

    def get_piece_moves(self, piece: Piece) -> List[PieceMovement]:
        # Get all possible moves for a given piece
        moves = []
        for row in self.cells:
            for cell in row:
                new_action = PieceMovement(piece, piece.position, cell.position)
                if self.is_move_legal(new_action):
                    moves.append(new_action)

        return moves

    def get_legal_moves(self, pieceColor: str) -> List[PieceMovement]:
        # Get all legal moves for a given color
        color_pieces = self.get_all_pieces(pieceColor)
        moves = []

        for piece in color_pieces:
            piece_actions = self.get_piece_moves(piece)
            moves.extend(piece_actions)

        return moves

    def is_game_draw(self):
        # Check if the board is full (no empty cells)
        for row in self.cells:
            for cell in row:
                if cell.is_empty():
                    return False
        return True

    def is_game_finished(self):
        # Check if the game is finished, return the result if so
        win_condition = self.check_for_win()
        if type(win_condition) == tuple:
            return win_condition

        return False

    def move_piece(self, move: PieceMovement) -> None:
        # Extract necessary details from the provided move
        originalPiece = move.getPiece()  # Get the piece involved in the move
        srcPosition = move.getSource()  # Get the source position of the piece
        destPosition = move.getDestination()  # Get the destination position of the piece

        # Create a copy of the piece to be moved
        copyPiece = Piece(originalPiece.size, originalPiece.color, originalPiece.stack_index)

        # Add the copied piece to the destination cell and update its position
        self.cells[destPosition.row][destPosition.col].add(copyPiece)
        self.cells[destPosition.row][destPosition.col].top().position = destPosition

        # Check if the piece was moved from an outside position
        if srcPosition.is_outside():
            # If the piece was moved from an outside position, update its stack index
            self.cells[destPosition.row][destPosition.col].top().stack_index = NONE
            # Remove the piece from the stack on the outside position
            self.stacks[originalPiece.color][originalPiece.stack_index].pop()
        else:
            # If the piece was moved from an inside cell, remove it from the source cell
            self.cells[srcPosition.row][srcPosition.col].pop()


if __name__ == "__main__":
    # Create a board object
    board = GameBoard()

    # Example usage: Make some moves and check game state

    # Display initial board state
    print("Initial Board State:")
    # Your logic to print the board state goes here

    # Get legal actions for a specific color
    legal_actions = board.get_legal_moves("WHITE")
    print("\nLegal Actions for WHITE:", legal_actions)

    # Make an move (move a piece)
    if len(legal_actions) > 0:
        selected_action = legal_actions[0]  # Select the first legal move
        print("\nSelected Action:", selected_action)

        # Apply the selected move on the board
        board.move_piece(selected_action)

        # Display updated board state after the move
        print("\nBoard State After the Action:")
        # Your logic to print the updated board state goes here

    # Check if the game is finished or if it's a draw
    if board.is_game_finished():
        result = board.is_game_finished()
        if result:
            print("\nGame Over! Winner:", result[1])
        else:
            print("\nIt's a draw!")

    # Check if the board is full (no empty cells)
    if board.is_game_draw():
        print("\nThe game ended in a draw.")