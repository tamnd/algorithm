# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/calkin-wilf-tree/. The authors are listed in prov/R06GGM.jsonl.

"""The Calkin-Wilf tree, stored implicitly.

A node is a positive fraction a/b in lowest terms, given as the pair (a, b).
The root is (1, 1); the children of (a, b) are (a, a + b) and (a + b, b).
Nodes are numbered in breadth-first order from 1, so node n has children 2n
and 2n + 1. Every operation works on the pair itself; nothing is stored.
Numerators and denominators are Python integers of any size. Pairs with a
non-positive entry, or not in lowest terms, raise ValueError.
"""


def _check(a: int, b: int) -> None:
    if a <= 0 or b <= 0:
        raise ValueError("a node is a pair of positive integers")


def children(a: int, b: int) -> tuple[tuple[int, int], tuple[int, int]]:
    """The left and right children of a/b."""
    _check(a, b)
    return (a, a + b), (a + b, b)  # @line L1


def parent(a: int, b: int) -> tuple[int, int] | None:
    """The parent of a/b, or None for the root 1/1."""
    _check(a, b)
    if a == b:  # @line L2
        if a != 1:
            raise ValueError("not in lowest terms")
        return None
    if a < b:  # @line L3
        return a, b - a
    return a - b, b  # @line L4


def at(n: int) -> tuple[int, int]:
    """The node with breadth-first index n >= 1."""
    if n < 1:
        raise ValueError("indices start at 1")
    a, b = 1, 1  # @line L5
    for i in range(n.bit_length() - 2, -1, -1):  # @line L6
        if (n >> i) & 1 == 0:  # @line L7
            b = a + b
        else:
            a = a + b
    return a, b  # @line L8


def index_of(a: int, b: int) -> int:
    """The breadth-first index of a/b, which must be in lowest terms."""
    _check(a, b)
    n, length = 0, 0  # @line L9
    while a != b:  # @line L10
        if a > b:  # @line L11
            q = (a - 1) // b  # right steps: a - q b lands in (0, b]
            a -= q * b
            n |= ((1 << q) - 1) << length
        else:  # @line L12
            q = (b - 1) // a  # left steps: zero digits
            b -= q * a
        length += q  # @line L13
    if a != 1:  # @line L14
        raise ValueError("not in lowest terms")
    return n | (1 << length)  # @line L15


def next_node(a: int, b: int) -> tuple[int, int]:
    """The node after a/b in breadth-first order (Newman's formula)."""
    _check(a, b)
    q = a // b  # @line L16
    return b, (2 * q + 1) * b - a  # @line L17


def depth(a: int, b: int) -> int:
    """The level of a/b; the root has depth 0."""
    return index_of(a, b).bit_length() - 1


def fusc(n: int) -> int:
    """Stern's diatomic sequence: fusc(0) = 0, fusc(1) = 1,
    fusc(2m) = fusc(m), fusc(2m + 1) = fusc(m) + fusc(m + 1)."""
    if n < 0:
        raise ValueError("fusc is defined for n >= 0")
    x, y = 1, 0  # invariant: fusc(original n) = x fusc(n) + y fusc(n + 1)
    while n > 0:
        if n & 1:
            y += x
        else:
            x += y
        n >>= 1
    return y
