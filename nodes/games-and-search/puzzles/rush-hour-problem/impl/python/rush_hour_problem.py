# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rush-hour-problem/. The authors are listed in prov/72JECE.jsonl.
"""Rush Hour: slide cars on a grid until the target car reaches the exit.

A board is a list of equal strings, '.' for empty and a letter for each car.
Car 'A' is the target; it is horizontal and the exit is at the right end of
its row. A car moves only along its own direction.

A state is a tuple with one number per car: the first column of a horizontal
car, or the first row of a vertical one. Two costs: a *move* slides one car
any distance; a *step* slides one car by one square.
"""

import heapq
from collections import deque


def parse(rows):
    h, w = len(rows), len(rows[0])
    cells = {}
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != '.':
                cells.setdefault(ch, []).append((r, c))
    names = sorted(cells)
    cars, start = [], []
    for name in names:
        cs = sorted(cells[name])
        horizontal = cs[0][0] == cs[-1][0]
        if horizontal:
            cars.append((name, True, cs[0][0], len(cs)))
            start.append(cs[0][1])
        else:
            cars.append((name, False, cs[0][1], len(cs)))
            start.append(cs[0][0])
    return {'h': h, 'w': w, 'cars': cars, 'start': tuple(start), 'target': names.index('A')}


def occupied(board, state):
    grid = [[False] * board['w'] for _ in range(board['h'])]
    for (name, horizontal, line, length), pos in zip(board['cars'], state):
        for i in range(length):
            if horizontal:
                grid[line][pos + i] = True
            else:
                grid[pos + i][line] = True
    return grid


def slides(board, state):
    """Yield (car index, distance, next state) for every slide by a nonzero distance."""
    grid = occupied(board, state)
    for k, ((name, horizontal, line, length), pos) in enumerate(zip(board['cars'], state)):
        size = board['w'] if horizontal else board['h']

        def free(x):
            return not (grid[line][x] if horizontal else grid[x][line])

        x = pos - 1
        while x >= 0 and free(x):
            yield k, x - pos, state[:k] + (x,) + state[k + 1:]
            x -= 1
        x = pos + length
        while x < size and free(x):
            yield k, x - pos - length + 1, state[:k] + (x - length + 1,) + state[k + 1:]
            x += 1


def solved(board, state):
    name, horizontal, line, length = board['cars'][board['target']]
    return state[board['target']] + length == board['w']


def bfs(board, unit_steps=False):
    """Breadth-first search: the least number of moves (or of steps), with one solution."""
    start = board['start']
    parent = {start: None}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        if solved(board, state):
            path = []
            while parent[state] is not None:
                state, move = parent[state]
                path.append(move)
            return len(path), path[::-1]
        for k, d, nxt in slides(board, state):
            if unit_steps and abs(d) != 1:
                continue
            if nxt not in parent:
                parent[nxt] = (state, (board['cars'][k][0], d))
                queue.append(nxt)
    return None


def iddfs_moves(board, limit=30):
    """Independent check: iterative deepening depth-first search on moves."""
    start = board['start']
    for depth in range(limit + 1):
        best = {}

        def dfs(state, left):
            if solved(board, state):
                return True
            if left == 0 or best.get(state, -1) >= left:
                return False
            best[state] = left
            return any(dfs(nxt, left - 1) for _, _, nxt in slides(board, state))

        if dfs(start, depth):
            return depth
    return None


def dijkstra_steps(board):
    """Independent check: Dijkstra on the move graph, where a slide costs its distance."""
    start = board['start']
    dist = {start: 0}
    heap = [(0, start)]
    while heap:
        d, state = heapq.heappop(heap)
        if d > dist[state]:
            continue
        if solved(board, state):
            return d
        for _, delta, nxt in slides(board, state):
            nd = d + abs(delta)
            if nd < dist.get(nxt, nd + 1):
                dist[nxt] = nd
                heapq.heappush(heap, (nd, nxt))
    return None


def component_size(board):
    """Number of states reachable from the start; moves can be undone, so this is a component."""
    seen = {board['start']}
    stack = [board['start']]
    while stack:
        state = stack.pop()
        for _, _, nxt in slides(board, state):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return len(seen)


def replay(board, moves):
    """Apply (car, distance) moves; return the final state or None at an illegal move."""
    state = board['start']
    names = [car[0] for car in board['cars']]
    for name, d in moves:
        options = {(names[k], delta): nxt for k, delta, nxt in slides(board, state)}
        if (name, d) not in options:
            return None
        state = options[(name, d)]
    return state
