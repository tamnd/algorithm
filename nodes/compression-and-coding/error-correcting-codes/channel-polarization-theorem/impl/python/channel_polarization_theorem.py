# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/channel-polarization-theorem/. The authors are listed in prov/Q74BAQ.jsonl.
"""Numerical checks of channel polarization.

A binary-input discrete memoryless channel W is a pair of rows (W[0], W[1]); W[x][y] is the
probability of output y given input x. The polar transform is x = u F^(kron n) with
F = [[1, 0], [1, 1]] and no bit reversal. The synthetic channel W_N^(i) has input u_i and
output (y, u_0 .. u_(i-1)), with u_(i+1) .. u_(N-1) uniform and unknown.
"""

import itertools
import math
from typing import Dict, List, Sequence, Tuple

Channel = Tuple[List[float], List[float]]


def bec(eps) -> Channel:
    """BEC(eps) with outputs 0, 1 and 2 (the erasure)."""
    return ([1 - eps, 0 * eps, eps], [0 * eps, 1 - eps, eps])


def bsc(p) -> Channel:
    return ([1 - p, p], [p, 1 - p])


def minus(w: Channel) -> Channel:
    """W^-(y1, y2 | u1) = 1/2 sum_u2 W(y1 | u1 xor u2) W(y2 | u2). Output index y1 * m + y2."""
    m = len(w[0])
    rows: List[List[float]] = [[], []]
    for u1 in (0, 1):
        for y1 in range(m):
            for y2 in range(m):
                rows[u1].append(sum(w[u1 ^ u2][y1] * w[u2][y2] for u2 in (0, 1)) / 2)
    return rows[0], rows[1]


def plus(w: Channel) -> Channel:
    """W^+(y1, y2, u1 | u2) = 1/2 W(y1 | u1 xor u2) W(y2 | u2). Output index (y1 m + y2) 2 + u1."""
    m = len(w[0])
    rows: List[List[float]] = [[], []]
    for u2 in (0, 1):
        for y1 in range(m):
            for y2 in range(m):
                for u1 in (0, 1):
                    rows[u2].append(w[u1 ^ u2][y1] * w[u2][y2] / 2)
    return rows[0], rows[1]


def bhattacharyya(w: Channel) -> float:
    """Z(W) = sum_y sqrt(W(y | 0) W(y | 1))."""
    return sum(math.sqrt(a * b) for a, b in zip(w[0], w[1]))


def symmetric_capacity(w: Channel) -> float:
    """I(W) in bits for a uniform input."""
    total = 0.0
    for x in (0, 1):
        for y, p in enumerate(w[x]):
            if p > 0:
                q = (w[0][y] + w[1][y]) / 2
                total += 0.5 * p * math.log2(p / q)
    return total


def synthetic_channel(w: Channel, n: int, i: int) -> Dict[tuple, List[float]]:
    """W_N^(i) by brute force from the definition: maps (y, u_0..u_(i-1)) to [P(. | 0), P(. | 1)]."""
    big = 1 << n
    m = len(w[0])
    out: Dict[tuple, List[float]] = {}
    for u in itertools.product((0, 1), repeat=big):
        x = polar_transform(list(u))
        for y in itertools.product(range(m), repeat=big):
            p = 1.0
            for xj, yj in zip(x, y):
                p *= w[xj][yj]
            if p == 0:
                continue
            key = (y, u[:i])
            out.setdefault(key, [0.0, 0.0])[u[i]] += p / 2 ** (big - 1)
    return out


def bhattacharyya_of_table(t: Dict[tuple, List[float]]) -> float:
    return sum(math.sqrt(a * b) for a, b in t.values())


def polar_transform(u: List[int]) -> List[int]:
    x = list(u)
    h = 1
    while h < len(x):
        for s in range(0, len(x), 2 * h):
            for j in range(s, s + h):
                x[j] ^= x[j + h]
        h *= 2
    return x


def bec_z(n: int, eps):
    """Z(W_N^(i)) on BEC(eps) for i = 0..N-1. Bit b of i, from the most significant one,
    applies z -> 2z - z^2 (b = 0) or z -> z^2 (b = 1)."""
    z = [eps]
    for _ in range(n):
        z = [w for v in z for w in (2 * v - v * v, v * v)]
    return z


def bec_log2_z(n: int, eps: float) -> List[float]:
    """log2 of bec_z(n, eps), computed in the log domain so that tiny values do not underflow."""
    lz = [math.log2(eps)]
    for _ in range(n):
        nxt = []
        for v in lz:
            nxt.append(v + math.log2(2 - 2 ** v))
            nxt.append(2 * v)
        lz = nxt
    return lz


def polarization_fractions(n: int, eps: float, delta: float) -> Tuple[float, float, float]:
    """Fractions of indices with Z < delta, Z > 1 - delta, and in between, on BEC(eps)."""
    z = bec_z(n, eps)
    big = len(z)
    good = sum(v < delta for v in z) / big
    bad = sum(v > 1 - delta for v in z) / big
    return good, bad, 1 - good - bad


def fraction_below(n: int, eps: float, beta: float) -> float:
    """Fraction of indices with Z <= 2^(-N^beta) on BEC(eps)."""
    lz = bec_log2_z(n, eps)
    limit = -((1 << n) ** beta)
    return sum(v <= limit for v in lz) / len(lz)


def channel_tree(w: Channel, n: int) -> List[Channel]:
    """All W_N^(i), i = 0..N-1, by the recursion W -> (W^-, W^+), first bit most significant."""
    chans = [w]
    for _ in range(n):
        chans = [c for v in chans for c in (minus(v), plus(v))]
    return chans


def same_channel(a: Sequence[float], b: Sequence[float], tol: float = 1e-12) -> bool:
    return len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))
