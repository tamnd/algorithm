# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-grid-quadrature/. The authors are listed in prov/W6G1K4.jsonl.

import math
from fractions import Fraction
from itertools import product
from typing import Callable, Dict, Hashable, Iterator, List, Sequence, Tuple

Rule = Callable[[int], List[Tuple[Hashable, object, object]]]


def points_at_level(i: int) -> int:
    """m_1 = 1 and m_i = 2^(i-1) + 1 for i >= 2: the nested Clenshaw-Curtis sizes."""
    if i < 1:
        raise ValueError("level must be >= 1")
    return 1 if i == 1 else 2 ** (i - 1) + 1


def clenshaw_curtis_rule(i: int) -> List[Tuple[Fraction, float, float]]:
    """Level-i Clenshaw-Curtis rule on [0, 1] as (key, node, weight) triples.

    Node j of m = 2^(i-1) + 1 points is sin^2(pi j / (2 n)), n = m - 1, the
    image of cos(pi j / n) under x = (1 - t)/2, computed without cancellation;
    level 1 is the midpoint rule. The key Fraction(j, n) identifies the point
    across levels, so nested points merge exactly. Exact for polynomials of
    degree m (m odd) and so for degree 2i - 1. Cost: O(m^2).
    """
    m = points_at_level(i)
    if m == 1:
        return [(Fraction(1, 2), 0.5, 1.0)]
    n = m - 1
    out = []
    for j in range(m):
        s = 0.0
        for k in range(1, n // 2 + 1):
            bk = 1.0 if 2 * k == n else 2.0
            s += bk / (4 * k * k - 1) * math.cos(2 * k * j * math.pi / n)
        cj = 1.0 if j in (0, n) else 2.0
        w = cj / n * (1 - s) / 2  # halved for [0, 1]
        key = Fraction(j, n)  # reduced, so a shared point gets the same float at every level
        x = 0.5 if 2 * key == 1 else math.sin(math.pi * key.numerator / (2 * key.denominator)) ** 2
        out.append((key, x, w))
    return out


def newton_cotes_rule(i: int) -> List[Tuple[Fraction, Fraction, Fraction]]:
    """Level-i closed Newton-Cotes rule on [0, 1] with m_i equispaced points, in exact rationals.

    Nested like Clenshaw-Curtis and exact for degree m (m odd) >= 2i - 1, but
    with negative weights from m = 9 on. For exact-arithmetic tests. Cost: O(m^3).
    """
    m = points_at_level(i)
    if m == 1:
        return [(Fraction(1, 2), Fraction(1, 2), Fraction(1))]
    xs = [Fraction(j, m - 1) for j in range(m)]
    # solve sum_j w_j x_j^k = 1/(k+1), k = 0..m-1, by exact Gaussian elimination
    M = [[x ** k for x in xs] + [Fraction(1, k + 1)] for k in range(m)]
    for c in range(m):
        p = next(r for r in range(c, m) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(m):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [u - f * v for u, v in zip(M[r], M[c])]
    return [(xs[j], xs[j], M[j][m] / M[j][j]) for j in range(m)]


def multi_indices(s: int, lo: int, hi: int) -> Iterator[Tuple[int, ...]]:
    """All i in N^s with i_j >= 1 and lo <= |i| <= hi, by an odometer (no recursion)."""
    i = [1] * s
    total = s
    if total > hi:
        return
    while True:
        if total >= lo:
            yield tuple(i)
        j = 0
        while j < s:
            if total < hi:
                i[j] += 1
                total += 1
                break
            total -= i[j] - 1
            i[j] = 1
            j += 1
        else:
            return


def sparse_grid(s: int, q: int, rule: Rule = clenshaw_curtis_rule) -> List[Tuple[Tuple, Tuple, object]]:
    """Points and weights of the Smolyak rule A(q, s) on [0, 1]^s.

    A(q, s) = sum over q - s + 1 <= |i| <= q of
    (-1)^(q - |i|) C(s - 1, q - |i|) U^(i_1) x ... x U^(i_s),
    with equal points merged by their keys. Returns (key, point, weight).
    Precondition: s >= 1, q >= s, and rule(i) a nested family. Cost: the sum
    of the component grid sizes, plus O(m^2) per one-dimensional rule.
    """
    if s < 1 or q < s:
        raise ValueError("need s >= 1 and q >= s")
    rules = {i: rule(i) for i in range(1, q - s + 2)}
    # @line L1
    W: Dict[Tuple, list] = {}
    # @line L2
    for idx in multi_indices(s, max(s, q - s + 1), q):
        # @line L3
        kappa = (-1) ** (q - sum(idx)) * math.comb(s - 1, q - sum(idx))
        # @line L4
        for combo in product(*(rules[i] for i in idx)):
            key = tuple(c[0] for c in combo)
            w = kappa
            for c in combo:
                w = w * c[2]
            # @line L5
            if key in W:
                W[key][1] = W[key][1] + w
            else:
                W[key] = [tuple(c[1] for c in combo), w]
    return [(k, v[0], v[1]) for k, v in W.items()]


def smolyak_quadrature(
    f: Callable[[Tuple], object],
    a: Sequence[float],
    b: Sequence[float],
    q: int,
    rule: Rule = clenshaw_curtis_rule,
) -> object:
    """Smolyak sparse grid approximation of the integral of f over the box [a, b].

    Level q >= s = len(a); the rule A(q, s) is exact for all polynomials of
    total degree <= 2(q - s) + 1 when rule(i) is exact for degree 2i - 1.
    With b_j < a_j the result is signed like an iterated integral; a_j = b_j
    gives 0 without evaluations. Cost: one evaluation of f per distinct
    sparse grid point, O(2^l l^(s-1)) points for l = q - s.
    """
    s = len(a)
    if len(b) != s:
        raise ValueError("a and b must have the same length")
    if any(math.isinf(x) for x in list(a) + list(b)):
        raise ValueError("finite box required")
    vol = 1
    for lo, hi in zip(a, b):
        vol = vol * (hi - lo)
    grid = sparse_grid(s, q, rule)
    if vol == 0:
        return 0 * vol
    terms = []
    # @line L6
    for _, u, w in grid:
        x = tuple(lo + (hi - lo) * uj for lo, hi, uj in zip(a, b, u))
        terms.append(w * f(x))
    if all(isinstance(t, Fraction) or isinstance(t, int) for t in terms):
        return vol * sum(terms)
    return vol * math.fsum(terms)
