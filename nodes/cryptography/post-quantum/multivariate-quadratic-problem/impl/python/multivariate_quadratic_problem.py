# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multivariate-quadratic-problem/. The authors are listed in prov/3KTP1K.jsonl.
"""Solving toy instances of the multivariate quadratic (MQ) problem.

- Fast exhaustive search over GF(2) in Gray code order (Bouillaguet et al.,
  CHES 2010): one step costs one XOR per polynomial word, with all m
  polynomials packed in one integer (bit i is polynomial i).
- Plain exhaustive search over GF(q), as a reference.
- Linearization and XL (Courtois, Klimov, Patarin and Shamir, Eurocrypt
  2000) over a prime field GF(p).

For study only. Nothing here is constant time, and it only handles toy sizes.
For real algebraic cryptanalysis use a computer algebra system with F4 or F5,
such as Magma, msolve or the libfes library for exhaustive search.
"""

import itertools
import random
from typing import Dict, List, Optional, Sequence, Tuple

# ---------------------------------------------------------------- GF(2), packed

class BinarySystem:
    """m quadratic polynomials over GF(2) in n variables, packed: quad[(j, l)]
    for j < l, lin[j] and const are m-bit integers, bit i for polynomial i.
    x_j^2 = x_j over GF(2), so squares sit in lin."""

    def __init__(self, n: int, m: int, quad: Dict[Tuple[int, int], int], lin: List[int], const: int):
        self.n, self.m, self.quad, self.lin, self.const = n, m, quad, lin, const

    def a(self, j: int, l: int) -> int:
        return self.quad.get((min(j, l), max(j, l)), 0)

    @classmethod
    def random(cls, n: int, m: int, rng: random.Random, planted: Optional[int] = None) -> "BinarySystem":
        quad = {(j, l): rng.getrandbits(m) for j in range(n) for l in range(j + 1, n)}
        lin = [rng.getrandbits(m) for _ in range(n)]
        sys_ = cls(n, m, quad, lin, rng.getrandbits(m))
        if planted is not None:
            sys_.const ^= sys_.evaluate(planted)       # now P(planted) = 0
        return sys_

    def evaluate(self, x: int) -> int:
        """The m values at x (bit j of x is x_j), packed in an integer."""
        v = self.const
        for j in range(self.n):
            if (x >> j) & 1:
                v ^= self.lin[j]
                for l in range(j + 1, self.n):
                    if (x >> l) & 1:
                        v ^= self.quad[(j, l)]
        return v


def fast_exhaustive_search(P: BinarySystem) -> List[int]:
    """All x in GF(2)^n with P(x) = 0, visited in Gray code order.

    Step i flips bit k1 = (lowest set bit of i). Then
    P(x_i) = P(x_{i-1}) + D_{k1}P(x_{i-1}), and the first derivative
    D_{k1}P changes only by the second derivative a_{k1,k2} since the last
    time bit k1 flipped, where k2 is the second lowest set bit of i."""
    n = P.n
    d1 = [P.lin[k] ^ (P.a(k - 1, k) if k > 0 else 0) for k in range(n)]
    f = P.const
    x = 0
    sols = [0] if f == 0 else []
    for i in range(1, 1 << n):
        k1 = (i & -i).bit_length() - 1
        rest = i ^ (1 << k1)
        if rest:
            k2 = (rest & -rest).bit_length() - 1
            d1[k1] ^= P.a(k1, k2)
        f ^= d1[k1]
        x ^= 1 << k1
        if f == 0:
            sols.append(x)
    return sols


# ---------------------------------------------------------------- GF(p), sparse polynomials

Monomial = Tuple[int, ...]          # exponent vector
Poly = Dict[Monomial, int]          # monomial -> coefficient in GF(p)


def evaluate(f: Poly, x: Sequence[int], p: int) -> int:
    total = 0
    for mon, c in f.items():
        t = c
        for xi, e in zip(x, mon):
            t = t * pow(xi, e, p) % p
        total += t
    return total % p


def random_quadratic_system(n: int, m: int, p: int, rng: random.Random,
                            planted: Optional[Sequence[int]] = None) -> List[Poly]:
    mons = monomials(n, 2)
    system = []
    for _ in range(m):
        f = {mon: rng.randrange(p) for mon in mons}
        if planted is not None:
            zero = (0,) * n
            f[zero] = (f[zero] - evaluate(f, planted, p)) % p
        system.append({mon: c for mon, c in f.items() if c})
    return system


def exhaustive_search(system: Sequence[Poly], n: int, p: int) -> List[Tuple[int, ...]]:
    """All common zeros in GF(p)^n, by trying all p^n points."""
    return [x for x in itertools.product(range(p), repeat=n)
            if all(evaluate(f, x, p) == 0 for f in system)]


