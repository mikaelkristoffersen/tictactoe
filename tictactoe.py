"""
Tic Tac Toe Player
"""
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


positions = [(i, j) for i in range(0, 3) for j in range(0, 3)]


def flatten(board):
    return [field for row in board for field in row]


fieldState = {
    X: 1,
    O: -1,
    None: 0
}


def boardState(board):
    return [fieldState[field] for field in flatten(board)]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count EMPTY fieds on the board
    if sum(boardState(board)) == 0:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    l = []
    i = 0
    bs = boardState(board)
    # we can optimize initial action to: [(1,1), (0,1), (0,0)]
    # since this represtents all possible startes with a transpose of the board
    if(all(b == 0 for b in bs)):
        return [(1,1),(0,1),(0,0)]
    for b in bs:
        if b == 0:
            l.append(positions[i])
        i = i + 1
    return l


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newBoard = copy.deepcopy(board)

    if action in actions(newBoard):
        newBoard[action[0]][action[1]] = player(newBoard)
        return newBoard
    print(action)
    print(board)
    raise Exception("Action not valid.")


def square_combis(lst, n):
    for i in range(0, len(lst), n):
        yield sum(lst[i:i + n])
    for i in range(0, n):
        yield sum(lst[i::n])
    yield sum(lst[0::n+1])
    yield sum(lst[n-1:1-n:n-1])


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for s in square_combis(boardState(board), 3):
        if(s == 3):
            return X
        if(s == -3):
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) != None or not actions(board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return fieldState[winner(board)]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    a = None
    if terminal(board):
        return a

    maximize = player(board) == X
    sign = -1 if maximize else 1
    prev_value = 2*sign

    for action in actions(board):
        # The maximizing player picks action a in Actions(s) that
        # produces the highest value of Min-Value(Result(s, a)).
        # The minimizing player picks action a in Actions(s) that
        # produces the lowest value of Max-Value(Result(s, a)).
        newValue = minmaxvalue(result(board, action), maximize, prev_value)
        if prev_value*sign >= newValue*sign:
            a = action
            prev_value = newValue
    return a


def minmaxvalue(board, minValue, prev_val=0):
    if terminal(board):
        return utility(board)
    v = 2 if minValue else -2
    for action in actions(board):
        # if min-value call: min(v,max-value)
        r = minmaxvalue(result(board, action), not minValue, v)
        v = min(v, r) if minValue else max(v, r)
        # Alpha-Beta Pruning skips some of the recursive computations that are decidedly unfavorable. 
        if(minValue and v < prev_val) or (not minValue and v > prev_val):
            break
    return v
