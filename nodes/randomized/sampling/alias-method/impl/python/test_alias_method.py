# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alias-method/. The authors are listed in prov/95DG3T.jsonl.

import random
from fractions import Fraction

import pytest

from alias_method import (
    alias_build,
    alias_build_float,
    alias_distribution,
    alias_sample,
    alias_sample_float,
)


class Branch(Exception):
    def __init__(self, k: int) -> None:
        self.k = k


class Script:
    """A fake generator that replays a prefix of choices and then asks to branch."""

    def __init__(self, prefix):
        self.prefix = prefix
        self.pos = 0

    def randrange(self, k: int) -> int:
        if self.pos < len(self.prefix):
            v, kk = self.prefix[self.pos]
            assert kk == k
            self.pos += 1
            return v
        raise Branch(k)


def enumerate_all(fn):
    """Run fn on every sequence of random choices; return the exact output law."""
    law = {}
    stack = [[]]
    while stack:
        prefix = stack.pop()
        try:
            out = fn(Script(prefix))
        except Branch as b:
            for v in range(b.k):
                stack.append(prefix + [(v, b.k)])
            continue
        p = Fraction(1)
        for _, k in prefix:
            p /= k
        law[out] = law.get(out, 0) + p
    return law


def exact_law(weights):
    W = sum(Fraction(w) for w in weights)
    return [Fraction(w) / W for w in weights]


def test_worked_example() -> None:
    prob, alias, W = alias_build([1, 2, 3, 4, 6])
    assert W == 16
    assert prob == [5, 10, 15, 16, 12]
    assert alias == [4, 4, 4, 3, 3]
    assert alias_distribution(prob, alias, W) == exact_law([1, 2, 3, 4, 6])


def test_enumeration_matches_weights() -> None:
    weights = [1, 2, 3, 4, 6]
    prob, alias, W = alias_build(weights)
    law = enumerate_all(lambda r: alias_sample(prob, alias, W, r))
    assert [law.get(i, 0) for i in range(5)] == exact_law(weights)


def test_edges() -> None:
    assert alias_build([7]) == ([7], [0], 7)
    prob, alias, W = alias_build([3, 3, 3])
    assert prob == [9, 9, 9] and alias == [0, 1, 2]
    prob, alias, W = alias_build([0, 5, 0])
    assert alias_distribution(prob, alias, W) == [0, 1, 0]
    with pytest.raises(ValueError):
        alias_build([])
    with pytest.raises(ValueError):
        alias_build([0, 0])
    with pytest.raises(ValueError):
        alias_build([1, -1, 2])


def test_fractions() -> None:
    weights = [Fraction(1, 3), Fraction(1, 6), Fraction(1, 2)]
    prob, alias, W = alias_build(weights)
    assert alias_distribution(prob, alias, W) == exact_law(weights)
    law = enumerate_all(lambda r: alias_sample(prob, alias, W, r))
    assert [law.get(i, 0) for i in range(3)] == exact_law(weights)


def test_random_weights_exact() -> None:
    rng = random.Random(7)
    for _ in range(600):
        n = rng.randrange(1, 9)
        weights = [rng.randrange(0, 12) for _ in range(n)]
        if sum(weights) == 0:
            weights[0] = 1
        prob, alias, W = alias_build(weights)
        assert all(0 <= p <= W for p in prob)
        assert all(prob[i] == W or weights[alias[i]] > 0 for i in range(n))
        assert alias_distribution(prob, alias, W) == exact_law(weights)
    for _ in range(40):
        n = rng.randrange(1, 5)
        weights = [rng.randrange(0, 5) for _ in range(n)]
        if sum(weights) == 0:
            weights[-1] = 2
        prob, alias, W = alias_build(weights)
        law = enumerate_all(lambda r: alias_sample(prob, alias, W, r))
        assert [law.get(i, 0) for i in range(n)] == exact_law(weights)


def test_wrong_scaling_fails() -> None:
    # A known wrong variant: threshold W but no factor n in q.
    weights = [1, 2, 3, 4, 6]
    n, W = len(weights), sum(weights)
    q = list(weights)
    prob = [min(x, W) for x in q]
    alias = [4] * n
    assert alias_distribution(prob, alias, W) != exact_law(weights)


def test_float_table_close_to_exact() -> None:
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randrange(1, 30)
        p = [rng.random() for _ in range(n)]
        prob, alias = alias_build_float(p)
        total = sum(p)
        got = [0.0] * n
        for i in range(n):
            got[i] += prob[i] / n
            got[alias[i]] += (1.0 - prob[i]) / n
        for i in range(n):
            assert abs(got[i] - p[i] / total) < 1e-12


def test_float_sampling_chi_squared() -> None:
    weights = [1, 2, 3, 4, 6]
    prob, alias = alias_build_float([float(w) for w in weights])
    rng = random.Random(2024)
    m = 160000
    counts = [0] * 5
    for _ in range(m):
        counts[alias_sample_float(prob, alias, rng)] += 1
    chi2 = sum((counts[i] - m * weights[i] / 16) ** 2 / (m * weights[i] / 16) for i in range(5))
    # 4 degrees of freedom: Pr[chi2 > 40] is below 5e-8.
    assert chi2 < 40
