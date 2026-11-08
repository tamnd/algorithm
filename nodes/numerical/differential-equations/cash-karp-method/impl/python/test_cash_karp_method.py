# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cash-karp-method/. The authors are listed in prov/1KQDQK.jsonl.

import math
from fractions import Fraction as Fr

import pytest

from cash_karp_method import A, B, BHAT, C, cash_karp, ck_step

S = 6
AF = [row + [Fr(0)] * (S - len(row)) for row in A]
f_ex = lambda t, y: -2 * t * y * y
y_ex = lambda t: 1 / (1 + t * t)


def _grow(t):
    """All trees obtained from t by adding one leaf, in canonical (sorted) form."""
    yield tuple(sorted(t + ((),)))
    for i, sub in enumerate(t):
        for g in _grow(sub):
            yield tuple(sorted(t[:i] + (g,) + t[i + 1:]))


def trees(n):
    """Rooted trees with n vertices, each a sorted tuple of subtrees."""
    level = {()}
    for _ in range(n - 1):
        level = {g for t in level for g in _grow(t)}
    return sorted(level)


def size(t):
    return 1 + sum(size(x) for x in t)


def gamma(t):
    g = size(t)
    for x in t:
        g *= gamma(x)
    return g


def phi(t):
    v = [Fr(1)] * S
    for sub in t:
        p = phi(sub)
        w = [sum(AF[i][j] * p[j] for j in range(S)) for i in range(S)]
        v = [a * b for a, b in zip(v, w)]
    return v


def order(b):
    for n in range(1, 8):
        if any(sum(x * y for x, y in zip(b, phi(t))) != Fr(1, gamma(t)) for t in trees(n)):
            return n - 1
    return 7


def test_tree_counts() -> None:
    assert [len(trees(n)) for n in range(1, 7)] == [1, 1, 2, 4, 9, 20]


def test_order_conditions_exact() -> None:
    assert all(C[i] == sum(AF[i]) for i in range(S))
    assert order(B) == 5 and order(BHAT) == 4
    # Cash and Karp's lower order solutions from the first stages
    pad = lambda w: w + [Fr(0)] * (S - len(w))
    assert order(pad([Fr(-3, 2), Fr(5, 2)])) == 2
    assert order(pad([Fr(19, 54), Fr(0), Fr(-10, 27), Fr(55, 54)])) == 3


def test_stability_polynomial() -> None:
    v, coeffs = [Fr(1)] * S, [Fr(1)]
    for _ in range(S):
        coeffs.append(sum(x * y for x, y in zip(B, v)))
        v = [sum(AF[i][j] * v[j] for j in range(S)) for i in range(S)]
    assert coeffs == [1, 1, Fr(1, 2), Fr(1, 6), Fr(1, 24), Fr(1, 120), Fr(1, 800)]
    for z in (-1.0, -3.7, 0.3 + 2.0j):
        y1, _ = ck_step(lambda t, y: [z * y[0]], 0.0, [1.0], 1.0)
        assert abs(y1[0] - sum(float(c) * z ** q for q, c in enumerate(coeffs))) < 1e-13
    r = lambda x: sum(float(c) * x ** q for q, c in enumerate(coeffs))
    assert abs(r(-3.7343596)) < 1 + 1e-6 and abs(r(-3.75)) > 1


def test_fixed_step_order_five() -> None:
    fv = lambda t, y: [f_ex(t, y[0])]

    def run(n):
        h, y = 2.0 / n, [1.0]
        for i in range(n):
            y, _ = ck_step(fv, i * h, y, h)
        return abs(y[0] - y_ex(2.0))

    e = [run(n) for n in (20, 40, 80)]
    assert all(abs(math.log2(e[i] / e[i + 1]) - 5) < 0.2 for i in range(2))


def test_adaptive_tolerance_and_cost() -> None:
    errs = []
    for tol in (1e-6, 1e-10):
        ts, ys, st = cash_karp(f_ex, 0.0, 1.0, 2.0, rtol=tol, atol=tol)
        assert ts[-1] == 2.0
        errs.append(max(abs(y - y_ex(t)) for t, y in zip(ts, ys)))
        assert st["evaluations"] == 1 + 6 * (st["accepted"] + st["rejected"])
    assert 1e3 < errs[0] / errs[1] < 1e5


def test_vector_and_linear_invariant() -> None:
    ts, ys, _ = cash_karp(lambda t, y: [y[1], -y[0]], 0.0, [1.0, 0.0], 2 * math.pi, rtol=1e-10, atol=1e-12)
    assert abs(ys[-1][0] - 1) < 1e-8 and abs(ys[-1][1]) < 1e-8
    f = lambda t, y: [-y[0] * y[1], y[0] * y[1] - 0.5 * y[1], 0.5 * y[1]]  # an SIR model: sum is constant
    _, ys, _ = cash_karp(f, 0.0, [0.99, 0.01, 0.0], 30.0, rtol=1e-6, atol=1e-9)
    assert all(abs(sum(y) - 1.0) < 1e-13 for y in ys)


def test_stiff_problem_needs_many_steps() -> None:
    f = lambda t, y: -1000.0 * (y - math.cos(t)) - math.sin(t)
    ts, ys, st = cash_karp(f, 0.0, 1.0, 1.0, rtol=1e-3, atol=1e-6)
    assert abs(ys[-1] - math.cos(1.0)) < 1e-2
    assert st["accepted"] > 250  # stability bounds h by about 3.73/1000


def test_edges() -> None:
    assert cash_karp(lambda t, y: y, 1.0, 2.0, 1.0)[:2] == ([1.0], [2.0])
    ts, ys, _ = cash_karp(lambda t, y: 2 * t, 0.0, 0.0, 0.3, h0=10.0)
    assert ts == [0.0, 0.3] and abs(ys[-1] - 0.09) < 1e-15
    ts, _, _ = cash_karp(lambda t, y: math.cos(t), 0.0, 0.0, 1.0, h_max=0.3)
    assert ts[-1] == 1.0 and all(b - a <= 0.3 + 1e-15 for a, b in zip(ts, ts[1:]))
    with pytest.raises(ValueError):
        cash_karp(lambda t, y: y, 1.0, 1.0, 0.0)
    with pytest.raises(ArithmeticError):
        cash_karp(lambda t, y: -1e6 * y, 0.0, 1.0, 1.0, max_steps=50)
