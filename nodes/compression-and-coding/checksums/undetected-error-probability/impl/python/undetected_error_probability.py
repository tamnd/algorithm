# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/undetected-error-probability/. The authors are listed in prov/SD1VWV.jsonl.

"""Probability of undetected error of a CRC code on a binary symmetric channel.

A generator G is an int with bit i the coefficient of x^i, of degree r with
G(0) = 1. The code of length n is the set of multiples of G of degree < n,
of dimension k = n - r. An error is missed when it is a nonzero codeword.
"""

import math
import random
from fractions import Fraction


def deg(a: int) -> int:
    return a.bit_length() - 1


def syndromes(g: int, n: int) -> list[int]:
    """s_i = x^i mod G for i < n."""
    r = deg(g)
    out, s = [], 1
    for _ in range(n):
        out.append(s)
        s <<= 1
        if s >> r:
            s ^= g
    return out


def weight_distribution(g: int, n: int) -> list[int]:
    """A[i] = number of codewords of weight i, by a Gray-code walk over all
    2^k codewords G*Q with deg Q < k."""
    k = n - deg(g)
    a = [0] * (n + 1)
    word = 0
    a[0] = 1
    for m in range(1, 1 << k):
        bit = (m & -m).bit_length() - 1
        word ^= g << bit
        a[word.bit_count()] += 1
    return a


def dual_weight_distribution(g: int, n: int) -> list[int]:
    """B[i] for the dual code, which has 2^r words. The dual word for a
    vector u of r bits has bit i equal to the parity of u AND s_i. Column j
    of the parity-check matrix is the n-bit mask of the i with bit j of s_i
    set; the dual words are the XORs of sets of these masks."""
    r = deg(g)
    s = syndromes(g, n)
    cols = [sum(1 << i for i in range(n) if (s[i] >> j) & 1) for j in range(r)]
    b = [0] * (n + 1)
    word = 0
    b[0] = 1
    for m in range(1, 1 << r):
        bit = (m & -m).bit_length() - 1
        word ^= cols[bit]
        b[word.bit_count()] += 1
    return b


def krawtchouk(n: int, j: int, i: int) -> int:
    return sum((-1) ** t * math.comb(i, t) * math.comb(n - i, j - t) for t in range(j + 1))


def macwilliams(b: list[int], n: int, dual_size: int) -> list[int]:
    """Weight distribution of a code from that of its dual:
    A_j = (1 / |dual|) * sum_i B_i K_j(i)."""
    out = []
    for j in range(n + 1):
        total = sum(b[i] * krawtchouk(n, j, i) for i in range(n + 1))
        assert total % dual_size == 0
        out.append(total // dual_size)
    return out


def p_ud(a: list[int], n: int, p):
    """P_ud(p) = sum over i >= 1 of A_i p^i (1 - p)^(n - i)."""
    return sum(a[i] * p**i * (1 - p) ** (n - i) for i in range(1, n + 1))


def p_ud_dual(b: list[int], n: int, r: int, p):
    """P_ud(p) = 2^-r sum_i B_i (1 - 2p)^i - (1 - p)^n."""
    if isinstance(p, Fraction):
        scale = Fraction(1, 2**r)
    else:
        scale = 2.0**-r
    return scale * sum(b[i] * (1 - 2 * p) ** i for i in range(n + 1)) - (1 - p) ** n


def monte_carlo(g: int, n: int, p: float, trials: int, seed: int) -> float:
    """Fraction of trials in which a binary symmetric channel with flip
    probability p gives a nonzero error that G divides. The flipped positions
    are drawn by geometric gaps, which has the same law as n independent
    flips."""
    rng = random.Random(seed)
    s = syndromes(g, n)
    log_q = math.log1p(-p)
    missed = 0
    for _ in range(trials):
        syn, flips, pos = 0, 0, -1
        while True:
            pos += 1 + int(math.log(1.0 - rng.random()) / log_q)
            if pos >= n:
                break
            syn ^= s[pos]
            flips += 1
        if flips and syn == 0:
            missed += 1
    return missed / trials


def worst_p(b: list[int], n: int, r: int, points: int = 2000) -> tuple[float, float]:
    """The largest P_ud on a grid of p in (0, 1/2], and the p where it occurs."""
    best = (0.0, 0.0)
    for t in range(1, points + 1):
        p = 0.5 * t / points
        v = p_ud_dual(b, n, r, p)
        if v > best[0]:
            best = (v, p)
    return best


def is_proper(b: list[int], n: int, r: int, points: int = 2000) -> bool:
    """A code is proper when P_ud does not decrease on [0, 1/2]. Checked on a
    grid, with a small tolerance for rounding."""
    prev = 0.0
    for t in range(1, points + 1):
        v = p_ud_dual(b, n, r, 0.5 * t / points)
        if v < prev - 1e-15:
            return False
        prev = v
    return True
