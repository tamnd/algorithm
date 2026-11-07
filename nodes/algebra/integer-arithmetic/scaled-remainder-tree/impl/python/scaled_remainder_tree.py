# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scaled-remainder-tree/. The authors are listed in prov/T3AFQR.jsonl.

"""Scaled remainder tree: x mod m_1, ..., x mod m_k by multiplications only.

A remainder tree pushes x mod Q down the product tree of the moduli, with one
division per node. The scaled tree pushes the fraction frac(x / Q) instead,
as a fixed-point number Y / 2^p with p = bitlength(Q) + G binary digits. For
Q = Q_c * Q_s, frac(x / Q_c) = frac(Q_s * frac(x / Q)), so each child costs
one product and a truncation. At a leaf m, x mod m = ceil(m * Y / 2^p) mod m.
All truncations round down, which keeps the error one-sided; G guard digits
with 2^G >= depth + 1 make every leaf exact.

Integers are Python ints; Stats counts the products and their sizes.
"""

import math


class Stats:
    def __init__(self) -> None:
        self.products = 0
        self.product_digits = 0  # the sum of the lengths of the larger factors
        self.divisions = 0
        self.depth = 0


def _mul(a: int, b: int, st: Stats | None) -> int:
    if st is not None:
        st.products += 1
        st.product_digits += max(a.bit_length(), b.bit_length())
    return a * b


class Node:
    __slots__ = ("q", "left", "right")

    def __init__(self, q: int, left: "Node | None" = None, right: "Node | None" = None) -> None:
        self.q = q
        self.left = left
        self.right = right


def product_tree(ms: list[int], st: Stats | None = None) -> Node:
    """The balanced product tree of the moduli, built bottom up."""
    if not ms:
        raise ValueError("need at least one modulus")
    if any(m < 1 for m in ms):
        raise ValueError("moduli must be positive")
    level = [Node(m) for m in ms]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level) - 1, 2):
            a, b = level[i], level[i + 1]
            nxt.append(Node(_mul(a.q, b.q, st), a, b))
        if len(level) % 2:
            nxt.append(level[-1])
        level = nxt
    return level[0]


def height(t: Node) -> int:
    if t.left is None:
        return 0
    return 1 + max(height(t.left), height(t.right))


def _descend(t: Node, Y: int, p: int, G: int, out: list[int], st: Stats | None, depth: int) -> None:
    if st is not None:
        st.depth = max(st.depth, depth)
    if t.left is None:  # @line L6: a leaf: x mod m = ceil(m Y / 2^p) mod m
        m = t.q
        out.append(((_mul(m, Y, st) + (1 << p) - 1) >> p) % m)
        return
    for c, s in ((t.left, t.right), (t.right, t.left)):  # @line L4: for each child c with sibling s
        pc = c.q.bit_length() + G
        Z = _mul(s.q, Y, st) & ((1 << p) - 1)  # @line L5: frac(Q_s * Y / 2^p), then keep p_c digits
        _descend(c, Z >> (p - pc), pc, G, out, st, depth + 1)


def scaled_remainders(x: int, ms: list[int], st: Stats | None = None, tree: Node | None = None) -> list[int]:
    """[x mod m for m in ms] for an integer x >= 0 and moduli m >= 1."""
    if x < 0:
        raise ValueError("x must be nonnegative")
    t = tree if tree is not None else product_tree(ms, st)  # @line L1: the product tree
    d = height(t)
    G = max(1, math.ceil(math.log2(d + 1)))  # @line L2: guard digits, 2^G >= depth + 1
    p = t.q.bit_length() + G
    if st is not None:
        st.divisions += 1
    Y = ((x % t.q) << p) // t.q  # @line L3: Y = floor(frac(x / P) 2^p), the one division
    out: list[int] = []
    _descend(t, Y, p, G, out, st, 0)
    return out  # @line L7


def remainder_tree(x: int, ms: list[int], st: Stats | None = None, tree: Node | None = None) -> list[int]:
    """The unscaled remainder tree, one division per node, for comparison."""
    t = tree if tree is not None else product_tree(ms, st)
    out: list[int] = []

    def go(v: Node, r: int) -> None:
        if st is not None:
            st.divisions += 1
        r %= v.q
        if v.left is None:
            out.append(r)
            return
        go(v.left, r)
        go(v.right, r)

    go(t, x)
    return out


def to_limbs(x: int, w: int) -> list[int]:
    out = []
    while x:
        out.append(x & ((1 << w) - 1))
        x >>= w
    return out


def from_limbs(d: list[int], w: int) -> int:
    v = 0
    for x in reversed(d):
        v = (v << w) | x
    return v


def scaled_remainders_limbs(x: list[int], ms: list[list[int]], w: int = 8) -> list[list[int]]:
    """The same on limb arrays in radix 2^w; each remainder has as many limbs as its modulus."""
    rs = scaled_remainders(from_limbs(x, w), [from_limbs(m, w) for m in ms])
    return [to_limbs(r, w) + [0] * (len(m) - len(to_limbs(r, w))) for r, m in zip(rs, ms)]
