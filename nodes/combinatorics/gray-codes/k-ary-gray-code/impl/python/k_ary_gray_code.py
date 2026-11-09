# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-ary-gray-code/. The authors are listed in prov/71AG12.jsonl.

from collections.abc import Iterator, Sequence


def reflected_mixed_radix(radices: Sequence[int]) -> Iterator[list[int]]:
    """Yield every digit array a with 0 <= a[j] < radices[j] in reflected Gray order.

    a[0] is the lowest digit. Each step changes one digit by +1 or -1. The same
    list object is yielded each time and is changed in place, so copy it if you
    keep it. Between two visits the work is bounded (Knuth's Algorithm H).
    """
    m = list(radices)
    n = len(m)
    if any(r < 2 for r in m):
        raise ValueError("every radix must be at least 2")
    a = [0] * n  # @line L1
    f = list(range(n + 1))  # @line L1: f_j = j
    o = [1] * n  # @line L1
    f[n] = n  # @line L2
    while True:  # @line L3
        yield a  # @line L4
        j = f[0]  # @line L5
        f[0] = 0  # @line L5
        if j == n:  # @line L6
            return  # @line L6
        a[j] += o[j]  # @line L7
        if a[j] == 0 or a[j] == m[j] - 1:  # @line L8
            o[j] = -o[j]  # @line L9
            f[j] = f[j + 1]  # @line L10
            f[j + 1] = j + 1  # @line L10


def k_ary_gray(n: int, k: int) -> list[tuple[int, ...]]:
    """Return the reflected k-ary Gray code of length n as tuples (a_0, ..., a_{n-1})."""
    if n < 0:
        raise ValueError("n must be non-negative")
    return [tuple(a) for a in reflected_mixed_radix([k] * n)]


def unrank(r: int, radices: Sequence[int]) -> list[int]:
    """Return the digit array at position r of the reflected mixed-radix code.

    Digit j is b_j if floor(r / (m_0 ... m_j)) is even, else m_j - 1 - b_j,
    where b_j is digit j of r in the mixed radix.
    """
    m = list(radices)
    total = 1
    for x in m:
        total *= x
    if not 0 <= r < total:
        raise ValueError("r is out of range")
    out = []
    q = r
    for mj in m:
        b = q % mj
        q //= mj
        out.append(b if q % 2 == 0 else mj - 1 - b)
    return out


def rank(a: Sequence[int], radices: Sequence[int]) -> int:
    """Return the position of the digit array a in the reflected mixed-radix code."""
    m = list(radices)
    if len(a) != len(m):
        raise ValueError("a and radices differ in length")
    r = 0
    for j in range(len(m) - 1, -1, -1):
        b = a[j] if r % 2 == 0 else m[j] - 1 - a[j]
        r = r * m[j] + b
    return r
