# Import necessary libraries and modules
from functools import partial
from tkinter import font
import tkinter as tk
from typing import Tuple, List
from PIL import ImageTk, Image
from time import sleep
from tkinter import Label
from GameComponents.pieceCollection import *
from GameComponents.gameBoard import *
from GameComponents.pieceCollection import PieceMovement
import menu_gui
import sys
import threading
from enum import Enum, auto

class PlayerTurn(Enum):
    BLACK = auto()
    WHITE = auto()

# Add this global variable
prev_turn = "B"
current_turn = PlayerTurn.WHITE
turn_label = PlayerTurn.BLACK
c_turn = "W"

cells = [0] * (GRID_DIMENSION * GRID_DIMENSION)  # Represents cells on the game board
stacks = {color: [0] * STACKS_COUNT for color in COLORS}  # Represents stacks for the pieces

clicks_count = 1  # Count of clicks made by the player
src_tuple = None  # Tuple to store source cell information for moves
dest_tuple = None  # Tuple to store destination cell information for moves
queue = []  # Queue to manage game actions
stop_threads = False  # Flag to stop threads



#_______________________________________________________________________________________
image_dict = {}

def load_and_resize_image(image_path, size):
    image = Image.open(image_path).resize(size)
    return ImageTk.PhotoImage(image)

def Initialize_images():
    image_dict['veryLarge_Black_stack'] = load_and_resize_image('Images/Very_Large_Black.png', (70, 70))
    image_dict['veryLarge_White_stack'] = load_and_resize_image('Images/Very_Large_White.png', (70, 70))
    image_dict['Large_Black_stack'] = load_and_resize_image('Images/Large_Black.png', (70, 70))
    image_dict['Large_White_stack'] = load_and_resize_image('Images/Large_White.png', (70, 70))
    image_dict['Medium_Black_stack'] = load_and_resize_image('Images/Medium_Black.png', (70, 70))
    image_dict['Medium_White_stack'] = load_and_resize_image('Images/Medium_White.png', (70, 70))
    image_dict['Small_Black_stack'] = load_and_resize_image('Images/Small_Black.png', (70, 70))
    image_dict['Small_White_stack'] = load_and_resize_image('Images/Small_White.png', (70, 70))
    image_dict['EmptySquare_stack'] = load_and_resize_image('Images/EmptySquare.png', (70, 70))
    image_dict['veryLarge_Black_cell'] = load_and_resize_image('Images/Very_Large_Black.png', (110, 110))
    image_dict['veryLarge_White_cell'] = load_and_resize_image('Images/Very_Large_White.png', (110, 110))
    image_dict['Large_Black_cell'] = load_and_resize_image('Images/Large_Black.png', (110, 110))
    image_dict['Large_White_cell'] = load_and_resize_image('Images/Large_White.png', (110, 110))
    image_dict['Medium_Black_cell'] = load_and_resize_image('Images/Medium_Black.png', (110, 110))
    image_dict['Medium_White_cell'] = load_and_resize_image('Images/Medium_White.png', (110, 110))
    image_dict['Small_Black_cell'] = load_and_resize_image('Images/Small_Black.png', (110, 110))
    image_dict['Small_White_cell'] = load_and_resize_image('Images/Small_White.png', (110, 110))
    image_dict['EmptySquare_cell'] = load_and_resize_image('Images/EmptySquare.png', (110, 110))
    image_dict[' veryLarge_White_start'] = load_and_resize_image('Images/Very_Large_White.png', (70, 70))
    image_dict[' veryLarge_Black_start'] = load_and_resize_image('Images/Very_Large_Black.png', (70, 70))
    image_dict['EmptySquare_start'] = load_and_resize_image('Images/EmptySquare.png', (110, 110))





def store_clicks(is_outside: bool, index: int, color: str = None) -> None:
    global src_tuple, dest_tuple, clicks_count, current_turn, prev_turn, c_turn

    if clicks_count == 1:
        dest_tuple = None
        src_tuple = is_outside, index, color
        clicks_count += 1

 
    elif clicks_count == 2:
        if src_tuple == (is_outside, index, color):
            dest_tuple = None
            clicks_count = 2
        else:
            dest_tuple = is_outside, index, color
            clicks_count = 1

            

    
            


def show_error_message(message):
    # Create a top-level window for error message display
    error_window = tk.Toplevel()
    error_window.title("Error")
    error_window.geometry("300x100")
    error_label = tk.Label(error_window, text=message, font=('Helvetica', 12), fg='red')
    error_label.pack(pady=20)
    ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
    ok_button.pack()

def get_clicks() -> Tuple[Tuple[bool, int, str], Tuple[bool, int, str]]:
    return src_tuple, dest_tuple

main_window = None
stop_threads_event = threading.Event()


def on_closing(window):
    global stop_threads
    stop_threads = True  # Set the flag to stop threads
    print("Closing")
    window.quit()
    window.destroy()    # After destroying the window, call sys.exit(0) after a short delay
        # Wait for the update_gui thread to finish
    

def buildBoard():
    # Build the game board UI
    # ...
    global current_turn
    global turn_label
    

    window = tk.Tk()
    window.iconbitmap("Images/iconx.ico")
    window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window))
    Initialize_images()
    global image_dict
    window.title('Gobblet')
    window.resizable(False, False)
    window.geometry("680x750")
    menu_gui.center_window(window, 680, 750)


    veryLarge_White_start = image_dict[' veryLarge_White_start']

    veryLarge_Black_start = image_dict[' veryLarge_Black_start']

    EmptySquare_start = image_dict['EmptySquare_start']

    background_image = Image.open("Images/Background.png")
    background_photo = ImageTk.PhotoImage(background_image)
    # Load the background image
    background_label = tk.Label(window, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    # Create a new game button
    # newGameButton = tk.Button(window, text="New Game", command=newGame)
    # newGameButton.place(x=500, y=15)
    # Create a label for displaying the current turn
    turn_label = Label(window, text="Yellow's Turn", font=('Helvetica', 14), bg='white', fg='red')
    turn_label.place(x=50, y=50)


    global yCor
    for i in range(GRID_DIMENSION * GRID_DIMENSION):
        if i < 4:
            yCor = 75
        if 4 <= i < 8:
            yCor = 195
        if 8 <= i < 12:
            yCor = 315
        if i >= 12:
            yCor = 435

        cells[i] = tk.Button(window, highlightcolor="black", bg="white", image=image_dict['EmptySquare_start'],
                             command=partial(store_clicks, False, i))
        cells[i].image = image_dict['EmptySquare_start']
        cells[i].place(x=25 + 120 * (i % 4) + 75, y=yCor + 80)

    for i in range(STACKS_COUNT):
        stacks[WHITE][i] = tk.Button(window, image=image_dict[' veryLarge_White_start'],
                                     command=partial(store_clicks, True, i, WHITE))
        stacks[WHITE][i].image = image_dict[' veryLarge_White_start']
        stacks[WHITE][i].place(x=110 + i * 90 + 100, y=15 + 50)

    for i in range(STACKS_COUNT):
        stacks[BLACK][i] = tk.Button(window,
                                     image=image_dict[' veryLarge_Black_start'],
                                     command=partial(store_clicks, True, i, BLACK))
        stacks[BLACK][i].image = image_dict[' veryLarge_Black_start']
        stacks[BLACK][i].place(x=110 + i * 90 + 100, y=470 + 180)

    window.after(50, lambda: update_gui(window,turn_label))  # Pass the window variable to update_gui
    window.mainloop()  # Start the Tkinter event loop
