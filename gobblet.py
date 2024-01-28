# Import necessary modules and dependencies
import sys
import menu_gui
import gui
import argparse
import threading
from gameBoard import GameBoard
from globals import *
from gameState import GameState
from time import sleep
from tkinter import *
from customtkinter import *
# Import Players and Heuristics classes
from Players.human_player import HumanPlayer
from Players.ai_player import AIPlayer
from Heuristics.general_heuristic import general_heuristic
from Heuristics.corners_heuristic import corners_heuristic





def current_player_turn(game_agent_name: str):
    if game_agent_name == HUMAN:
        return HumanPlayer()
    elif game_agent_name == MINIMAX_GENERAL:
        return AIPlayer(evaluation_heuristic=general_heuristic, max_search_depth=2,
                        player_name=MINIMAX_GENERAL,
                        use_randomness=False)
       #return MinimaxAlpaBetaAgent(heuristic=general_heuristic, max_depth=2,
                                 #  name=MINIMAX_GENERAL,
                                  # with_random=False)

    elif game_agent_name == MINIMAX_CORNERS:
        return AIPlayer(evaluation_heuristic=corners_heuristic, max_search_depth=1,
                        player_name=MINIMAX_CORNERS,
                        use_randomness=False)



# Run matches between all combinations of agents provided in agents_list
def execute_all_agent_matches(list_of_agents, number_of_iterations: int, display_game: bool):
    # If the agents_list contains only [ALL], replace it with all agents except HUMAN
    if list_of_agents == [ALL]:
        list_of_agents = ALL_AGENTS_WITHOUT_HUMAN

    # Iterate through each pair of agents and run matches if they are different
    for agent1_name in list_of_agents:
        for agent2_name in list_of_agents:
            if agent1_name != agent2_name:
                # Print the matchup between agent1 and agent2
                print(f'{Style.HEADER}===== {agent1_name} vs {agent2_name} ====={Style.ENDC}')
                # Run a match between agent1 and agent2
                execute_single_match(agent1_name, agent2_name, number_of_iterations, display_game)


# Run a match between two agents and collect statistics
def execute_single_match(agent1_name, agent2_name, iterations: int, show_display: bool):
    # Initialize a dictionary to store match results including wins and average action time for each color
    global agent1, agent2
    match_results = {color: {WINS: 0} for color in COLORS}
    match_results[DRAW] = 0

    # Play the match for the specified number of iterations
    for match in range(iterations):
        # Create instances of agent1 and agent2
        agent1 = current_player_turn(agent1_name)
        agent2 = current_player_turn(agent2_name)
        # Play the game between agent1 and agent2, collect statistics
        winner = play_single_game(agent1, agent2, show_display)

        # Update win counts for each agent if there's a winner, else update for a draw
        if winner is not None:
            if winner == agent1.get_name():
                match_results[WHITE][WINS] += 1
            elif winner == agent2.get_name():
                match_results[BLACK][WINS] += 1
        else:
            match_results[DRAW] += 1

    # Print the match results including wins, average action times, and draws


# Play a single game between two agents
def play_single_game(agent1, agent2, show_display: bool = False):
    # Initialize game components and variables
    board_game = GameBoard()
    player_turn = WHITE
    currentPlayer = agent1
    opponent = agent2
    state = GameState(player_turn, board_game)
    turns = 0
    # Play the game until a terminal state is reached or the maximum number of turns is reached
    while not state.is_end_of_game() and not gui.stop_threads:
        if turns == MAX_TURNS_ALLOWED:
            print("Max Reached!")
            break
        turns += 1
        # Measure action time and get the new action to be performed
        new_action = currentPlayer.determine_best_action(state)

        # Append action to the GUI queue if display is enabled
        if show_display:
            gui.queue.append((new_action, state.board))

        # Generate successor state based on the chosen action
        state = state.create_successor(new_action)

        # Switch player turns for the next round
        player_turn = switch_player_turn(player_turn)
        currentPlayer, opponent = opponent, currentPlayer

    # Check game result and determine the winner or if it's a draw
    if turns == MAX_TURNS_ALLOWED:
        game_result = DRAW
    else:
        game_result = state.board.is_game_over()
    winner = None
    if type(game_result) == tuple:  # Found a winner
        winner = game_result[1]  # Determine winner's color
        if winner == WHITE:
            winner = agent1.get_name()
        else:
            winner = agent2.get_name()
        if show_display:
            gui.queue.append((None, state.board))
    elif game_result == DRAW:  # Game resulted in a draw
        gui.show_draw_message()
        print(f'{agent1.get_name()} vs {agent2.get_name()}: Draw!')

    return winner




# Function to switch player turns
def switch_player_turn(player_turn: str) -> str:
    if player_turn == WHITE:
        return BLACK
    return WHITE


def center_gui_window(root, width, height):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

def display_loading_page():
    root1 = Tk()
    root1.geometry("200x50")
    root1.iconbitmap("Images/iconx.ico")
    root1.title("   ")
    center_gui_window(root1, 200, 50)
    root1.configure(background='white')

    loading_label = Label(root1, text="Loading, please wait...", font=("Helvetica", 12))
    loading_label.pack()
    
    def on_closing():
        root1.destroy()
        
    root1.after(2000, on_closing)

    root1.mainloop()



def gobblet_main():

    
    menu_gui.main_start()
    if(menu_gui.menu_gui_open_flag == True):
        agents_list= menu_gui.get_game_mode().split(" ")
        if (agents_list[0] == "H" and agents_list[1] == "H"):
            agent1 = current_player_turn(agents_list[0])
            agent2 = current_player_turn(agents_list[1])
            
        elif (agents_list[0] == "H" and agents_list[1] == "PC"):
            if(menu_gui.get_Normal_PC_difficulty() == 1):
                agent1 = current_player_turn(agents_list[0])
                agent2 = current_player_turn("MM_C")
            else:
                agent1 = current_player_turn(agents_list[0])
                agent2 = current_player_turn("MM_G")
        
        elif(agents_list[0] == "PC" and agents_list[1] == "PC"):
            blank = menu_gui.get_PC1_and_PC2_difficulty()
            if(blank[0] == 1 and blank[1] == 1):
                agent1 = current_player_turn("MM_C")
                agent2 = current_player_turn("MM_C")
            elif(blank[0] == 2 and blank[1] == 2):
                agent1 = current_player_turn("MM_G")
                agent2 = current_player_turn("MM_G")
            elif(blank[0] == 1 and blank[1] == 2):
                agent1 = current_player_turn("MM_C")
                agent2 = current_player_turn("MM_G")
            elif(blank[0] == 2 and blank[1] == 1):
                agent1 = current_player_turn("MM_G")
                agent2 = current_player_turn("MM_C")
            else: 
                print("Error")
        else:
            print("Error")
                
                

            
        display_loading_page()
        play_thread = threading.Thread(target=play_single_game, args=(agent1, agent2, True))
        window_thread = threading.Thread(target=gui.buildBoard)
        window_thread.start()
        sleep(0.5)
        play_thread.start()
        window_thread.join()
        play_thread.join()
        gui.main_window.destroy()
        sys.exit()
        





        

    
if __name__ == '__main__':
    gobblet_main()







