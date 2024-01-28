import random
import sys
from Players.player import Player
from globals import *
from gameState import GameState
from pieceCollection import PieceAction
from time import *

class AIPlayer(Player):
    """
    MiniMax agent with alpha-beta pruning and iterative deepening
    """

    def __init__(self, evaluation_heuristic, max_search_depth: int, player_name: str, use_randomness: bool):
        self.evaluation_function = evaluation_heuristic  # The heuristic function to evaluate game states
        self.max_depth = max_search_depth  # The maximum depth to search in the game tree
        self.with_random = use_randomness  # Whether to include randomness in action selection
        self.random_value = 3  # Initial value for random action selection
        self.name = player_name  # The name of the AI player

    def alpha_beta_search(self, current_depth, agent_turn, curr_state: GameState, alpha, beta):
        # Recursive function for alpha-beta pruning
        if current_depth == 0:  # If the maximum depth is reached or the game is finished
            return self.evaluation_function(curr_state)  # Return the heuristic value of the current state

        if agent_turn == MAX:  # If it's the maximizing player's turn
            for legal_action in curr_state.get_legal_actions():  # For each legal action
                child_state = curr_state.create_successor(legal_action)  # Generate the successor state
                curr_score = self.alpha_beta_search(current_depth - 1, MIN, child_state, alpha, beta)  # Recurse
                if beta <= alpha:  # If beta is less than or equal to alpha, prune the branch
                    break
                alpha = max(alpha, curr_score)  # Update alpha
            return alpha  # Return the maximum value

        else:  # If it's the minimizing player's turn
            for legal_action in curr_state.get_legal_actions():  # For each legal action
                child_state = curr_state.create_successor(legal_action)  # Generate the successor state
                curr_score = self.alpha_beta_search(current_depth - 1, MAX, child_state, alpha, beta)  # Recurse
                if beta <= alpha:  # If beta is less than or equal to alpha, prune the branch
                    break
                beta = min(beta, curr_score)  # Update beta
            return beta  # Return the minimum value

    def determine_best_action(self, state: GameState) -> PieceAction:
        # Function to get the best action for the current state
        if self.with_random:  # If randomness is included
            self.random_value += 0.8  # Increase the random value
            if random.random() < (3.5 / (self.random_value ** 2)):  # If a random number is less than a threshold
                return random.choice(state.get_legal_actions())  # Return a random action

        best_action = None  # Initialize the best action
        for depth in range(1, self.max_depth + 1):  # For each depth up to the maximum depth
            print("entered")
            actions_scores = []  # Initialize the list of action-score pairs
            for legal_action in state.get_legal_actions():  # For each legal action
                child_state = state.create_successor(legal_action)  # Generate the successor state
                score = self.alpha_beta_search(depth - 1, MIN, child_state, alpha=-sys.maxsize, beta=sys.maxsize)  # Get the score
                actions_scores.append((legal_action, score))  # Add the action-score pair to the list

            just_scores = [score for _, score in actions_scores]  # Get the list of scores
            best_score = max(just_scores)  # Get the best score
            best_actions = [action for action, score in actions_scores if score == best_score]  # Get the best actions
            sleep(0.5)
            best_action = random.choice(best_actions)  # Choose a random best action

        return best_action  # Return the best action

    def get_name(self) -> str:
        # Function to get the name of the AI player
        return self.name