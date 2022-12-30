import random
from gomoku import Move, GameState, check_win, move, pretty_board
from GmUtils import GmUtils

from node import Node

import time
import copy


class Champion:

    def __init__(self, color_: bool = True): 
        """Constructor for the player."""
        self.color = color_     #True is black, False if white
        self.state = None

    def new_game(self, color_: bool):
        """At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.

        :param color_: player color black or white
        """
        self.color = color_
        self.previous_tree_root = None


    def find_spot_to_expand(self, node :Node):
        """
        This function is used to find the next node to expand.
        It is called recurisvely until a node is found that has not been expanded.
        
        The node is found by traversing the tree from the root node to the best child node.
        The best child node is the node with the highest UCT value.
                
        :param node: The node tree with all the game information stored in it.
        
        :return node: A node that is to be expanded.
        """
                   
        if(GmUtils.isWinningMove(node.last_move, node.state[0]) or len(node.valid_moves) == 0): # Return node if game is finished
            return node

        elif node.last_move is not None and GmUtils.isWinningMove(node.last_move, node.state[0]):
            return node

        elif len(node.valid_moves) > len(node.child_nodes):
            valid_moves = node.valid_moves
            new_move = valid_moves[0]
            move_isvalid, winning_move, new_state = move(copy.deepcopy(node.state), new_move)
            valid_moves.remove(new_move)
            child_node = Node(
                            self.color, 
                            new_state, 
                            new_move, 
                            parent_node=node, 
                            valid_moves=valid_moves
                            )
            node.child_nodes.append(child_node)
            return child_node
        return self.find_spot_to_expand(node.best_child())        
                
        
            
 
    def rollout(self, node: Node) -> float:
        """
        This function is used to simulate a random game from the current state of the game.
        It is used to estimate the value of a node.
        
        :param node: The leaf node that was most recently visited.
        
        :return value: It returns 1 if the current player wins, 0 if the current player loses, and 0.5 if the game is a draw.
        """

        if(node.parent_node is not None):
            while(True):
                valid_moves = GmUtils.getValidMoves(node.state[0], node.state[1])
                node.last_move = random.choice(valid_moves)
                move(node.state, node.last_move)
                node.valid_moves = GmUtils.getValidMoves(node.state[0], node.state[1])
                if(GmUtils.isWinningMove(node.last_move, node.state[0]) or len(GmUtils.getValidMoves(node.state[0], node.state[1])) == 0):
                    break
        else:
            return None

        if(GmUtils.isWinningMove(node.last_move, node.state[0])):
            if(node.player_id == self.color):
                return 1 #Win
            else:
                return 0 #Lose
        else:
            return 0.5 # Draw
            


    def backup_value(self, node: Node, value: float):
        """
        This function is used to backup the value of a node in the tree.
        It is called after a simulation is run from the root to a leaf, and the value of the
        leaf node is known(see the 'move' function for more details on how values are
        assigned to leaf nodes). This value is propagated up the tree to the root, updating
        the "N" and "Q" values of each node along the path.
        N's are amount of visits to the node and Q's a number of accrued points.

        :param node: The leaf node that was most recently visited.
        :param value: The value of the leaf node that was most recently visited. 
        The value of a node is the value of the node's children determined by a
        win(1), draw(0.5) or loss(0)        
        """
        while node is not None:
            node.N += 1
            
            if node:# if node corresponds to a game state where the opponent is to move
                node.Q = node.Q - value
            else:
                node.Q = node.Q + value
            
            node = node.parent_node
            


    def move(
        self, state: GameState, last_move: Move, max_time_to_move: int = 1000
    ) -> Move:
        """
        This function is called by the game engine to request a move from the player.
        The game engine will call this function repeatedly until the game is over.
        
        :param state: GameState object with the current state of the game.
        :param last_move: Move object with the last move that was made.
        :param max_time_to_move: The maximum time in milliseconds that the player 
        is allowed to take to make a move.
        
        :return: Move object with the move that the player wants to make.
        """
    
        
        self.state = state
        self.our_last_played_move = None
        
        pretty_board(state[0])

        current_time = time.time_ns() # Get current time
        end_time = current_time + max_time_to_move # Time in milliseconds
        valid_move_list = GmUtils.getValidMoves(state[0], state[1])
        root_node = Node(                   
                    color=self.color, 
                    state=state, 
                    last_move=last_move, 
                    parent_node=self.previous_tree_root, 
                    valid_moves=valid_move_list
                    )

        if state[1] == 1:   # First move must be 9,9 to initialize the game.
            return (9,9)
        
        else:
            while(current_time < end_time):     # Time must not exceed time limit
                leaf_node = self.find_spot_to_expand(root_node) 
                value = self.rollout(leaf_node) 
                self.backup_value(leaf_node, value)

                current_time = time.time_ns() # Update current time
            
            self.our_last_played_move = root_node.best_move()
            self.previous_tree_root = root_node
            print(root_node.best_move())
            return root_node.best_move()
            
             
    def id(self) -> str:
        return "Champion player Matthijs Koelewijn (1716853) "
