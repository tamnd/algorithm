# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/numberlink-problem/. The authors are listed in prov/KZXTYY.jsonl.
"""Numberlink solver: backtracking that grows one path head at a time.

An instance is the grid size (h, w) and a list of terminal pairs
[(s1, t1), (s2, t2), ...], all cells distinct. A solution is a list of
vertex-disjoint simple paths, path i from s_i to t_i, each a list of cells
in which consecutive cells share a side. With cover=True every cell of the
grid must lie on some path (the Flow Free rule).
"""


def _neighbors(h, w, cell):
    r, c = cell
    for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
        if 0 <= nr < h and 0 <= nc < w:
            yield nr, nc


def is_solution(h, w, pairs, paths, cover=False):
    if len(paths) != len(pairs):
        return False
    used = set()
    for (s, t), path in zip(pairs, paths):
        if not path or path[0] != s or path[-1] != t:
            return False
        for a, b in zip(path, path[1:]):
            if b not in set(_neighbors(h, w, a)):
                return False
        for cell in path:
            if cell in used or not (0 <= cell[0] < h and 0 <= cell[1] < w):
                return False
            used.add(cell)
    return not cover or len(used) == h * w


def _free_component(h, w, start, free):
    seen = {start}
    stack = [start]
    while stack:
        cell = stack.pop()
        for nb in _neighbors(h, w, cell):
            if nb in free and nb not in seen:
                seen.add(nb)
                stack.append(nb)
    return seen


def _alive(h, w, pairs, paths, done, free, cover):
    """False when some open pair can no longer be joined, or a cell can no longer be covered."""
    reached = set()
    for i, (s, t) in enumerate(pairs):
        if done[i]:
            continue
        head = paths[i][-1]
        region = _free_component(h, w, head, free | {head, t})
        if t not in region:
            return False
        reached |= region
    if cover and not free <= reached:
        return False
    return True


def solve(h, w, pairs, cover=False, limit=None):
    """All solutions, each a list of paths."""
    k = len(pairs)
    terminals = {cell for pair in pairs for cell in pair}
    free = {(r, c) for r in range(h) for c in range(w)} - terminals
    paths = [[s] for s, _ in pairs]
    done = [s == t for s, t in pairs]
    out = []

    def moves(i):
        head = paths[i][-1]
        target = pairs[i][1]
        return [nb for nb in _neighbors(h, w, head) if nb in free or nb == target]

    def search():
        if all(done):
            if not cover or not free:  # @line L1
                out.append([list(p) for p in paths])
            return
        if not _alive(h, w, pairs, paths, done, free, cover):  # @line L2
            return
        open_pairs = [i for i in range(k) if not done[i]]
        i = min(open_pairs, key=lambda j: len(moves(j)))  # @line L3
        target = pairs[i][1]
        for nb in moves(i):  # @line L4
            paths[i].append(nb)  # @line L5
            if nb == target:
                done[i] = True
            else:
                free.discard(nb)
            search()  # @line L6
            if nb == target:  # @line L7
                done[i] = False
            else:
                free.add(nb)
            paths[i].pop()  # @line L8
            if limit is not None and len(out) >= limit:
                return

    search()
    return out


def brute_force(h, w, pairs, cover=False):
    """All solutions: every simple path for pair 1, then for pair 2 on the cells left, and so on."""
    out = []
    terminals = {cell for pair in pairs for cell in pair}

    def simple_paths(s, t, blocked):
        res = []
        path = [s]
        on_path = {s}

        def walk():
            cell = path[-1]
            if cell == t:
                res.append(list(path))
                return
            for nb in _neighbors(h, w, cell):
                if nb not in on_path and nb not in blocked:
                    path.append(nb)
                    on_path.add(nb)
                    walk()
                    on_path.discard(nb)
                    path.pop()

        walk()
        return res

    def place(i, used, chosen):
        if i == len(pairs):
            if is_solution(h, w, pairs, chosen, cover):
                out.append([list(p) for p in chosen])
            return
        s, t = pairs[i]
        other = terminals - {s, t}
        for p in simple_paths(s, t, used | other):
            place(i + 1, used | set(p), chosen + [p])

    place(0, set(), [])
    return out
