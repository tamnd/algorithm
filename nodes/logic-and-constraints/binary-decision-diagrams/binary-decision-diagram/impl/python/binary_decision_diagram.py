# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-decision-diagram/. The authors are listed in prov/DBR5MN.jsonl.

"""A general binary decision diagram (a branching program).

Node 0 is the terminal FALSE and node 1 is the terminal TRUE. An inner node
u is the triple nodes[u] = (var, lo, hi), and its children have smaller ids,
so the graph is acyclic. Nothing more is assumed: a path may test the
variables in any order, and it may test a variable more than once.
The variables are x_0, ..., x_{n-1} (x_i of the page is index i - 1 here).
"""

FALSE, TRUE = 0, 1


class BDD:
    def __init__(self, n: int) -> None:
        self.n = n
        self.nodes: list[tuple[int, int, int]] = [(-1, 0, 0), (-1, 1, 1)]

    def node(self, i: int, lo: int, hi: int) -> int:
        assert 0 <= i < self.n and 0 <= lo < len(self.nodes) and 0 <= hi < len(self.nodes)
        self.nodes.append((i, lo, hi))
        return len(self.nodes) - 1

    def evaluate(self, u: int, x: list[int]) -> int:
        while u > TRUE:  # @line L1
            i, lo, hi = self.nodes[u]
            u = hi if x[i] else lo  # @line L2
        return u  # @line L3

    def from_cnf(self, clauses: list[list[int]]) -> int:
        """A BDD for a CNF formula; literals are DIMACS ints over 1..n."""
        s = TRUE  # @line L4
        for clause in reversed(clauses):  # @line L5
            t = FALSE  # @line L6
            for lit in reversed(clause):  # @line L7
                v = abs(lit) - 1
                if lit > 0:
                    t = self.node(v, t, s)  # @line L8
                else:
                    t = self.node(v, s, t)  # @line L9
            s = t  # @line L10
        return s  # @line L11

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
        return sorted(seen)  # ids grow from children to parents

    def is_free(self, r: int) -> bool:
        """True if no path from r tests a variable twice (a free BDD)."""
        d: dict[int, int] = {}  # a bit mask of the variables tested below
        for u in self.reachable(r):  # @line L12
            if u <= TRUE:
                d[u] = 0  # @line L13
                continue
            i, lo, hi = self.nodes[u]
            below = d[lo] | d[hi]
            d[u] = below | (1 << i)
            if below >> i & 1:  # @line L14
                return False
        return True  # @line L15

    def sat_free(self, r: int) -> bool:
        """Satisfiability of a free BDD: is TRUE reachable from r?"""
        return TRUE in self.reachable(r)  # @line L16

    def size(self, r: int) -> int:
        return len(self.reachable(r))
