# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aig-rewriting/. The authors are listed in prov/CJJRNE.jsonl.

"""DAG-aware AIG rewriting with 3-input cuts and a library of smallest AIGs.

The AIG uses the literal code of the and-inverter-graph page: a literal
is 2 * id + c, node 0 is the constant 0, nodes 1 to n are inputs, and
every later node is an AND of two literals. The graph is changed in
place. For each node the pass looks at its cuts of at most 3 leaves,
finds the NPN class of the function of the cut, and tries the smallest
AIG of that class. The gain counts the nodes that would be freed (the
maximum fanout-free cone of the node over the cut) minus the nodes that
the new structure would add, where an old node that the structure reuses
through the hash table counts as added only if it is in that cone.

The paper of Mishchenko, Chatterjee and Brayton uses 4-input cuts and
the 222 NPN classes of 4-input functions. This version uses 3 inputs and
the 14 classes of 3-input functions, whose smallest AIGs are stored below.
"""

from itertools import permutations
from typing import Iterable, Optional

FULL3 = 0xFF
VAR3 = (0xF0, 0xCC, 0xAA)  # x1, x2, x3 as 8-bit truth tables, x1 the high bit

# NPN class representative -> (gates, root) of a smallest AIG over y1, y2, y3.
# Literals: 0 and 1 are constants, 2 * j + c is y_j for j = 1, 2, 3, and gate
# number g (from 0) is the node 4 + g, with the literal 2 * (4 + g).
LIBRARY: dict[int, tuple[list[tuple[int, int]], int]] = {
    0: ([], 0),
    1: ([(5, 7), (3, 8)], 10),
    3: ([(3, 5)], 8),
    6: ([(5, 6), (4, 7), (9, 11), (3, 13)], 14),
    7: ([(4, 6), (3, 9)], 10),
    15: ([], 3),
    22: ([(3, 7), (2, 6), (5, 11), (4, 8), (9, 12), (15, 17)], 19),
    23: ([(3, 5), (6, 9), (2, 4), (11, 13)], 14),
    24: ([(2, 7), (5, 8), (4, 6), (3, 12), (11, 15)], 17),
    25: ([(3, 4), (5, 7), (6, 8), (11, 13)], 15),
    27: ([(4, 7), (2, 6), (9, 11)], 12),
    30: ([(5, 7), (3, 8), (2, 9), (11, 13)], 14),
    60: ([(2, 4), (3, 5), (9, 11)], 12),
    105: ([(3, 6), (2, 7), (9, 11), (4, 12), (5, 13), (15, 17)], 18),
}


def npn_transform(t: int, perm: tuple[int, ...], neg: int, out: int) -> int:
    """The table c with t(x) = out XOR c(y), where y_j = x_perm[j] XOR bit j of neg."""
    c = 0
    for ym in range(8):
        x = [0, 0, 0]
        for j in range(3):
            x[perm[j]] = ((ym >> (2 - j)) & 1) ^ ((neg >> j) & 1)
        xm = (x[0] << 2) | (x[1] << 1) | x[2]
        c |= (((t >> xm) & 1) ^ out) << ym
    return c


def _npn_table() -> dict[int, tuple[int, tuple[int, ...], int, int]]:
    best: dict[int, tuple[int, tuple[int, ...], int, int]] = {}
    for t in range(256):
        for perm in permutations(range(3)):
            for neg in range(8):
                for out in (0, 1):
                    c = npn_transform(t, perm, neg, out)
                    if t not in best or c < best[t][0]:
                        best[t] = (c, perm, neg, out)
    return best


NPN = _npn_table()


