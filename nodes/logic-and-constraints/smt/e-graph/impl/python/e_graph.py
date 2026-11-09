# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/e-graph/. The authors are listed in prov/S6Y6MV.jsonl.
"""An e-graph with a hash-cons table and deferred rebuilding.

An e-node is a tuple (f, c1, ..., ck) of a function symbol and k e-class ids.
A term is a string (a constant) or a tuple (f, t1, ..., tk) of a symbol and
terms. Merges only link classes; rebuild() restores the congruence invariant.
The design follows the rebuilding of Willsey et al. (egg, 2021), with the
parent entries of the smaller class put on a pending list, as in Downey,
Sethi and Tarjan (1980).
"""

from typing import Callable, Optional, Union

Term = Union[str, tuple]
ENode = tuple


class EGraph:
    def __init__(self) -> None:
        self.uf: list[int] = []  # union-find parent of each e-class id
        self.nodes: list[list[ENode]] = []  # the e-nodes of each root class
        self.parents: list[list[tuple[ENode, int]]] = []  # (e-node, its class)
        self.memo: dict[ENode, int] = {}  # canonical e-node -> an e-class id
        self.pending: list[tuple[ENode, int]] = []

    # ------------------------------------------------------------ union-find
    def find(self, x: int) -> int:
        while self.uf[x] != x:
            self.uf[x] = self.uf[self.uf[x]]  # path halving
            x = self.uf[x]
        return x

    def canonical(self, n: ENode) -> ENode:
        return (n[0],) + tuple(self.find(c) for c in n[1:])

    # ------------------------------------------------------------ updates
    def add(self, n: ENode) -> int:
        """Add the e-node n and return its e-class."""
        n = self.canonical(n)  # @line L1
        if n in self.memo:  # @line L2
            return self.find(self.memo[n])
        x = len(self.uf)  # @line L3
        self.uf.append(x)
        self.nodes.append([n])
        self.parents.append([])
        for c in n[1:]:  # @line L4
            self.parents[c].append((n, x))
        self.memo[n] = x  # @line L5
        return x  # @line L6

    def add_term(self, t: Term) -> int:
        """Add a term and all its subterms, without recursion."""
        done: dict[Term, int] = {}
        stack: list[tuple[Term, bool]] = [(t, False)]
        while stack:
            u, ready = stack.pop()
            if u in done:
                continue
            if isinstance(u, str):
                done[u] = self.add((u,))
            elif ready:
                done[u] = self.add((u[0],) + tuple(done[a] for a in u[1:]))
            else:
                stack.append((u, True))
                stack.extend((a, False) for a in u[1:] if a not in done)
        return done[t]

    def merge(self, x: int, y: int) -> bool:
        """Join two e-classes. Return False if they were already one class."""
        x, y = self.find(x), self.find(y)  # @line L7
        if x == y:  # @line L8
            return False
        if len(self.parents[x]) > len(self.parents[y]):  # @line L9
            x, y = y, x
        self.uf[x] = y  # @line L10
        self.nodes[y].extend(self.nodes[x])  # @line L11
        self.nodes[x] = []
        self.pending.extend(self.parents[x])  # @line L12
        self.parents[y].extend(self.parents[x])  # @line L13
        self.parents[x] = []
        return True  # @line L14

    def rebuild(self) -> int:
        """Restore the congruence invariant. Return the number of merges."""
        merges = 0
        while self.pending:  # @line L15
            n, x = self.pending.pop()  # @line L16
            n = self.canonical(n)  # @line L17
            y = self.memo.get(n)
            if y is not None and self.find(y) != self.find(x):  # @line L18
                self.merge(y, x)
                merges += 1
            self.memo[n] = self.find(x)  # @line L19
        return merges

    # ------------------------------------------------------------ queries
    def is_clean(self) -> bool:
        return not self.pending

    def lookup(self, t: Term) -> Optional[int]:
        """The e-class that represents t, or None. Needs a clean e-graph."""
        if self.pending:
            raise RuntimeError("call rebuild() first")
        done: dict[Term, Optional[int]] = {}
        stack: list[tuple[Term, bool]] = [(t, False)]
        while stack:
            u, ready = stack.pop()
            if u in done:
                continue
            if isinstance(u, str):
                c = self.memo.get((u,))
                done[u] = None if c is None else self.find(c)
            elif ready:
                kids = [done[a] for a in u[1:]]  # @line L20
                if any(k is None for k in kids):  # @line L21
                    done[u] = None
                else:
                    c = self.memo.get(self.canonical((u[0],) + tuple(kids)))  # @line L22
                    done[u] = None if c is None else self.find(c)  # @line L23
            else:
                stack.append((u, True))
                stack.extend((a, False) for a in u[1:] if a not in done)
        return done[t]

    def equivalent(self, s: Term, t: Term) -> bool:
        self.rebuild()
        return self.find(self.add_term(s)) == self.find(self.add_term(t))

    def classes(self) -> list[int]:
        return [x for x in range(len(self.uf)) if self.uf[x] == x]

    def enodes(self, x: int) -> list[ENode]:
        """The distinct canonical e-nodes of the class of x."""
        return list(dict.fromkeys(self.canonical(n) for n in self.nodes[self.find(x)]))

    def extract(self, cost: Callable[[ENode], int] = lambda n: 1) -> dict[int, tuple[int, Term]]:
        """For each class, a term of least total cost. Needs a clean e-graph.

        Costs are positive. The loop is a Bellman-Ford style fixpoint: a best
        term never repeats a class on a path from its root, so its depth is
        at most the number of classes, and that many rounds are enough.
        """
        if self.pending:
            raise RuntimeError("call rebuild() first")
        best: dict[int, tuple[int, Term]] = {}
        roots = self.classes()
        for _ in range(len(roots)):
            changed = False
            for x in roots:
                for n in self.enodes(x):
                    kids = [self.find(c) for c in n[1:]]
                    if all(k in best for k in kids):
                        total = cost(n) + sum(best[k][0] for k in kids)
                        if x not in best or total < best[x][0]:
                            term = n[0] if not kids else (n[0],) + tuple(best[k][1] for k in kids)
                            best[x] = (total, term)
                            changed = True
            if not changed:
                break
        return best
