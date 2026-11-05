# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/breaking-sorting-barrier-sssp/. The authors are listed in prov/WVPFW7.jsonl.

import heapq
import math

INF = math.inf
TOP = (INF, INF, INF, INF)  # a bound above every finite label


class _Frontier:
    """The structure D: keys with values; Insert keeps the smaller value, Pull removes
    up to M keys of smallest value and returns a bound separating them from the rest.

    This version uses a binary heap with lazy deletion. It has the same behaviour as
    the block-based structure of Duan et al., but not its amortized time bounds.
    """

    def __init__(self, m: int, bound):
        self.m = m
        self.bound = bound
        self.val: dict[int, tuple] = {}
        self.heap: list = []

    def insert(self, key: int, value) -> None:
        if key not in self.val or value < self.val[key]:
            self.val[key] = value
            heapq.heappush(self.heap, (value, key))

    def batch_prepend(self, pairs) -> None:
        for key, value in pairs:  # all values are below every value already present
            self.insert(key, value)

    def _clean(self) -> None:
        while self.heap and self.val.get(self.heap[0][1]) != self.heap[0][0]:
            heapq.heappop(self.heap)

    def pull(self):
        out = []
        self._clean()
        while self.heap and len(out) < self.m:
            _, key = heapq.heappop(self.heap)
            del self.val[key]
            out.append(key)
            self._clean()
        sep = self.heap[0][0] if self.heap else self.bound
        return sep, out

    def __bool__(self) -> bool:
        return bool(self.val)


def bmssp_sssp(
    adj: list[list[tuple[int, float]]],
    s: int,
    k: int | None = None,
    t: int | None = None,
    trace: list | None = None,
) -> tuple[list, list]:
    """Single-source shortest paths by the bounded multi-source recursion of Duan et al.

    The graph has the vertices 0 .. n-1; adj[u] lists the edges (v, w) out of u, and
    every w must be a real number >= 0 (ValueError otherwise). Returns (d, parent):
    d[v] is the distance from s (math.inf if unreachable), parent[v] the previous
    vertex on a shortest path (None for s and unreachable vertices). k and t are the
    parameters of the paper, floor(log^(1/3) n) and floor(log^(2/3) n) by default.
    If trace is a list, each call appends (level, bound length, frontier, pivots,
    returned bound length, completed set) when it returns.
    """
    n = len(adj)
    for u in range(n):
        for _, w in adj[u]:
            if not w >= 0:  # also rejects NaN
                raise ValueError("weights must be nonnegative")
    lg = math.log2(max(n, 2))
    k = k or max(1, int(lg ** (1 / 3)))
    t = t or max(1, int(lg ** (2 / 3)))
    top_level = max(1, math.ceil(math.log2(n + 1) / t))
    # label of v: (length, hops, v, predecessor); all labels of different vertices
    # differ, and extending a path by an edge makes its label strictly larger
    lab: list[tuple] = [(INF, INF, v, -1) for v in range(n)]  # @line L1
    lab[s] = (0, 0, s, -1)

    def ext(u: int, v: int, w: float) -> tuple:
        lu = lab[u]
        return (lu[0] + w, lu[1] + 1, v, u)

    def find_pivots(bound, frontier: list[int]):
        w_all = set(frontier)
        layer = list(frontier)
        for _ in range(k):  # k rounds of Bellman-Ford from the frontier
            nxt = set()
            for u in layer:
                for v, w in adj[u]:
                    c = ext(u, v, w)
                    if c <= lab[v]:
                        lab[v] = c
                        if c < bound:
                            nxt.add(v)
            w_all |= nxt
            if len(w_all) > k * len(frontier):
                return list(frontier), w_all
            layer = list(nxt)
        # forest of tight predecessor edges inside W; pivots are big-tree roots in S
        children: dict[int, list[int]] = {}
        roots = []
        for v in w_all:
            p = lab[v][3]
            if p in w_all and _tight(p, v):
                children.setdefault(p, []).append(v)
            else:
                roots.append(v)
        fset = set(frontier)
        pivots = []
        for r in roots:
            if r in fset:
                size, stack = 0, [r]
                while stack and size < k:
                    x = stack.pop()
                    size += 1
                    stack.extend(children.get(x, ()))
                if size >= k:
                    pivots.append(r)
        return pivots, w_all

    def _tight(p: int, v: int) -> bool:
        for x, w in adj[p]:
            if x == v and ext(p, v, w) == lab[v]:
                return True
        return False

    def base_case(bound, x: int):
        heap = [(lab[x], x)]
        got: list[int] = []
        seen = set()
        while heap and len(got) < k + 1:  # Dijkstra from x, at most k + 1 vertices
            key, u = heapq.heappop(heap)
            if u in seen or key != lab[u]:
                continue
            seen.add(u)
            got.append(u)
            for v, w in adj[u]:
                c = ext(u, v, w)
                if c <= lab[v] and c < bound and v not in seen:
                    lab[v] = c
                    heapq.heappush(heap, (c, v))
        if len(got) <= k:
            return bound, set(got)
        b2 = max(lab[v] for v in got)
        return b2, {v for v in got if lab[v] < b2}

    def bmssp(level: int, bound, frontier: list[int]):
        if level == 0:  # @line L2
            b_out, done = base_case(bound, frontier[0])
            if trace is not None:
                trace.append((0, bound[0], sorted(frontier), None, b_out[0], sorted(done)))
            return b_out, done
        pivots, w_all = find_pivots(bound, frontier)  # @line L3
        d = _Frontier(2 ** ((level - 1) * t), bound)  # @line L4
        for x in pivots:
            d.insert(x, lab[x])
        result = None
        done: set[int] = set()
        while len(done) < k * 2 ** (level * t) and d:  # @line L5
            bi, si = d.pull()  # @line L6
            si = [x for x in si if x not in done]  # already complete in this call
            if not si:
                continue
            bpi, ui = bmssp(level - 1, bi, si)  # @line L7
            done |= ui
            result = bpi
            prepend = []
            for u in ui:  # @line L8
                for v, w in adj[u]:
                    c = ext(u, v, w)
                    if c <= lab[v]:
                        lab[v] = c
                        if bi <= c < bound:
                            d.insert(v, c)  # @line L9
                        elif bpi <= c < bi:
                            prepend.append((v, c))
            prepend += [(x, lab[x]) for x in si if bpi <= lab[x] < bi]
            d.batch_prepend(prepend)  # @line L10
        b_out = bound if result is None else min(result, bound)
        done |= {x for x in w_all if lab[x] < b_out}  # @line L11
        if trace is not None:
            trace.append((level, bound[0], sorted(frontier), sorted(pivots), b_out[0], sorted(done)))
        return b_out, done

    bmssp(top_level, TOP, [s])  # @line L12
    dist = [lab[v][0] for v in range(n)]
    parent = [lab[v][3] if v != s and lab[v][0] < INF else None for v in range(n)]
    return dist, parent
