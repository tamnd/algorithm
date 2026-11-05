# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bliss/. The authors are listed in prov/XYMF0D.jsonl.
"""A small model of bliss: individualization-refinement with certificates.

Graphs are simple and undirected, given as (n, edges) with vertices 0..n-1,
with optional integer vertex colors. The partition is kept as one array of
vertices and a list of cell starts, as in bliss. Refinement uses a splitter
queue and records a trace (the certificate of the node). The search is
iterative, cuts nodes whose certificate is worse than the best path and
differs from the first path, and cuts children by orbits of the
automorphisms found so far.

This is a teaching model of the method of Junttila and Kaski, not of the
program, which adds many data-structure and pruning techniques.
"""

Edges = list[tuple[int, int]]


class Partition:
    """Ordered partition: elems[start:end] is the cell starting at start."""

    def __init__(self, elems: list[int], starts: list[int]) -> None:
        self.elems = elems
        self.starts = starts  # sorted list of cell starts
        self.cell_of = [0] * len(elems)
        self.end: dict[int, int] = {}
        bounds = starts + [len(elems)]
        for i, s in enumerate(starts):
            self.end[s] = bounds[i + 1]
            for p in range(s, bounds[i + 1]):
                self.cell_of[elems[p]] = s

    def copy(self) -> "Partition":
        return Partition(list(self.elems), list(self.starts))

    def discrete(self) -> bool:
        return len(self.starts) == len(self.elems)


def refine(adj: list[list[int]], part: Partition, queue: list[int]) -> tuple[int, ...]:
    """Refine part in place to an equitable partition; return the trace.

    Splitters are taken in FIFO order. A cell split while it waits in the
    queue puts all pieces in the queue; otherwise all pieces except the
    first largest one. The trace lists, for each split, the start of the
    split cell and the sizes and neighbor counts of its pieces.
    Cost: O((n + m) log n) splitter work plus sorting, O(n m) here in the worst case.
    """
    trace: list[int] = []
    in_queue = set(queue)
    head = 0
    while head < len(queue):
        s = queue[head]
        head += 1
        in_queue.discard(s)
        splitter = part.elems[s:part.end[s]]
        trace.append(-1 - s)
        count: dict[int, int] = {}
        for v in splitter:
            for x in adj[v]:
                count[x] = count.get(x, 0) + 1
        touched = sorted({part.cell_of[x] for x in count})
        for c in touched:
            e = part.end[c]
            if e - c == 1:
                continue
            cell = part.elems[c:e]
            groups: dict[int, list[int]] = {}
            for v in cell:
                groups.setdefault(count.get(v, 0), []).append(v)
            if len(groups) == 1:
                continue
            keys = sorted(groups)
            pos = c
            pieces: list[tuple[int, int]] = []
            for k in keys:
                g = groups[k]
                part.elems[pos:pos + len(g)] = g
                pieces.append((pos, pos + len(g)))
                trace.extend((c, k, len(g)))
                pos += len(g)
            new_starts = [a for a, _ in pieces[1:]]
            for a, b in pieces:
                part.end[a] = b
                for p in range(a, b):
                    part.cell_of[part.elems[p]] = a
            part.starts = sorted(part.starts + new_starts)
            if c in in_queue:
                add = new_starts
            else:
                largest = max(range(len(pieces)), key=lambda i: (pieces[i][1] - pieces[i][0], -i))
                add = [a for i, (a, _) in enumerate(pieces) if i != largest]
            for a in add:
                queue.append(a)
                in_queue.add(a)
    return tuple(trace)


def individualize(part: Partition, w: int) -> int:
    """Move w to the front of its cell and split it off; return its start."""
    c = part.cell_of[w]
    e = part.end[c]
    i = part.elems.index(w, c, e)
    part.elems[c], part.elems[i] = part.elems[i], part.elems[c]
    part.end[c] = c + 1
    part.end[c + 1] = e
    for p in range(c + 1, e):
        part.cell_of[part.elems[p]] = c + 1
    part.starts = sorted(part.starts + [c + 1])
    return c


