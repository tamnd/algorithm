# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/golden-section-search/. The authors are listed in prov/ZDRDPS.jsonl.

import random

from golden_section_search import RHO, golden_section_min


class Counter:
    def __init__(self, f):
        self.f = f
        self.calls = 0

    def __call__(self, x):
        self.calls += 1
        return self.f(x)


def test_example() -> None:
    x = golden_section_min(lambda t: (t - 2) ** 2, 0.0, 5.0)
    assert abs(x - 2.0) < 1e-7


def test_example_eight_evaluations() -> None:
    f = Counter(lambda t: (t - 2) ** 2)
    x = golden_section_min(f, 0.0, 5.0, steps=6)
    assert f.calls == 8
    assert abs(x - 1.99590) < 1e-4
    assert abs(x - 2.0) <= 5.0 * RHO ** 7 / 2


def test_evaluation_count() -> None:
    for steps in range(0, 30):
        f = Counter(lambda t: abs(t - 0.3))
        golden_section_min(f, 0.0, 1.0, steps)
        assert f.calls == steps + 2


def test_bracket_bound_random() -> None:
    rng = random.Random(7)
    for _ in range(2000):
        a = rng.uniform(-100, 100)
        b = a + rng.uniform(0.1, 100)
        m = rng.uniform(a, b)
        steps = rng.randrange(0, 40)
        left = rng.uniform(0.1, 5)
        right = rng.uniform(0.1, 5)
        f = lambda t: left * (m - t) if t < m else right * (t - m)
        x = golden_section_min(f, a, b, steps)
        assert abs(x - m) <= (b - a) * RHO ** (steps + 1) / 2 + 1e-9 * (b - a)


def test_maximum_by_negation() -> None:
    x = golden_section_min(lambda t: -(t * (4 - t)), 0.0, 4.0, 80)
    assert abs(x - 2.0) < 1e-7


def test_minimum_at_an_end() -> None:
    assert golden_section_min(lambda t: t, 0.0, 1.0) < 1e-12
    assert golden_section_min(lambda t: -t, 0.0, 1.0) > 1 - 1e-12
