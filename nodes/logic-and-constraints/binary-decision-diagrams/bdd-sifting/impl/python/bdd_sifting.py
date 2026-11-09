# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bdd-sifting/. The authors are listed in prov/KV4EXG.jsonl.

"""Rudell's sifting on a shared reduced ordered BDD.

Node 0 is FALSE and node 1 is TRUE. An inner node u is nodes[u] = [var, lo, hi].
order[k] is the variable on level k (level 0 is the top), and level[v] is the
level of variable v. The variables are x_0, ..., x_{n-1}. The roots are the
external references; the size counts the nodes that a root reaches, with the
sinks. An adjacent swap rewrites the nodes of the upper variable in place, so
the node ids of the roots never change.

Cost: one swap of levels k and k+1 takes O(c + s) time, where c is the number
of nodes on the two levels and s is the size for the garbage collection.
Sifting makes O(n^2) swaps. Precondition for build: len(table) == 2^n.
"""

FALSE, TRUE = 0, 1


class Manager:
    def __init__(self, n: int, order: list[int] | None = None) -> None:
        self.n = n
        self.order = list(range(n)) if order is None else list(order)
        assert sorted(self.order) == list(range(n))
        self.level = [0] * n
        for k, v in enumerate(self.order):
            self.level[v] = k
        self.nodes: dict[int, list[int]] = {}
        self.unique: list[dict[tuple[int, int], int]] = [{} for _ in range(n)]
        self.next_id = 2
        self.roots: list[int] = []

    def lev(self, u: int) -> int:
        return self.n if u <= TRUE else self.level[self.nodes[u][0]]

    def mk(self, v: int, lo: int, hi: int) -> int:
        if lo == hi:
            return lo
        key = (lo, hi)
        u = self.unique[v].get(key)
        if u is None:
            u = self.next_id
            self.next_id += 1
            self.nodes[u] = [v, lo, hi]
            self.unique[v][key] = u
        return u

    def build(self, table: list[int]) -> int:
        """Add a root for the function with this truth table (bit v of the index is x_v)."""
        assert len(table) == 1 << self.n
        memo: dict[tuple[int, int], int] = {}

        def go(k: int, a: int) -> int:
            if k == self.n:
                return TRUE if table[a] else FALSE
            v = self.order[k]
            key = (k, a)
            if key not in memo:
                memo[key] = self.mk(v, go(k + 1, a), go(k + 1, a | 1 << v))
            return memo[key]

        root = go(0, 0)
        self.roots.append(root)
        return root

    def evaluate(self, u: int, a: int) -> int:
        while u > TRUE:
            v, lo, hi = self.nodes[u]
            u = hi if a >> v & 1 else lo
        return u

    def reachable(self) -> set[int]:
        seen = {FALSE, TRUE} & set(self.roots)
        stack = [r for r in self.roots if r > TRUE]
        seen.update(stack)
        while stack:
            u = stack.pop()
            for w in self.nodes[u][1:]:
                if w not in seen:
                    seen.add(w)
                    if w > TRUE:
                        stack.append(w)
        return seen

    def size(self) -> int:
        return len(self.reachable())

    def collect(self) -> None:
        """Delete the nodes that no root reaches."""
        live = self.reachable()
        for u in [u for u in self.nodes if u not in live]:
            v, lo, hi = self.nodes.pop(u)
            del self.unique[v][(lo, hi)]

    def swap(self, k: int) -> None:
        """Exchange the variables on levels k and k+1. The functions stay the same."""
        x, y = self.order[k], self.order[k + 1]
        for u in list(self.unique[x].values()):
            _, lo, hi = self.nodes[u]
            lo_y = lo > TRUE and self.nodes[lo][0] == y
            hi_y = hi > TRUE and self.nodes[hi][0] == y
            if not (lo_y or hi_y):
                continue  # u does not test y; it moves down with x
            f00, f01 = (self.nodes[lo][1], self.nodes[lo][2]) if lo_y else (lo, lo)
            f10, f11 = (self.nodes[hi][1], self.nodes[hi][2]) if hi_y else (hi, hi)
            del self.unique[x][(lo, hi)]
            new_lo = self.mk(x, f00, f10)
            new_hi = self.mk(x, f01, f11)
            self.nodes[u] = [y, new_lo, new_hi]
            self.unique[y][(new_lo, new_hi)] = u
        self.order[k], self.order[k + 1] = y, x
        self.level[x], self.level[y] = k + 1, k
        self.collect()

    def check_invariant(self) -> None:
        for v in range(self.n):
            for (lo, hi), u in self.unique[v].items():
                assert self.nodes[u] == [v, lo, hi]
                assert lo != hi
                assert self.lev(lo) > self.level[v] and self.lev(hi) > self.level[v]
        assert sum(len(t) for t in self.unique) == len(self.nodes)


def sift(m: Manager, max_growth: float = 2.0) -> int:
    """Sift each variable once, the largest levels first. Return the final size.

    A move in one direction stops early when the size passes max_growth times
    the best size seen for this variable. The size never ends above the start.
    """
    counts = [0] * m.n
    for u in m.nodes:
        counts[m.nodes[u][0]] += 1
    for v in sorted(range(m.n), key=lambda w: -counts[w]):  # @line L1
        best = m.size()  # @line L2
        best_pos = m.level[v]
        if m.level[v] < m.n - 1 - m.level[v]:  # @line L3
            directions = (1, -1)  # go down first: the bottom is nearer
        else:
            directions = (-1, 1)
        for d in directions:  # @line L4
            while 0 <= m.level[v] + d < m.n:  # @line L5
                k = m.level[v]
                m.swap(k if d == 1 else k - 1)  # @line L6
                s = m.size()
                if s < best:  # @line L7
                    best, best_pos = s, m.level[v]
                if s > max_growth * best:  # @line L8
                    break
        while m.level[v] > best_pos:  # @line L9
            m.swap(m.level[v] - 1)
        while m.level[v] < best_pos:
            m.swap(m.level[v])
    return m.size()  # @line L10
