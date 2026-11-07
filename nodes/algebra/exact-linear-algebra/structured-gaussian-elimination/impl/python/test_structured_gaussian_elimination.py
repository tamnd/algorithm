# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/structured-gaussian-elimination/. The authors are listed in prov/FPBFNE.jsonl.

import math
import random
from fractions import Fraction

import pytest

from structured_gaussian_elimination import Inconsistent, structured_solve


def rank(rows, n, p):
    m = [[Fraction(r.get(j, 0)) if p is None else r.get(j, 0) % p for j in range(n)] for r in rows]
    rk = 0
    for col in range(n):
        piv = next((i for i in range(rk, len(m)) if m[i][col] != 0), None)
        if piv is None:
            continue
        m[rk], m[piv] = m[piv], m[rk]
        for i in range(rk + 1, len(m)):
            if m[i][col] != 0:
                f = m[i][col] / m[rk][col] if p is None else m[i][col] * pow(m[rk][col], -1, p) % p
                m[i] = [a - f * b if p is None else (a - f * b) % p for a, b in zip(m[i], m[rk])]
        rk += 1
    return rk


def consistent(rows, c, n, p):
    aug = [{**r, n: v} for r, v in zip(rows, c)]
    return rank(rows, n, p) == rank(aug, n + 1, p)


def residual_ok(rows, c, x, p):
    for r, v in zip(rows, c):
        s = sum(a * x[j] for j, a in r.items()) - v
        if (s if p is None else s % p) != 0:
            return False
    return True


def random_sparse(rng, m, n, p, density):
    rows = []
    for _ in range(m):
        r = {}
        for j in range(n):
            if rng.random() < density:
                v = rng.randrange(1, p) if p else rng.choice([-3, -2, -1, 1, 2, 3])
                r[j] = v
        rows.append(r)
    return rows


def test_worked_example():
    # x0 + x1 = 3, x1 + x2 + x4 = 10, x2 + x3 = 7, x0 + x3 + x4 = 10, x2 + x4 = 8; the solution is (1, 2, 3, 4, 5)
    a = [{0: 1, 1: 1}, {1: 1, 2: 1, 4: 1}, {2: 1, 3: 1}, {0: 1, 3: 1, 4: 1}, {2: 1, 4: 1}]
    c = [3, 10, 7, 10, 8]
    stats = {}
    x = structured_solve(a, c, 5, stats=stats)
    assert x == [1, 2, 3, 4, 5]
    assert stats == {"heavy": 1, "pivots": 4, "dense_rows": 1}
    assert structured_solve(a, c, 5, p=7) == [1, 2, 3, 4, 5]


def test_edges():
    assert structured_solve([], [], 0) == []
    assert structured_solve([], [], 3) == [0, 0, 0]  # no equations, every x works
    assert structured_solve([{}], [0], 0) == []
    with pytest.raises(Inconsistent):
        structured_solve([{}], [1], 2)  # a zero row with a nonzero right side
    assert structured_solve([{0: 5}], [10], 1) == [2]
    assert structured_solve([{0: 3}], [1], 1, p=7) == [5]
    x = structured_solve([{1: 2}, {1: 4}], [2, 4], 3)  # zero columns 0 and 2
    assert x == [0, 1, 0]
    with pytest.raises(Inconsistent):
        structured_solve([{0: 1, 1: 1}, {0: 2, 1: 2}], [1, 3], 2)  # singular and inconsistent
    with pytest.raises(ValueError):
        structured_solve([{3: 1}], [1], 2)


def test_triangular_needs_no_heavy_columns():
    rng = random.Random(3)
    for _ in range(50):
        n = rng.randrange(1, 30)
        perm_r, perm_c = list(range(n)), list(range(n))
        rng.shuffle(perm_r)
        rng.shuffle(perm_c)
        rows = [dict() for _ in range(n)]
        for i in range(n):
            rows[perm_r[i]][perm_c[i]] = rng.randrange(1, 101)
            for j in range(i + 1, n):
                if rng.random() < 0.2:
                    rows[perm_r[i]][perm_c[j]] = rng.randrange(101)
        x0 = [rng.randrange(101) for _ in range(n)]
        c = [sum(v * x0[j] for j, v in r.items()) % 101 for r in rows]
        stats = {}
        assert structured_solve(rows, c, n, p=101, stats=stats) == x0
        assert stats["heavy"] == 0


@pytest.mark.parametrize("p", [2, 3, 7, 101])
def test_random_mod_p(p):
    rng = random.Random(1000 + p)
    for _ in range(250):
        m, n = rng.randrange(0, 13), rng.randrange(0, 13)
        rows = random_sparse(rng, m, n, p, rng.choice([0.1, 0.25, 0.5]))
        if rng.random() < 0.6:
            x0 = [rng.randrange(p) for _ in range(n)]
            c = [sum(v * x0[j] for j, v in r.items()) % p for r in rows]
        else:
            c = [rng.randrange(p) for _ in range(m)]
        if consistent(rows, c, n, p):
            x = structured_solve(rows, c, n, p)
            assert residual_ok(rows, c, x, p) and all(0 <= v < p for v in x)
        else:
            with pytest.raises(Inconsistent):
                structured_solve(rows, c, n, p)


def test_random_over_q_and_full_rank_uniqueness():
    rng = random.Random(77)
    for _ in range(200):
        m, n = rng.randrange(0, 11), rng.randrange(0, 11)
        rows = random_sparse(rng, m, n, None, rng.choice([0.15, 0.3, 0.6]))
        x0 = [Fraction(rng.randrange(-9, 10), rng.randrange(1, 5)) for _ in range(n)]
        c = [sum(v * x0[j] for j, v in r.items()) for r in rows]
        x = structured_solve(rows, c, n)
        assert residual_ok(rows, c, x, None)
        if rank(rows, n, None) == n:
            assert x == x0


def test_large_entries():
    rng = random.Random(9)
    for _ in range(30):
        n = rng.randrange(1, 9)
        rows = [{j: rng.randrange(-2**64, 2**64) for j in range(n) if rng.random() < 0.5} for _ in range(n + 2)]
        x0 = [rng.randrange(-2**40, 2**40) for _ in range(n)]
        c = [sum(v * x0[j] for j, v in r.items()) for r in rows]
        x = structured_solve(rows, c, n)
        assert residual_ok(rows, c, x, None)
        if rank(rows, n, None) == n:
            assert x == x0


def test_sparse_reduction_shrinks_the_system():
    # 310 rows with 10 entries in 300 columns, column j chosen with probability about 1/(j+1),
    # like the factor base of index calculus: the dense part has far fewer columns
    rng = random.Random(5)
    p, n, m, w = 1_000_003, 300, 310, 10
    rows = []
    for _ in range(m):
        r = {}
        while len(r) < w:
            j = int(math.exp(rng.random() * math.log(n + 1))) - 1
            r[min(j, n - 1)] = rng.randrange(1, p)
        rows.append(r)
    x0 = [rng.randrange(p) for _ in range(n)]
    c = [sum(v * x0[j] for j, v in r.items()) % p for r in rows]
    stats = {}
    x = structured_solve(rows, c, n, p, stats)
    assert residual_ok(rows, c, x, p)
    assert stats["heavy"] < n // 5
