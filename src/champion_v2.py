import gomoku
from gomoku import Board, Move, GameState, check_win, valid_moves

import random
import copy
import math
import time

class Node():
    def __init__(self, state, parent_node = None, last_move = None, valid_moves = None):
        self.state = state
        self.last_move = last_move 
        self.parent_node = parent_node       # Pointer for previous state     
        self.valid_moves = valid_moves
        self.child_nodes = []           # Container with children nodes
        self.N = 0                      # A number of accrued points
        self.Q = 0                      # A number of accrued points

        self.player_id = 1 if (self.state[1] % 2 == 0) else 2 

    def calculate_uct_value(self):
        """
        Calculates the UCT value for a node.

        :param self: The node to calculate the UCT value for.
        :return: The UCT value for the node.
        
        Runtime complexity: O(1), Only 1 operation is executed.
        """
        value = self.Q / self.N
        c = math.sqrt(2)
        parent_visited = math.sqrt((math.log(self.parent_node.N)) / self.N)
        result = value + c * parent_visited
        return result

    def best_child(self):
        """
        This function returns the best child node of the current node.
        The best child node is the one with the highest UCT value.
        
        :return: The child with highest UCT value.

        Runtime complexity: O(n), Only loop through all children
        """
        value = -math.inf
        child = None
        for chld in self.child_nodes:
            if chld.calculate_uct_value() > value:
                value = chld.calculate_uct_value()
                child = chld
        return child

    def best_move(self):
        """
        This function returns the best move for the current player.
        The best move is the move that has the highest Q/N value.

        :return: Tuple with the best move for the current player.
        
        Runtime complexity: O(n), Only loop through all children
        """
        highest_value = -math.inf
        best_child = None
        for child in self.child_nodes:
            child_value = child.Q / child.N
            if child_value > highest_value:
                highest_value = child_value
                best_child = child.last_move
        return best_child

class ChampionV2:
    """This class specifies a player that just does random moves.
    The use of this class is two-fold: 1) You can use it as a base random roll-out policy.
    2) it specifies the required methods that will be used by the competition to run
    your player
    """

    def __init__(self, black_: bool = True):
        """Constructor for the player."""
        self.black = black_


    def new_game(self, black_: bool):
        """At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.
        """
        self.black = black_
          

    def game_result(self, num_turns: int, is_black: bool) -> int:
        """ This function returns the result of the game.

        :param num_turns: The number of turns played.
        :parm is_black: Whether the player is black (True) or white (False).

        :return: The result of the game. Returns 1 if the player with the specified color is the winner,
        -1 if they are the loser.

        Runtime complexity: O(1), no loops or iterations in this function
        """
        if is_black:
            if num_turns % 2 == 0: 
                return 1
            else:
                return -1
        else:
            if num_turns % 2 == 1:
                return 1
            else:
                return -1

   
    def find_spot_to_expand(self, node: Node) -> Node:
        """
        This function is used to find the next node to expand.
        It is called recurisvely until a node is found that has not been expanded.
        
        The node is found by traversing the tree from the root node to the best child node.
        The best child node is the node with the highest UCT value.
                
        :param node: The node tree with all the game information stored in it.
        
        :return node: A node that is to be expanded.

        Runtime complexity: O(n) Its recursive, and calls multiple functions
        """

        if check_win(node.state[0], node.last_move) or len(node.valid_moves) == 0: # Return node if game is finished
            return node

        valid_moves = copy.deepcopy(node.valid_moves)
        copied_state = copy.deepcopy(node.state)

        if len(node.child_nodes) != len(valid_moves):
            new_move = random.choice(valid_moves)
            move_is_valid, winning_move, new_state = gomoku.move(copied_state, new_move)
            valid_moves.remove(new_move)
            child_node = Node(new_state, node, new_move, valid_moves)
            node.child_nodes.append(child_node)
            return child_node

        return self.find_spot_to_expand(node.best_child())

    def rollout(self, node: Node) -> int:
        """
        This function is used to simulate a random game from the current state of the game.
        It is used to estimate the value of a node.
        
        :param node: The leaf node that was most recently visited.
        
        :return value: It returns 1 if the current player wins, 0 if the current player loses, and 0.5 if the game is a draw.

        Runtime complexity: O(n), this function rolls out random moves untill the game is won or there are no moves left
        """
        
        if check_win(node.state[0], node.last_move):
            return self.game_result(node.state[1], self.black)
        
        if(node.parent_node is not None):
            valid_moves = copy.deepcopy(node.valid_moves)
            copied_state = copy.deepcopy(node.state)
            random.shuffle(valid_moves)
            
            while len(valid_moves) > 0:
                random_move = valid_moves.pop()
                move_is_valid, winning_move, copied_state = gomoku.move(copied_state, random_move)

                if winning_move:
                    return self.game_result(copied_state[1], self.black)                
        return 0


    def backup_value(self, value: float, node: Node) -> None:
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

        Runtime complexity: O(n), loops over all nodes
        """
        while node is not None:
            node.N += 1
            if (node.player_id != self.black):
                node.Q = node.Q - value

            else:
                node.Q = node.Q + value

            node = node.parent_node

    def move(
        self, 
        state: GameState, 
        last_move: Move, 
        max_time_to_move: int = 1000
        ) -> Move:
        """
        This function is called by the game engine to request a move from the player.
        The game engine will call this function repeatedly until the game is over.
        
        :param state: GameState object with the current state of the game.
        :param last_move: Move object with the last move that was made.
        :param max_time_to_move: The maximum time in milliseconds that the player 
        is allowed to take to make a move.
        
        :return: Move object with the move that the player wants to make.

        Runtime complexity: O(n), loops untill there is no more time left.
        """
        
        start_time = time.time_ns()
        valid_move_list = copy.deepcopy(valid_moves(state))
        root_node = Node(copy.deepcopy(state), None, last_move, valid_move_list)

        while (((time.time_ns() - start_time) / 1000000) < max_time_to_move):
            leaf_node = self.find_spot_to_expand(root_node)
            for i in range(10):
                value = self.rollout(leaf_node)
                self.backup_value(value, leaf_node)

        return root_node.best_move()

    def id(self) -> str:
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "Champion player V2 Matthijs Koelewijn (1716853)"