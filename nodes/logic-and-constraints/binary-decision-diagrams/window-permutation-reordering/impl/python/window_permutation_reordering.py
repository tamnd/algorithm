# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/window-permutation-reordering/. The authors are listed in prov/83R3H0.jsonl.

"""Window permutation reordering on a shared reduced ordered BDD.

Node 0 is FALSE and node 1 is TRUE. An inner node u is nodes[u] = [var, lo, hi].
order[k] is the variable on level k (level 0 is the top), and level[v] is the
level of variable v. The variables are x_0, ..., x_{n-1}. The size counts the
nodes that a root reaches, with the sinks. An adjacent swap rewrites the nodes
of the upper variable in place, so the node ids of the roots never change.

A window is w adjacent levels. The method visits all w! orders of the window
by w! - 1 adjacent swaps (the Steinhaus-Johnson-Trotter sequence), keeps the
best one, and moves on. Passes repeat until a pass gives no improvement.

Cost: one pass makes O(n w!) swaps; a swap of levels k and k+1 takes O(c + s)
time, where c is the number of nodes on the two levels and s is the size.
The number of passes is at most the start size. Precondition: 2 <= w <= n.
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


def sjt_swaps(w: int) -> list[int]:
    """Offsets j such that swapping positions j and j+1 in turn visits all w! orders."""
    perm = list(range(w))
    direction = [-1] * w
    out: list[int] = []
    while True:
        mobile = -1
        for i in range(w):
            j = i + direction[perm[i]]
            if 0 <= j < w and perm[j] < perm[i] and (mobile < 0 or perm[i] > perm[mobile]):
                mobile = i
        if mobile < 0:
            return out
        v = perm[mobile]
        j = mobile + direction[v]
        perm[mobile], perm[j] = perm[j], perm[mobile]
        out.append(min(mobile, j))
        for u in range(v + 1, w):
            direction[u] = -direction[u]


def window_permutation(m: Manager, w: int = 3) -> int:
    """Reorder by windows of w levels until no window improves. Return the size."""
    assert 2 <= w <= max(m.n, 2)
    if m.n < w:
        return m.size()
    seq = sjt_swaps(w)
    improved = True
    while improved:  # @line L1
        improved = False  # @line L2
        for k in range(m.n - w + 1):  # @line L3
            start = best = m.size()  # @line L4
            best_window = m.order[k:k + w]
            for j in seq:  # @line L5
                m.swap(k + j)  # @line L6
                s = m.size()
                if s < best:  # @line L7
                    best, best_window = s, m.order[k:k + w]
            for i, v in enumerate(best_window):  # @line L8
                while m.level[v] > k + i:
                    m.swap(m.level[v] - 1)
            if best < start:  # @line L9
                improved = True
    return m.size()  # @line L10
