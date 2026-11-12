# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/channel-capacity/. The authors are listed in prov/MBQ0RF.jsonl.
"""Channel capacity of a discrete memoryless channel by the Blahut-Arimoto algorithm.

A channel is a matrix W with one row per input x and one column per output y, where
W[x][y] = P(Y = y | X = x) and each row sums to 1. The capacity is the largest mutual
information I(X; Y) over all input laws r, in bits per channel use.
"""

import math
from typing import List, Sequence, Tuple

Matrix = Sequence[Sequence[float]]


def mutual_information(r: Sequence[float], w: Matrix) -> float:
    """I(X; Y) in bits for the input law r: sum over x, y of r(x) W(y|x) log2(W(y|x) / q(y))."""
    ny = len(w[0])
    q = [sum(r[x] * w[x][y] for x in range(len(w))) for y in range(ny)]
    total = 0.0
    for x, row in enumerate(w):
        for y, p in enumerate(row):
            if r[x] > 0 and p > 0:
                total += r[x] * p * math.log2(p / q[y])
    return total


def blahut_arimoto(w: Matrix, tol: float = 1e-12, max_iter: int = 100000) -> Tuple[float, List[float], int]:
    """Return (capacity in bits, a capacity-achieving input law, number of iterations).

    Each step computes the output law q = r W and, for each input x, the divergence
    D_x = D(W(.|x) || q). With c(x) = 2^(D_x) the step keeps the bounds
        log2 sum_x r(x) c(x)  <=  C  <=  log2 max_x c(x),
    and updates r(x) <- r(x) c(x) / sum_x' r(x') c(x'). It stops when the gap is below tol.
    Cost per step: O(|X| |Y|).
    """
    nx, ny = len(w), len(w[0])
    r = [1.0 / nx] * nx
    lower = upper = 0.0
    for it in range(1, max_iter + 1):
        q = [sum(r[x] * w[x][y] for x in range(nx)) for y in range(ny)]
        d = []
        for x in range(nx):
            s = 0.0
            for y in range(ny):
                if w[x][y] > 0:
                    s += w[x][y] * math.log2(w[x][y] / q[y])
            d.append(s)
        c = [2.0 ** dx for dx in d]
        z = sum(r[x] * c[x] for x in range(nx))
        lower = math.log2(z)
        upper = math.log2(max(c))
        if upper - lower < tol:
            return lower, r, it
        r = [r[x] * c[x] / z for x in range(nx)]
    return lower, r, max_iter


def bsc(p: float) -> List[List[float]]:
    return [[1 - p, p], [p, 1 - p]]


def bec(eps: float) -> List[List[float]]:
    """Outputs 0, 1 and the erasure."""
    return [[1 - eps, 0.0, eps], [0.0, 1 - eps, eps]]


def z_channel(p: float) -> List[List[float]]:
    """Input 0 always arrives as 0; input 1 arrives as 0 with probability p."""
    return [[1.0, 0.0], [p, 1 - p]]


def z_channel_capacity(p: float) -> float:
    """Closed form log2(1 + (1 - p) p^(p / (1 - p))) for 0 <= p < 1."""
    if p == 0:
        return 1.0
    return math.log2(1.0 + (1.0 - p) * p ** (p / (1.0 - p)))
