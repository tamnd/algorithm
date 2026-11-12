# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-flipping-decoding/. The authors are listed in prov/8C2WTA.jsonl.

"""Hard-decision decoders for LDPC codes on the Tanner graph of H.

bit_flip_decode is Gallager's bit flipping: each round, flip every bit that
sits in the largest number of unsatisfied checks. gallager_a and gallager_b
are Gallager's two hard message-passing algorithms. weighted_bit_flip is the
weighted rule of Kou, Lin and Fossorier (2001), which also uses |y|.
gallager_a_de is the density evolution recursion of algorithm A on a
(dv, dc)-regular ensemble over BSC(p). Bits are 0 and 1; H is a list of rows.
"""

from math import comb
from typing import Dict, List, Sequence, Tuple


def _adjacency(h: Sequence[Sequence[int]]) -> Tuple[List[List[int]], List[List[int]]]:
    m, n = len(h), len(h[0])
    chk = [[j for j in range(n) if h[i][j]] for i in range(m)]
    var = [[i for i in range(m) if h[i][j]] for j in range(n)]
    return chk, var


def bit_flip_decode(h: Sequence[Sequence[int]], hard: Sequence[int],
                    max_iter: int) -> Tuple[List[int], int, bool]:
    """Return (word, rounds used, syndrome is zero). Theta(E) per round."""
    chk, var = _adjacency(h)
    c = list(hard)  # @line L1
    for it in range(max_iter + 1):
        syn = [sum(c[j] for j in row) & 1 for row in chk]  # @line L2
        if not any(syn):  # @line L3
            return c, it, True
        if it == max_iter:
            break
        count = [sum(syn[i] for i in col) for col in var]  # @line L4
        top = max(count)  # @line L5
        for j in range(len(c)):
            if count[j] == top:
                c[j] ^= 1  # @line L6
    return c, max_iter, False  # @line L7


def gallager_b(h: Sequence[Sequence[int]], hard: Sequence[int], max_iter: int,
               b: int) -> Tuple[List[int], int, bool]:
    """Gallager's algorithm B with threshold b: a variable sends the opposite
    of its received bit to a check when at least b of its other checks say so.
    b = dv - 1 on a dv-regular code is algorithm A."""
    chk, var = _adjacency(h)
    n = len(hard)
    v2c: Dict[Tuple[int, int], int] = {(i, j): hard[j] for i in range(len(chk)) for j in chk[i]}
    c2v: Dict[Tuple[int, int], int] = {}
    word = list(hard)
    for it in range(1, max_iter + 1):
        for i, row in enumerate(chk):
            total = sum(v2c[(i, j)] for j in row) & 1
            for j in row:
                c2v[(i, j)] = total ^ v2c[(i, j)]  # parity of the other bits
        for j in range(n):
            ones = sum(c2v[(i, j)] for i in var[j])
            zeros = len(var[j]) - ones
            vote = ones + hard[j] - (zeros + 1 - hard[j])
            word[j] = hard[j] if vote == 0 else int(vote > 0)  # majority, ties keep the channel
            for i in var[j]:
                against = sum(1 for k in var[j] if k != i and c2v[(k, j)] != hard[j])
                v2c[(i, j)] = 1 - hard[j] if against >= b else hard[j]
        if not any(sum(word[j] for j in row) & 1 for row in chk):
            return word, it, True
    return word, max_iter, False


def gallager_a(h: Sequence[Sequence[int]], hard: Sequence[int],
               max_iter: int) -> Tuple[List[int], int, bool]:
    """Algorithm A: flip the outgoing message only when all other checks agree."""
    chk, var = _adjacency(h)
    dv = max(len(col) for col in var)
    return gallager_b(h, hard, max_iter, dv - 1)


def weighted_bit_flip(h: Sequence[Sequence[int]], y: Sequence[float],
                      max_iter: int) -> Tuple[List[int], int, bool]:
    """Weighted bit flipping for BPSK x = 1 - 2c. Check i has weight
    w_i = min |y_j| over its bits; bit j has E_j = sum over its checks of
    (2 s_i - 1) w_i; flip the one bit with the largest E_j."""
    chk, var = _adjacency(h)
    c = [0 if v >= 0 else 1 for v in y]
    w = [min(abs(y[j]) for j in row) if row else 0.0 for row in chk]
    for it in range(max_iter + 1):
        syn = [sum(c[j] for j in row) & 1 for row in chk]
        if not any(syn):
            return c, it, True
        if it == max_iter:
            break
        e = [sum((2 * syn[i] - 1) * w[i] for i in col) for col in var]
        c[max(range(len(c)), key=e.__getitem__)] ^= 1
    return c, max_iter, False


def gallager_a_de(p: float, dv: int, dc: int, iterations: int) -> float:
    """Error probability of a variable-to-check message after the given
    number of rounds of algorithm A on the (dv, dc) ensemble over BSC(p)."""
    x = p
    for _ in range(iterations):
        good = (1 + (1 - 2 * x) ** (dc - 1)) / 2
        bad = 1 - good
        x = p - p * good ** (dv - 1) + (1 - p) * bad ** (dv - 1)
    return x


def gallager_b_de(p: float, dv: int, dc: int, b: int, iterations: int) -> float:
    """The same recursion for algorithm B with threshold b."""
    x = p
    for _ in range(iterations):
        good = (1 + (1 - 2 * x) ** (dc - 1)) / 2
        bad = 1 - good
        fix = sum(comb(dv - 1, t) * good ** t * bad ** (dv - 1 - t) for t in range(b, dv))
        hurt = sum(comb(dv - 1, t) * bad ** t * good ** (dv - 1 - t) for t in range(b, dv))
        x = p - p * fix + (1 - p) * hurt
    return x


def gallager_a_threshold(dv: int, dc: int, tol: float = 1e-7, iterations: int = 5000) -> float:
    """The largest p for which the recursion goes to zero, by bisection."""
    lo, hi = 0.0, 0.5
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if gallager_a_de(mid, dv, dc, iterations) < 1e-10:
            lo = mid
        else:
            hi = mid
    return lo
