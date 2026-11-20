# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gold-sequences/. The authors are listed in prov/BGG18W.jsonl.

"""Gold sequences from a preferred pair of m-sequences, with integer correlations.

A polynomial over GF(2) is the list of its exponents, for example [5, 2, 0]
for x^5 + x^2 + 1. The m-sequence of f satisfies
s[k + n] = XOR over the exponents i < n of s[k + i].
The Gold family of a preferred pair (u, v) of period N = 2^n - 1 is
u, v and u XOR (v shifted by t) for t = 0, ..., N - 1: N + 2 sequences.
"""


def mseq(exps: list[int], state: list[int] | None = None) -> list[int]:
    """One period of the recurrence of f, from the state 1, 0, ..., 0 by default."""
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


def shift(s: list[int], t: int) -> list[int]:
    """The cyclic shift s[(k + t) mod N]."""
    n = len(s)
    return [s[(k + t) % n] for k in range(n)]


def gold_family(u: list[int], v: list[int]) -> list[list[int]]:
    """The N + 2 sequences u, v and u XOR shift(v, t) for t = 0, ..., N - 1 (as bits)."""
    n = len(u)
    if len(v) != n:
        raise ValueError("lengths differ")
    fam = [list(u), list(v)]  # @line L1
    for t in range(n):  # @line L2
        fam.append([u[k] ^ v[(k + t) % n] for k in range(n)])  # @line L3
    return fam


def xcorr(a: list[int], b: list[int], t: int) -> int:
    """Periodic correlation sum over k of (-1)^(a[k] XOR b[k + t]) for two bit sequences."""
    n = len(a)
    return n - 2 * sum(a[k] ^ b[(k + t) % n] for k in range(n))  # @line L4


def correlation_values(a: list[int], b: list[int]) -> set[int]:
    """The set of values of the periodic cross-correlation of a and b over all shifts."""
    return {xcorr(a, b, t) for t in range(len(a))}


def max_correlation(fam: list[list[int]]) -> int:
    """theta_max: the largest |correlation| over all pairs and shifts, except the peaks at shift 0 of a with a."""
    best = 0
    for i, a in enumerate(fam):
        for j in range(i, len(fam)):
            b = fam[j]
            for t in range(len(a)):
                if i == j and t == 0:
                    continue
                best = max(best, abs(xcorr(a, b, t)))  # @line L5
    return best


def gold_t(n: int) -> int:
    """t(n) = 1 + 2^floor((n + 2) / 2)."""
    return 1 + (1 << ((n + 2) // 2))


def is_preferred_pair(u: list[int], v: list[int], n: int) -> bool:
    """True if the cross-correlation of u and v takes exactly the values -1, -t(n) and t(n) - 2."""
    t = gold_t(n)
    return correlation_values(u, v) == {-1, -t, t - 2}
