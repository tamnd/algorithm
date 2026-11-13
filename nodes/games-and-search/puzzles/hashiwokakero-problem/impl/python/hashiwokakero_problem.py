# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hashiwokakero-problem/. The authors are listed in prov/BYSQMT.jsonl.
"""Hashiwokakero solver: backtracking over bridge slots with propagation.

An instance is a dict from island positions (r, c) to their numbers. Bridges
run straight along a row or a column between two islands with no island in
between, at most two on one slot, and no two bridges cross. A solution gives
each slot 0, 1 or 2 bridges so that each island has as many bridges as its
number and the islands with their bridges form a connected graph.
"""


def slots(islands):
    """The pairs of islands that see each other along a row or a column."""
    out = []
    pos = sorted(islands)
    for a in pos:
        r, c = a
        right = [b for b in pos if b[0] == r and b[1] > c]
        down = [b for b in pos if b[1] == c and b[0] > r]
        if right:
            out.append((a, min(right, key=lambda b: b[1])))
        if down:
            out.append((a, min(down, key=lambda b: b[0])))
    return out


def crossings(slot_list):
    """Pairs of slot indices whose segments cross."""
    out = []
    for i, (a, b) in enumerate(slot_list):
        if a[0] != b[0]:
            continue
        r, c0, c1 = a[0], a[1], b[1]
        for j, (p, q) in enumerate(slot_list):
            if p[1] != q[1]:
                continue
            c, r0, r1 = p[1], p[0], q[0]
            if c0 < c < c1 and r0 < r < r1:
                out.append((i, j))
    return out


def connected(islands, slot_list, counts):
    nodes = list(islands)
    if not nodes:
        return True
    adj = {v: [] for v in nodes}
    for (a, b), k in zip(slot_list, counts):
        if k:
            adj[a].append(b)
            adj[b].append(a)
    seen = {nodes[0]}
    stack = [nodes[0]]
    while stack:
        v = stack.pop()
        for u in adj[v]:
            if u not in seen:
                seen.add(u)
                stack.append(u)
    return len(seen) == len(nodes)


def is_solution(islands, slot_list, counts):
    deg = {v: 0 for v in islands}
    for (a, b), k in zip(slot_list, counts):
        if k not in (0, 1, 2):
            return False
        deg[a] += k
        deg[b] += k
    if any(deg[v] != islands[v] for v in islands):
        return False
    for i, j in crossings(slot_list):
        if counts[i] and counts[j]:
            return False
    return connected(islands, slot_list, counts)


def brute_force(islands):
    """All solutions by trying all 3^m slot counts."""
    sl = slots(islands)
    m = len(sl)
    out = []
    for code in range(3 ** m):
        counts = []
        for _ in range(m):
            counts.append(code % 3)
            code //= 3
        if is_solution(islands, sl, counts):
            out.append(counts)
    return out


def solve(islands, limit=None):
    """All solutions as lists of slot counts, in the order of slots(islands)."""
    sl = slots(islands)
    m = len(sl)
    cross = [[] for _ in range(m)]
    for i, j in crossings(sl):
        cross[i].append(j)
        cross[j].append(i)
    at = {v: [] for v in islands}
    for i, (a, b) in enumerate(sl):
        at[a].append(i)
        at[b].append(i)

    def propagate(x, queue):
        # x[i] is a set of possible counts for slot i.
        while queue:
            v = queue.pop()
            ids = at[v]
            need = islands[v]
            low = sum(min(x[i]) for i in ids)
            high = sum(max(x[i]) for i in ids)
            if not low <= need <= high:
                return False
            for i in ids:
                others_low = low - min(x[i])
                others_high = high - max(x[i])
                keep = {k for k in x[i] if others_low + k <= need <= others_high + k}
                if not keep:
                    return False
                if keep != x[i]:
                    x[i] = keep
                    queue.extend(sl[i])
                    if 0 not in keep:
                        for j in cross[i]:
                            if 0 not in x[j]:
                                return False
                            if x[j] != {0}:
                                x[j] = {0}
                                queue.extend(sl[j])
        return True

    def may_connect(x):
        return connected(islands, sl, [max(s) for s in x])

    out = []
    start = [{0, 1, 2} for _ in range(m)]
    if not propagate(start, list(islands)):  # @line L1
        return out
    stack = [start]
    while stack:  # @line L2
        x = stack.pop()
        if not may_connect(x):  # @line L3
            continue
        open_slots = [i for i in range(m) if len(x[i]) > 1]
        if not open_slots:
            counts = [min(s) for s in x]
            if is_solution(islands, sl, counts):  # @line L4
                out.append(counts)
                if limit is not None and len(out) >= limit:
                    break
            continue
        i = min(open_slots, key=lambda k: len(x[k]))  # @line L5
        for k in sorted(x[i], reverse=True):
            y = [set(s) for s in x]
            y[i] = {k}  # @line L6
            if k:
                for j in cross[i]:
                    y[j] = y[j] & {0}
            if all(y) and propagate(y, list(sl[i]) + [v for j in cross[i] for v in sl[j]]):  # @line L7
                stack.append(y)  # @line L8
    return out
