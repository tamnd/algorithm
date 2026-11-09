# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cross-entropy-method/. The authors are listed in prov/HK9SF5.jsonl.

import math
import random

from cross_entropy_method import (
    ce_bernoulli,
    ce_gaussian,
    cut_value,
    elite_count,
    max_cut_brute_force,
    random_graph,
)

N = 16
W = random_graph(N, random.Random(7))
P0 = [0.5] * (N - 1) + [0.0]  # vertex 15 is fixed on side 0, which removes the symmetry of cuts


def cut(x):
    return cut_value(W, x)


def test_instance_optimum() -> None:
    assert max_cut_brute_force(W) == 140.0


def test_update_is_smoothed_elite_frequency() -> None:
    for alpha in (1.0, 0.7):
        trace = []
        ce_bernoulli(cut, P0, 50, 0.1, alpha, 15, random.Random(1), trace)
        k = elite_count(50, 0.1)
        prev = P0
        for _, p in trace:
            assert all(0.0 <= q <= 1.0 for q in p)
            for q, r in zip(p, prev):
                w = (q - (1 - alpha) * r) / alpha  # the elite frequency
                assert abs(w * k - round(w * k)) < 1e-9 and 0 <= round(w * k) <= k
                if r in (0.0, 1.0):
                    assert q == r  # a component at 0 or 1 never moves again
            prev = p


def test_invariant_under_increasing_transformation() -> None:
    a = ce_bernoulli(cut, P0, 50, 0.1, 0.7, 20, random.Random(2))
    b = ce_bernoulli(lambda x: math.exp(cut(x) / 10), P0, 50, 0.1, 0.7, 20, random.Random(2))
    assert a[0] == b[0] and a[2] == b[2]


def test_degenerate_limit_need_not_be_optimal() -> None:
    x, s, p = ce_bernoulli(cut, P0, 200, 0.1, 0.7, 30, random.Random(0))
    assert all(q in (0.0, 1.0) or min(q, 1 - q) < 1e-6 for q in p)
    assert cut([round(q) for q in p]) == 139.0 < 140.0


def test_fixed_seed_reaches_optimum() -> None:
    x, s, p = ce_bernoulli(cut, P0, 200, 0.1, 0.3, 60, random.Random(1))
    assert s == 140.0 and cut(x) == 140.0
    ras = lambda x: 20 + sum(t * t - 10 * math.cos(2 * math.pi * t) for t in x)
    trace = []
    x, fx, mu, sigma = ce_gaussian(ras, [3.0, 3.0], [5.0, 5.0], 500, 0.1, 0.7, 100, random.Random(0), trace)
    assert fx < 1e-6
    assert all(s >= 0 for _, _, sig in trace for s in sig)
