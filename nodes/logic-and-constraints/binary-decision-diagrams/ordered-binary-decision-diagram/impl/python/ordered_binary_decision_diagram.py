# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ordered-binary-decision-diagram/. The authors are listed in prov/8Z0NZS.jsonl.

"""An ordered binary decision diagram (OBDD) with a chosen variable order.

Node 0 is the terminal FALSE and node 1 is the terminal TRUE. An inner node
u is the triple nodes[u] = (var, lo, hi). The order is a list of the
variables from the top level to the bottom level, and level[v] is the
position of variable v in it; the terminals have level n. The diagram is
ordered when each edge goes to a node of a larger level. The variables are
x_0, ..., x_{n-1} (x_i of the page is index i - 1 here).
"""

FALSE, TRUE = 0, 1


class OBDD:
    def __init__(self, n: int, order: list[int] | None = None) -> None:
        self.n = n
        self.order = list(range(n)) if order is None else list(order)
        assert sorted(self.order) == list(range(n))
        self.level = [0] * n
        for k, v in enumerate(self.order):
            self.level[v] = k
        self.nodes: list[tuple[int, int, int]] = [(-1, 0, 0), (-1, 1, 1)]
        self.unique: dict[tuple[int, int, int], int] = {}  # used by reduce only

    def lev(self, u: int) -> int:
        return self.n if u <= TRUE else self.level[self.nodes[u][0]]

    def node(self, i: int, lo: int, hi: int) -> int:
        """Append a node with no check and no sharing."""
        self.nodes.append((i, lo, hi))
        return len(self.nodes) - 1

    def evaluate(self, u: int, x: list[int]) -> int:
        while u > TRUE:  # @line L1
            i, lo, hi = self.nodes[u]
            u = hi if x[i] else lo  # @line L2
        return u  # @line L3

    def reachable(self, r: int) -> list[int]:
        """The nodes reachable from r, children before parents."""
        seen = {r}
        stack = [r]
        while stack:
            u = stack.pop()
            if u > TRUE:
                for c in self.nodes[u][1:]:
                    if c not in seen:
                        seen.add(c)
                        stack.append(c)
        return sorted(seen)  # a child always has a smaller id

    def is_ordered(self, r: int) -> bool:
        for u in self.reachable(r):  # @line L4
            if u > TRUE:
                for c in self.nodes[u][1:]:  # @line L5
                    if self.lev(c) <= self.lev(u):  # @line L6
                        return False
        return True  # @line L7

    def tree(self, table: list[int]) -> int:
        """The complete decision tree of a truth table, in the order of self.order.

        Entry a of the table is f(x) with x_j = bit j of a.
        """
        assert len(table) == 1 << self.n

        def go(k: int, a: int) -> int:
            if k == self.n:  # @line L8
                return TRUE if table[a] else FALSE
            i = self.order[k]  # @line L9
            return self.node(i, go(k + 1, a), go(k + 1, a | (1 << i)))  # @line L10

        return go(0, 0)

    def reduce(self, r: int) -> int:
        """The reduced OBDD of f_r. Equal functions give the same node id."""
        red: dict[int, int] = {}
        for u in self.reachable(r):  # @line L11
            if u <= TRUE:
                red[u] = u  # @line L12
                continue
            i, lo, hi = self.nodes[u]
            l, h = red[lo], red[hi]  # @line L13
            if l == h:  # @line L14
                red[u] = l
            elif (i, l, h) in self.unique:  # @line L15
                red[u] = self.unique[(i, l, h)]
            else:
                red[u] = self.unique[(i, l, h)] = self.node(i, l, h)  # @line L16
        return red[r]  # @line L17

    def truth_table(self, r: int) -> list[int]:
        return [self.evaluate(r, [(a >> j) & 1 for j in range(self.n)]) for a in range(1 << self.n)]

    def size(self, r: int) -> int:
        return len(self.reachable(r))
