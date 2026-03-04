from collections import deque
import copy
import time

def display(board):
    for r in board:
        print(r)
    print()

def check_win(state, symbol):
    for r in state:
        if r[0] == r[1] == r[2] == symbol:
            return True

    for c in range(3):
        if state[0][c] == state[1][c] == state[2][c] == symbol:
            return True

    if state[0][0] == state[1][1] == state[2][2] == symbol:
        return True

    if state[0][2] == state[1][1] == state[2][0] == symbol:
        return True

    return False

def board_full(state):
    for r in state:
        if ' ' in r:
            return False
    return True

def generate_moves(state, symbol):
    next_states = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == ' ':
                temp = copy.deepcopy(state)
                temp[i][j] = symbol
                next_states.append(temp)
    return next_states

def bfs_search(start):
    q = deque()
    q.append((start, 'X'))
    seen = set()
    count = 0

    while q:
        current, turn = q.popleft()
        count += 1

        state_key = tuple(tuple(row) for row in current)
        if state_key in seen:
            continue
        seen.add(state_key)

        if check_win(current, 'X'):
            return current, count

        if board_full(current):
            continue

        next_turn = 'O' if turn == 'X' else 'X'

        for move in generate_moves(current, turn):
            q.append((move, next_turn))

    return None, count

def dfs_search(start):
    stack = []
    stack.append((start, 'X'))
    seen = set()
    count = 0

    while stack:
        current, turn = stack.pop()
        count += 1

        state_key = tuple(tuple(row) for row in current)
        if state_key in seen:
            continue
        seen.add(state_key)

        if check_win(current, 'X'):
            return current, count

        if board_full(current):
            continue

        next_turn = 'O' if turn == 'X' else 'X'

        for move in generate_moves(current, turn):
            stack.append((move, next_turn))

    return None, count

if __name__ == "__main__":

    empty_board = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]

    print("BFS Execution")
    t1 = time.time()
    bfs_result, bfs_nodes = bfs_search(empty_board)
    t2 = time.time()

    print("Nodes Expanded (BFS):", bfs_nodes)
    print("Time Taken (BFS):", t2 - t1)

    if bfs_result:
        print("Winning State Found by BFS:")
        display(bfs_result)

    print("DFS Execution")
    t3 = time.time()
    dfs_result, dfs_nodes = dfs_search(empty_board)
    t4 = time.time()

    print("Nodes Expanded (DFS):", dfs_nodes)
    print("Time Taken (DFS):", t4 - t3)

    if dfs_result:
        print("Winning State Found by DFS:")
        display(dfs_result)
