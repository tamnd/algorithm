# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matrix-balancing/. The authors are listed in prov/T97X37.jsonl.

import math
import random
from fractions import Fraction

import pytest

from matrix_balancing import balance, offdiag_norms, offdiag_sum


def charpoly(a):
    """Exact characteristic polynomial det(tI - A) by Faddeev-LeVerrier, coefficients highest first."""
    n = len(a)
    af = [[Fraction(x) for x in row] for row in a]
    m = [[Fraction(0)] * n for _ in range(n)]
    coeffs = [Fraction(1)]
    for k in range(1, n + 1):
        am = [[sum(af[i][t] * m[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        m = [[am[i][j] + (coeffs[-1] if i == j else 0) for j in range(n)] for i in range(n)]
        am = [[sum(af[i][t] * m[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        coeffs.append(-sum(am[i][i] for i in range(n)) / k)
    return coeffs


def frob(a):
    return math.sqrt(sum(x * x for row in a for x in row))


def graded(n, rng, spread=8):
    """D M D^-1 with M random and D = diag(10^k) for random integer k in [-spread, spread]."""
    m = [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(n)]
    e = [rng.randint(-spread, spread) for _ in range(n)]
    a = [[m[i][j] * 10.0 ** (e[i] - e[j]) for j in range(n)] for i in range(n)]
    return a, m


def is_power_of(x, radix):
    m, e = math.frexp(x)
    if m != 0.5:
        return False
    k = round(math.log(radix, 2))
    return (e - 1) % k == 0


def check(a, res, radix=2.0):
    n = len(a)
    for x in res.d:
        assert is_power_of(x, radix)
    for i in range(n):
        for j in range(n):
            assert res.b[i][j] == a[i][j] * res.d[j] / res.d[i]  # exact: powers of the radix
    assert offdiag_sum(res.b) <= offdiag_sum(a) * (1 + 1e-15)


def check_local_optimum(res, factor=0.95):
    """At convergence no power-of-2 rescaling of one index lowers c + r by 5 percent."""
    for i in range(len(res.b)):
        c, r = offdiag_norms(res.b, i)
        if c == 0.0 or r == 0.0:
            continue
        for m in range(-8, 9):
            assert c * 2.0**m + r * 2.0**-m >= factor * (c + r) * (1 - 1e-12)


def test_exact_similarity_many_seeds():
    worst_sweeps = 0
    for seed in range(60):
        rng = random.Random(seed)
        n = rng.randint(2, 12)
        a, _ = graded(n, rng)
        res = balance(a)
        assert res.converged
        check(a, res)
        check_local_optimum(res)
        worst_sweeps = max(worst_sweeps, res.sweeps)
    assert worst_sweeps <= 20


def test_exact_characteristic_polynomial_is_unchanged():
    for seed in range(12):
        rng = random.Random(100 + seed)
        n = rng.randint(2, 5)
        a, _ = graded(n, rng, spread=5)
        res = balance(a)
        assert charpoly(res.b) == charpoly(a)


def test_trace_and_determinant_are_exactly_unchanged():
    rng = random.Random(5)
    a, _ = graded(6, rng)
    res = balance(a)
    assert sum(Fraction(res.b[i][i]) for i in range(6)) == sum(Fraction(a[i][i]) for i in range(6))
    assert charpoly(res.b)[-1] == charpoly(a)[-1]


def test_norm_reduction_on_graded_matrices():
    for seed in range(30):
        rng = random.Random(200 + seed)
        n = rng.randint(3, 10)
        a, m = graded(n, rng)
        res = balance(a)
        # the grading is removed: the balanced matrix is close in size to the ungraded M
        assert frob(res.b) <= 4.0 * frob(m)
        assert frob(res.b) <= frob(a) * (1 + 1e-15) or frob(a) <= 4.0 * frob(m)


def test_page_example():
    n = 4
    s = [[1.0 if i != j else float(i + 1) for j in range(n)] for i in range(n)]
    a = [[s[i][j] * 0.001 ** (j - i) for j in range(n)] for i in range(n)]
    res = balance(a)
    assert res.converged and res.sweeps == 3 and res.updates == 7
    assert res.d == [2.0**-24, 2.0**-14, 2.0**-4, 2.0**6]
    assert frob(a) == pytest.approx(1.000001e9, rel=1e-9)
    assert frob(res.b) == pytest.approx(6.484215, abs=1e-6)
    assert res.b[0][1] == pytest.approx(1.024, abs=1e-12)
    assert res.b[1][0] == pytest.approx(0.9765625, abs=1e-12)
    c = charpoly(a)
    assert [round(float(t), 9) for t in c] == [1.0, -10.0, 29.0, -28.0, 6.0]


def test_symmetric_and_diagonal_matrices_are_left_alone():
    rng = random.Random(9)
    n = 6
    s = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            s[i][j] = s[j][i] = rng.uniform(-1, 1)
    res = balance(s)
    assert res.updates == 0 and res.sweeps == 1 and res.b == s
    d = [[float(i == j) * (i + 1) for j in range(n)] for i in range(n)]
    res = balance(d)
    assert res.updates == 0 and res.b == d


def test_zero_one_by_one_and_empty():
    assert balance([]).b == [] and balance([]).converged
    assert balance([[7.0]]).b == [[7.0]]
    z = [[0.0] * 3 for _ in range(3)]
    res = balance(z)
    assert res.converged and res.updates == 0


def test_reducible_triangular_matrices_terminate():
    for seed in range(20):
        rng = random.Random(300 + seed)
        n = rng.randint(2, 8)
        a, _ = graded(n, rng)
        for i in range(n):
            for j in range(i):
                a[i][j] = 0.0  # upper triangular
        res = balance(a)
        assert res.converged
        check(a, res)
        for i in range(n):
            assert res.b[i][i] == a[i][i]  # the eigenvalues, exactly


def test_idempotent():
    rng = random.Random(17)
    a, _ = graded(8, rng)
    once = balance(a)
    twice = balance(once.b)
    assert twice.updates == 0 and twice.b == once.b


def test_sweep_cap_and_radix():
    rng = random.Random(23)
    a, _ = graded(8, rng)
    capped = balance(a, maxsweeps=1)
    assert not capped.converged and capped.sweeps == 1
    check(a, capped)
    res16 = balance(a, radix=16.0)
    assert res16.converged
    check(a, res16, radix=16.0)
    with pytest.raises(ValueError):
        balance([[1.0, 2.0]])
    with pytest.raises(ValueError):
        balance([[1.0]], radix=1.0)
