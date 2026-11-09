# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schwartz-zippel-lemma/. The authors are listed in prov/B38MAX.jsonl.

"""Exact checks of the Schwartz-Zippel lemma by enumeration.

A polynomial in m variables over Z/qZ is a dict that maps an exponent tuple
(e_1, ..., e_m) to a coefficient in {1, ..., q-1}. The modulus q is a prime
for the lemma (a field); a composite q is allowed only to show that the lemma
fails without the integral domain property.
"""

import itertools
import random
from fractions import Fraction
from typing import Iterable, Sequence

Poly = dict[tuple[int, ...], int]


def normalize(poly: Poly, q: int) -> Poly:
    """Reduce the coefficients mod q and drop the zero terms."""
    out: Poly = {}
    for exps, c in poly.items():
        c %= q
        if c:
            out[exps] = (out.get(exps, 0) + c) % q
            if out[exps] == 0:
                del out[exps]
    return out


def total_degree(poly: Poly) -> int:
    """The total degree of a nonzero polynomial; -1 for the zero polynomial."""
    return max((sum(e) for e in poly), default=-1)


def individual_degrees(poly: Poly, m: int) -> list[int]:
    """The degree of the polynomial in each variable."""
    degs = [0] * m
    for exps in poly:
        for i, e in enumerate(exps):
            degs[i] = max(degs[i], e)
    return degs


def evaluate(poly: Poly, point: Sequence[int], q: int) -> int:
    """The value of the polynomial at a point, mod q."""
    total = 0
    for exps, c in poly.items():
        term = c
        for x, e in zip(point, exps):
            if e:
                term = term * pow(x, e, q) % q
        total = (total + term) % q
    return total


def count_zeros(poly: Poly, S: Sequence[int], m: int, q: int) -> int:
    """The number of points of S^m where the polynomial is zero, by brute force."""
    return sum(1 for pt in itertools.product(S, repeat=m) if evaluate(poly, pt, q) == 0)


def sz_bound(d: int, s: int) -> Fraction:
    """The Schwartz-Zippel bound d/|S| on the fraction of zeros."""
    return Fraction(d, s)


def nonzero_lower_bound(degs: Sequence[int], s: int) -> int:
    """The individual-degree form: at least prod(|S| - d_i) nonzeros if all d_i <= |S|."""
    out = 1
    for d in degs:
        out *= max(s - d, 0)
    return out


def all_polys(m: int, max_deg: int, q: int) -> Iterable[Poly]:
    """Every polynomial over Z/qZ in m variables of total degree at most max_deg."""
    monos = [e for e in itertools.product(range(max_deg + 1), repeat=m) if sum(e) <= max_deg]
    for coeffs in itertools.product(range(q), repeat=len(monos)):
        yield {e: c for e, c in zip(monos, coeffs) if c}


def random_poly(m: int, max_deg: int, q: int, terms: int, rng: random.Random) -> Poly:
    """A random polynomial with at most `terms` monomials of total degree at most max_deg."""
    poly: Poly = {}
    for _ in range(terms):
        exps = [0] * m
        budget = rng.randint(0, max_deg)
        for _ in range(budget):
            exps[rng.randrange(m)] += 1
        poly[tuple(exps)] = rng.randrange(1, q)
    return normalize(poly, q)


def linear_factor_product(roots: Sequence[int], m: int, q: int) -> Poly:
    """The polynomial (x_1 - r_1)(x_1 - r_2)...(x_1 - r_d) in m variables, which meets the bound."""
    coeffs = [1]  # coefficients of the univariate product, lowest degree first
    for r in roots:
        new = [0] * (len(coeffs) + 1)
        for i, c in enumerate(coeffs):
            new[i + 1] = (new[i + 1] + c) % q
            new[i] = (new[i] - r * c) % q
        coeffs = new
    return normalize({(i,) + (0,) * (m - 1): c for i, c in enumerate(coeffs)}, q)


def random_identity_test(p1: Poly, p2: Poly, S: Sequence[int], m: int, q: int, k: int, rng: random.Random) -> bool:
    """Return True ("probably equal") if p1 and p2 agree at k random points of S^m."""
    for _ in range(k):
        pt = [S[rng.randrange(len(S))] for _ in range(m)]
        if evaluate(p1, pt, q) != evaluate(p2, pt, q):
            return False
    return True
