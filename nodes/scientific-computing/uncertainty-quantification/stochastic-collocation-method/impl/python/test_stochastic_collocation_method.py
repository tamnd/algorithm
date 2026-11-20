# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-collocation-method/. The authors are listed in prov/S37CZP.jsonl.
import itertools
import math
import random

from stochastic_collocation_method import (
    cc_weights,
    collocate,
    evaluate,
    ishigami,
    level_keys,
    moments,
    node,
    quadrature_weights,
    smolyak_terms,
)


def mono_mean(beta):
    return math.prod(0.0 if b % 2 else 1.0 / (b + 1) for b in beta)


def test_node_counts():
    assert [len(collocate(lambda x: 0.0, 2, L)["values"]) for L in range(5)] == [1, 5, 13, 29, 65]
    assert [len(collocate(lambda x: 0.0, 3, L)["values"]) for L in range(5)] == [1, 7, 25, 69, 177]


def test_levels_are_nested():
    for lv in range(1, 6):
        assert set(level_keys(lv - 1)) <= set(level_keys(lv))


def test_clenshaw_curtis_weights():
    for lv in range(6):
        xs = [node(k) for k in level_keys(lv)]
        w = cc_weights(lv)
        assert abs(sum(w) - 1.0) < 1e-14
        assert all(v > 0 for v in w)
        exact_degree = 1 if lv == 0 else 2**lv + 1
        for k in range(exact_degree + 1):
            got = sum(wi * xi**k for wi, xi in zip(w, xs))
            assert abs(got - mono_mean([k])) < 1e-13


def test_combination_coefficients_sum_to_one():
    for d in (1, 2, 3, 4):
        for L in range(5):
            assert sum(c for c, _ in smolyak_terms(d, L)) == 1


def test_surrogate_interpolates_at_the_nodes():
    sc = collocate(lambda x: math.exp(x[0] - 0.5 * x[1] + 0.3 * x[2]), 3, 3)
    for keys, y in sc["values"].items():
        assert abs(evaluate(sc, [node(k) for k in keys]) - y) < 1e-12


def test_reproduces_polynomials_of_total_degree_at_most_level():
    rng = random.Random(4)
    d, L = 3, 3
    monos = [b for b in itertools.product(range(L + 1), repeat=d) if sum(b) <= L]
    coef = {b: rng.uniform(-1, 1) for b in monos}

    def poly(x):
        return sum(c * math.prod(xk**bk for xk, bk in zip(x, b)) for b, c in coef.items())

    sc = collocate(poly, d, L)
    for _ in range(20):
        x = [rng.uniform(-1, 1) for _ in range(d)]
        assert abs(evaluate(sc, x) - poly(x)) < 1e-11


def test_quadrature_is_exact_through_total_degree_2l_plus_1():
    d, L = 2, 3
    w = quadrature_weights(collocate(lambda x: 0.0, d, L))
    for beta in itertools.product(range(2 * L + 2), repeat=d):
        if sum(beta) <= 2 * L + 1:
            got = sum(wk * math.prod(node(k) ** b for k, b in zip(key, beta)) for key, wk in w.items())
            assert abs(got - mono_mean(beta)) < 1e-12
    beta = (2, 2 * L)
    got = sum(wk * math.prod(node(k) ** b for k, b in zip(key, beta)) for key, wk in w.items())
    assert abs(got - mono_mean(beta)) > 1e-6


def test_ishigami_moments():
    sc = collocate(ishigami, 3, 6)
    assert len(sc["values"]) == 1073
    mean, var = moments(sc)
    assert abs(mean - 3.5) < 1e-12
    assert abs(var - 13.844588) < 1e-3
