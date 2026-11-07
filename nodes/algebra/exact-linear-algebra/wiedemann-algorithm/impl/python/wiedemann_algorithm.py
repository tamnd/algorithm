# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wiedemann-algorithm/. The authors are listed in prov/HAH02Z.jsonl.

"""Wiedemann's method for a nonsingular sparse system A x = b over Z/pZ, with A given as a black box."""

import random
from typing import Callable, Optional

Vector = list[int]
BlackBox = Callable[[Vector], Vector]


class SingularMatrix(ValueError):
    """Raised when the computation proves that A is singular."""


def berlekamp_massey(s: list[int], p: int) -> list[int]:
    """Return the monic minimal polynomial of the sequence s over Z/pZ, lowest coefficient first.

    The result f = f_0 + f_1 x + ... + x^L satisfies sum_j f_j s[i + j] = 0 for 0 <= i < len(s) - L,
    and L is as small as possible. f is unique when len(s) >= 2L; for a sequence with a minimal
    polynomial of degree d, 2d terms determine it.
    """
    c, b = [1], [1]  # connection polynomials, c(0) = 1
    big_l, m, last = 0, 1, 1
    for i in range(len(s)):
        disc = s[i] % p
        for j in range(1, big_l + 1):
            disc = (disc + c[j] * s[i - j]) % p
        if disc == 0:
            m += 1
            continue
        coef = disc * pow(last, -1, p) % p
        old = c[:]
        if len(c) < len(b) + m:
            c += [0] * (len(b) + m - len(c))
        for j, v in enumerate(b):
            c[j + m] = (c[j + m] - coef * v) % p
        if 2 * big_l <= i:
            big_l, b, last, m = i + 1 - big_l, old, disc, 1
        else:
            m += 1
    c += [0] * (big_l + 1 - len(c))
    return [c[big_l - j] % p for j in range(big_l + 1)]  # reverse: f(x) = x^L c(1/x)


def sparse_black_box(rows: list[dict[int, int]], p: int) -> BlackBox:
    """Black box v -> A v for a sparse matrix given as one {column: value} dictionary per row."""

    def apply(v: Vector) -> Vector:
        return [sum(a * v[j] for j, a in r.items()) % p for r in rows]

    return apply


def dense_black_box(a: list[list[int]], p: int) -> BlackBox:
    """Black box v -> A v for a dense matrix given as a list of rows."""
    return sparse_black_box([{j: x % p for j, x in enumerate(r) if x % p} for r in a], p)


def sequence_minpoly(apply: BlackBox, b: Vector, u: Vector, p: int) -> list[int]:
    """Minimal polynomial over Z/pZ of the sequence u^T A^i b, i = 0, ..., 2n - 1."""
    n = len(b)
    s, v = [], [x % p for x in b]
    for i in range(2 * n):
        s.append(sum(x * y for x, y in zip(u, v)) % p)
        if i < 2 * n - 1:
            v = apply(v)
    return berlekamp_massey(s, p)


def wiedemann_solve(apply: BlackBox, b: Vector, p: int, rng: Optional[random.Random] = None,
                    max_tries: int = 64, stats: Optional[dict] = None) -> Vector:
    """Solve A x = b over Z/pZ for a nonsingular n by n matrix A given by apply(v) = A v.

    Las Vegas: the returned x is always checked. Raises SingularMatrix when the minimal
    polynomial found has a zero constant term, which proves that A is singular, and
    RuntimeError after max_tries failed projections. With u drawn from all of Z/pZ, one
    try succeeds with probability at least 1 - deg(mu_{A,b}) / p.
    """
    rng = rng or random.Random(0)
    n = len(b)
    b = [x % p for x in b]
    if all(x == 0 for x in b):  # @line L1
        return [0] * n
    for tries in range(1, max_tries + 1):  # @line L2
        u = [rng.randrange(p) for _ in range(n)]  # @line L3
        f = sequence_minpoly(apply, b, u, p)  # @line L4
        d = len(f) - 1  # @line L5
        if d == 0:  # u is orthogonal to the Krylov space, a failed try
            continue
        if f[0] == 0:  # @line L6
            raise SingularMatrix("the minimal polynomial of the sequence is divisible by x")
        y = b[:]  # @line L7  (Horner: y = f_1 b + f_2 A b + ... + f_d A^(d-1) b)
        for j in range(d - 1, 0, -1):
            ay = apply(y)
            y = [(w + f[j] * bi) % p for w, bi in zip(ay, b)]
        c = (-pow(f[0], -1, p)) % p
        x = [c * w % p for w in y]
        if apply(x) == b:  # @line L8
            if stats is not None:
                stats["tries"] = tries
            return x  # @line L9
    raise RuntimeError("no projection gave the minimal polynomial; A is probably singular")
