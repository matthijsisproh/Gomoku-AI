import random
from gomoku import Move, GameState, check_win, move
from GmUtils import GmUtils

import time
import math

class Node:
    def __init__(self, state, parent_node = None):
        self.state = state
        self.parent_node = parent_node  # pointer for ease of use corresponding the previous game state
        self.children_nodes = []        # Container with children nodes
        self.N = 0                      # A number of visits to the node
        self.Q = 0                      # A number of accrued points 

    def calculate_uct_value(self):
        uct = self.Q / self.N + math.sqrt(2 in self.parent_node.N / self.N)
        return uct
    
    def add_children_node(self, children_node):
        self.children_nodes.append(children_node)


# This default base player does a randomn move
class Champion:

    def __init__(self, black_: bool = True):
        """Constructor for the player."""
        self.black = black_

    def new_game(self, black_: bool):
        """At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.
        """
        self.black = black_





    def find_spot_to_expand(self, node :Node, last_move :Move):
        if(check_win(node, last_move)):
            return node

        fully_expanded = False

        if node is not fully_expanded:
            child_node = Node(parent_node=node) # New child node for a not-yet-explored move(with node as its parent)
            node.add_child_node(child_node) # Add child_node to other children nodes
            return child_node
        
        # dict = {}
        # highest_uct_value = 0
        # uct_value = child_node.calculate_uct_value()
        # if uct_value > highest_uct_value:
        #     highest_uct_value = uct_value
        
        return self.find_spot_to_expand(node, last_move)



    def rollout(self, node, state : GameState):
        x = False
        y = False
        result_value = 0
        last_move = 0


        while(state is not check_win(node, last_move)):
            action = 10 # random move
            x, y, state = move(state, move)
        
        return result_value # 1 if win, 0 if loss, 0.5 if draw

    def backup_value(self, node, value):
        while node is not None:
            node.N += 1
            
            if node:# if node corresponds to a game state where the opponent is to move
                node.Q = node.Q - value
            else:
                node.Q = node.Q + value
            
            node = node.parent


    def move(
        self, state: GameState, last_move: Move, max_time_to_move: int = 1000
    ) -> Move:

        root_node = Node(state) # TUPLE (Current board and ply number)

        current_time = time.time() # Get current time
        end_time = current_time + max_time_to_move # time in milliseconds
        while(current_time < end_time):
            leaf_node = self.find_spot_to_expand(root_node, last_move)

            #value = self.rollout(leaf_node)

            # self.backup_value(leaf_node, value)

            # print(value)
            current_time = time.time() # Update current time

        
        # return move # Return move with best child 


        """This is the most important method: the agent will get:
        1) the current state of the game
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        moves = GmUtils.getValidMoves(state[0])
        return random.choice(moves)

    def id(self) -> str:
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "random_player"
