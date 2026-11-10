# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vitter-reservoir-skip/. The authors are listed in prov/2ZA0EM.jsonl.

import itertools
import math
import random
from fractions import Fraction

from vitter_reservoir_skip import skip_x, skip_z, vitter_reservoir_skip


def algorithm_r(stream, k, rng):
    """The reference method (Algorithm R), used as the oracle in distribution."""
    r = []
    for t, x in enumerate(stream, 1):
        if t <= k:
            r.append(x)
        else:
            j = rng.randrange(t)
            if j < k:
                r[j] = x
    return r


class Counting:
    """A wrapper of a seeded generator that counts the calls of random and randrange."""

    def __init__(self, seed: int) -> None:
        self.rng = random.Random(seed)
        self.calls = 0

    def random(self) -> float:
        self.calls += 1
        return self.rng.random()

    def randrange(self, stop: int) -> int:
        self.calls += 1
        return self.rng.randrange(stop)


def chi2_threshold(df: int, z: float = 6.0) -> float:
    """Wilson-Hilferty approximation of the chi-squared quantile at about z normal deviations."""
    a = 2.0 / (9.0 * df)
    return df * (1.0 - a + z * math.sqrt(a)) ** 3


def subset_chi2(sampler, n: int, k: int, trials: int, seed: int) -> float:
    rng = random.Random(seed)
    cells = list(itertools.combinations(range(n), k))
    counts = dict.fromkeys(cells, 0)
    for _ in range(trials):
        counts[tuple(sorted(sampler(range(n), k, rng)))] += 1
    e = trials / len(cells)
    return sum((c - e) ** 2 / e for c in counts.values())


def skip_pmf(t: int, k: int, s: int) -> Fraction:
    """f(s) = Pr[skip = s] = k / (t + s + 1) * prod_{i<k} (t - i) / (t + s - i)."""
    p = Fraction(k, t + s + 1)
    for i in range(k):
        p *= Fraction(t - i, t + s - i)
    return p


def test_edges() -> None:
    rng = random.Random(1)
    assert vitter_reservoir_skip([], 2, rng) == []
    assert vitter_reservoir_skip([1], 2, rng) == [1]
    assert vitter_reservoir_skip([1, 2, 3], 0, rng) == []
    assert sorted(vitter_reservoir_skip([1, 2, 3], 3, rng, threshold=0)) == [1, 2, 3]


def test_sample_is_a_subset() -> None:
    rng = random.Random(2)
    for _ in range(500):
        n = rng.randrange(0, 80)
        k = rng.randrange(0, 6)
        th = rng.choice([0.0, 1.0, 22.0])
        out = vitter_reservoir_skip(iter(range(n)), k, rng, threshold=th)
        assert len(out) == min(n, k)
        assert len(set(out)) == len(out)


def test_envelope_inequalities_exactly() -> None:
    # h(s) <= f(s) <= c g(x) for s <= x < s + 1: the lemma behind Algorithm Z.
    for k in range(1, 5):
        for t in range(k, k + 25):
            c = Fraction(t + 1, t - k + 1)
            term = t - k + 1
            for s in range(0, 40):
                f = skip_pmf(t, k, s)
                h = Fraction(k, t + 1) * Fraction(term, term + s) ** (k + 1)
                assert h <= f
                for x in (Fraction(s), s + Fraction(1, 2), s + Fraction(99, 100)):
                    g = Fraction(k, 1) / (t + x) * (Fraction(t) / (t + x)) ** k
                    assert f <= c * g


def test_skip_laws() -> None:
    for t, k in ((3, 3), (30, 3), (100, 2)):
        bins = 25
        pmf = [skip_pmf(t, k, s) for s in range(bins)]
        probs = [float(p) for p in pmf] + [1.0 - float(sum(pmf))]
        for which in ("x", "z"):
            rng = random.Random(7 + t)
            counts = [0] * (bins + 1)
            w = math.exp(-math.log(1.0 - rng.random()) / k)
            trials = 30000
            for _ in range(trials):
                if which == "x":
                    s = skip_x(t, k, rng)
                else:
                    s, w = skip_z(t, k, w, rng)
                counts[min(s, bins)] += 1
            chi2 = sum((c - trials * p) ** 2 / (trials * p) for c, p in zip(counts, probs))
            assert chi2 < chi2_threshold(bins)


def test_same_distribution_as_algorithm_r() -> None:
    n, k, trials = 12, 3, 44000
    df = math.comb(n, k) - 1

    def pure_z(s, kk, r):
        return vitter_reservoir_skip(s, kk, r, threshold=0.0)

    def mixed(s, kk, r):
        return vitter_reservoir_skip(s, kk, r, threshold=2.0)

    assert subset_chi2(pure_z, n, k, trials, 3) < chi2_threshold(df)
    assert subset_chi2(mixed, n, k, trials, 4) < chi2_threshold(df)
    assert subset_chi2(vitter_reservoir_skip, n, k, trials, 5) < chi2_threshold(df)


def test_inclusion_probability_long_stream() -> None:
    n, k, trials = 400, 4, 20000
    rng = random.Random(8)
    counts = [0] * n
    for _ in range(trials):
        for x in vitter_reservoir_skip(range(n), k, rng, threshold=3.0):
            counts[x] += 1
    e = trials * k / n
    chi2 = sum((c - e) ** 2 / e for c in counts)
    assert chi2 < chi2_threshold(n - 1)


def test_number_of_random_draws() -> None:
    n, k, runs = 100000, 10, 400
    entries = k * sum(1.0 / t for t in range(k + 1, n + 1))  # about 91.6
    total = 0
    for seed in range(runs):
        rng = Counting(seed)
        vitter_reservoir_skip(range(n), k, rng)  # type: ignore[arg-type]
        total += rng.calls
    mean = total / runs
    # Two draws per entry (the skip and the slot) plus the rejected rounds of Z.
    assert 2 * entries < mean < 3 * entries
    assert mean < (n - k) / 300
