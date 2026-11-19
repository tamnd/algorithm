# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-features/. The authors are listed in prov/AZKQ3W.jsonl.

"""Delta and delta-delta (acceleration) coefficients of a sequence of feature vectors.

The regression formula of HTK:

    d_t = sum_{n=1}^{Theta} n (c_{t+n} - c_{t-n}) / (2 sum_{n=1}^{Theta} n^2),

with Theta = 2 by default. At the edges the first and the last frames are repeated,
so c_{t} for t < 0 is c_0 and for t >= T is c_{T-1}. The delta-deltas are the
deltas of the deltas, with the same formula. Thirteen static coefficients give a
vector of 13 + 13 + 13 = 39 numbers per frame.
"""

from typing import List, Sequence


def deltas(c: Sequence[Sequence[float]], theta: int = 2) -> List[List[float]]:
    """The deltas of T frames of D values each. Returns T frames of D values."""
    if theta < 1:
        raise ValueError("theta must be at least 1")
    t_count = len(c)
    if t_count == 0:
        return []
    dim = len(c[0])
    denom = 2.0 * sum(n * n for n in range(1, theta + 1))  # @line L1
    out = []
    for t in range(t_count):
        row = []
        for j in range(dim):
            acc = 0.0
            for n in range(1, theta + 1):
                ahead = c[min(t + n, t_count - 1)][j]  # @line L2
                behind = c[max(t - n, 0)][j]
                acc += n * (ahead - behind)  # @line L3
            row.append(acc / denom)  # @line L4
        out.append(row)
    return out


def add_deltas(c: Sequence[Sequence[float]], theta: int = 2) -> List[List[float]]:
    """Each frame becomes [static, delta, delta-delta], 3 D values."""
    d = deltas(c, theta)  # @line L5
    dd = deltas(d, theta)  # @line L6
    return [list(a) + b + e for a, b, e in zip(c, d, dd)]
