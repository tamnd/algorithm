# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-expression-evaluation/. The authors are listed in prov/D1DXVT.jsonl.

"""Evaluate an arithmetic expression tree by deterministic tree contraction (the shunt).

The tree is a full binary tree: each internal node has an operator in {+, -, *} and
exactly two children, and each leaf has an integer. Each node v carries a linear
function g_v(x) = a x + b, the change that a value undergoes on the edge from v to its
parent (the identity at the start, and at the root). A rake of a leaf u removes u and
its parent p and links the sibling s of u to the parent of p, with the new function
g_p(c op g_s(x)), where c = g_u(value of u). Each round rakes the leaves with odd
numbers: first those that are left children, then those that are right children.
The rakes of one substep run in parallel; the code records the cells each one touches
so that the tests can check that they are disjoint.
"""

from dataclasses import dataclass, field


@dataclass
class Tree:
    """A full binary expression tree. op[v] is '+', '-' or '*' at an internal node and None at a leaf."""

    op: list[str | None]
    left: list[int | None]
    right: list[int | None]
    value: list[int]  # the value of a leaf; ignored at an internal node
    root: int


@dataclass
class Trace:
    rounds: int = 0
    rakes: int = 0
    substeps: list[list[set[tuple[str, int]]]] = field(default_factory=list)


def leaves_in_order(t: Tree) -> list[int]:
    """The leaves from left to right. In parallel this is the Euler tour plus list ranking."""
    out, stack = [], [t.root]
    while stack:
        v = stack.pop()
        if t.op[v] is None:
            out.append(v)
        else:
            stack.append(t.right[v])  # type: ignore[arg-type]
            stack.append(t.left[v])  # type: ignore[arg-type]
    return out


def with_constant(op: str, c: int, c_is_left: bool, a: int, b: int) -> tuple[int, int]:
    """Return (a', b') with a' x + b' = c op (a x + b), or (a x + b) op c when c is the right operand."""
    if op == "+":
        return a, b + c
    if op == "*":
        return c * a, c * b
    if op == "-":
        return (-a, c - b) if c_is_left else (a, b - c)
    raise ValueError(op)


class Contraction:
    def __init__(self, t: Tree) -> None:
        n = len(t.op)
        self.t = t
        self.left, self.right = list(t.left), list(t.right)
        self.parent: list[int | None] = [None] * n
        self.is_left = [False] * n  # the side of v below its parent
        for v in range(n):
            if self.left[v] is not None:
                self.parent[self.left[v]] = v  # type: ignore[index]
                self.is_left[self.left[v]] = True  # type: ignore[index]
            if self.right[v] is not None:
                self.parent[self.right[v]] = v  # type: ignore[index]
        self.a, self.b = [1] * n, [0] * n  # @line L1: g_v is the identity
        self.root = t.root

    def cells(self, u: int) -> set[tuple[str, int]]:
        """The cells that the rake of leaf u reads or writes."""
        p = self.parent[u]
        assert p is not None
        s = self.right[p] if self.is_left[u] else self.left[p]
        g = self.parent[p]
        out = {("a", u), ("b", u), ("value", u), ("parent", u), ("side", u)}
        out |= {("op", p), ("left", p), ("right", p), ("a", p), ("b", p), ("parent", p), ("side", p)}
        out |= {("a", s), ("b", s), ("parent", s), ("side", s)}  # type: ignore[arg-type]
        if g is not None:
            out.add(("left", g) if self.is_left[p] else ("right", g))
        return out

    def rake(self, u: int) -> None:
        """Remove leaf u and its parent p; the sibling s takes the place of p."""
        p = self.parent[u]
        assert p is not None
        s = self.right[p] if self.is_left[u] else self.left[p]
        assert s is not None
        g = self.parent[p]
        c = self.a[u] * self.t.value[u] + self.b[u]  # @line L8: the value that u sends up
        sa, sb = with_constant(self.t.op[p], c, self.is_left[u], self.a[s], self.b[s])  # type: ignore[arg-type]
        self.a[s], self.b[s] = self.a[p] * sa, self.a[p] * sb + self.b[p]  # @line L9: g_s <- g_p o (c op g_s)
        self.parent[s] = g  # @line L10
        self.is_left[s] = self.is_left[p]
        if g is None:
            self.root = s
        elif self.is_left[p]:
            self.left[g] = s
        else:
            self.right[g] = s


def evaluate(t: Tree, trace: Trace | None = None) -> int:
    """Return the value of the expression, in exactly ceil(log2 l) rounds for l leaves."""
    k = Contraction(t)
    leaves = leaves_in_order(t)  # @line L2: number the leaves from left to right
    while len(leaves) > 1:  # @line L3
        odd = leaves[1::2]
        for want_left in (True, False):  # @line L4 (left children) and @line L5 (right children)
            batch = [u for u in odd if k.is_left[u] == want_left]
            touched = [k.cells(u) for u in batch]  # all reads happen before the writes
            for u in batch:  # parallel: the rakes of one substep touch disjoint cells
                k.rake(u)
            if trace is not None:
                trace.substeps.append(touched)
                trace.rakes += len(batch)
        leaves = leaves[0::2]  # @line L6: the even leaves stay, and their numbers halve
        if trace is not None:
            trace.rounds += 1
    u = leaves[0]
    assert u == k.root
    return k.a[u] * t.value[u] + k.b[u]  # @line L7: the root is a leaf, apply its function
