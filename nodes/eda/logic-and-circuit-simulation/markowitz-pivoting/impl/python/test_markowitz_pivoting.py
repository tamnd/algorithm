# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markowitz-pivoting/. The authors are listed in prov/RPNJK6.jsonl.

import random
from fractions import Fraction as F

import pytest

from markowitz_pivoting import SingularMatrixError, markowitz_lu, markowitz_solve
from sim3dense import solve


def star(leaves):
    """Grounded conductance matrix of a hub node 0 joined by 1 S to each leaf, each leaf 1 S to ground."""
    n = leaves + 1
    a = [[F(0)] * n for _ in range(n)]
    a[0][0] = F(leaves)
    for k in range(1, n):
        a[0][k] = a[k][0] = F(-1)
        a[k][k] = F(2)
    return a


def symbolic_fill(pattern, order):
    """Brute force: dense symbolic elimination along the pivot order; returns fill per step."""
    n = len(pattern)
    s = [row[:] for row in pattern]
    done_r, done_c, out = set(), set(), []
    for p, q in order:
        rs = [i for i in range(n) if i not in done_r and i != p and s[i][q]]
        cs = [j for j in range(n) if j not in done_c and j != q and s[p][j]]
        made = 0
        for i in rs:
            for j in cs:
                if not s[i][j]:
                    s[i][j] = True
                    made += 1
        done_r.add(p)
        done_c.add(q)
        out.append(made)
    return out


def reconstruct(f):
    n = f.n
    pos = {r: k for k, r in enumerate(f.prow)}
    lo = [[F(0)] * n for _ in range(n)]
    up = [[F(0)] * n for _ in range(n)]
    cpos = {c: k for k, c in enumerate(f.pcol)}
    for k in range(n):
        lo[k][k] = F(1)
        for i, l in f.lower[k].items():
            lo[pos[i]][k] = l
        for j, v in f.upper[k].items():
            up[k][cpos[j]] = v
    return [[sum(lo[i][t] * up[t][j] for t in range(n)) for j in range(n)] for i in range(n)]


def random_sparse(rng, n, density):
    while True:
        a = [[F(rng.randint(-9, 9)) if rng.random() < density else F(0) for _ in range(n)] for _ in range(n)]
        try:
            solve(a, [F(1)] * n)
            return a
        except ValueError:
            continue


def test_star_example():
    a = star(3)
    f = markowitz_lu(a)
    assert f.fill == 0
    assert [c for c, _ in f.steps] == [1, 1, 1, 0]
    pattern = [[x != 0 for x in row] for row in a]
    assert sum(symbolic_fill(pattern, [(k, k) for k in range(4)])) == 6
    x = markowitz_solve(a, [F(1), F(0), F(0), F(0)])
    assert x == solve(a, [F(1), F(0), F(0), F(0)]) == [F(2, 3), F(1, 3), F(1, 3), F(1, 3)]


def test_factors_exact_and_fill_bound():
    rng = random.Random(11)
    for _ in range(150):
        n = rng.randint(1, 7)
        a = random_sparse(rng, n, rng.choice([0.3, 0.5, 0.8]))
        for u in (F(1), F(1, 10)):
            f = markowitz_lu(a, u)
            pa = [[a[f.prow[i]][f.pcol[j]] for j in range(n)] for i in range(n)]
            assert reconstruct(f) == pa
            for count, made in f.steps:
                assert made <= count
            pattern = [[x != 0 for x in row] for row in a]
            assert symbolic_fill(pattern, list(zip(f.prow, f.pcol))) == [m for _, m in f.steps]
            for low in f.lower:
                for l in low.values():
                    assert abs(l) <= 1 / u
            b = [F(rng.randint(-5, 5)) for _ in range(n)]
            assert markowitz_solve(a, b, u) == solve(a, b)


def test_pivot_has_least_count():
    rng = random.Random(12)
    for _ in range(80):
        n = rng.randint(2, 6)
        a = random_sparse(rng, n, 0.5)
        u = F(1, 4)
        f = markowitz_lu(a, u)
        m = [row[:] for row in a]
        pat = [[x != 0 for x in row] for row in a]
        act_r, act_c = set(range(n)), set(range(n))
        for k in range(n):
            best = None
            for j in act_c:
                mx = max(abs(m[i][j]) for i in act_r if pat[i][j])
                for i in act_r:
                    if pat[i][j] and abs(m[i][j]) >= u * mx:
                        r = sum(1 for c in act_c if pat[i][c])
                        c = sum(1 for t in act_r if pat[t][j])
                        best = min(best, (r - 1) * (c - 1)) if best is not None else (r - 1) * (c - 1)
            p, q = f.prow[k], f.pcol[k]
            assert f.steps[k][0] == best
            for i in act_r - {p}:
                if pat[i][q]:
                    l = m[i][q] / m[p][q]
                    for j in act_c:
                        if pat[p][j]:
                            m[i][j] -= l * m[p][j]
                            pat[i][j] = True
            act_r.discard(p)
            act_c.discard(q)


def test_mna_matrix_with_zero_diagonal():
    # 6 V source at node 1, 2 ohm from 1 to 2, 3 ohm from 2 to ground, 1 A into node 2.
    a = [[F(1, 2), F(-1, 2), F(1)], [F(-1, 2), F(5, 6), F(0)], [F(1), F(0), F(0)]]
    b = [F(0), F(1), F(6)]
    assert markowitz_solve(a, b) == [F(6), F(24, 5), F(-3, 5)]


def test_singular():
    with pytest.raises(SingularMatrixError):
        markowitz_lu([[F(1), F(2)], [F(2), F(4)]])
    with pytest.raises(SingularMatrixError):
        markowitz_lu([[F(1), F(0)], [F(1), F(0)]])


def test_float_ladder():
    rng = random.Random(13)
    n = 30
    a = [[0.0] * n for _ in range(n)]
    for i in range(n):
        g = rng.uniform(0.5, 2.0)
        a[i][i] += g
        if i + 1 < n:
            h = rng.uniform(0.5, 2.0)
            a[i][i] += h
            a[i + 1][i + 1] += h
            a[i][i + 1] -= h
            a[i + 1][i] -= h
    b = [rng.uniform(-1, 1) for _ in range(n)]
    f = markowitz_lu(a, 0.1)
    assert f.fill == 0
    x = markowitz_solve(a, b, 0.1)
    y = solve(a, b)
    assert max(abs(p - q) for p, q in zip(x, y)) < 1e-12
