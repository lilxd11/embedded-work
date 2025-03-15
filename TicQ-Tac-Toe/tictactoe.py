import time
import copy

X = "X"
O = "O"
EMPTY = None
time_num = []

def initial_state():
    time_num.clear()
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    x_num = 0
    o_num = 0
    for i in board:
        for j in i:
            if j == "X":
                x_num += 1
            elif j == "O":
                o_num += 1
    if x_num == 0 and o_num == 0:
        return X
    elif x_num > o_num:
        return O
    elif x_num == o_num:
        return X


def vacancy(board):
    vacancy_list = []
    for a in range(3):
        for b in range(3):
            if board[a][b] == EMPTY:
                vacancy_list.append((a, b))
    return vacancy_list


def action(board, move):
    board_copy = copy.deepcopy(board)
    add = player(board_copy)
    board_copy[move[0]][move[1]] = add
    return board_copy


def judgment(board):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    for condition in win_conditions:
        if condition[0] == condition[1] == condition[2] != None:
            return condition[0]
    return None


def terminal(board):
    if judgment(board) is not None:
        return True
    else:
        for i in board:
            for j in i:
                if j == EMPTY:
                    return False

        return True


def utility(board):
    if terminal(board) is True:
        a = judgment(board)
        if a == X:
            return 1
        elif a == O:
            return -1
        else:
            return 0

def move_minimax(board):
    start_time = time.time()
    a = vacancy(board)
    vmax = float('-inf')
    vmin = float('inf')
    judge_for_player = player(board)
    if judge_for_player is X:
        for pos1 in a:
            v1_every = minimaxSearch(action(board, pos1), O)
            if vmax <= v1_every:
                vmax = v1_every
                position = pos1
    else:
        for pos2 in a:
            v2_every = minimaxSearch(action(board, pos2), X)
            if vmin>= v2_every:
                vmin= v2_every
                position = pos2
    end_time = time.time()
    tmp_time = end_time - start_time
    time_num.append(tmp_time)
    total_time = sum(time_num)
    print(f"Move {judge_for_player} took {tmp_time:.4f} seconds")
    print(f"Total time: {total_time:.4f} seconds")
    return position


def minimaxSearch(board, player):
    if terminal(board):
        return utility(board)
    if player is X:
        vmax = float('-inf')
        for pos1 in vacancy(board):
            v1_every = minimaxSearch(action(board, pos1), O)
            if vmax <= v1_every:
                vmax = copy.deepcopy(v1_every)
        return vmax
    else:
        vmin = float('inf')
        for pos2 in vacancy(board):
            v2_every = minimaxSearch(action(board, pos2), X)
            if vmin >= v2_every:
                vmin = copy.deepcopy(v2_every)
        return vmin



def move_alphabeta(board):
    start_time = time.time()
    a = vacancy(board)
    va = float('-inf')
    vb = float('inf')
    judge_for_player = player(board)
    if judge_for_player is X:
        for pos1 in a:
            v1_every = alphabetaSearch(action(board, pos1), O,va, vb)
            if va <= v1_every:
                va = v1_every
                position = pos1
    else:
        for pos2 in a:
            v2_every = alphabetaSearch(action(board, pos2), X,va, vb)
            if vb >= v2_every:
                vb = v2_every
                position = pos2
    end_time = time.time()
    tmp_time = end_time - start_time
    time_num.append(tmp_time)
    total_time = sum(time_num)
    print(f"Move {judge_for_player} took {tmp_time:.4f} seconds")
    print(f"Total time: {total_time:.4f} seconds")
    return position


def alphabetaSearch(board,player,alpha,beta):
    if terminal(board):
        return utility(board)
    if player is X:
        v2 = float('-inf')
        for i2 in vacancy(board):
            v2 = max(v2, alphabetaSearch(action(board, i2), O,alpha, beta))
            if v2 >= beta:
                return v2
            alpha = max(alpha, v2)
        return v2
    else:
        v3 = float('inf')
        for i3 in vacancy(board):
            v3 = min(v3, alphabetaSearch(action(board, i3), X, alpha, beta))
            if v3 <= alpha:
                return v3
            beta = min(beta, v3)
        return v3