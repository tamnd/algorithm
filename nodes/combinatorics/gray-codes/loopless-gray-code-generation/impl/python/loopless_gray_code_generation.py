# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loopless-gray-code-generation/. The authors are listed in prov/32MDEZ.jsonl.

from collections.abc import Iterator


def loopless_gray(n: int) -> Iterator[list[int]]:
    """Yield the bit array a of each n-bit string in reflected Gray code order.

    a[j] is bit j (weight 2**j). The same list object is yielded each time and is
    changed in place between visits, so copy it if you keep it. Between two visits
    the generator does a fixed number of operations (focus pointers, Knuth's
    Algorithm L).
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    a = [0] * n  # @line L1
    f = list(range(n + 1))  # @line L1: f_j = j for j < n
    f[n] = n  # @line L2
    while True:  # @line L3
        yield a  # @line L4
        j = f[0]  # @line L5
        f[0] = 0  # @line L5
        if j == n:  # @line L6
            return  # @line L6
        f[j] = f[j + 1]  # @line L7
        f[j + 1] = j + 1  # @line L7
        a[j] = 1 - a[j]  # @line L8


def gray_delta_sequence(n: int) -> list[int]:
    """Return the bits flipped by loopless_gray(n), one per step (2**n - 1 entries)."""
    out: list[int] = []
    prev: list[int] | None = None
    for a in loopless_gray(n):
        if prev is not None:
            changed = [j for j in range(n) if a[j] != prev[j]]
            out.append(changed[0])
        prev = a[:]
    return out


def gray_codes(n: int) -> list[int]:
    """Return the visited strings as integers sum(a[j] * 2**j)."""
    return [sum(bit << j for j, bit in enumerate(a)) for a in loopless_gray(n)]
