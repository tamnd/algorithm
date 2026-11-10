# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bernoulli-sampling/. The authors are listed in prov/9SBD59.jsonl.

import itertools
import math
import random
from fractions import Fraction

from bernoulli_sampling import bernoulli_sample, bernoulli_sample_direct, geometric


class Branch(Exception):
    def __init__(self, weights):
        self.weights = weights


class Script:
    """Replays a prefix of choices; asks the enumerator to branch at the end of it."""

    def __init__(self, prefix):
        self.prefix = prefix
        self.pos = 0

    def choose(self, weights):
        if self.pos < len(self.prefix):
            v = self.prefix[self.pos][0]
            self.pos += 1
            return v
        raise Branch(weights)

    def randrange(self, k):
        return self.choose([Fraction(1, k)] * k)


def enumerate_all(fn):
    """Exact output law of fn(script) over every sequence of random choices."""
    law = {}
    stack = [[]]
    while stack:
        prefix = stack.pop()
        try:
            out = fn(Script(prefix))
        except Branch as b:
            for v, w in enumerate(b.weights):
                if w:
                    stack.append(prefix + [(v, w)])
            continue
        p = Fraction(1)
        for _, w in prefix:
            p *= w
        law[out] = law.get(out, 0) + p
    return law


def geometric_choices(n, p):
    """Weights of the gaps 0 .. n - 1, and of 'n or more' as the last choice."""
    q = 1 - p
    return [q ** g * p for g in range(n)] + [q ** n]


def bernoulli_law(n, p):
    q = 1 - p
    return {
        tuple(i for i in range(n) if bits[i]): p ** sum(bits) * q ** (n - sum(bits))
        for bits in itertools.product([0, 1], repeat=n)
    }


def test_skip_method_exact() -> None:
    for n in range(0, 6):
        for p in [Fraction(1, 3), Fraction(1, 2), Fraction(3, 4)]:
            def run(s, n=n, p=p):
                return tuple(bernoulli_sample(n, 0.5, None, geo=lambda: s.choose(geometric_choices(n, p))))
            assert enumerate_all(run) == bernoulli_law(n, p)


def test_wrong_skip_fails() -> None:
    # Starting at i = 0 instead of i = -1 is a known wrong variant: item 0 is never kept.
    n, p = 4, Fraction(1, 3)

    def run(s):
        S, i = [], 0
        while True:
            i += s.choose(geometric_choices(n, p)) + 1
            if i >= n:
                return tuple(S)
            S.append(i)

    assert enumerate_all(run) != bernoulli_law(n, p)


def test_direct_exact() -> None:
    for n in range(0, 5):
        for a, b in [(0, 3), (1, 3), (2, 3), (3, 3), (2, 5)]:
            law = enumerate_all(lambda s: tuple(bernoulli_sample_direct(n, a, b, s)))
            want = {k: v for k, v in bernoulli_law(n, Fraction(a, b)).items() if v}
            assert law == want


def test_example() -> None:
    rng = random.Random(6)
    assert bernoulli_sample(20, 0.25, rng) == [5, 11, 14, 16, 17]


def test_edges() -> None:
    rng = random.Random(1)
    assert bernoulli_sample(0, 0.5, rng) == []
    assert bernoulli_sample(10, 0.0, rng) == []
    assert bernoulli_sample(10, 1.0, rng) == list(range(10))
    assert bernoulli_sample(10 ** 9, 1e-18, rng) == []
    s = bernoulli_sample(1000, 0.3, rng)
    assert s == sorted(set(s)) and all(0 <= i < 1000 for i in s)


def test_log_without_log1p_fails() -> None:
    p = 1e-17
    assert math.log(1.0 - p) == 0.0  # so ln U / ln(1 - p) divides by zero
    assert math.log1p(-p) < 0.0


def test_geometric_moments() -> None:
    rng = random.Random(3)
    p, m = 0.2, 100000
    xs = [geometric(p, rng) for _ in range(m)]
    mean = sum(xs) / m
    # E[G] = (1 - p) / p = 4 and Var[G] = (1 - p) / p^2 = 20.
    assert abs(mean - 4.0) < 6 * math.sqrt(20.0 / m)
    counts = [0] * 6
    for x in xs:
        counts[min(x, 5)] += 1
    probs = [(1 - p) ** g * p for g in range(5)] + [(1 - p) ** 5]
    chi2 = sum((counts[g] - m * probs[g]) ** 2 / (m * probs[g]) for g in range(6))
    # 5 degrees of freedom: Pr[chi2 > 45] is below 2e-8.
    assert chi2 < 45


def test_sample_size_and_inclusion() -> None:
    rng = random.Random(8)
    n, p, runs = 30, 0.1, 20000
    size_counts = [0] * 8
    hits = [0] * n
    for _ in range(runs):
        s = bernoulli_sample(n, p, rng)
        size_counts[min(len(s), 7)] += 1
        for i in s:
            hits[i] += 1
    probs = [math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(7)]
    probs.append(1 - sum(probs))
    chi2 = sum((size_counts[k] - runs * probs[k]) ** 2 / (runs * probs[k]) for k in range(8))
    # 7 degrees of freedom: Pr[chi2 > 50] is below 2e-8.
    assert chi2 < 50
    sd = math.sqrt(runs * p * (1 - p))
    assert all(abs(h - runs * p) < 6 * sd for h in hits)


def test_skip_against_direct_statistically() -> None:
    rng = random.Random(21)
    n, runs = 12, 30000
    total_skip = sum(len(bernoulli_sample(n, 0.25, rng)) for _ in range(runs))
    total_direct = sum(len(bernoulli_sample_direct(n, 1, 4, rng)) for _ in range(runs))
    sd = math.sqrt(runs * n * 0.25 * 0.75)
    assert abs(total_skip - runs * n * 0.25) < 6 * sd
    assert abs(total_direct - runs * n * 0.25) < 6 * sd