def _orbit_ids(n: int, gens: list[list[int]]) -> list[int]:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for g in gens:
        for v in range(n):
            a, b = find(v), find(g[v])
            if a != b:
                parent[a] = b
    return [find(v) for v in range(n)]


def _worse(cert: list[tuple], ref: list[tuple]) -> bool:
    """True when every sequence starting with cert is smaller than ref."""
    for a, b in zip(cert, ref):
        if a != b:
            return a < b
    return False


def canonical_form(n: int, edges: Edges, colors: list[int] | None = None
                   ) -> tuple[tuple, list[int], list[list[int]], int]:
    """Return (form, labeling, generators, |Aut|) of a vertex-colored graph.

    labeling[v] is the canonical name of v; form is the color sequence and
    the adjacency rows after relabeling, so equal forms mean isomorphic
    graphs. Cost: exponential in the worst case, one refinement per node.
    """
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    colors = colors if colors is not None else [0] * n
    if n == 0:
        return (), [], [], 1
    # @line L1
    elems = sorted(range(n), key=lambda v: colors[v])
    starts = [i for i in range(n) if i == 0 or colors[elems[i]] != colors[elems[i - 1]]]
    root = Partition(elems, starts)
    root_cert = refine(adj, root, list(starts))
    gens: list[list[int]] = []
    first: tuple[list[tuple], list[int]] | None = None
    best: tuple[list[tuple], list[int]] | None = None
    first_path: list[tuple[list[int], list[int], int]] = []
    # @line L2
    # a frame: [partition, prefix, certificate list, target cell, next index, tried]
    stack: list[list] = [[root, [], [root_cert], -1, 0, []]]
    # @line L3
    while stack:
        frame = stack[-1]
        part, prefix, cert = frame[0], frame[1], frame[2]
        # @line L4
        if (best is not None and _worse(cert, best[0])
                and cert != first[0][:len(cert)]):
            stack.pop()
            continue
        # @line L5
        if part.discrete():
            stack.pop()
            lab = [0] * n
            for i, v in enumerate(part.elems):
                lab[v] = i
            rows = tuple(sum(1 << lab[x] for x in adj[v]) for v in part.elems)
            key = cert + [tuple(colors[v] for v in part.elems) + rows]
            # @line L6
            if first is None:
                first = best = (key, lab)
                continue
            for ref in (first, best):
                # @line L7
                if key == ref[0]:
                    inv = part.elems
                    gens.append([inv[ref[1][v]] for v in range(n)])
                    break
            else:
                # @line L8
                if key > best[0]:
                    best = (key, lab)
            continue
        # @line L9
        if frame[3] < 0:
            big = max(part.starts, key=lambda s: (part.end[s] - s, -s))
            frame[3] = big
        c = frame[3]
        cell = part.elems[c:part.end[c]]
        on_first_path = first is None
        # @line L10
        fixing = [g for g in gens if all(g[p] == p for p in prefix)]
        orbit = _orbit_ids(n, fixing)
        tried = {orbit[t] for t in frame[5]}
        w = -1
        while frame[4] < len(cell):
            cand = cell[frame[4]]
            frame[4] += 1
            if orbit[cand] not in tried:
                w = cand
                break
        if w < 0:
            stack.pop()
            continue
        if on_first_path:
            first_path.append((list(prefix), cell, w))
        frame[5].append(w)
        # @line L11
        child = part.copy()
        s = individualize(child, w)
        trace = refine(adj, child, [s])
        stack.append([child, prefix + [w], cert + [trace], -1, 0, []])
    # @line L12
    order = 1
    for prefix, cell, w in first_path:
        orbit = _orbit_ids(n, [g for g in gens if all(g[p] == p for p in prefix)])
        order *= sum(1 for v in cell if orbit[v] == orbit[w])
    assert best is not None
    return best[0][-1], best[1], gens, order


def isomorphic(g: tuple[int, Edges], h: tuple[int, Edges],
               cg: list[int] | None = None, ch: list[int] | None = None) -> bool:
    """Test isomorphism of two colored graphs by comparing canonical forms."""
    if g[0] != h[0] or len(g[1]) != len(h[1]):
        return False
    return canonical_form(g[0], g[1], cg)[0] == canonical_form(h[0], h[1], ch)[0]
