
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from customtkinter import CTkSlider, CTkButton
import math
import threading
import gobblet
import gui
import argparse
import gobblet
from functools import partial
from tkinter import font
import tkinter as tk
from typing import Tuple, List
from PIL import ImageTk, Image
from time import sleep
from tkinter import Label




# Import Players and Heuristics classes
from Players.human_player import HumanPlayer
from Players.ai_player import AIPlayer
from Heuristics.general_heuristic import general_heuristic
from Heuristics.corners_heuristic import corners_heuristic
from Heuristics.aggressive_heuristic import aggressive_heuristic
menu_gui_open_flag = True
# Global variables
game_mode = NONE # Variable to store the game mode (Player vs Player, Player vs PC, PC vs PC)
Normal_PC_difficulty = 1  # Variable to store the difficulty level for the PC

PC1_difficulty = 1  # Variable to store the difficulty level for the PC first player
PC2_difficulty = 2  # Variable to store the difficulty level for the PC second player

def get_game_mode():
    global game_mode
    return game_mode

def get_Normal_PC_difficulty():
    global Normal_PC_difficulty
    if Normal_PC_difficulty != 0:
        return Normal_PC_difficulty
    
def get_PC1_and_PC2_difficulty():
    global PC1_difficulty,PC2_difficulty
    if PC1_difficulty != 0 and PC2_difficulty != 0:
        return [PC1_difficulty, PC2_difficulty]



class FirstGUI(Frame):
    def __init__(self, master):

        self.master = master
        self.master.title("Start Menu")
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)
        self.frame = Frame(self.master)
        self.frame.pack()
        self.second_gui = SecondGUI(master=self.master, app=self)
        self.third_gui = ThirdGUI(master=self.master, app=self)
        # Create a Canvas for the background
        self.background_photo = PhotoImage(file="Images/Start_Background.png")
        self.canvas = Canvas(self.frame, width=580, height=680)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")
        
        self.text = self.canvas.create_text(290, 140, text="Start Menu", font=("calibri", 24, "bold"),fill="white")


        # Create buttons
        button1 = self.create_button(self.canvas, "Player Vs Player", 290, self.start_the_Game)
        button2 = self.create_button(self.canvas, "Player Vs PC", 340, self.make_SecondGUI)
        button3 = self.create_button(self.canvas, "PC Vs PC", 390,self.make_ThirdGUI)
        #bind button1 to set gameMode variable to "player vs player"
        button1.bind("<Button-1>", lambda event: self.set_game_mode("H H"))
        button2.bind("<Button-1>", lambda event: self.set_game_mode("H PC"))
        button3.bind("<Button-1>", lambda event: self.set_game_mode("PC PC"))

        # Store buttons in a list
        self.buttons = [button1, button2, button3]
        self.circular_motion_animation(0)
        
    def start_the_Game(self):
        sleep(0.1)
        self.master.destroy()

        
    
    def set_game_mode(self, mode):
        global game_mode
        game_mode = mode

        

    def create_button(self, canvas, text, y_coord, incoming_command):
        button = Button(
            canvas,
            text=text,
            font=("Helvetica", 12, "bold"),
            bg="#1d84f2",
            fg="white",
            width=13,
            command = incoming_command
        )
        canvas.create_window(290, y_coord, window=button)  # Adjust coordinates

        # Bind events to functions
        button.bind("<Enter>", self.on_enter)
        button.bind("<Leave>", self.on_leave)

        return button


    def on_enter(self, event):
        # Increase the size of the button and change background when hovered
        event.widget.config(font=("Helvetica", 20, "bold"), bg="#0269d6")

        # Change background color for other buttons
        for button in self.buttons:
            if button != event.widget:
                button.config(bg="grey")

    def on_leave(self, event):
        # Restore the original size and background when not hovered
        for button in self.buttons:
                button.config(font=("Helvetica", 15, "bold"), bg="#1d84f2")
            
        
    def make_FirstGUI(self):
        self.frame.pack()
    
    def make_SecondGUI(self):
        self.frame.pack_forget()
        self.second_gui.make_SecondGUI()
        
    def make_ThirdGUI(self):
        self.frame.pack_forget()
        self.third_gui.make_ThirdGUI()

    
    def circular_motion_animation(self, time):
        # Simulate circular motion animation
        radius = 50
        angular_speed = 0.03
        center_x, center_y = 300, 150

        # Calculate the new position of the text in a circular motion
        x = center_x + radius * math.cos(angular_speed * time)
        y = center_y + radius * math.sin(angular_speed * time)

        # Update the position of the text
        self.canvas.coords(self.text, x, y)

        # Scale animation
        scale_factor = 1 + 0.2 * math.sin(math.radians(5 * time))
        self.canvas.scale(self.text, center_x, center_y, scale_factor, scale_factor)

        # Rotation animation
        rotation_angle = 10 * math.sin(math.radians(4 * time))
        self.canvas.itemconfig(self.text, angle=rotation_angle)

        # Continue the animation
        self.master.after(20, lambda: self.circular_motion_animation(time + 1))
        
    def close_window(self):
        # This function will be called when the window is closed
        self.master.quit()
