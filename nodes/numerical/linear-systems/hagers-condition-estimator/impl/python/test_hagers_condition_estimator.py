# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hagers-condition-estimator/. The authors are listed in prov/TXN1K8.jsonl.

import random
from fractions import Fraction as F

import pytest

from hagers_condition_estimator import (
    Singular,
    cond1_estimate,
    lu_factor,
    lu_solve,
    lu_solve_t,
    norm1,
    norm1_estimate,
)


def ops(b):
    n = len(b)
    return (lambda x: [sum(r[j] * x[j] for j in range(n)) for r in b],
            lambda x: [sum(b[i][j] * x[i] for i in range(n)) for j in range(n)])


def inverse(a):
    a = [[F(v) for v in r] for r in a]
    f = lu_factor(a)
    n = len(a)
    cols = [lu_solve(f, [F(int(i == j)) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def test_page_example():
    a = [[F(2), F(-1), F(0)], [F(-1), F(2), F(-1)], [F(0), F(-1), F(2)]]
    st = {}
    assert cond1_estimate(a, stats=st) == 8
    assert st == {"products": 4, "iterations": 2}  # stops on the repeated sign vector
    seen = []
    f = lu_factor(a)

    def ap(x):
        y = lu_solve(f, x)
        seen.append(sum(abs(t) for t in y))
        return y

    est, v = norm1_estimate(ap, lambda x: lu_solve_t(f, x), 3, "hager")
    assert seen == [F(5, 3), 2] and est == 2 and v == [0, 1, 0]


def test_lower_bound_and_attained_exact_500():
    rng = random.Random(1)
    exact = total = 0
    for t in range(500):
        n = rng.randint(1, 9)
        b = [[F(rng.randint(-9, 9)) for _ in range(n)] for _ in range(n)]
        ap, at = ops(b)
        true = norm1(b)
        for var in ("hager", "higham"):
            st = {}
            est, v = norm1_estimate(ap, at, n, var, stats=st)
            assert est <= true
            assert est == sum(abs(t) for t in ap(v)) / sum(abs(t) for t in v)
            if var == "hager":
                assert st["iterations"] <= n + 1
            else:
                assert st["products"] <= 2 * 5 + 1 and st["iterations"] <= 5
            total += 1
            exact += est == true
    assert exact >= 0.5 * total  # observed: 57 percent exact for random integer B


def test_estimates_increase_strictly():
    rng = random.Random(2)
    for _ in range(500):
        n = rng.randint(2, 9)
        b = [[F(rng.randint(-9, 9)) for _ in range(n)] for _ in range(n)]
        ap, at = ops(b)
        seen = []

        def rec(x):
            y = ap(x)
            seen.append(sum(abs(t) for t in y))
            return y

        norm1_estimate(rec, at, n, "hager")
        # All but possibly the last product strictly increase the estimate.
        assert all(p < q for p, q in zip(seen[:-2], seen[1:-1]))


def test_kappa_estimate_floats_lower_bound_and_quality():
    rng = random.Random(3)
    worst = 1.0
    for t in range(150):
        n = rng.randint(2, 14)
        a = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
        if t % 4 == 0:
            for i in range(n):
                a[i][i] *= 1e-8
        k = float(norm1(a) * norm1(inverse(a)))
        e = cond1_estimate(a)
        assert e <= k * (1 + 1e-6)
        worst = min(worst, e / k)
    assert worst > 0.2  # observed, not a theorem


def test_hilbert():
    for n in range(2, 11):
        h = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
        k = float(norm1(h) * norm1(inverse(h)))
        st = {}
        e = cond1_estimate(h, stats=st)
        assert abs(e / k - 1) < 1e-4
        assert st["products"] <= 5
    h = [[1.0 / (i + j + 1) for j in range(10)] for i in range(10)]
    assert 3.4e13 < cond1_estimate(h) < 3.6e13


def test_pure_hager_can_fail_arbitrarily():
    """B = I - (1 - d) e e^T / n has B e = d e: Hager stops at once with d."""
    for n in (2, 5, 9):
        for d in (F(1, 10), F(1, 1000), F(1, 10 ** 9)):
            b = [[(1 if i == j else 0) - (1 - d) / n for j in range(n)] for i in range(n)]
            ap, at = ops(b)
            assert norm1_estimate(ap, at, n, "hager")[0] == d
            assert norm1_estimate(ap, at, n, "higham")[0] == norm1(b)
    b = [[F(1), F(-1)], [F(-1), F(1)]]
    ap, at = ops(b)
    assert norm1_estimate(ap, at, 2, "hager")[0] == 0
    assert norm1_estimate(ap, at, 2, "higham")[0] == 2


def test_alternative_vector_helps():
    # Every column has the same norm, signs alternate: the iteration stalls
    # but the alternative vector catches the norm.
    rng = random.Random(4)
    helped = 0
    for _ in range(500):
        n = rng.randint(2, 7)
        b = [[F(rng.randint(-3, 3)) for _ in range(n)] for _ in range(n)]
        ap, at = ops(b)
        e1 = norm1_estimate(ap, at, n, "higham", itmax=1)[0]
        if n > 1:
            bb = [(-1) ** i * (1 + F(i, n - 1)) for i in range(n)]
            alt = 2 * sum(abs(t) for t in ap(bb)) / (3 * n)
            assert e1 >= alt
            helped += alt == e1 and alt > 0
    assert helped > 0


def test_singular_reports_failure():
    with pytest.raises(Singular):
        cond1_estimate([[1.0, 2.0], [2.0, 4.0]])
    with pytest.raises(Singular):
        cond1_estimate([[F(1), F(2), F(3)], [F(4), F(5), F(6)], [F(7), F(8), F(9)]])
    with pytest.raises(Singular):
        cond1_estimate([[0.0]])


def test_edge_cases():
    assert cond1_estimate([[F(5)]]) == 1
    d = [F(3), F(-1, 2), F(7), F(1, 4)]
    a = [[d[i] if i == j else F(0) for j in range(4)] for i in range(4)]
    assert cond1_estimate(a) == 7 / F(1, 4)
    # Pivot swap needed: a permutation matrix has kappa 1.
    assert cond1_estimate([[0.0, 1.0], [1.0, 0.0]]) == 1.0
    # Triangular, with known inverse: ||A^-1||_1 = 2^(n-1) for the unit
    # upper triangular matrix with -1 above the diagonal.
    n = 12
    a = [[F(1) if i == j else F(-1) if j > i else F(0) for j in range(n)] for i in range(n)]
    assert cond1_estimate(a) == norm1(a) * 2 ** (n - 1)
    # SPD and indefinite symmetric.
    assert cond1_estimate([[F(4), F(1)], [F(1), F(3)]]) == norm1(inverse([[4, 1], [1, 3]])) * 5
    assert cond1_estimate([[F(1), F(3)], [F(3), F(1)]]) == 4 * norm1(inverse([[1, 3], [3, 1]]))
    # Transposed solves are right.
    rng = random.Random(5)
    for _ in range(50):
        n = rng.randint(1, 8)
        a = [[F(rng.randint(-5, 5)) for _ in range(n)] for _ in range(n)]
        try:
            f = lu_factor(a)
        except Singular:
            continue
        b = [F(rng.randint(-5, 5)) for _ in range(n)]
        x = lu_solve_t(f, b)
        assert [sum(a[i][j] * x[i] for i in range(n)) for j in range(n)] == b
