# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/determinant-decision-diagram/. The authors are listed in prov/09FYV2.jsonl.

import itertools
import random
from fractions import Fraction

from determinant_decision_diagram import DDD


def leibniz_terms(n: int, entries: dict) -> set:
    """Full expansion: every permutation whose entries are all nonzero, with its sign."""
    out = set()
    for p in itertools.permutations(range(n)):
        if all((i, p[i]) in entries for i in range(n)):
            inv = sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
            out.add((-1 if inv % 2 else 1, tuple((i, p[i]) for i in range(n))))
    return out


def gauss_det(n: int, a: list) -> Fraction:
    m = [[Fraction(x) for x in row] for row in a]
    det = Fraction(1)
    for col in range(n):
        piv = next((r for r in range(col, n) if m[r][col] != 0), None)
        if piv is None:
            return Fraction(0)
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            det = -det
        det *= m[col][col]
        for r in range(col + 1, n):
            f = m[r][col] / m[col][col]
            for c in range(col, n):
                m[r][c] -= f * m[col][c]
    return det


def random_pattern(n: int, density: float, rng: random.Random) -> dict:
    return {(i, j): f"a{i}{j}" for i in range(n) for j in range(n) if i == j or rng.random() < density}


def tridiagonal(n: int) -> dict:
    return {(i, j): f"a{i}{j}" for i in range(n) for j in range(n) if abs(i - j) <= 1}


def check(n: int, entries: dict, rng: random.Random) -> DDD:
    d = DDD(n, entries)
    terms = leibniz_terms(n, entries)
    assert set(d.terms()) == terms
    assert len(d.terms()) == len(terms) == d.count_terms()
    for _ in range(3):
        vals = {s: Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for s in entries.values()}
        a = [[vals[entries[(i, j)]] if (i, j) in entries else 0 for j in range(n)] for i in range(n)]
        assert d.evaluate(vals) == gauss_det(n, a)
    return d


def test_example_4x4() -> None:
    letters = iter("abcdefghij")
    e = {k: next(letters) for k in sorted(tridiagonal(4))}
    d = DDD(4, e)
    assert d.count_terms() == 5
    got = {(s, "".join(e[p] for p in path)) for s, path in d.terms()}
    assert got == {(1, "adgj"), (-1, "adhi"), (-1, "aefj"), (-1, "bcgj"), (1, "bchi")}
    assert d.size() == 10
    vals = dict(zip("abcdefghij", range(1, 11)))
    assert d.evaluate(vals) == gauss_det(4, [[1, 2, 0, 0], [3, 4, 5, 0], [0, 6, 7, 8], [0, 0, 9, 10]])


def test_edges() -> None:
    assert DDD(0, {}).root == 1
    d = DDD(1, {(0, 0): "x"})
    assert d.count_terms() == 1 and d.evaluate({"x": 3}) == 3
    d = DDD(2, {(0, 1): "x", (1, 1): "y"})  # singular pattern: no term
    assert d.root == 0 and d.count_terms() == 0 and d.size() == 0


def test_random_sparse_against_leibniz_and_gauss() -> None:
    rng = random.Random(2000)
    for n in range(1, 7):
        for _ in range(15):
            check(n, random_pattern(n, rng.choice([0.2, 0.4, 0.7]), rng), rng)


def test_dense() -> None:
    rng = random.Random(7)
    for n in range(1, 7):
        e = {(i, j): f"a{i}{j}" for i in range(n) for j in range(n)}
        d = check(n, e, rng)
        assert d.count_terms() == len(list(itertools.permutations(range(n))))
        assert d.size() == n * 2 ** (n - 1)


def test_tridiagonal_fibonacci_terms_linear_size() -> None:
    fib = [0, 1]
    while len(fib) < 40:
        fib.append(fib[-1] + fib[-2])
    for n in range(1, 31):
        d = DDD(n, tridiagonal(n))
        assert d.count_terms() == fib[n + 1]
        assert d.size() == 3 * n - 2
