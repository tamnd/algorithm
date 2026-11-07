# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coppersmith-winograd-algorithm/. The authors are listed in prov/YF5DJV.jsonl.

import random

import pytest

from coppersmith_winograd_algorithm import (
    best_complete_bound,
    complete_bound,
    count_products,
    coppersmith_winograd_algorithm as cw,
    cw_approximate,
    cw_exact_by_interpolation,
    decomposition,
    easy_bound,
)


def schoolbook(a, b, mod=None):
    n, m, p = len(a), len(b), len(b[0]) if b else 0
    c = [[0] * p for _ in range(n)]
    for i in range(n):
        for j in range(p):
            s = 0
            for k in range(m):
                s += a[i][k] * b[k][j]
            c[i][j] = s % mod if mod is not None else s
    return c


def phi(x, y, q, mod=None):
    """Direct evaluation of the CW bilinear map with 3q + 3 products."""
    out = [sum(x[i] * y[i] for i in range(1, q + 1)) + x[0] * y[q + 1] + x[q + 1] * y[0]]
    out += [x[0] * y[i] + x[i] * y[0] for i in range(1, q + 1)]
    out.append(x[0] * y[0])
    return [v % mod for v in out] if mod is not None else out


def rand(rng, d, lo=-9, hi=9):
    return [rng.randint(lo, hi) for _ in range(d)]


def test_example() -> None:
    assert cw([1, 2, 3, 4], [5, 6, 7, 8], 2) == [61, 16, 22, 5]
    assert cw_exact_by_interpolation([1, 2, 3, 4], [5, 6, 7, 8], 2) == [61, 16, 22, 5]


def test_small_q() -> None:
    assert cw([3, 4], [5, 6], 0) == [3 * 6 + 4 * 5, 15]
    assert cw([2, 3, 4], [5, 6, 7], 1) == [3 * 6 + 2 * 7 + 4 * 5, 2 * 6 + 3 * 5, 10]
    assert count_products(0) == 2 and count_products(6) == 8


def test_zero_and_unit() -> None:
    for q in range(0, 6):
        z = [0] * (q + 2)
        assert cw(z, z, q) == [0] * (q + 2)
        e0 = [1] + [0] * (q + 1)
        assert cw(e0, e0, q) == [0] * (q + 1) + [1]


def test_random_over_z() -> None:
    rng = random.Random(20260)
    for _ in range(600):
        q = rng.randint(0, 9)
        x, y = rand(rng, q + 2), rand(rng, q + 2)
        assert cw(x, y, q) == phi(x, y, q)


@pytest.mark.parametrize("mod", [2, 3, 5, 7])
def test_random_mod(mod: int) -> None:
    rng = random.Random(mod)
    for _ in range(200):
        q = rng.randint(0, 8)
        x, y = rand(rng, q + 2, 0, mod - 1), rand(rng, q + 2, 0, mod - 1)
        assert cw(x, y, q, mod) == phi(x, y, q, mod)


def test_interpolation_exact() -> None:
    rng = random.Random(7)
    for _ in range(150):
        q = rng.randint(0, 6)
        x, y = rand(rng, q + 2), rand(rng, q + 2)
        assert cw_exact_by_interpolation(x, y, q) == phi(x, y, q)
    for mod in (11, 13, 101):
        for _ in range(60):
            q = rng.randint(0, 6)
            x, y = rand(rng, q + 2, 0, mod - 1), rand(rng, q + 2, 0, mod - 1)
            assert cw_exact_by_interpolation(x, y, q, mod) == phi(x, y, q, mod)
    for bad in (7, 9, 2):
        with pytest.raises(ValueError):
            cw_exact_by_interpolation([1, 1], [1, 1], 0, bad)


def test_decomposition_is_eps3_T() -> None:
    """Sum of the q + 2 rank-one terms has eps^0..eps^2 parts zero and eps^3 part T_q."""
    for q in range(0, 7):
        d = q + 2
        terms = decomposition(q)
        assert len(terms) == q + 2
        coef = {}
        for u, v, w in terms:
            for a in range(d):
                for b in range(d):
                    for c in range(d):
                        for i, ua in enumerate(u[a]):
                            for j, vb in enumerate(v[b]):
                                for k, wc in enumerate(w[c]):
                                    if ua * vb * wc and i + j + k <= 3:
                                        key = (i + j + k, a, b, c)
                                        coef[key] = coef.get(key, 0) + ua * vb * wc
        target = {}
        for i in range(1, q + 1):
            for t in ((0, i, i), (i, 0, i), (i, i, 0)):
                target[t] = 1
        for t in ((0, 0, q + 1), (0, q + 1, 0), (q + 1, 0, 0)):
            target[t] = 1
        for (deg, a, b, c), val in coef.items():
            if deg < 3:
                assert val == 0
            else:
                assert val == target.get((a, b, c), 0)
        assert sum(1 for k, v in coef.items() if k[0] == 3 and v) == len(target) == 3 * q + 3


def test_contains_matrix_products() -> None:
    """Pieces of T_q are matrix products; check them against the schoolbook loop."""
    rng = random.Random(3)
    for _ in range(100):
        q = rng.randint(1, 8)
        u, v = rand(rng, q), rand(rng, q)
        # <1, q, 1>: x0 = y0 = 0 and x_{q+1} = y_{q+1} = 0 leaves the inner product in phi_0.
        out = cw([0] + u + [0], [0] + v + [0], q)
        assert out[0] == schoolbook([u], [[t] for t in v])[0][0]
        # <1, 1, q>: only x0 = a nonzero on the x side gives a times y in phi_1..phi_q.
        a = rng.randint(-9, 9)
        out = cw([a] + [0] * (q + 1), [0] + v + [0], q)
        assert out[1 : q + 1] == schoolbook([[a]], [v])[0]


def test_float_error_is_order_eps() -> None:
    x, y, q = [1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0], 2
    exact = phi(x, y, q)
    errs = []
    for eps in (1e-1, 1e-2, 1e-3):
        approx = cw_approximate(x, y, q, eps)
        errs.append(max(abs(a - b) for a, b in zip(approx, exact)))
    assert errs[0] > errs[1] > errs[2]
    assert errs[1] < 1.5 and errs[2] < 0.2
    assert abs(errs[1] / errs[2] - 10) < 1.5


def test_bounds() -> None:
    assert abs(easy_bound(8) - 2.40363) < 1e-4
    assert easy_bound(4) == pytest.approx(2.5)
    assert min(range(2, 30), key=easy_bound) == 8
    b, a = best_complete_bound(6)
    assert abs(b - 2.38719) < 1e-4 and abs(a - 0.31733) < 1e-3
    assert b < 2.388
    assert min(range(2, 30), key=lambda q: best_complete_bound(q)[0]) == 6
    assert abs(best_complete_bound(2)[0] - 2.69856) < 1e-4
    for q in range(2, 20):
        assert 2 < best_complete_bound(q)[0] <= complete_bound(q, 1 / 3) + 1e-12
        assert best_complete_bound(q)[0] <= easy_bound(q) + 1e-12


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        cw([1, 2], [1, 2, 3], 1)
    with pytest.raises(ValueError):
        cw([], [], -2)
    with pytest.raises(ValueError):
        easy_bound(1)
    with pytest.raises(ValueError):
        complete_bound(6, 0.5)
