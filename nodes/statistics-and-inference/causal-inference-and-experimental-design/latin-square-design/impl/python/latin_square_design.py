# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/latin-square-design/. The authors are listed in prov/AR1SZ9.jsonl.
"""Latin squares for experimental design: construction, randomization, orthogonal mates,
and the analysis of variance of a Latin square experiment.

A Latin square of order n is an n x n array on n symbols in which each symbol occurs once
in each row and once in each column. In a Latin square design, rows and columns are two
blocking factors and the symbols are the treatments.
"""

import math
import random
from collections.abc import Sequence
from itertools import product

Square = list[list[int]]


def cyclic(n: int) -> Square:
    """L(i, j) = (i + j) mod n, a Latin square for every n >= 1."""
    return [[(i + j) % n for j in range(n)] for i in range(n)]


def is_latin(sq: Sequence[Sequence[int]]) -> bool:
    n = len(sq)
    full = list(range(n))
    return (all(len(r) == n and sorted(r) == full for r in sq)
            and all(sorted(sq[i][j] for i in range(n)) == full for j in range(n)))


def are_orthogonal(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]]) -> bool:
    """Superimposed, the two squares show each ordered pair of symbols exactly once."""
    n = len(a)
    return len({(a[i][j], b[i][j]) for i in range(n) for j in range(n)}) == n * n


def randomize(sq: Sequence[Sequence[int]], rng: random.Random) -> Square:
    """Permute rows, columns and symbols at random (the usual randomization of a design)."""
    n = len(sq)
    rows, cols, syms = (rng.sample(range(n), n) for _ in range(3))
    return [[syms[sq[rows[i]][cols[j]]] for j in range(n)] for i in range(n)]


# ---------------------------------------------------------------- finite fields


def _prime_power(q: int) -> tuple[int, int]:
    for p in range(2, q + 1):
        if q % p == 0:
            m, r = 0, q
            while r % p == 0:
                r //= p
                m += 1
            if r != 1:
                raise ValueError("q must be a prime power")
            return p, m
    raise ValueError("q must be a prime power >= 2")


def _poly_mod(a: list[int], f: list[int], p: int) -> list[int]:
    """a mod f over GF(p); coefficient lists, lowest degree first, f monic."""
    a = a[:]
    while len(a) >= len(f):
        c = a[-1] % p
        if c:
            shift = len(a) - len(f)
            for i, fi in enumerate(f):
                a[shift + i] = (a[shift + i] - c * fi) % p
        a.pop()
    return a


def _irreducible(p: int, m: int) -> list[int]:
    """The first monic irreducible polynomial of degree m over GF(p), by trial division."""
    for tail in product(range(p), repeat=m):
        f = list(tail) + [1]
        if m == 1:
            return f
        reducible = False
        for d in range(1, m // 2 + 1):
            for gt in product(range(p), repeat=d):
                if not any(_poly_mod(f, list(gt) + [1], p)):
                    reducible = True
                    break
            if reducible:
                break
        if not reducible:
            return f
    raise AssertionError("an irreducible polynomial exists for every degree")


def field(q: int) -> tuple[list[list[int]], list[list[int]]]:
    """Addition and multiplication tables of GF(q); element e codes the polynomial with
    the base-p digits of e as coefficients, so 0 and 1 are the field's 0 and 1."""
    p, m = _prime_power(q)
    f = _irreducible(p, m)
    digits = [[(e // p ** i) % p for i in range(m)] for e in range(q)]
    code = lambda c: sum((v % p) * p ** i for i, v in enumerate(c))
    add = [[code([x + y for x, y in zip(digits[a], digits[b])]) for b in range(q)] for a in range(q)]
    mul = []
    for a in range(q):
        row = []
        for b in range(q):
            prod_ = [0] * (2 * m - 1)
            for i, x in enumerate(digits[a]):
                for j, y in enumerate(digits[b]):
                    prod_[i + j] += x * y
            r = _poly_mod(prod_, f, p) if m > 1 else [prod_[0] % p]
            row.append(code(r + [0] * (m - len(r))))
        mul.append(row)
    return add, mul


def mols(q: int) -> list[Square]:
    """q - 1 mutually orthogonal Latin squares of prime power order q: L_a(x, y) = a x + y."""
    add, mul = field(q)
    return [[[add[mul[a][x]][y] for y in range(q)] for x in range(q)] for a in range(1, q)]


# ---------------------------------------------------------------- analysis


def latin_square_anova(y: Sequence[Sequence[float]], sq: Sequence[Sequence[int]]) -> dict[str, tuple[float, int]]:
    """Sums of squares and degrees of freedom of rows, columns, treatments and error
    for the additive model y_ij = mu + row_i + col_j + tau_(L(i, j)) + e_ij."""
    n = len(y)
    if n < 3 or not is_latin(sq):
        raise ValueError("need a Latin square of order n >= 3 (error df (n - 1)(n - 2))")
    total = math.fsum(v for r in y for v in r)
    g = total / (n * n)
    row_m = [math.fsum(r) / n for r in y]
    col_m = [math.fsum(y[i][j] for i in range(n)) / n for j in range(n)]
    trt_m = [0.0] * n
    for i in range(n):
        for j in range(n):
            trt_m[sq[i][j]] += y[i][j] / n
    ss = {
        "rows": n * math.fsum((m - g) ** 2 for m in row_m),
        "columns": n * math.fsum((m - g) ** 2 for m in col_m),
        "treatments": n * math.fsum((m - g) ** 2 for m in trt_m),
    }
    ss["error"] = math.fsum((y[i][j] - row_m[i] - col_m[j] - trt_m[sq[i][j]] + 2 * g) ** 2
                            for i in range(n) for j in range(n))
    df = {"rows": n - 1, "columns": n - 1, "treatments": n - 1, "error": (n - 1) * (n - 2)}
    return {key: (ss[key], df[key]) for key in ss}
