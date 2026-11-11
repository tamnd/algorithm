# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/push-sum/. The authors are listed in prov/X9WP5N.jsonl.

import itertools
import random
from fractions import Fraction

from push_sum import (contribution_step, kdg_rounds, potential, relative_error, round_step, run)


def test_mass_is_conserved_exactly() -> None:
    rng = random.Random(2003)
    for seed in range(6):
        n = rng.randint(2, 24)
        x = [rng.randint(-50, 50) for _ in range(n)]
        for s, w in run(x, 40, seed, exact=True):
            assert sum(s) == sum(x)
            assert sum(w) == n
            assert all(v > 0 for v in w)


def test_initial_potential_is_n_minus_1() -> None:
    for n in (1, 2, 5, 9):
        v = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
        assert potential(v, [Fraction(1)] * n) == n - 1


def test_expected_potential_drops_by_the_exact_factor() -> None:
    # Average over all n^n target assignments, in exact arithmetic, from a
    # state reached after two random rounds.
    for n in (2, 3, 4):
        rng = random.Random(n)
        v = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
        w = [Fraction(1)] * n
        for _ in range(2):
            v, w = contribution_step(v, w, [rng.randrange(n) for _ in range(n)])
        phi = potential(v, w)
        total = Fraction(0)
        for targets in itertools.product(range(n), repeat=n):
            nv, nw = contribution_step(v, w, targets)
            total += potential(nv, nw)
        assert total / n ** n == (Fraction(1, 2) - Fraction(1, 4 * n)) * phi


def test_the_error_never_grows() -> None:
    rng = random.Random(5)
    for seed in range(10):
        n = rng.randint(3, 40)
        x = [rng.uniform(-10, 10) for _ in range(n)]
        mean = sum(x) / n
        last = float("inf")
        for s, w in run(x, 60, seed):
            err = max(abs(a / b - mean) for a, b in zip(s, w))
            assert err <= last + 1e-12
            last = err


def test_error_is_below_eps_within_the_stated_rounds() -> None:
    delta = 0.1
    rng = random.Random(482)
    for n in (16, 64, 256):
        for eps in (1e-2, 1e-4):
            t = kdg_rounds(n, eps, delta)
            fails = 0
            runs = 30
            for _ in range(runs):
                x = [rng.uniform(0, 100) for _ in range(n)]
                s, w = [float(v) for v in x], [1.0] * n
                for _ in range(t):
                    s, w = round_step(s, w, [rng.randrange(n) for _ in range(n)])
                if relative_error(x, s, w) > eps:
                    fails += 1
            assert fails <= delta * runs, (n, eps, fails)
            assert fails == 0
