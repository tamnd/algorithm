# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regret-matching/. The authors are listed in prov/FJGSGJ.jsonl.
"""Tests of conditional and unconditional regret matching."""

import math
import random
from fractions import Fraction

import pytest

from agtgame import from_bimatrix, is_coarse_correlated, is_correlated, profiles, random_game
from regret_matching import RegretMatcher, ce_gap, expected_self_play, payoff_range, regret_matching

F = Fraction
CHICKEN = from_bimatrix([[0, 7], [2, 6]], [[0, 2], [7, 6]])  # strategy 0 is D, 1 is C


def ce_terms(game, z):
    """Return the CE inequality terms sum_{s: s_i = j} z(s) (u_i(l, s_-i) - u_i(s)), from z only."""
    sizes, pay = game
    out = []
    for i, k in enumerate(sizes):
        rows = [[F(0)] * k for _ in range(k)]
        for s, q in z.items():
            for l in range(k):
                if l != s[i]:
                    rows[s[i]][l] += q * (pay[s[:i] + (l,) + s[i + 1:]][i] - pay[s][i])
        out.append(rows)
    return out


def test_identity_regrets_equal_ce_terms_on_random_games():
    rng = random.Random(9001)
    for _ in range(40):
        sizes = tuple(rng.randint(2, 3) for _ in range(rng.randint(2, 3)))
        game = random_game(rng, sizes, -4, 4)
        T = rng.randint(1, 120)
        z, D = regret_matching(game, T, rng)
        assert sum(z.values()) == 1 and all(q > 0 for q in z.values())
        terms = ce_terms(game, z)
        for i, k in enumerate(sizes):
            for j in range(k):
                for l in range(k):
                    assert terms[i][j][l] == D[i][j][l] / T
        gap = ce_gap(D, T)
        assert (gap == 0) == is_correlated(game, z)


def test_chicken_converges():
    for seed in (1, 2, 3):
        T = 1500
        z, D = regret_matching(CHICKEN, T, random.Random(seed))
        gap = ce_gap(D, T)
        assert gap <= F(1, 50)  # measured: below 1/300 for these seeds
        assert max(ce_terms(CHICKEN, z)[i][j][l] for i in range(2) for j in range(2) for l in range(2)) == gap


def test_prisoners_dilemma_reaches_defection():
    pd = from_bimatrix([[3, 0], [5, 1]], [[3, 5], [0, 1]])  # strategy 1 is defect
    for seed in (5, 6):
        z, _ = regret_matching(pd, 400, random.Random(seed))
        assert z.get((1, 1), 0) >= F(9, 10)


def test_page_trace_is_absorbing():
    # From (C, C) with mu = 8: one regret of 1 each, then (D, C) is never left.
    class Draws:
        def __init__(self, xs):
            self.xs = list(xs)

        def randrange(self, k):
            return 1

        def random(self):
            return self.xs.pop(0) if self.xs else 0.5

    z, D = regret_matching(CHICKEN, 4, Draws([0.05, 0.95]), mu=8)
    assert z == {(1, 1): F(1, 4), (0, 1): F(3, 4)}
    assert D[0][1][0] == 1 and D[0][0][1] == -3
    assert D[1][1][0] == 1 - 2 * 3
    assert ce_gap(D, 4) == F(1, 4)


def test_mu_must_be_large_enough():
    with pytest.raises(ValueError):
        regret_matching(CHICKEN, 10, random.Random(1), mu=7)
    with pytest.raises(ValueError):
        regret_matching(CHICKEN, 0, random.Random(1))
    assert payoff_range(CHICKEN, 0) == 7
    z, D = regret_matching(CHICKEN, 1, random.Random(1))
    assert len(z) == 1 and list(z.values()) == [1]


def test_unconditional_bound_against_adversary_every_round():
    rng = random.Random(31337)
    for _ in range(30):
        k = rng.randint(1, 5)
        lo, hi = -rng.randint(0, 3), rng.randint(1, 4)
        m = RegretMatcher(k)
        cum, got = [0.0] * k, 0.0
        for t in range(1, 401):
            u = [rng.uniform(lo, hi) if rng.random() < 0.7 else float(rng.choice((lo, hi))) for _ in range(k)]
            p = m.strategy()
            assert abs(sum(p) - 1.0) < 1e-12 and min(p) >= 0.0
            got += m.update(u)
            cum = [c + x for c, x in zip(cum, u)]
            assert max(cum) - got <= (hi - lo) * math.sqrt(k * t) + 1e-9


def test_expected_self_play_gives_cce():
    rng = random.Random(2718)
    for _ in range(6):
        sizes = tuple(rng.randint(2, 3) for _ in range(rng.randint(2, 3)))
        game = random_game(rng, sizes, 0, 5)
        T = 150
        hist = expected_self_play(game, T)
        n = len(sizes)
        eps_coef = max(float(payoff_range(game, i)) * math.sqrt(sizes[i]) for i in range(n))
        avg = {s: 0.0 for s in profiles(sizes)}
        for t, sigma in enumerate(hist, start=1):
            for s in avg:
                w = 1.0
                for i, a in enumerate(s):
                    w *= sigma[i][a]
                avg[s] += w
            if t % 25 == 0:
                # Check every CCE inequality of the average distribution directly.
                for i in range(n):
                    here = sum(q * float(game[1][s][i]) for s, q in avg.items()) / t
                    for b in range(sizes[i]):
                        dev = sum(q * float(game[1][s[:i] + (b,) + s[i + 1:]][i]) for s, q in avg.items()) / t
                        assert dev - here <= eps_coef / math.sqrt(t) + 1e-9


def test_rps_cce_but_not_ce_check():
    # The helper checks agree with the page claim: the uniform off-diagonal RPS distribution
    # is a CCE and not a CE, so external regret alone does not certify a CE.
    rps = from_bimatrix([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], [[0, 1, -1], [-1, 0, 1], [1, -1, 0]])
    z = {(a, b): F(1, 6) for a in range(3) for b in range(3) if a != b}
    assert is_coarse_correlated(rps, z) and not is_correlated(rps, z)
