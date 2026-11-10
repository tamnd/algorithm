# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/agm-graph-sketch/. The authors are listed in prov/25M25W.jsonl.
"""The AGM graph sketch of Ahn, Guha and McGregor (2012) for spanning forests.

Vertices are 1..n. The edge {u, v} with u < v has the index e = (u - 1) n + v.
The signed incidence vector a_w of a vertex w has +1 at the index of every edge
{w, v} with w < v, and -1 at the index of every edge {u, w} with u < w. For a
vertex set S the sum of a_w over S is nonzero exactly on the edges that leave S.

Each vertex keeps one L0 sampler of a_w per round, and all vertices share the
seeds of a round, so the samplers of the vertices of S add up to a sampler of
the sum. Borůvka rounds then merge components along sampled edges. Each round
uses its own fresh samplers, because the components of a round depend on the
answers of the earlier rounds.
"""

from __future__ import annotations

import math
import random

P = (1 << 61) - 1
EMPTY = "empty"
FAIL = "fail"


def edge_index(n: int, u: int, v: int) -> int:
    if u > v:
        u, v = v, u
    return (u - 1) * n + v


def edge_of(n: int, e: int) -> tuple[int, int]:
    return (e - 1) // n + 1, (e - 1) % n + 1


def signed_incidence(n: int, edges, w: int) -> dict[int, int]:
    """The vector a_w as a dict from edge index to +1 or -1 (multi-edges add up)."""
    a: dict[int, int] = {}
    for u, v in edges:
        if w in (u, v) and u != v:
            e = edge_index(n, u, v)
            a[e] = a.get(e, 0) + (1 if w == min(u, v) else -1)
    return {e: s for e, s in a.items() if s}


class AGMSketch:
    """rounds x copies x (levels + 1) one-sparse cells (A, B, C) per vertex."""

    def __init__(self, n: int, rng: random.Random, delta: float = 0.25, fail: float = 0.01, k: int = 8) -> None:
        self.n = n
        dim = max(2, n * n)
        self.levels = math.ceil(math.log2(dim)) + 2
        self.copies = max(1, math.ceil(math.log(1 / delta) / math.log(32 / 17)))
        rho = (1 + delta) / 2  # expected shrink factor of the open components per round
        self.rounds = max(1, math.ceil(math.log(max(n, 2) / fail) / math.log(1 / rho)))
        self.hashes = [[[rng.randrange(P) for _ in range(k)] for _ in range(self.copies)] for _ in range(self.rounds)]
        self.zs = [[rng.randrange(1, P) for _ in range(self.copies)] for _ in range(self.rounds)]
        size = self.copies * (self.levels + 1)
        # cells[r][w] is a flat list of [A, B, C] triples, copy-major
        self.cells = [[[[0, 0, 0] for _ in range(size)] for _ in range(n + 1)] for _ in range(self.rounds)]

    def _level(self, r: int, c: int, e: int) -> int:
        h = 0
        for coef in self.hashes[r][c]:
            h = (h * e + coef) % P
        j = 0
        while j < self.levels and h < P >> (j + 1):
            j += 1
        return j

    def update(self, u: int, v: int, d: int = 1) -> None:
        """Insert (d = +1) or delete (d = -1) the edge {u, v}."""
        if u == v or not (1 <= u <= self.n and 1 <= v <= self.n):
            raise ValueError("bad edge")
        if u > v:
            u, v = v, u
        e = edge_index(self.n, u, v)  # @line L1
        for r in range(self.rounds):  # @line L2
            for c in range(self.copies):
                top = self._level(r, c, e)
                fp = pow(self.zs[r][c], e, P)
                base = c * (self.levels + 1)
                for j in range(top + 1):
                    for w, s in ((u, d), (v, -d)):  # +d at the smaller endpoint, -d at the larger
                        cell = self.cells[r][w][base + j]
                        cell[0] += s
                        cell[1] += s * e
                        cell[2] = (cell[2] + s * fp) % P

    def _decode(self, a: int, b: int, cc: int, z: int):
        if a == 0 and b == 0 and cc == 0:
            return None
        if a != 0 and b % a == 0:
            e = b // a
            if 1 <= e <= self.n * self.n and cc == (a * pow(z, e, P)) % P:
                return (e, a)
        return "many"

    def sample_cut(self, r: int, comp) -> object:
        """Query the round-r sampler of the sum of a_w over w in comp."""
        size = self.copies * (self.levels + 1)
        total = [[0, 0, 0] for _ in range(size)]
        for w in comp:
            for t, cell in zip(total, self.cells[r][w]):
                t[0] += cell[0]
                t[1] += cell[1]
                t[2] = (t[2] + cell[2]) % P
        for c in range(self.copies):
            base = c * (self.levels + 1)
            all_zero = True
            for j in range(self.levels, -1, -1):
                res = self._decode(*total[base + j], self.zs[r][c])
                if res is None:
                    continue
                all_zero = False
                if res != "many":
                    return edge_of(self.n, res[0])
                break
            if all_zero:
                return EMPTY
        return FAIL

    def spanning_forest(self) -> tuple[list[tuple[int, int]], dict]:
        """Borůvka on sampled cut edges. Returns the forest edges and some statistics."""
        parent = list(range(self.n + 1))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        forest: list[tuple[int, int]] = []  # @line L3
        closed: set[int] = set()  # roots of components with no edge leaving them
        stats = {"rounds_used": 0, "fails": 0}
        for r in range(self.rounds):  # @line L4
            comps: dict[int, list[int]] = {}
            for w in range(1, self.n + 1):
                comps.setdefault(find(w), []).append(w)
            open_comps = [root for root in comps if root not in closed]
            if not open_comps:
                break
            stats["rounds_used"] += 1
            picked = []
            for root in open_comps:  # @line L5
                res = self.sample_cut(r, comps[root])  # @line L6
                if res == EMPTY:  # @line L7
                    closed.add(root)
                elif res == FAIL:
                    stats["fails"] += 1
                else:
                    picked.append(res)
            for a, b in picked:  # @line L8
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[ra] = rb
                    closed.discard(ra)
                    closed.discard(rb)
                    forest.append((min(a, b), max(a, b)))
        return forest, stats  # @line L9


def components_from_forest(n: int, forest) -> list[frozenset]:
    parent = list(range(n + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in forest:
        parent[find(a)] = find(b)
    groups: dict[int, set] = {}
    for w in range(1, n + 1):
        groups.setdefault(find(w), set()).add(w)
    return sorted((frozenset(g) for g in groups.values()), key=min)


def components_direct(n: int, edges) -> list[frozenset]:
    """Connected components by breadth-first search, for the tests."""
    adj: dict[int, set] = {w: set() for w in range(1, n + 1)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    seen: set = set()
    out = []
    for s in range(1, n + 1):
        if s in seen:
            continue
        comp, todo = {s}, [s]
        seen.add(s)
        while todo:
            x = todo.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    comp.add(y)
                    todo.append(y)
        out.append(frozenset(comp))
    return sorted(out, key=min)
