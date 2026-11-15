# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sentential-decision-diagram/. The authors are listed in prov/YVT6ET.jsonl.
"""Compressed and trimmed sentential decision diagrams (SDDs) for a fixed vtree.

The variables are the integers 1 to n, and a literal is v or -v.

A vtree is a full binary tree whose leaves are the variables, in a fixed
left to right order. It is given as a nested structure: an int is a leaf
and a pair (left, right) is an inner node. right_linear, balanced and
random_vtree build the usual shapes.

An SDD node of the manager is one of

    0                              FALSE
    1                              TRUE
    ("lit", l)                     a literal, at the leaf of its variable
    ("dec", v, ((p1, s1), ...))    a decomposition at the inner vtree node v

In a decomposition the primes p_i are SDDs for the variables of the left
subtree of v, and the subs s_i for the right subtree. The primes are
consistent, pairwise exclusive and their disjunction is TRUE, and the node
means (p1 and s1) or (p2 and s2) or ... . Every node that the manager makes
is compressed (the subs of one decomposition are distinct) and trimmed (no
decomposition {(TRUE, a)} and no decomposition {(a, TRUE), (not a, FALSE)}).
A unique table maps each node to one id, so for a fixed vtree two
equivalent SDDs get the same id (Darwiche 2011, Theorem 10).
"""

from __future__ import annotations

import random

FALSE, TRUE = 0, 1
AND, OR = "and", "or"


class Vtree:
    """A vtree with integer node ids; leaves carry a variable."""

    def __init__(self, shape) -> None:
        self.left: list[int | None] = []
        self.right: list[int | None] = []
        self.var: list[int | None] = []
        self.parent: list[int | None] = []
        self.depth: list[int] = []
        self.lo: list[int] = []
        self.hi: list[int] = []
        self.vars: list[frozenset[int]] = []
        self.leaf_of: dict[int, int] = {}
        self._leaves = 0
        self.root = self._build(shape, None, 0)

    def _build(self, shape, parent, depth) -> int:
        u = len(self.var)
        self.left.append(None)
        self.right.append(None)
        self.var.append(None)
        self.parent.append(parent)
        self.depth.append(depth)
        self.lo.append(0)
        self.hi.append(0)
        self.vars.append(frozenset())
        if isinstance(shape, int):
            self.var[u] = shape
            self.leaf_of[shape] = u
            self.lo[u] = self.hi[u] = self._leaves
            self._leaves += 1
            self.vars[u] = frozenset([shape])
        else:
            a = self._build(shape[0], u, depth + 1)
            b = self._build(shape[1], u, depth + 1)
            self.left[u], self.right[u] = a, b
            self.lo[u], self.hi[u] = self.lo[a], self.hi[b]
            self.vars[u] = self.vars[a] | self.vars[b]
        return u

    def is_leaf(self, u: int) -> bool:
        return self.var[u] is not None

    def inside(self, a: int, v: int) -> bool:
        """Is vtree node a in the subtree of v?"""
        return self.lo[v] <= self.lo[a] and self.hi[a] <= self.hi[v]

    def lca(self, a: int, b: int) -> int:
        while self.depth[a] > self.depth[b]:
            a = self.parent[a]
        while self.depth[b] > self.depth[a]:
            b = self.parent[b]
        while a != b:
            a, b = self.parent[a], self.parent[b]
        return a


def right_linear(order):
    """The vtree (x1, (x2, (... , xn))): each left child is a leaf."""
    shape = order[-1]
    for v in reversed(order[:-1]):
        shape = (v, shape)
    return Vtree(shape)


def balanced(order):
    def build(vs):
        if len(vs) == 1:
            return vs[0]
        h = len(vs) // 2
        return (build(vs[:h]), build(vs[h:]))

    return Vtree(build(list(order)))


def random_vtree(order, rng: random.Random):
    def build(vs):
        if len(vs) == 1:
            return vs[0]
        h = rng.randint(1, len(vs) - 1)
        return (build(vs[:h]), build(vs[h:]))

    return Vtree(build(list(order)))