class Aig:
    """A structurally hashed AIG that can be changed in place."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.fanin0: list[int] = [-1] * (n + 1)
        self.fanin1: list[int] = [-1] * (n + 1)
        self.alive: list[bool] = [True] * (n + 1)
        self.table: dict[tuple[int, int], int] = {}
        self.outputs: list[int] = []
        self.refs: list[int] = [0] * (n + 1)
        self.fanouts: list[set[int]] = [set() for _ in range(n + 1)]

    def is_and(self, v: int) -> bool:
        return v > self.n

    @staticmethod
    def trivial(a: int, b: int) -> Optional[int]:
        """The literal of a AND b when a trivial rule gives it, else None (with a <= b)."""
        if a == 0 or a == b ^ 1:
            return 0
        if a == 1 or a == b:
            return b
        return None

    def and_(self, a: int, b: int) -> int:
        if a > b:
            a, b = b, a
        r = self.trivial(a, b)
        if r is not None:
            return r
        v = self.table.get((a, b))
        if v is not None:
            return 2 * v
        v = len(self.fanin0)
        self.fanin0.append(a)
        self.fanin1.append(b)
        self.alive.append(True)
        self.refs.append(0)
        self.fanouts.append(set())
        self.table[(a, b)] = v
        for x in (a, b):
            self.refs[x >> 1] += 1
            self.fanouts[x >> 1].add(v)
        return 2 * v

    # ------------------------------------------------------------ whole graph

    def live_ands(self) -> list[int]:
        """The AND nodes that the outputs reach, in a topological order."""
        order: list[int] = []
        seen: set[int] = set()
        for o in self.outputs:
            stack = [(o >> 1, False)]
            while stack:
                v, done = stack.pop()
                if done:
                    order.append(v)
                    continue
                if v in seen or not self.is_and(v):
                    continue
                seen.add(v)
                stack.append((v, True))
                stack.append((self.fanin1[v] >> 1, False))
                stack.append((self.fanin0[v] >> 1, False))
        return order

    def num_ands(self) -> int:
        return len(self.live_ands())

    def collect_garbage(self) -> None:
        """Delete the AND nodes that no output reaches and recount the fanouts."""
        live = set(self.live_ands())
        for v in range(self.n + 1, len(self.fanin0)):
            if self.alive[v] and v not in live:
                self.alive[v] = False
                key = (self.fanin0[v], self.fanin1[v])
                if self.table.get(key) == v:
                    del self.table[key]
        self.refs = [0] * len(self.fanin0)
        self.fanouts = [set() for _ in range(len(self.fanin0))]
        for v in live:
            for x in (self.fanin0[v], self.fanin1[v]):
                self.refs[x >> 1] += 1
                self.fanouts[x >> 1].add(v)
        for o in self.outputs:
            self.refs[o >> 1] += 1

    def simulate(self, lits: Optional[Iterable[int]] = None) -> list[int]:
        """Truth tables over all 2^n input points of the outputs (or of the given literals)."""
        lits = self.outputs if lits is None else list(lits)
        full = (1 << (1 << self.n)) - 1
        val = [0] * len(self.fanin0)
        for i in range(1, self.n + 1):
            t = 0
            for m in range(1 << self.n):
                if (m >> (self.n - i)) & 1:
                    t |= 1 << m
            val[i] = t
        saved = self.outputs
        self.outputs = lits
        order = self.live_ands()
        self.outputs = saved
        for v in order:
            a, b = self.fanin0[v], self.fanin1[v]
            val[v] = (val[a >> 1] ^ (full if a & 1 else 0)) & (val[b >> 1] ^ (full if b & 1 else 0))
        return [val[o >> 1] ^ (full if o & 1 else 0) for o in lits]

    # ------------------------------------------------------------ local views

    def cuts(self, v: int, k: int = 3) -> list[frozenset[int]]:
        """All cuts of node v with at most k leaves, the trivial cut first."""
        memo: dict[int, list[frozenset[int]]] = {}

        def go(u: int) -> list[frozenset[int]]:
            if u in memo:
                return memo[u]
            res = [frozenset([u])]
            if self.is_and(u):
                seen = {res[0]}
                for c0 in go(self.fanin0[u] >> 1):
                    for c1 in go(self.fanin1[u] >> 1):
                        c = c0 | c1
                        if len(c) <= k and c not in seen:
                            seen.add(c)
                            res.append(c)
            memo[u] = res
            return res

        return go(v)

    def cut_table(self, v: int, leaves: list[int]) -> int:
        """The 8-bit truth table of node v over the leaves, leaf j being x_(j+1)."""
        val = {u: VAR3[j] for j, u in enumerate(leaves)}

        def go(u: int) -> int:
            if u not in val:
                a, b = self.fanin0[u], self.fanin1[u]
                va = go(a >> 1) ^ (FULL3 if a & 1 else 0)
                vb = go(b >> 1) ^ (FULL3 if b & 1 else 0)
                val[u] = va & vb
            return val[u]

        return go(v)

    def mffc(self, v: int, leaves: frozenset[int]) -> set[int]:
        """The nodes freed if v is removed: v and the nodes above the leaves used only inside."""
        refs: dict[int, int] = {}
        cone = {v}
        stack = [v]
        while stack:
            u = stack.pop()
            for x in (self.fanin0[u], self.fanin1[u]):
                w = x >> 1
                if w in leaves or not self.is_and(w):
                    continue
                refs[w] = refs.get(w, self.refs[w]) - 1
                if refs[w] == 0:
                    cone.add(w)
                    stack.append(w)
        return cone


def leaf_map(leaves: list[int], perm: tuple[int, ...], neg: int) -> dict[int, int]:
    """Map the library literals of y1, y2, y3 and the constants to literals of the graph."""
    m = {0: 0, 1: 1}
    for j in range(3):
        if perm[j] < len(leaves):
            lit = 2 * leaves[perm[j]] ^ ((neg >> j) & 1)
        else:
            lit = 0  # the function does not depend on this input
        m[2 * (j + 1)] = lit
        m[2 * (j + 1) + 1] = lit ^ 1
    return m


def count_added(g: Aig, gates: list[tuple[int, int]], root: int, m: dict[int, int], freed: set[int]) -> tuple[int, Optional[int]]:
    """Dry run of a library structure: the nodes it would add and its root literal (None if new)."""
    big = 2 * len(g.fanin0)  # literals at or above big stand for nodes not yet made
    val = dict(m)
    added = 0
    counted: set[int] = set()
    for i, (a, b) in enumerate(gates):
        x, y = val[a], val[b]
        if x > y:
            x, y = y, x
        r = Aig.trivial(x, y)
        if r is None:
            if y < big:
                w = g.table.get((x, y))
                if w is not None:
                    r = 2 * w
                    if w in freed and w not in counted:
                        counted.add(w)
                        added += 1
            if r is None:
                r = big + 2 * i
                added += 1
        val[2 * (4 + i)] = r
        val[2 * (4 + i) + 1] = r ^ 1
    out = val[root]
    return added, (out if out < big else None)


def build(g: Aig, gates: list[tuple[int, int]], root: int, m: dict[int, int]) -> int:
    val = dict(m)
    for i, (a, b) in enumerate(gates):
        r = g.and_(val[a], val[b])
        val[2 * (4 + i)] = r
        val[2 * (4 + i) + 1] = r ^ 1
    return val[root]


def replace(g: Aig, old: int, new: int) -> None:
    """Move every use of node old to the literal new, and merge or simplify the fanouts that change."""
    work = [(old, new)]
    moved: dict[int, int] = {}
    while work:
        o, r = work.pop()
        while r >> 1 in moved:
            r = moved[r >> 1] ^ (r & 1)
        if not g.alive[o] or o == r >> 1:
            continue
        g.outputs = [r ^ (x & 1) if x >> 1 == o else x for x in g.outputs]
        for p in list(g.fanouts[o]):
            if not g.alive[p]:
                continue
            a, b = g.fanin0[p], g.fanin1[p]
            if g.table.get((a, b)) == p:
                del g.table[(a, b)]
            a = r ^ (a & 1) if a >> 1 == o else a
            b = r ^ (b & 1) if b >> 1 == o else b
            if a > b:
                a, b = b, a
            g.fanin0[p], g.fanin1[p] = a, b
            g.fanouts[o].discard(p)
            g.fanouts[r >> 1].add(p)
            t = Aig.trivial(a, b)
            if t is not None:
                work.append((p, t))
            elif (a, b) in g.table:
                work.append((p, 2 * g.table[(a, b)]))
            else:
                g.table[(a, b)] = p
        key = (g.fanin0[o], g.fanin1[o])
        if g.table.get(key) == o:
            del g.table[key]
        g.alive[o] = False
        moved[o] = r


def rewrite(g: Aig) -> list[tuple[int, int, int]]:
    """One pass of DAG-aware rewriting in place. Returns (gain, size before, size after) per change."""
    g.collect_garbage()
    log: list[tuple[int, int, int]] = []
    for v in g.live_ands():  # @line L1
        if not g.alive[v] or not g.is_and(v) or g.refs[v] == 0:
            continue
        best = None  # @line L2
        for cut in g.cuts(v)[1:]:  # @line L3
            leaves = sorted(cut)
            canon, perm, neg, out = NPN[g.cut_table(v, leaves)]  # @line L4
            freed = g.mffc(v, cut)  # @line L5
            gates, root = LIBRARY[canon]  # @line L6
            m = leaf_map(leaves, perm, neg)
            added, lit = count_added(g, gates, root ^ out, m, freed)  # @line L7
            if lit is not None and lit >> 1 == v:
                continue
            gain = len(freed) - added
            if best is None or gain > best[0]:  # @line L8
                best = (gain, gates, root ^ out, m)
        if best is None or best[0] <= 0:  # @line L9
            continue
        before = g.num_ands()
        r = build(g, best[1], best[2], best[3])  # @line L10
        replace(g, v, r)  # @line L11
        g.collect_garbage()  # @line L12
        log.append((best[0], before, g.num_ands()))
    return log
