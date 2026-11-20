# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/saltelli-sampling-scheme/. The authors are listed in prov/SEW99Y.jsonl.
import math
import random

from saltelli_sampling_scheme import brute_force_first_order, ishigami, ishigami_exact, saltelli


def unif_pi(u, i):
    return -math.pi + 2 * math.pi * u


def unit(u, i):
    return u


def tolerance(res, key, i):
    """Four standard errors of the numerator, plus four of the variance in the denominator."""
    return 4 * (res[key + "_err"][i] + abs(res[key][i]) * res["variance_rel_err"])


def test_ishigami_exact_values():
    ex = ishigami_exact()
    assert abs(ex["variance"] - 13.84459) < 1e-5
    assert [round(x, 4) for x in ex["S"]] == [0.3139, 0.4424, 0.0]
    assert [round(x, 4) for x in ex["ST"]] == [0.5576, 0.4424, 0.2437]


def test_ishigami_indices_within_four_standard_errors():
    ex = ishigami_exact()
    res = saltelli(ishigami, 3, 10000, random.Random(2002), unif_pi)
    assert res["runs"] == 10000 * (3 + 2)
    for i in range(3):
        assert abs(res["S"][i] - ex["S"][i]) < tolerance(res, "S", i)
        assert abs(res["ST"][i] - ex["ST"][i]) < tolerance(res, "ST", i)
    # x3 acts only through its interaction with x1
    assert res["ST"][2] - res["S"][2] > 0.15


def test_linear_model_has_equal_first_order_and_total_indices():
    c = [1.0, 2.0, 3.0]
    f = lambda x: sum(ci * xi for ci, xi in zip(c, x))  # noqa: E731
    res = saltelli(f, 3, 5000, random.Random(5), unit)
    total = sum(ci * ci for ci in c)
    for i in range(3):
        exact = c[i] ** 2 / total
        assert abs(res["S"][i] - exact) < tolerance(res, "S", i)
        assert abs(res["ST"][i] - exact) < tolerance(res, "ST", i)


def test_an_input_that_the_model_ignores_gets_exactly_zero():
    f = lambda x: x[0] ** 2 + math.sin(x[0])  # noqa: E731
    res = saltelli(f, 3, 500, random.Random(8), unit)
    assert res["S"][1] == 0.0 and res["ST"][1] == 0.0
    assert res["S"][2] == 0.0 and res["ST"][2] == 0.0
    assert abs(res["ST"][0] - 1.0) < tolerance(res, "ST", 0)


def test_first_order_agrees_with_the_double_loop_estimate():
    ex = ishigami_exact()
    res = saltelli(ishigami, 3, 4000, random.Random(13), unif_pi)
    v1 = brute_force_first_order(ishigami, 3, 0, 300, 100, random.Random(17), unif_pi)
    s1_brute = v1 / ex["variance"]
    assert abs(res["S"][0] - s1_brute) < 0.08
