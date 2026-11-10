# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-prefix/. The authors are listed in prov/98XS2A.jsonl.

"""Prefix circuits as lists of gates, with their size and depth.

A circuit on n wires is a list of gates (s, t) with s < t. The gate sets
wire t to (wire s) ⊕ (wire t). Gates run in list order, and the depth of a
wire is one more than the larger depth of the two inputs of its last gate.
A prefix circuit leaves wire j holding a[0] ⊕ ... ⊕ a[j].
"""

from typing import Callable, TypeVar

T = TypeVar("T")
Gate = tuple[int, int]


def evaluate(op: Callable[[T, T], T], gates: list[Gate], a: list[T]) -> tuple[list[T], int, int]:
    """Run the gates on input a. Return (outputs, size, depth)."""
    x = list(a)
    depth = [0] * len(a)
    for s, t in gates:
        assert s < t
        x[t] = op(x[s], x[t])
        depth[t] = max(depth[s], depth[t]) + 1
    return x, len(gates), max(depth, default=0)


def ladner_fischer(n: int, k: int) -> list[Gate]:
    """The circuit P_k(n) of Ladner and Fischer (1980)."""
    gates: list[Gate] = []

    def build(w: list[int], k: int) -> None:
        m = len(w)
        if m <= 1:  # @line L1
            return
        if k == 0:  # @line L2
            c = (m + 1) // 2  # @line L3
            build(w[:c], 1)  # @line L4
            build(w[c:], 0)  # @line L5
            for j in range(c, m):  # @line L6
                gates.append((w[c - 1], w[j]))
            return
        # @line L7: k >= 1
        for i in range(m // 2):  # @line L8
            gates.append((w[2 * i], w[2 * i + 1]))
        sub = [w[2 * i + 1] for i in range(m // 2)]
        if m % 2 == 1:
            sub.append(w[m - 1])
        build(sub, k - 1)  # @line L9
        for j in range(2, m - 1, 2):  # @line L10
            gates.append((w[j - 1], w[j]))

    build(list(range(n)), k)
    return gates


def serial(n: int) -> list[Gate]:
    return [(j - 1, j) for j in range(1, n)]


def sklansky(n: int) -> list[Gate]:
    """Divide and conquer: each right half reads the last wire of its left half."""
    gates = []
    d = 1
    while d < n:
        for j in range(n):
            if (j // d) % 2 == 1:
                gates.append(((j // d) * d - 1, j))
        d *= 2
    return gates


def kogge_stone(n: int) -> list[Gate]:
    """The Hillis-Steele scan as a circuit. Descending j reads old values."""
    gates = []
    d = 1
    while d < n:
        for j in range(n - 1, d - 1, -1):
            gates.append((j - d, j))
        d *= 2
    return gates


def brent_kung(n: int) -> list[Gate]:
    """An up-sweep tree, then a down-sweep that fills in the other wires."""
    gates = []
    d = 1
    while 2 * d <= n:
        for j in range(2 * d - 1, n, 2 * d):
            gates.append((j - d, j))
        d *= 2
    d //= 2
    while d >= 1:
        for j in range(3 * d - 1, n, 2 * d):
            gates.append((j - d, j))
        d //= 2
    return gates