def monomials(n: int, d: int) -> List[Monomial]:
    """All monomials in n variables of total degree at most d."""
    out = []
    for deg in range(d + 1):
        for c in itertools.combinations_with_replacement(range(n), deg):
            e = [0] * n
            for i in c:
                e[i] += 1
            out.append(tuple(e))
    return out


def multiply(f: Poly, mon: Monomial, p: int) -> Poly:
    return {tuple(a + b for a, b in zip(k, mon)): c for k, c in f.items()}


def xl_rows(system: Sequence[Poly], n: int, D: int, p: int) -> List[Poly]:
    """XL at degree D: every t * f with f in the system and deg t <= D - 2.
    D = 2 is plain linearization."""
    return [multiply(f, t, p) for f in system for t in monomials(n, D - 2)]


def column_order(n: int, D: int) -> List[Monomial]:
    """Monomials of degree <= D, largest first, with the monomials in the
    last variable only (and 1) at the end, so that echelon form exposes
    univariate polynomials in x_{n-1}."""
    mons = monomials(n, D)
    uni = [m for m in mons if all(e == 0 for e in m[:-1])]
    other = [m for m in mons if m not in uni]
    other.sort(key=lambda m: (sum(m), m), reverse=True)
    uni.sort(key=lambda m: m[-1], reverse=True)
    return other + uni


def echelon(rows: List[Poly], cols: List[Monomial], p: int) -> List[List[int]]:
    """Row echelon form mod p of the linearized rows."""
    index = {m: i for i, m in enumerate(cols)}
    mat = []
    for f in rows:
        r = [0] * len(cols)
        for mon, c in f.items():
            r[index[mon]] = c % p
        mat.append(r)
    out, col = [], 0
    while mat and col < len(cols):
        piv = next((r for r in mat if r[col]), None)
        if piv is None:
            col += 1
            continue
        mat.remove(piv)
        inv = pow(piv[col], p - 2, p)
        piv = [v * inv % p for v in piv]
        mat = [[(a - r[col] * b) % p for a, b in zip(r, piv)] if r[col] else r for r in mat]
        out.append(piv)
        col += 1
    return out


def univariate_from_xl(system: Sequence[Poly], n: int, D: int, p: int) -> Optional[List[int]]:
    """Run XL at degree D. Return the coefficients (high degree first) of a
    nonzero univariate polynomial in x_{n-1} in the span, or None.
    A nonzero constant means that the system has no solution."""
    cols = column_order(n, D)
    first_uni = next(i for i, m in enumerate(cols) if all(e == 0 for e in m[:-1]))
    best = None
    for row in echelon(xl_rows(system, n, D, p), cols, p):
        lead = next(i for i, v in enumerate(row) if v)
        if lead >= first_uni:
            best = row[lead:]        # leads grow, so the last one has the lowest degree
    return best


def substitute_last(system: Sequence[Poly], value: int, p: int) -> List[Poly]:
    """Set the last variable to value and drop it."""
    out = []
    for f in system:
        g: Poly = {}
        for mon, c in f.items():
            k = mon[:-1]
            g[k] = (g.get(k, 0) + c * pow(value, mon[-1], p)) % p
        out.append({k: c for k, c in g.items() if c})
    return out


def xl_solve(system: Sequence[Poly], n: int, p: int, max_degree: int = 6) -> List[Tuple[int, ...]]:
    """All solutions in GF(p)^n, found with XL: raise D until a univariate
    polynomial in the last variable appears, find its roots in GF(p) by
    trial, substitute each root and recurse on n - 1 variables."""
    system = [f for f in system if f]
    if n == 0:
        return [()] if not system else []
    if not system:
        return [x for x in itertools.product(range(p), repeat=n)]
    for D in range(2, max_degree + 1):
        u = univariate_from_xl(system, n, D, p)
        if u is None:
            continue
        deg = len(u) - 1
        roots = [r for r in range(p) if sum(c * pow(r, deg - i, p) for i, c in enumerate(u)) % p == 0]
        sols = []
        for r in roots:
            for rest in xl_solve(substitute_last(system, r, p), n - 1, p, max_degree):
                sols.append(rest + (r,))
        return sols
    raise ValueError("XL found no univariate polynomial up to max_degree")


def xl_degree(system: Sequence[Poly], n: int, p: int, max_degree: int = 6) -> Optional[int]:
    """The smallest D at which XL yields a univariate polynomial."""
    for D in range(2, max_degree + 1):
        if univariate_from_xl(system, n, D, p) is not None:
            return D
    return None
