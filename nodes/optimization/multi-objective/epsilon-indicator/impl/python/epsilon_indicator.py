# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epsilon-indicator/. The authors are listed in prov/56A304.jsonl.

"""The additive and multiplicative epsilon indicators of Zitzler et al. (2003), minimization.

    I_eps+(A, B) = max over b in B of min over a in A of max over m of (a_m - b_m)
    I_eps(A, B)  = max over b in B of min over a in A of max over m of a_m / b_m   (positive values)

I_eps+(A, B) is the smallest eps such that every b is weakly dominated by some
a - eps. The unary form uses a reference set R as B. Each call costs
O(p |A| |B|). With int or Fraction input the results are exact.
"""

from fractions import Fraction
from typing import Sequence

Points = Sequence[Sequence]


def eps_additive(a: Points, b: Points):
    return max(min(max(u - v for u, v in zip(x, y)) for x in a) for y in b)


def eps_multiplicative(a: Points, b: Points):
    """All coordinates must be positive."""
    return max(min(max(Fraction(u) / v for u, v in zip(x, y)) for x in a) for y in b)


def weakly_dominates_set(a: Points, b: Points) -> bool:
    return all(any(all(u <= v for u, v in zip(x, y)) for x in a) for y in b)


def better(a: Points, b: Points) -> bool:
    """A is better than B: A weakly dominates B and B does not weakly dominate A."""
    return eps_additive(a, b) <= 0 and eps_additive(b, a) > 0
