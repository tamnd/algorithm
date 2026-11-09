# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/free-binary-decision-diagram/. The authors are listed in prov/DQZTGE.jsonl.

"""Free binary decision diagrams (FBDDs), also called read-once branching programs.

Node 0 is the sink FALSE and node 1 is the sink TRUE. An inner node u is
nodes[u] = (var, lo, hi) with var in 0..n-1 (x_{i+1} of the page is x_i here).
A diagram is free when each path from the root tests each variable at most
once. Different paths may test the variables in different orders.

mk shares equal nodes and drops a node with lo == hi, so the diagram has no
duplicate and no redundant node, but an FBDD of a function is not unique.
All operations below are iterative and take O(s) arithmetic steps for a
diagram with s nodes; is_free takes O(s n) with sets of variables as masks.
"""

import random

FALSE, TRUE = 0, 1


class FBDD:
    def __init__(self, n: int) -> None:
        self.n = n
        self.nodes: list[tuple[int, int, int]] = [(-1, 0, 0), (-1, 1, 1)]
        self.unique: dict[tuple[int, int, int], int] = {}

    def mk(self, v: int, lo: int, hi: int) -> int:
        if lo == hi:
            return lo
        key = (v, lo, hi)
        u = self.unique.get(key)
        if u is None:
            u = len(self.nodes)
            self.nodes.append(key)
            self.unique[key] = u
        return u

    def topo(self, root: int) -> list[int]:
        """The inner nodes that the root reaches, each after its children."""
        out: list[int] = []
        seen: set[int] = set()
        stack = [(root, False)]
        while stack:
            u, done = stack.pop()
            if done:
                out.append(u)
                continue
            if u <= TRUE or u in seen:
                continue
            seen.add(u)
            stack.append((u, True))
            for w in self.nodes[u][1:]:
                if w not in seen:
                    stack.append((w, False))
        return out

    def evaluate(self, root: int, x: list[int]) -> int:
        u = root
        while u > TRUE:  # @line L1
            v, lo, hi = self.nodes[u]
            u = hi if x[v] else lo  # @line L2
        return u  # @line L3

    def is_free(self, root: int) -> bool:
        """True when no path from the root tests a variable twice."""
        below: dict[int, int] = {FALSE: 0, TRUE: 0}
        for u in self.topo(root):  # @line L4
            v, lo, hi = self.nodes[u]
            under = below[lo] | below[hi]
            if under >> v & 1:  # @line L5
                return False
            below[u] = under | 1 << v  # @line L6
        return True

    def count(self, root: int) -> int:
        """The number of x in {0,1}^n with f(x) = 1. Precondition: the diagram is free."""
        c: dict[int, int] = {FALSE: 0, TRUE: 1 << self.n}
        for u in self.topo(root):  # @line L7
            _, lo, hi = self.nodes[u]
            s = c[lo] + c[hi]
            assert s % 2 == 0
            c[u] = s // 2  # @line L8
        return c[root]

    def arith(self, root: int, r: list[int], p: int) -> int:
        """The multilinear extension of f at the point r, modulo the prime p."""
        val: dict[int, int] = {FALSE: 0, TRUE: 1}
        for u in self.topo(root):  # @line L9
            v, lo, hi = self.nodes[u]
            val[u] = ((1 - r[v]) * val[lo] + r[v] * val[hi]) % p  # @line L10
        return val[root]

    def check_invariant(self) -> None:
        for u in range(2, len(self.nodes)):
            v, lo, hi = self.nodes[u]
            assert 0 <= v < self.n and lo != hi and lo < u and hi < u
            assert self.unique[(v, lo, hi)] == u


def probably_equal(a: FBDD, f: int, b: FBDD, g: int, rng: random.Random, trials: int = 3) -> bool:
    """Blum, Chandra and Wegman: compare the multilinear extensions at random points.

    Equal functions always give True. Different functions give True with
    probability at most (n / p)^trials, with p = 2^61 - 1.
    """
    p = (1 << 61) - 1
    for _ in range(trials):
        r = [rng.randrange(p) for _ in range(a.n)]
        if a.arith(f, r, p) != b.arith(g, r, p):  # @line L11
            return False
    return True  # @line L12


def hwb(n: int) -> tuple[FBDD, int]:
    """An FBDD of the hidden weighted bit function with at most n(n+1) + 2 nodes.

    HWB(x) = x_s with s = x_1 + ... + x_n (1-based) and x_0 = 0. The node
    (a, b, g) has the unread interval x_a..x_b and computes x_t with
    t = a - g + (the number of ones in x_a..x_b). It tests x_b when g = 1 and
    x_a when g = 0.
    """
    d = FBDD(n)
    node: dict[tuple[int, int, int], int] = {}
    for length in range(0, n + 1):
        for a in range(1, n + 2 - length):
            b = a + length - 1
            for g in (0, 1):
                if length == 0:
                    node[(a, b, g)] = FALSE if g == 1 else TRUE
                elif g == 1:  # test x_b; a one moves the target up by one
                    node[(a, b, g)] = d.mk(b - 1, node[(a, b - 1, 1)], node[(a, b - 1, 0)])
                else:  # test x_a
                    node[(a, b, g)] = d.mk(a - 1, node[(a + 1, b, 1)], node[(a + 1, b, 0)])
    return d, node[(1, n, 1)] if n > 0 else FALSE
