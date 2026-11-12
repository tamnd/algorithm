# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hamming-bound/. The authors are listed in prov/39271D.jsonl.

"""The Hamming (sphere packing) bound and tests of perfectness.

A binary word of length n is an int whose bit i is coordinate i. A q-ary word
is a tuple of ints in range(q). All counts are exact integers.
"""

from itertools import combinations, product
from math import comb, log


def volume(q: int, n: int, r: int) -> int:
    """V_q(n, r): the number of words of length n within distance r of a fixed word."""
    return sum(comb(n, i) * (q - 1) ** i for i in range(min(r, n) + 1))


def hamming_bound(q: int, n: int, d: int) -> int:
    """floor(q^n / V_q(n, t)) with t = floor((d - 1) / 2): an upper bound on A_q(n, d)."""
    t = (d - 1) // 2
    return q ** n // volume(q, n, t)


def meets_hamming_bound(q: int, n: int, size: int, d: int) -> bool:
    """True when a code with these parameters would be perfect: size * V_q(n, t) = q^n."""
    return size * volume(q, n, (d - 1) // 2) == q ** n


def perfect_parameter_sets(q: int, n_max: int, t_max: int) -> list[tuple[int, int, int]]:
    """All (n, t, k) with 1 <= t <= t_max, 2t + 1 < n <= n_max and V_q(n, t) = q^(n - k).

    These are the lengths where the sphere packing condition is met by a code of
    q^k words. The repetition codes (n = 2t + 1) are left out.
    """
    out = []
    for t in range(1, t_max + 1):
        for n in range(2 * t + 2, n_max + 1):
            v, r = volume(q, n, t), 0
            while v % q == 0:
                v, r = v // q, r + 1
            if v == 1:
                out.append((n, t, n - r))
    return out


def hamming_code_words(r: int) -> list[int]:
    """The binary Hamming code of length 2^r - 1: the words whose set positions XOR to 0.

    Position i (0-based) has the parity-check column i + 1 written in binary.
    """
    n = 2 ** r - 1
    words = []
    for x in range(2 ** n):
        s, y, i = 0, x, 1
        while y:
            if y & 1:
                s ^= i
            y >>= 1
            i += 1
        if s == 0:
            words.append(x)
    return words


def min_distance_linear(words: list[int]) -> int:
    """Minimum distance of a binary linear code given by all its words: the least nonzero weight."""
    return min(w.bit_count() for w in words if w)


def binary_syndromes_distinct(h_columns: list[int], t: int) -> tuple[bool, int]:
    """For a binary linear code with parity-check columns h_columns (ints), check that
    the error patterns of weight at most t have distinct syndromes.

    Returns (all distinct, number of patterns). Distinct syndromes mean the balls of
    radius t around the codewords are disjoint. If also the number of patterns is
    2^(n - k), the balls fill the space and the code is perfect.
    """
    n = len(h_columns)
    seen = set()
    count = 0
    for w in range(t + 1):
        for pos in combinations(range(n), w):
            s = 0
            for p in pos:
                s ^= h_columns[p]
            if s in seen:
                return False, count
            seen.add(s)
            count += 1
    return True, count


def qary_linear_code(gen: list[tuple[int, ...]], q: int) -> list[tuple[int, ...]]:
    """All q^k words m G of the linear code over GF(q), q prime, with generator rows gen."""
    k, n = len(gen), len(gen[0])
    words = []
    for m in product(range(q), repeat=k):
        words.append(tuple(sum(m[i] * gen[i][j] for i in range(k)) % q for j in range(n)))
    return words


def qary_min_distance(words: list[tuple[int, ...]]) -> int:
    """Minimum distance of a linear code: the least weight of a nonzero word."""
    return min(sum(1 for a in w if a) for w in words if any(w))


def entropy_q(x: float, q: int) -> float:
    """The q-ary entropy function h_q(x) for 0 <= x <= 1."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return log(q - 1, q)
    return x * log(q - 1, q) - x * log(x, q) - (1 - x) * log(1 - x, q)


def hamming_rate_bound(delta: float, q: int = 2) -> float:
    """Asymptotic Hamming bound: R <= 1 - h_q(delta / 2), for 0 <= delta <= 1."""
    return max(0.0, 1.0 - entropy_q(delta / 2, q))
