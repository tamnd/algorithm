# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slitherlink-problem/. The authors are listed in prov/0NPZ8T.jsonl.
"""Slitherlink solver: backtracking over edges with local propagation.

The board has h by w cells. clues[r][c] is 0, 1, 2, 3 or None. The lattice
has (h + 1) by (w + 1) points, and an edge joins two points at distance 1.
A solution is a set of edges that forms one simple closed loop, such that
each clued cell has exactly its clue of edges on its four sides.
"""


def edges_of(h, w):
    """All edges as pairs of lattice points, in a fixed order."""
    out = []
    for r in range(h + 1):
        for c in range(w):
            out.append(((r, c), (r, c + 1)))
    for r in range(h):
        for c in range(w + 1):
            out.append(((r, c), (r + 1, c)))
    return out


def cell_edges(r, c):
    return [((r, c), (r, c + 1)), ((r + 1, c), (r + 1, c + 1)),
            ((r, c), (r + 1, c)), ((r, c + 1), (r + 1, c + 1))]


def is_single_loop(edge_set):
    """True when the edges form exactly one simple cycle."""
    if not edge_set:
        return False
    deg = {}
    adj = {}
    for a, b in edge_set:
        deg[a] = deg.get(a, 0) + 1
        deg[b] = deg.get(b, 0) + 1
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    if any(d != 2 for d in deg.values()):
        return False
    start = next(iter(adj))
    seen = {start}
    stack = [start]
    while stack:
        p = stack.pop()
        for q in adj[p]:
            if q not in seen:
                seen.add(q)
                stack.append(q)
    return len(seen) == len(adj)


def is_solution(clues, edge_set):
    h, w = len(clues), len(clues[0])
    for r in range(h):
        for c in range(w):
            k = clues[r][c]
            if k is not None and sum(e in edge_set for e in cell_edges(r, c)) != k:
                return False
    return is_single_loop(edge_set)


class _Board:
    def __init__(self, clues):
        self.clues = clues
        self.h, self.w = len(clues), len(clues[0])
        self.edges = edges_of(self.h, self.w)
        self.index = {e: i for i, e in enumerate(self.edges)}
        # Constraints as (edge indices, allowed counts).
        self.groups = []
        points = {}
        for i, (a, b) in enumerate(self.edges):
            points.setdefault(a, []).append(i)
            points.setdefault(b, []).append(i)
        for ids in points.values():
            self.groups.append((ids, (0, 2)))
        for r in range(self.h):
            for c in range(self.w):
                if clues[r][c] is not None:
                    self.groups.append(([self.index[e] for e in cell_edges(r, c)], (clues[r][c],)))
        self.groups_of = [[] for _ in self.edges]
        for g, (ids, _) in enumerate(self.groups):
            for i in ids:
                self.groups_of[i].append(g)

    def propagate(self, x, queue):
        """Unit rules on points and cells. x[i] is 1, 0 or -1. False on a conflict."""
        while queue:
            g = queue.pop()
            ids, allowed = self.groups[g]
            on = sum(1 for i in ids if x[i] == 1)
            free = [i for i in ids if x[i] == -1]
            fits = [k for k in allowed if on <= k <= on + len(free)]
            if not fits:
                return False
            if not free:
                continue
            value = None
            if fits == [on]:
                value = 0
            elif fits == [on + len(free)]:
                value = 1
            if value is not None:
                for i in free:
                    x[i] = value
                    queue.extend(self.groups_of[i])
        return True

    def no_early_loop(self, x):
        """A closed loop of fixed edges must be the whole answer."""
        adj = {}
        for i, v in enumerate(x):
            if v == 1:
                a, b = self.edges[i]
                adj.setdefault(a, []).append(b)
                adj.setdefault(b, []).append(a)
        seen = set()
        comps = 0
        closed = False
        for start in adj:
            if start in seen:
                continue
            comps += 1
            seen.add(start)
            stack = [start]
            comp_closed = True
            while stack:
                p = stack.pop()
                if len(adj[p]) != 2:
                    comp_closed = False
                for q in adj[p]:
                    if q not in seen:
                        seen.add(q)
                        stack.append(q)
            closed = closed or comp_closed
        return not (closed and comps > 1)


def solve(clues, limit=None):
    """All solutions as sets of edges."""
    board = _Board(clues)
    m = len(board.edges)
    out = []
    first = [-1] * m
    if not board.propagate(first, list(range(len(board.groups)))):  # @line L1
        return out
    stack = [first]
    while stack:  # @line L2
        x = stack.pop()
        if not board.no_early_loop(x):  # @line L3
            continue
        free = [i for i in range(m) if x[i] == -1]
        if not free:
            chosen = {board.edges[i] for i in range(m) if x[i] == 1}
            if is_solution(clues, chosen):  # @line L4
                out.append(chosen)
                if limit is not None and len(out) >= limit:
                    break
            continue
        i = free[0]  # @line L5
        for v in (0, 1):
            child = list(x)
            child[i] = v  # @line L6
            if board.propagate(child, list(board.groups_of[i])):  # @line L7
                stack.append(child)  # @line L8
    return out


def all_loops(h, w):
    """Every simple loop of the board, as the boundary of a set of cells.

    A simple loop in the plane bounds one region, so each loop is the boundary
    of exactly one set of cells, the cells inside it.
    """
    loops = []
    for mask in range(1, 1 << (h * w)):
        inside = {(r, c) for r in range(h) for c in range(w) if mask >> (r * w + c) & 1}
        boundary = set()
        for r, c in inside:
            for (dr, dc), e in zip(((-1, 0), (1, 0), (0, -1), (0, 1)), cell_edges(r, c)):
                if (r + dr, c + dc) not in inside:
                    boundary.add(e)
        if is_single_loop(boundary):
            loops.append(boundary)
    return loops
