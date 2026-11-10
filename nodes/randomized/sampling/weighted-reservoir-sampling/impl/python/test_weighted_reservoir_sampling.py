# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-reservoir-sampling/. The authors are listed in prov/8720DK.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from weighted_reservoir_sampling import a_expj, a_res, power_key


class InsertionSource:
    """A fake source of uniform reals that enumerates their relative order.

    Call number m (counting from 0) has m + 1 possible places among the values
    returned so far, each with probability 1 / (m + 1). This is exactly the
    law of the relative order of independent uniform reals. The script fixes
    the places; places after the end of the script are 0.
    """

    def __init__(self, script: list[int]) -> None:
        self.script = script
        self.values: list[Fraction] = []
        self.choices: list[int] = []
        self.sizes: list[int] = []

    def random(self) -> Fraction:
        m = len(self.values)
        c = self.script[m] if m < len(self.script) else 0
        s = sorted(self.values)
        lo = Fraction(0) if c == 0 else s[c - 1]
        hi = Fraction(1) if c == m else s[c]
        v = (lo + hi) / 2
        self.values.append(v)
        self.choices.append(c)
        self.sizes.append(m + 1)
        return v


def exact_distribution(run) -> dict:
    """Run run(source) over all relative orders and add up the exact probabilities."""
    dist: dict = {}
    script: list[int] = []
    while True:
        src = InsertionSource(script)
        out = run(src)
        p = Fraction(1)
        for size in src.sizes:
            p /= size
        dist[out] = dist.get(out, Fraction(0)) + p
        i = len(src.choices) - 1
        while i >= 0 and src.choices[i] == src.sizes[i] - 1:
            i -= 1
        if i < 0:
            return dist
        script = src.choices[:i] + [src.choices[i] + 1]


def max_key(w: float, rng) -> Fraction:
    """For an integer weight w, the largest of w uniforms has the law of u^(1/w)."""
    return max(rng.random() for _ in range(int(w)))


def successive(weights: dict, k: int) -> dict:
    """Exact law of weighted sampling without replacement, as ordered k-tuples."""
    exact_w = {x: Fraction(w) for x, w in weights.items()}
    total = sum(exact_w.values())
    dist = {}
    for seq in itertools.permutations(weights, min(k, len(weights))):
        p = Fraction(1)
        left = total
        for x in seq:
            p *= exact_w[x] / left
            left -= exact_w[x]
        dist[seq] = p
    return dist


class Scripted:
    """Returns the given reals in order, for a worked example."""

    def __init__(self, values: list[float]) -> None:
        self.values = list(values)

    def random(self) -> float:
        return self.values.pop(0)


def chi2_threshold(df: int, z: float = 6.0) -> float:
    a = 2.0 / (9.0 * df)
    return df * (1.0 - a + z * math.sqrt(a)) ** 3


def test_worked_example() -> None:
    # u = 0.5, 0.3, 0.8, 0.2 for weights 1, 2, 3, 4; the source returns 1 - u.
    stream = [("a", 1), ("b", 2), ("c", 3), ("d", 4)]
    assert a_res(stream, 2, Scripted([0.5, 0.7, 0.2, 0.8])) == ["c", "d"]  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "weights,k",
    [
        ({"a": 1, "b": 2, "c": 3}, 2),
        ({"a": 1, "b": 2, "c": 1, "d": 2}, 2),
        ({"a": 2, "b": 1, "c": 1, "d": 1, "e": 1}, 3),
        ({"a": 3, "b": 1, "c": 2}, 1),
        ({"a": 1, "b": 1, "c": 1, "d": 1}, 2),
    ],
)
def test_exact_successive_sampling(weights: dict, k: int) -> None:
    stream = list(weights.items())
    got = exact_distribution(lambda src: tuple(a_res(stream, k, src, key=max_key)))
    assert got == successive(weights, k)


def test_exact_inclusion_is_not_proportional() -> None:
    # Successive sampling is not "inclusion probability proportional to weight".
    weights = {"a": 1, "b": 2, "c": 3}
    dist = successive(weights, 2)
    incl_c = sum(p for seq, p in dist.items() if "c" in seq)
    assert incl_c == Fraction(1, 2) + Fraction(1, 6) * Fraction(3, 5) + Fraction(1, 3) * Fraction(3, 4)
    assert incl_c != Fraction(2 * 3, 6)


def chi2_against(sampler, weights: dict, k: int, trials: int, seed: int) -> float:
    rng = random.Random(seed)
    exact = successive(weights, k)
    counts = dict.fromkeys(exact, 0)
    stream = list(weights.items())
    for _ in range(trials):
        counts[tuple(sampler(stream, k, rng))] += 1
    return sum((counts[s] - trials * float(p)) ** 2 / (trials * float(p)) for s, p in exact.items())


def test_power_key_and_expj_match_successive_sampling() -> None:
    weights = {"a": 1.0, "b": 2.0, "c": 3.0, "d": 4.0, "e": 0.5, "f": 6.5}
    df = 6 * 5 - 1
    assert chi2_against(a_res, weights, 2, 30000, 1) < chi2_threshold(df)
    assert chi2_against(a_expj, weights, 2, 30000, 2) < chi2_threshold(df)
    assert chi2_against(a_expj, {"a": 0.1, "b": 5.0, "c": 1.0, "d": 0.3}, 3, 30000, 3) < chi2_threshold(23)


def test_wrong_key_fails() -> None:
    def linear_key(w, rng):
        return w * rng.random()

    weights = {"a": 1.0, "b": 2.0, "c": 3.0, "d": 4.0}
    assert chi2_against(lambda s, k, r: a_res(s, k, r, key=linear_key), weights, 2, 30000, 4) > 10 * chi2_threshold(11)


def test_edges_and_subsets() -> None:
    rng = random.Random(5)
    assert a_res([], 3, rng) == []
    assert a_expj([], 3, rng) == []
    assert a_res([("x", 1.0)], 3, rng) == ["x"]
    assert a_expj([("x", 1.0)], 3, rng) == ["x"]
    assert a_res([("x", 1.0)], 0, rng) == []
    with pytest.raises(ValueError):
        a_res([("x", 0.0)], 1, rng)
    with pytest.raises(ValueError):
        a_expj([("x", 1.0), ("y", -1.0)], 1, rng)
    for _ in range(300):
        n = rng.randrange(0, 40)
        k = rng.randrange(0, 6)
        stream = [(i, rng.uniform(0.01, 10.0)) for i in range(n)]
        for f in (a_res, a_expj):
            out = f(stream, k, rng)
            assert len(out) == min(n, k)
            assert len(set(out)) == len(out)


def test_power_key_range() -> None:
    rng = random.Random(6)
    for _ in range(1000):
        r = power_key(rng.uniform(0.001, 100.0), rng)
        assert 0.0 < r <= 1.0


class Counting:
    def __init__(self, seed: int) -> None:
        self.rng = random.Random(seed)
        self.calls = 0

    def random(self) -> float:
        self.calls += 1
        return self.rng.random()


def test_expj_draws_few_random_numbers() -> None:
    n, k, runs = 20000, 10, 300
    entries = k * sum(1.0 / t for t in range(k + 1, n + 1))
    stream = [(i, 1.0) for i in range(n)]
    total = 0
    for seed in range(runs):
        rng = Counting(seed)
        a_expj(stream, k, rng)  # type: ignore[arg-type]
        total += rng.calls
    mean = total / runs
    expected = k + 1 + 2 * entries
    assert abs(mean - expected) < 6
