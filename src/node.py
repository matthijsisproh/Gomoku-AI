import math

class Node:
    def __init__(self, color, state, last_move, parent_node=None, valid_moves=None):
        self.color = False
        self.state = state
        self.last_move = last_move
        self.parent_node = parent_node  # pointer for ease of use corresponding the previous game state
        self.valid_moves = valid_moves
        self.child_nodes = []        # Container with children nodes
        self.N = 0                      # A number of visits to the node
        self.Q = 0                      # A number of accrued points
        self.player_id = 1 if (self.state[1] % 2 == 0) else 2 

    def calculate_uct_value(self):
        """
        Runtime complexity of O(1) because only 1 operation is executed. This doesn't vary.
        :return: the uct value of a node.
        """
        return (self.Q / self.N) + (
                2 / math.sqrt(2) * math.sqrt(math.log(self.parent_node.N, 2) / self.N))
    

    def best_child(self):
        """
        Find the best child in the tree
        Runtime-complexity of O(n) because you only loop though all children once.
        :return: the child with highest value.
        """
        value = 0
        child = self.child_nodes[0]
        for chld in self.child_nodes:
            val = chld.calculate_uct_value()
            if val > value:
                value = val
                child = chld
        return child



    def best_move(self) -> tuple:
        """
        Worst-case the runtime complexity will be O(n) because we need to loop over all the children.
        So the more children a node has, the longer this function will run. Therefore a complexity of O(n)
        :return: Tuple: returns the last move of the best child
        """
        highest_value = self.child_nodes[0].Q / self.child_nodes[0].N
        best_child = self.child_nodes[0]
        for child in self.child_nodes:
            if child.Q / child.N > highest_value:
                highestVal = child.Q / child.N
                best_child = child
        return best_child.last_move
    
