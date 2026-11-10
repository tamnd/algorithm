# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karp-luby-estimator/. The authors are listed in prov/KKHPVT.jsonl.

import random
from fractions import Fraction

import pytest

from karp_luby_estimator import (
    coverage_estimate,
    dnf_count_brute_force,
    dnf_oracles,
    karp_luby,
    sample_count,
)


class ScriptedRandom:
    """A fake source: randrange(size) returns the next scripted value (0 after the script)."""

    def __init__(self, script: list[int]) -> None:
        self.script = script
        self.calls: list[tuple[int, int]] = []

    def randrange(self, size: int) -> int:
        i = len(self.calls)
        v = self.script[i] if i < len(self.script) else 0
        assert 0 <= v < size
        self.calls.append((v, size))
        return v


def exact_expectation(run) -> tuple[Fraction, Fraction]:
    """E[run(src)] and E[run(src)^2] over every sequence of random integers."""
    e1 = Fraction(0)
    e2 = Fraction(0)
    script: list[int] = []
    while True:
        src = ScriptedRandom(script)
        out = Fraction(run(src))
        p = Fraction(1)
        for _, size in src.calls:
            p /= size
        e1 += p * out
        e2 += p * out * out
        i = len(src.calls) - 1
        while i >= 0 and src.calls[i][0] == src.calls[i][1] - 1:
            i -= 1
        if i < 0:
            return e1, e2
        script = [v for v, _ in src.calls[:i]] + [src.calls[i][0] + 1]


EXAMPLE = [[1, 2], [-1, 3], [2, 3]]  # (x1 and x2) or (not x1 and x3) or (x2 and x3)


def test_worked_example_counts() -> None:
    sizes, _, _ = dnf_oracles(EXAMPLE, 3)
    assert sizes == [2, 2, 2]
    assert dnf_count_brute_force(EXAMPLE, 3) == 4


FORMULAS = [
    (EXAMPLE, 3),
    ([[1], [2], [3]], 3),
    ([[1, -2], [2, -3], [3, -1], [1, 2, 3]], 3),
    ([[1, -1], [2]], 3),
    ([[1, 2, 3, 4]], 4),
    ([[1], [1], [1]], 2),
    ([[-1, 2], [3, 4], [-2, -4], [1, 3]], 4),
]


@pytest.mark.parametrize("clauses,n_vars", FORMULAS)
def test_exact_unbiased_single_sample(clauses, n_vars) -> None:
    sizes, sample, contains = dnf_oracles(clauses, n_vars)
    true = dnf_count_brute_force(clauses, n_vars)
    m = len(sizes)
    w = sum(sizes)

    def zero_one(src):
        return karp_luby(sizes, sample, contains, 0.5, 0.5, src, n_samples=1)

    def coverage(src):
        x = sample_and_keep(src)
        return Fraction(w, sum(1 for j in range(m) if contains(j, x)))

    def sample_and_keep(src):
        # one draw of the pair (i, x), as in coverage_estimate
        prefix, s = [], 0
        for v in sizes:
            s += v
            prefix.append(s)
        r = src.randrange(w)
        i = next(k for k, p in enumerate(prefix) if r < p)
        return sample(i, src)

    e1, e2 = exact_expectation(zero_one)
    assert e1 == true
    # relative variance of the 0-1 estimator is W/|U| - 1 <= m - 1
    assert e2 / (e1 * e1) - 1 == Fraction(w, true) - 1
    assert Fraction(w, true) - 1 <= m - 1

    c1, c2 = exact_expectation(coverage)
    assert c1 == true
    assert c2 / (c1 * c1) - 1 <= m - 1
    assert c2 <= w * c1


def test_coverage_function_matches_exact_mean() -> None:
    sizes, sample, contains = dnf_oracles(EXAMPLE, 3)

    def run(src):
        return Fraction(coverage_estimate(sizes, sample, contains, 1, src)).limit_denominator(1000)

    e1, _ = exact_expectation(run)
    assert e1 == 4


def random_dnf(rng: random.Random, n_vars: int, m: int) -> list[list[int]]:
    out = []
    for _ in range(m):
        width = rng.randrange(1, n_vars + 1)
        vars_ = rng.sample(range(1, n_vars + 1), width)
        out.append([v if rng.random() < 0.5 else -v for v in vars_])
    return out


def test_against_brute_force() -> None:
    rng = random.Random(1)
    eps, delta = 0.1, 0.01
    misses = 0
    for _ in range(25):
        n_vars = rng.randrange(4, 13)
        m = rng.randrange(1, 9)
        clauses = random_dnf(rng, n_vars, m)
        true = dnf_count_brute_force(clauses, n_vars)
        sizes, sample, contains = dnf_oracles(clauses, n_vars)
        est = karp_luby(sizes, sample, contains, eps, delta, rng)
        if abs(est - true) > eps * true:
            misses += 1
    assert misses <= 1


def test_coverage_against_brute_force() -> None:
    rng = random.Random(2)
    for _ in range(10):
        n_vars = rng.randrange(4, 11)
        m = rng.randrange(1, 7)
        clauses = random_dnf(rng, n_vars, m)
        true = dnf_count_brute_force(clauses, n_vars)
        sizes, sample, contains = dnf_oracles(clauses, n_vars)
        est = coverage_estimate(sizes, sample, contains, sample_count(m, 0.1, 0.01), rng)
        assert abs(est - true) <= 0.1 * true


def test_sparse_formula_where_plain_monte_carlo_fails() -> None:
    # 2 satisfying assignments out of 2^40: plain sampling sees none, Karp-Luby is exact here.
    n_vars = 40
    clauses = [list(range(1, 41)), [-v for v in range(1, 41)]]
    sizes, sample, contains = dnf_oracles(clauses, n_vars)
    assert sizes == [1, 1]
    assert karp_luby(sizes, sample, contains, 0.1, 0.01, random.Random(3)) == 2.0


def test_sample_count_and_errors() -> None:
    assert sample_count(1, 0.5, 0.5) == 17  # ceil(3 ln 4 / 0.25) = ceil(16.64)
    with pytest.raises(ValueError):
        sample_count(1, 0.0, 0.5)
    with pytest.raises(ValueError):
        sample_count(1, 0.5, 1.0)
    sizes, sample, contains = dnf_oracles([[1, -1]], 2)
    assert sizes == [0]
    assert karp_luby(sizes, sample, contains, 0.5, 0.5, random.Random(4)) == 0.0