class SddManager:
    def __init__(self, vtree: Vtree) -> None:
        self.vtree = vtree
        self.nodes: list = [("false",), ("true",)]
        self.vt: list[int | None] = [None, None]
        self.unique: dict[tuple, int] = {}
        self.apply_cache: dict[tuple, int] = {}
        self.neg_cache: dict[int, int] = {FALSE: TRUE, TRUE: FALSE}

    def _make(self, key: tuple, v: int) -> int:
        u = self.unique.get(key)
        if u is None:
            u = len(self.nodes)
            self.nodes.append(key)
            self.vt.append(v)
            self.unique[key] = u
        return u

    def literal(self, l: int) -> int:
        return self._make(("lit", l), self.vtree.leaf_of[abs(l)])

    def _decomposition(self, v: int, elements) -> int:
        """Compress, trim and look up a decomposition at vtree node v."""
        by_sub: dict[int, int] = {}
        for p, s in elements:
            if p == FALSE:
                continue
            by_sub[s] = self.apply(by_sub[s], p, OR) if s in by_sub else p  # @line L15
        if len(by_sub) == 1:  # @line L16
            ((s, p),) = by_sub.items()
            return s  # {(TRUE, s)} trims to s
        if len(by_sub) == 2 and set(by_sub) == {TRUE, FALSE}:  # @line L17
            return by_sub[TRUE]  # {(a, TRUE), (not a, FALSE)} trims to a
        elems = tuple(sorted((p, s) for s, p in by_sub.items()))
        return self._make(("dec", v, elems), v)  # @line L18

    def negate(self, u: int) -> int:
        r = self.neg_cache.get(u)
        if r is not None:
            return r
        key = self.nodes[u]
        if key[0] == "lit":  # @line L19
            r = self.literal(-key[1])
        else:
            r = self._decomposition(key[1], [(p, self.negate(s)) for p, s in key[2]])  # @line L20
        self.neg_cache[u] = r
        self.neg_cache[r] = u
        return r

    def _elements_at(self, u: int, v: int):
        """The node u written as a partition at the inner vtree node v above or at vt(u)."""
        if self.vt[u] == v:  # @line L12
            return self.nodes[u][2]
        if self.vtree.inside(self.vt[u], self.vtree.left[v]):  # @line L13
            return ((u, TRUE), (self.negate(u), FALSE))
        return ((TRUE, u),)  # @line L14

    def apply(self, a: int, b: int, op: str) -> int:
        if op == AND:  # @line L1
            if a == FALSE or b == FALSE:
                return FALSE
            if a == TRUE:
                return b
            if b == TRUE:
                return a
        else:
            if a == TRUE or b == TRUE:
                return TRUE
            if a == FALSE:
                return b
            if b == FALSE:
                return a
        if a == b:
            return a
        if a > b:
            a, b = b, a
        key = (op, a, b)
        r = self.apply_cache.get(key)
        if r is not None:  # @line L2
            return r
        va, vb = self.vt[a], self.vt[b]
        if va == vb and self.vtree.is_leaf(va):  # @line L3
            # Two different literals of one variable: x and not x.
            r = FALSE if op == AND else TRUE
        else:
            v = self.vtree.lca(va, vb)  # @line L4
            elements = []  # @line L5
            for p, s in self._elements_at(a, v):  # @line L6
                for q, t in self._elements_at(b, v):  # @line L7
                    pq = self.apply(p, q, AND)  # @line L8
                    if pq != FALSE:  # @line L9
                        elements.append((pq, self.apply(s, t, op)))
            r = self._decomposition(v, elements)  # @line L10
        self.apply_cache[key] = r  # @line L11
        return r

    def conjoin(self, a: int, b: int) -> int:
        return self.apply(a, b, AND)

    def disjoin(self, a: int, b: int) -> int:
        return self.apply(a, b, OR)

    # ---------------------------------------------------------------- queries

    def evaluate(self, u: int, assignment: dict[int, bool]) -> bool:
        while True:
            if u in (FALSE, TRUE):
                return u == TRUE
            key = self.nodes[u]
            if key[0] == "lit":
                return assignment[abs(key[1])] == (key[1] > 0)
            u = next(s for p, s in key[2] if self.evaluate(p, assignment))

    def _count_over(self, u: int, w: int, memo: dict) -> int:
        """The number of models of u over the variables of vtree node w (vt(u) is inside w)."""
        width = len(self.vtree.vars[w])
        if u == FALSE:  # @line L21
            return 0
        if u == TRUE:
            return 1 << width
        return self._count(u, memo) << (width - len(self.vtree.vars[self.vt[u]]))  # @line L23

    def _count(self, u: int, memo: dict) -> int:
        if u in memo:
            return memo[u]
        key = self.nodes[u]
        if key[0] == "lit":
            r = 1
        else:
            v = key[1]
            left, right = self.vtree.left[v], self.vtree.right[v]
            r = sum(self._count_over(p, left, memo) * self._count_over(s, right, memo) for p, s in key[2])  # @line L22
        memo[u] = r
        return r

    def model_count(self, u: int) -> int:
        """The number of models of u over all the variables of the vtree."""
        return self._count_over(u, self.vtree.root, {})

    def reachable(self, u: int) -> set[int]:
        seen = set()
        stack = [u]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            key = self.nodes[x]
            if key[0] == "dec":
                for p, s in key[2]:
                    stack.append(p)
                    stack.append(s)
        return seen

    def size(self, u: int) -> int:
        """The sum of the number of elements over the decompositions below u."""
        return sum(len(self.nodes[x][2]) for x in self.reachable(u) if self.nodes[x][0] == "dec")
