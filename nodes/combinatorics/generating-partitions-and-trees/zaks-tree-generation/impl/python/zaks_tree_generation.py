# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zaks-tree-generation/. The authors are listed in prov/R3V9R0.jsonl.

from collections.abc import Iterator


def next_z(z: list[int], t: int = 2) -> bool:
    """Turn the z-sequence z of a t-ary tree into the next one in lexicographic order.

    z[i - 1] is the preorder position (1-based) of the i-th internal node in
    the extended tree with t * n + 1 nodes, so 1 = z[0] < z[1] < ... and
    z[i - 1] <= t * (i - 1) + 1. The list is changed in place. Return True if
    z had a successor; if z is the last sequence, leave it and return False.
    """
    n = len(z)
    j = n  # @line L1
    while j >= 1 and z[j - 1] == t * (j - 1) + 1:  # @line L2
        j -= 1
    if j == 0:  # @line L3
        return False
    z[j - 1] += 1  # @line L4
    for i in range(j, n):  # @line L5
        z[i] = z[i - 1] + 1
    return True  # @line L6


def z_sequences(n: int, t: int = 2) -> Iterator[tuple[int, ...]]:
    """Yield the z-sequences of all t-ary trees with n internal nodes, in lexicographic order."""
    if n < 0 or t < 2:
        raise ValueError("need n >= 0 and t >= 2")
    z = list(range(1, n + 1))
    while True:
        yield tuple(z)
        if not next_z(z, t):
            return


def z_to_bits(z: tuple[int, ...] | list[int], t: int = 2) -> str:
    """Return the preorder word of the extended tree: '1' for an internal node, '0' for a leaf."""
    n = len(z)
    bits = ["0"] * (t * n + 1)
    for p in z:
        bits[p - 1] = "1"
    return "".join(bits)


def z_to_dyck(z: tuple[int, ...] | list[int]) -> str:
    """For a binary tree, return the bracket word: the preorder word without its last 0, 1 = '('."""
    return z_to_bits(z, 2)[:-1].replace("1", "(").replace("0", ")")
