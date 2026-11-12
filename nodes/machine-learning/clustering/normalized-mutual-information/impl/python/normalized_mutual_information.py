# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normalized-mutual-information/. The authors are listed in prov/3MRTH1.jsonl.
"""Mutual information of two partitions, its normalized forms (NMI), the expected
mutual information under the permutation model, and the adjusted form (AMI).

Logarithms are natural. The base cancels in NMI and AMI.
"""

from collections import Counter
from math import comb, log, sqrt
from typing import Hashable, Sequence


def contingency(u: Sequence[Hashable], v: Sequence[Hashable]):
    if len(u) != len(v):
        raise ValueError("the two labelings must have the same length")
    return Counter(zip(u, v)), Counter(u), Counter(v)


def entropy_of_labels(u: Sequence[Hashable]) -> float:
    """H(U) = -sum_i (a_i / n) log(a_i / n)."""
    n = len(u)
    return -sum(m / n * log(m / n) for m in Counter(u).values())


def mutual_information(u: Sequence[Hashable], v: Sequence[Hashable]) -> float:
    """I(U, V) = sum_ij (n_ij / n) log(n n_ij / (a_i b_j)) over the nonzero cells."""
    cells, rows, cols = contingency(u, v)
    n = len(u)
    return sum(m / n * log(n * m / (rows[x] * cols[y])) for (x, y), m in cells.items())


def _normalizer(hu: float, hv: float, method: str) -> float:
    if method == "sqrt":
        return sqrt(hu * hv)
    if method == "arithmetic":
        return (hu + hv) / 2
    if method == "max":
        return max(hu, hv)
    if method == "min":
        return min(hu, hv)
    raise ValueError("method must be sqrt, arithmetic, max or min")


def normalized_mutual_information(u, v, method: str = "sqrt") -> float:
    """NMI = I(U, V) / N(H(U), H(V)). The default "sqrt" is the form of Strehl and Ghosh (2002).

    Conventions: 1 when n = 0 or both partitions are one cluster (both entropies 0);
    0 when only the normalizer is 0 (one partition is one cluster, so I = 0).
    """
    if len(u) == 0:
        return 1.0
    hu, hv = entropy_of_labels(u), entropy_of_labels(v)
    if hu == 0 and hv == 0:
        return 1.0
    z = _normalizer(hu, hv, method)
    if z == 0:
        return 0.0
    return mutual_information(u, v) / z


def expected_mutual_information(u: Sequence[Hashable], v: Sequence[Hashable]) -> float:
    """E[I] under the permutation model (Vinh, Epps and Bailey 2010).

    With the row sums a_i and the column sums b_j fixed, the cell n_ij of a random
    arrangement is hypergeometric: P(n_ij = t) = C(b_j, t) C(n - b_j, a_i - t) / C(n, a_i).
    By linearity of expectation, E[I] = sum_ij sum_t P(n_ij = t) (t / n) log(n t / (a_i b_j)).
    The number of terms is at most sum_ij min(a_i, b_j) <= n * min(rows, columns).
    """
    _, rows, cols = contingency(u, v)
    n = len(u)
    total = 0.0
    for a in rows.values():
        for b in cols.values():
            for t in range(max(1, a + b - n), min(a, b) + 1):
                p = comb(b, t) * comb(n - b, a - t) / comb(n, a)
                total += p * (t / n) * log(n * t / (a * b))
    return total


def _same_partition(u, v) -> bool:
    cells, rows, cols = contingency(u, v)
    return len(cells) == len(rows) == len(cols)


def adjusted_mutual_information(u, v, method: str = "arithmetic") -> float:
    """AMI = (I - E[I]) / (N(H(U), H(V)) - E[I]).

    When the denominator is 0, return 1 for equal partitions (for example both one
    cluster, or both all singletons) and 0 otherwise.
    """
    if len(u) == 0:
        return 1.0
    hu, hv = entropy_of_labels(u), entropy_of_labels(v)
    emi = expected_mutual_information(u, v)
    den = _normalizer(hu, hv, method) - emi
    if abs(den) < 1e-15:
        return 1.0 if _same_partition(u, v) else 0.0
    return (mutual_information(u, v) - emi) / den
