def get_winning_move(board, valid_moves):
    for move in valid_moves:
        y, x = move
        board[x][y] = 2  # assume opponent places a stone at the move
        if check_win(board, 2):  # check if opponent wins
            board[x][y] = 0  # undo the assumption
            return move
        board[x][y] = 0  # undo the assumption

    for move in valid_moves:
        y, x = move
        board[x][y] = 1  # assume player places a stone at the move
        if check_win(board, 1):  # check if player wins
            board[x][y] = 0  # undo the assumption
            return move
        board[x][y] = 0  # undo the assumption

    return None  # no winning move found


def get_valid_moves(board):
    valid_moves = []
    for i in range(7):
        for j in range(7):
            if board[i][j] == 0:
                valid_moves.append((i, j))
    return valid_moves


def check_win(board, player):
    board_size = len(board)

    # check rows
    for i in range(board_size):
        for j in range(3):
            if board[i][j] == player and board[i][j+1] == player and board[i][j+2] == player and board[i][j+3] == player and board[i][j+4] == player:
                return True
    # check columns
    for i in range(3):
        for j in range(board_size):
            if board[i][j] == player and board[i+1][j] == player and board[i+2][j] == player and board[i+3][j] == player and board[i+4][j] == player:
                return True
    # check diagonals
    for i in range(3):
        for j in range(3):
            if board[i][j] == player and board[i+1][j+1] == player and board[i+2][j+2] == player and board[i+3][j+3] == player and board[i+4][j+4] == player:
                return True
    for i in range(3):
        for j in range(4, board_size):
            if board[i][j] == player and board[i+1][j-1] == player and board[i+2][j-2] == player and board[i+3][j-3] == player and board[i+4][j-4] == player:
                return True
    return False


board = [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 1, 0, 0, 0],
         [1, 0, 0, 0, 0, 2, 0],
         [0, 0, 2, 2, 2, 0, 0],
         [2, 0, 2, 0, 0, 0, 2]]


valid_moves = get_valid_moves(board)

print(get_winning_move(board, valid_moves ))