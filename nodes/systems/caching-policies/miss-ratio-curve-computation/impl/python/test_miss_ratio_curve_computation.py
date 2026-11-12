# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/miss-ratio-curve-computation/. The authors are listed in prov/XPW03J.jsonl.

import random
from fractions import Fraction

from miss_ratio_curve_computation import (
    aet_curve,
    curve_from_distances,
    lru_curve,
    mattson_distances,
    simulate_curve,
    tree_distances,
)


def zipf_trace(rng: random.Random, n: int, m: int, s: float = 1.0) -> list[int]:
    weights = [1 / (i + 1) ** s for i in range(m)]
    return rng.choices(range(m), weights, k=n)


def test_example_distances() -> None:
    trace = list("abcbadac")
    assert tree_distances(trace) == [None, None, None, 1, 2, None, 1, 3]
    assert lru_curve(trace, 4) == [1, 1, Fraction(6, 8), Fraction(5, 8), Fraction(4, 8)]


def test_tree_equals_mattson_stack() -> None:
    rng = random.Random(1)
    for _ in range(200):
        trace = [rng.randrange(rng.randint(1, 40)) for _ in range(rng.randint(0, 300))]
        assert tree_distances(trace) == mattson_distances(trace)


def test_curve_equals_simulation() -> None:
    rng = random.Random(2)
    for _ in range(40):
        trace = zipf_trace(rng, rng.randint(1, 400), 30)
        assert lru_curve(trace, 32) == simulate_curve(trace, 32)
        assert curve_from_distances(mattson_distances(trace), 32) == simulate_curve(trace, 32)


def test_tree_method_is_fast_on_a_long_trace() -> None:
    rng = random.Random(3)
    trace = zipf_trace(rng, 200_000, 50_000, 0.9)
    d = tree_distances(trace)
    assert len(d) == len(trace)
    # spot check a few requests against a direct count of distinct items
    for t in rng.sample(range(len(trace)), 20):
        if d[t] is not None:
            p = max(i for i in range(t) if trace[i] == trace[t])
            assert d[t] == len(set(trace[p + 1 : t]))


def test_aet_is_exact_on_a_loop() -> None:
    trace = list(range(20)) * 30
    exact = [float(x) for x in lru_curve(trace, 25)]
    assert aet_curve(trace, 25) == exact


def test_aet_is_close_on_a_zipf_trace() -> None:
    rng = random.Random(4)
    trace = zipf_trace(rng, 100_000, 10_000, 0.9)
    sizes = 3000
    exact = lru_curve(trace, sizes)
    model = aet_curve(trace, sizes)
    mae = sum(abs(float(e) - a) for e, a in zip(exact, model)) / (sizes + 1)
    assert mae < 0.005  # about 0.0008 with this seed; the largest error is about 0.007
