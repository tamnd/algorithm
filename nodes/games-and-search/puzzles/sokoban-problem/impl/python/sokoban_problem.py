# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sokoban-problem/. The authors are listed in prov/N70HNE.jsonl.
"""Sokoban: push every box onto a goal square.

Levels use the usual text format: '#' wall, ' ' floor, '.' goal, '$' box,
'*' box on a goal, '@' player, '+' player on a goal. Solutions use LURD
letters: lowercase for a walk, uppercase for a push.

A state is (player, boxes) with cells numbered r * width + c.
"""

from collections import deque

DIRS = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}


def parse(text):
    rows = text.strip('\n').split('\n')
    # one extra column of wall on the right, so a step never wraps to another row
    width = max(len(r) for r in rows) + 1
    walls, goals, boxes = set(), set(), set()
    player = None
    for r in range(-1, len(rows) + 1):
        for c in range(width):
            row = rows[r] if 0 <= r < len(rows) else ''
            ch = row[c] if c < len(row) else '#'
            cell = r * width + c
            if ch == '#':
                walls.add(cell)
            if ch in '.*+':
                goals.add(cell)
            if ch in '$*':
                boxes.add(cell)
            if ch in '@+':
                player = cell
    steps = {k: dr * width + dc for k, (dr, dc) in DIRS.items()}
    return {'walls': frozenset(walls), 'goals': frozenset(goals), 'steps': steps,
            'start': (player, frozenset(boxes)), 'width': width}


def successors(level, state):
    """Yield (letter, next_state) for every legal single move."""
    walls, steps = level['walls'], level['steps']
    player, boxes = state
    for k, d in steps.items():
        nxt = player + d
        if nxt in walls:
            continue
        if nxt in boxes:
            beyond = nxt + d
            if beyond in walls or beyond in boxes:
                continue
            yield k.upper(), (nxt, boxes - {nxt} | {beyond})
        else:
            yield k, (nxt, boxes)


def solved(level, state):
    return state[1] == level['goals']


def bfs_moves(level):
    """Breadth-first search over (player, boxes): a solution with the fewest moves."""
    start = level['start']
    parent = {start: None}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        if solved(level, state):
            return _path(parent, state)
        for letter, nxt in successors(level, state):
            if nxt not in parent:
                parent[nxt] = (state, letter)
                queue.append(nxt)
    return None


def _path(parent, state):
    out = []
    while parent[state] is not None:
        state, letter = parent[state]
        out.append(letter)
    return ''.join(reversed(out))


def reachable(level, player, boxes):
    """Cells the player can walk to without pushing."""
    walls, steps = level['walls'], level['steps']
    seen = {player}
    stack = [player]
    while stack:
        p = stack.pop()
        for d in steps.values():
            q = p + d
            if q not in seen and q not in walls and q not in boxes:
                seen.add(q)
                stack.append(q)
    return seen


def bfs_pushes(level):
    """Breadth-first search over pushes: the fewest pushes, walks are free.

    A node is (boxes, the least cell the player can reach); one edge is one push.
    """
    walls, steps = level['walls'], level['steps']
    player, boxes = level['start']
    area = reachable(level, player, boxes)
    start = (boxes, min(area))
    dist = {start: 0}
    queue = deque([(start, area)])
    while queue:
        (boxes, _), area = queue.popleft()
        if boxes == level['goals']:
            return dist[(boxes, min(area))]
        for box in boxes:
            for d in steps.values():
                stand, beyond = box - d, box + d
                if stand not in area or beyond in walls or beyond in boxes:
                    continue
                nb = boxes - {box} | {beyond}
                na = reachable(level, box, nb)
                key = (nb, min(na))
                if key not in dist:
                    dist[key] = dist[(boxes, min(area))] + 1
                    queue.append((key, na))
    return None


def zero_one_pushes(level):
    """Independent check: 0-1 BFS over (player, boxes) with walks costing 0 and pushes 1."""
    start = level['start']
    dist = {start: 0}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        d = dist[state]
        if solved(level, state):
            return d
        for letter, nxt in successors(level, state):
            w = 1 if letter.isupper() else 0
            if nxt not in dist or d + w < dist[nxt]:
                dist[nxt] = d + w
                if w:
                    queue.append(nxt)
                else:
                    queue.appendleft(nxt)
    return None


def iddfs_moves(level, limit=40):
    """Independent check: iterative deepening depth-first search for the fewest moves."""
    start = level['start']
    for depth in range(limit + 1):
        best = {}

        def dfs(state, left):
            if solved(level, state):
                return ''
            if left == 0 or best.get(state, -1) >= left:
                return None
            best[state] = left
            for letter, nxt in successors(level, state):
                tail = dfs(nxt, left - 1)
                if tail is not None:
                    return letter + tail
            return None

        found = dfs(start, depth)
        if found is not None:
            return found
    return None


def replay(level, solution):
    """Play a LURD string; return the final state, or None at an illegal move."""
    state = level['start']
    for letter in solution:
        options = dict(successors(level, state))
        if letter not in options:
            return None
        state = options[letter]
    return state
