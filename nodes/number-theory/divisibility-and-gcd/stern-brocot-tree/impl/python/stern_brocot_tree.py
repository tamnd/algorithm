# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stern-brocot-tree/. The authors are listed in prov/5DMN7F.jsonl.

"""The Stern-Brocot tree, stored implicitly.

A node is the pair of its bounds a/b < c/d, with b c - a d = 1, and its
value is the mediant (a + c)/(b + d). The root has the bounds 0/1 and 1/0.
A path from the root is a list of runs ("L", k) or ("R", k), so that nodes
of large depth, such as n/1 at depth n - 1, have short descriptions.

Costs, with arbitrary precision integers: children, parent and value take
O(1) operations; encode(p, q) takes O(log min(p, q) + 1) divisions, as
Euclid's algorithm does; decode takes O(1) operations per run; and
best_approximation(u, v, n) takes O(log n + 1) iterations.
"""

from dataclasses import dataclass

Run = tuple[str, int]  # ("L" or "R", length >= 1)


@dataclass(frozen=True)
class Node:
    """A node of the Stern-Brocot tree, given by its bounds a/b and c/d."""

    a: int
    b: int
    c: int
    d: int

    @property
    def value(self) -> tuple[int, int]:
        """The fraction at the node, (numerator, denominator), in lowest terms."""
        return self.a + self.c, self.b + self.d

    def left(self) -> "Node":
        """The left child, the mediant of a/b and the node."""
        p, q = self.value
        return Node(self.a, self.b, p, q)

    def right(self) -> "Node":
        """The right child, the mediant of the node and c/d."""
        p, q = self.value
        return Node(p, q, self.c, self.d)

    def parent(self) -> "Node | None":
        """The parent node, or None at the root. O(1) operations."""
        a, b, c, d = self.a, self.b, self.c, self.d
        if (a, b, c, d) == (0, 1, 1, 0):  # @line L12
            return None
        if a + b > c + d:  # @line L13
            return Node(a - c, b - d, c, d)
        return Node(a, b, c - a, d - b)


ROOT = Node(0, 1, 1, 0)


def encode(p: int, q: int) -> list[Run]:
    """Return the path from the root to p/q as a list of runs.

    Precondition: p >= 1 and q >= 1; p/q need not be in lowest terms.
    Zero and negative inputs raise ValueError, since the tree holds only
    positive rationals. The run lengths are the partial quotients of the
    continued fraction of p/q, with the last one decreased by 1.
    """
    if p < 1 or q < 1:
        raise ValueError("the Stern-Brocot tree holds positive fractions only")
    runs: list[Run] = []  # @line L1
    direction = "R"
    while q != 0:  # @line L2
        k, r = divmod(p, q)  # @line L3
        p, q = q, r
        if q == 0:  # @line L4
            k -= 1
        if k > 0:  # @line L5
            runs.append((direction, k))
        direction = "L" if direction == "R" else "R"  # @line L6
    return runs  # @line L7


def decode(runs: list[Run]) -> Node:
    """Return the node reached from the root by the given runs."""
    a, b, c, d = 0, 1, 1, 0  # @line L8
    for direction, k in runs:  # @line L9
        if direction == "R":  # @line L10
            a, b = a + k * c, b + k * d
        else:
            c, d = c + k * a, d + k * b
    return Node(a, b, c, d)  # @line L11


def node_of(p: int, q: int) -> Node:
    """The node whose value is p/q in lowest terms (p, q >= 1)."""
    return decode(encode(p, q))


def depth(runs: list[Run]) -> int:
    """The depth of the node with the given path (the root has depth 0)."""
    return sum(k for _, k in runs)


def best_approximation(u: int, v: int, n: int) -> tuple[int, int]:
    """Closest fraction to x = u/v with denominator at most n.

    Precondition: u >= 0, v >= 1, n >= 1; otherwise ValueError. Returns
    (p, q) in lowest terms with 1 <= q <= n minimizing |x - p/q|; on a tie
    between two fractions it returns the smaller one.
    """
    if u < 0 or v < 1 or n < 1:
        raise ValueError("need u >= 0, v >= 1 and n >= 1")
    a, b, c, d = 0, 1, 1, 0  # @line L14
    while b + d <= n:  # @line L15
        p, q = a + c, b + d
        if u * q == v * p:  # @line L16
            return p, q
        if u * q > v * p:  # @line L17
            k = (n - b) // d if d > 0 else -1  # limit from the denominator
            k_x = (u * b - a * v - 1) // (c * v - u * d)  # stay below x
            k = k_x if k < 0 else min(k, k_x)
            a, b = a + k * c, b + k * d
        else:  # @line L18
            k = (n - d) // b  # limit from the denominator, b >= 1
            gap = u * b - a * v  # zero only when x = a/b = 0/1
            if gap > 0:
                k = min(k, (c * v - u * d - 1) // gap)  # stay above x
            c, d = c + k * a, d + k * b
    if d == 0 or (u * b - a * v) * d <= (c * v - u * d) * b:  # @line L19
        return a, b
    return c, d
