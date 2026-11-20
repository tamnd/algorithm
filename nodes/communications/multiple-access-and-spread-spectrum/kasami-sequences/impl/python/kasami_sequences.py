# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kasami-sequences/. The authors are listed in prov/H5NT6J.jsonl.

"""The small set of Kasami sequences, with integer correlations.

A polynomial over GF(2) is the list of its exponents, for example [6, 1, 0]
for x^6 + x + 1. For even n, let u be an m-sequence of period N = 2^n - 1 and
w = u decimated by s = 2^(n/2) + 1, which has period 2^(n/2) - 1. The small
Kasami set is u together with u XOR (w shifted by t) for
t = 0, ..., 2^(n/2) - 2: 2^(n/2) sequences of period N.
"""

import math


def mseq(exps: list[int], state: list[int] | None = None) -> list[int]:
    """One period of the recurrence s[k + n] = XOR over the exponents i < n of s[k + i]."""
    n = max(exps)
    s = list(state) if state is not None else [1] + [0] * (n - 1)
    taps = [i for i in exps if i < n]
    while len(s) < (1 << n) - 1:
        k = len(s) - n
        bit = 0
        for i in taps:
            bit ^= s[k + i]
        s.append(bit)
    return s


def decimate(s: list[int], q: int) -> list[int]:
    """The sequence s[q k mod N], k = 0, ..., N - 1."""
    n = len(s)
    return [s[(q * k) % n] for k in range(n)]


def least_period(s: list[int]) -> int:
    """The least p > 0 with s[k] = s[(k + p) mod N] for all k."""
    n = len(s)
    for p in range(1, n + 1):
        if n % p == 0 and all(s[k] == s[(k + p) % n] for k in range(n)):
            return p
    return n


def kasami_small(u: list[int]) -> list[list[int]]:
    """The small Kasami set of an m-sequence u of even degree n (as bit lists)."""
    big = len(u)
    n = (big + 1).bit_length() - 1
    if (1 << n) - 1 != big or n % 2:
        raise ValueError("u must have period 2^n - 1 with n even")
    s = (1 << (n // 2)) + 1
    w = decimate(u, s)  # @line L1
    fam = [list(u)]  # @line L2
    for t in range((1 << (n // 2)) - 1):  # @line L3
        fam.append([u[k] ^ w[(k + t) % big] for k in range(big)])  # @line L4
    return fam


def xcorr(a: list[int], b: list[int], t: int) -> int:
    """Periodic correlation sum over k of (-1)^(a[k] XOR b[k + t])."""
    n = len(a)
    return n - 2 * sum(a[k] ^ b[(k + t) % n] for k in range(n))


def max_correlation(fam: list[list[int]]) -> int:
    """theta_max over all pairs and shifts, except the peaks of a sequence with itself at shift 0."""
    best = 0
    for i, a in enumerate(fam):
        for j in range(i, len(fam)):
            for t in range(len(a)):
                if i == j and t == 0:
                    continue
                best = max(best, abs(xcorr(a, fam[j], t)))  # @line L5
    return best


def welch_sequence_bound(m: int, n: int) -> float:
    """The Welch bound N sqrt((M - 1) / (M N - 1)) on theta_max for M sequences of length N and energy N."""
    return n * math.sqrt((m - 1) / (m * n - 1))
