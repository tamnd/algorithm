# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/singleton-bound/. The authors are listed in prov/HQ6X1P.jsonl.

"""The Singleton bound, Reed-Solomon codes that meet it, and a search for binary MDS codes.

Words over GF(p), p prime, are tuples of ints in range(p). Binary words are ints.
"""

from itertools import product
from math import log


def singleton_bound(q: int, n: int, d: int) -> int:
    """q^(n - d + 1): an upper bound on A_q(n, d) for every code, linear or not."""
    return q ** (n - d + 1)


def puncture_is_injective(words: list[tuple[int, ...]], d: int) -> bool:
    """The step of the proof: deleting the last d - 1 positions keeps the words distinct."""
    n = len(words[0])
    cut = {w[: n - d + 1] for w in words}
    return len(cut) == len(set(words))


def reed_solomon_words(p: int, points: list[int], k: int, infinity: bool = False) -> list[tuple[int, ...]]:
    """The Reed-Solomon code over GF(p): the values of each polynomial of degree < k at the points.

    With infinity=True one more position holds the coefficient of x^(k-1) (the doubly
    extended code when points is all of GF(p)). Cost: p^k words, each in O(n k) field operations.
    """
    words = []
    for coef in product(range(p), repeat=k):
        w = []
        for a in points:
            v = 0
            for c in reversed(coef):  # Horner's rule
                v = (v * a + c) % p
            w.append(v)
        if infinity:
            w.append(coef[k - 1])
        words.append(tuple(w))
    return words


def min_distance(words: list[tuple[int, ...]]) -> int:
    """Minimum distance of a linear code: the least weight of a nonzero word."""
    return min(sum(1 for a in w if a) for w in words if any(w))


def is_mds(q: int, n: int, k: int, d: int) -> bool:
    """True when the linear [n, k, d]_q code meets the Singleton bound, d = n - k + 1."""
    return d == n - k + 1


def binary_linear_codes_systematic(n: int, k: int):
    """Yield the generator rows of every binary [n, k] code [I | P] in systematic form.

    Every binary linear code is equivalent to one of these by a permutation of the
    positions, which keeps the minimum distance.
    """
    r = n - k
    for bits in range(2 ** (k * r)):
        rows = []
        for i in range(k):
            p = (bits >> (i * r)) & ((1 << r) - 1)
            rows.append((1 << i) | (p << k))
        yield rows


def binary_code_distance(rows: list[int]) -> int:
    """Least weight of a nonzero word in the span of the rows (ints)."""
    best = None
    k = len(rows)
    for m in range(1, 2 ** k):
        c = 0
        for i in range(k):
            if (m >> i) & 1:
                c ^= rows[i]
        w = c.bit_count()
        if best is None or w < best:
            best = w
    return best if best is not None else 0


def binary_mds_parameters(n: int) -> set[tuple[int, int]]:
    """All (k, d) with 1 <= k <= n for which a binary [n, k, d] MDS code exists."""
    out = set()
    for k in range(1, n + 1):
        for rows in binary_linear_codes_systematic(n, k):
            d = binary_code_distance(rows)
            if d == n - k + 1:
                out.add((k, d))
                break
    return out


def hamming_rate(delta: float, q: int) -> float:
    """1 - h_q(delta / 2): the asymptotic Hamming bound, for comparison."""
    x = delta / 2
    if x <= 0:
        return 1.0
    h = x * log(q - 1, q) - x * log(x, q) - (1 - x) * log(1 - x, q)
    return max(0.0, 1.0 - h)


def singleton_rate(delta: float) -> float:
    """Asymptotic Singleton bound: R <= 1 - delta."""
    return max(0.0, 1.0 - delta)
