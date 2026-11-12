# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/list-decoding/. The authors are listed in prov/4JPZFM.jsonl.
"""List decoding: the brute force decoder, the Johnson bound, and list decoding capacity.

A code is a list of codewords, each a tuple of symbols of the same length n.
The list decoding problem with radius e asks for every codeword within Hamming
distance e of a received word y.
"""

import math


def hamming_distance(a: tuple[int, ...] | list[int], b: tuple[int, ...] | list[int]) -> int:
    return sum(1 for x, y in zip(a, b) if x != y)


def list_decode_brute_force(code: list[tuple[int, ...]], y: tuple[int, ...] | list[int],
                            e: int) -> list[tuple[int, ...]]:
    """All codewords within distance e of y, in the order of the code.

    Precondition: every codeword has the length of y. Cost: O(|code| n).
    """
    return [c for c in code if hamming_distance(c, y) <= e]


def johnson_list_bound(n: int, d: int, e: int) -> int | None:
    """An upper bound on the list size for radius e in any code of length n and distance d.

    With agreement a = n - e and s = n - d, the bound is n (a - s) / (a^2 - n s),
    valid when a^2 > n s, that is e < n - sqrt(n (n - d)). It does not depend on
    the alphabet size. Returns None when the condition fails.
    """
    a, s = n - e, n - d
    if a * a <= n * s:
        return None
    return (n * (a - s)) // (a * a - n * s)


def johnson_radius(delta: float, q: int | None = None) -> float:
    """The Johnson radius as a fraction of n for relative distance delta.

    For an alphabet of size q, J_q = (1 - 1/q) (1 - sqrt(1 - q delta / (q - 1))).
    With q = None (any alphabet), J = 1 - sqrt(1 - delta).
    """
    if q is None:
        return 1 - math.sqrt(1 - delta)
    theta = 1 - 1 / q
    return theta * (1 - math.sqrt(max(0.0, 1 - delta / theta)))


def entropy_q(p: float, q: int) -> float:
    """The q-ary entropy h_q(p) = p log_q(q - 1) - p log_q p - (1 - p) log_q (1 - p), for 0 <= p <= 1 - 1/q."""
    if p == 0:
        return 0.0
    out = p * math.log(q - 1) - p * math.log(p)
    if p < 1:
        out -= (1 - p) * math.log(1 - p)
    return out / math.log(q)


def capacity_radius(rate: float, q: int) -> float:
    """The list decoding capacity: the p in [0, 1 - 1/q] with h_q(p) = 1 - rate, by bisection.

    Codes of rate rate <= 1 - h_q(p) - eps exist that are list decodable to radius p n
    with lists of size O(1 / eps); above 1 - h_q(p) the lists are exponential.
    """
    lo, hi = 0.0, 1 - 1 / q
    for _ in range(100):
        mid = (lo + hi) / 2
        if entropy_q(mid, q) < 1 - rate:
            lo = mid
        else:
            hi = mid
    return lo
