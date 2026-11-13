# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/counterfactual-regret-minimization/. The authors are listed in prov/XFPEGD.jsonl.

import math
import random
from fractions import Fraction

import pytest

from counterfactual_regret_minimization import (
    CFR,
    KuhnPoker,
    MatrixGame,
    best_response_value,
    expected_value,
    exploitability,
    kuhn_equilibrium,
    pure_strategies,
    regret_matching,
)

F = Fraction
KUHN = KuhnPoker()
KUHN_VALUE = F(-1, 18)


def merge(a, b):
    out = dict(a)
    out.update(b)
    return out


def brute_force_best_response(game, strategy, player):
    """Try every pure strategy of `player` against the other player's part of strategy."""
    values = [expected_value(game, merge(strategy, pure)) for pure in pure_strategies(game, player)]
    return max(values) if player == 0 else min(values)


def exact_2x2_value(a):
    (p, q), (r, s) = a
    lower = max(min(p, q), min(r, s))
    upper = min(max(p, r), max(q, s))
    if lower == upper:
        return F(lower)
    return F(p * s - q * r, p + s - q - r)


def test_regret_matching():
    assert regret_matching([0.0, 0.0]) == [0.5, 0.5]
    assert regret_matching([-1.0, -2.0, -3.0]) == [1 / 3] * 3
    assert regret_matching([3.0, -1.0, 1.0]) == [0.75, 0.0, 0.25]


def test_kuhn_shape():
    assert len(list(pure_strategies(KUHN, 0))) == 64
    assert len(list(pure_strategies(KUHN, 1))) == 64
    # The uniform profile: value 1/8, and the two best responses together gain 11/12.
    assert expected_value(KUHN, {}) == F(1, 8)
    assert exploitability(KUHN, {}) == F(11, 12)


def test_kuhn_equilibrium_family_has_value_minus_one_eighteenth():
    rng = random.Random(1950)
    alphas = [F(0), F(1, 6), F(1, 3)] + [F(rng.randint(0, 30), 90) for _ in range(20)]
    for alpha in alphas:
        s = kuhn_equilibrium(alpha)
        assert expected_value(KUHN, s) == KUHN_VALUE
        assert best_response_value(KUHN, s, 0) == KUHN_VALUE
        assert best_response_value(KUHN, s, 1) == KUHN_VALUE
        assert exploitability(KUHN, s) == 0
    with pytest.raises(ValueError):
        kuhn_equilibrium(F(1, 2))


def test_kuhn_perturbed_equilibrium_is_exploitable():
    base = kuhn_equilibrium(F(1, 6))
    for key, (p, b) in base.items():
        nb = b + F(1, 10) if b <= F(1, 2) else b - F(1, 10)
        s = dict(base)
        s[key] = [1 - nb, nb]
        assert exploitability(KUHN, s) > 0, key


def test_best_response_against_brute_force():
    rng = random.Random(1953)
    keys = [k for k in kuhn_equilibrium(0)]
    for _ in range(250):
        s = {}
        for k in keys:
            b = rng.random() if rng.random() < 0.7 else rng.choice([0.0, 1.0])
            s[k] = [1 - b, b]
        for player in (0, 1):
            assert math.isclose(best_response_value(KUHN, s, player), brute_force_best_response(KUHN, s, player), abs_tol=1e-12)
        assert best_response_value(KUHN, s, 0) >= expected_value(KUHN, s) - 1e-12 >= best_response_value(KUHN, s, 1) - 2e-12


def test_cfr_on_kuhn_poker():
    cfr = CFR(KUHN)
    gaps = []
    done = 0
    for t in (10, 100, 1000):
        avg = cfr.run(t - done)
        done = t
        gaps.append(exploitability(KUHN, avg))
    assert gaps[0] > gaps[1] > gaps[2]
    gap = gaps[2]
    # Measured after 1000 iterations: about 0.0145. Theorems 2 and 4 of Zinkevich et al. give
    # 2 * 4 * 6 * sqrt(2) / sqrt(1000), about 2.15, a much weaker bound.
    assert gap < 0.02
    assert gap <= 2 * 4 * 6 * math.sqrt(2) / math.sqrt(1000)
    # The game value -1/18 lies between the two best response values of any profile.
    assert best_response_value(KUHN, avg, 1) <= KUHN_VALUE <= best_response_value(KUHN, avg, 0)
    assert abs(expected_value(KUHN, avg) - KUHN_VALUE) <= gap
    # The average strategy has the shape of Kuhn's family.
    bet = {c: avg[(c, "")][1] for c in (1, 2, 3)}
    assert bet[2] < 0.01 and avg[(3, "pb")][1] > 0.99 and avg[(1, "pb")][1] < 0.01
    assert abs(bet[3] - 3 * bet[1]) < 0.05
    assert abs(avg[(1, "p")][1] - 1 / 3) < 0.05 and abs(avg[(2, "b")][1] - 1 / 3) < 0.05


def test_cfr_on_the_matrix_game_of_the_minimax_page():
    game = MatrixGame([[3, -1], [-2, 1]])
    avg = CFR(game).run(2000)
    assert abs(avg[("row",)][0] - 3 / 7) < 0.02
    assert abs(avg[("column",)][0] - 2 / 7) < 0.02
    # Measured: about 0.054 after 2000 iterations.
    assert exploitability(game, avg) < 0.1


def test_cfr_on_random_matrix_games():
    rng = random.Random(2007)
    t = 200
    for _ in range(250):
        n, m = rng.randint(2, 3), rng.randint(2, 3)
        a = [[rng.randint(-5, 5) for _ in range(m)] for _ in range(n)]
        game = MatrixGame(a)
        avg = CFR(game).run(t)
        hi, lo = best_response_value(game, avg, 0), best_response_value(game, avg, 1)
        spread = max(map(max, a)) - min(map(min, a))
        # One information set per player: the regret bound of Theorem 4 for each player, summed.
        assert hi - lo <= 2 * spread * math.sqrt(max(n, m)) / math.sqrt(t) + 1e-9
        if n == m == 2:
            v = exact_2x2_value(a)
            assert lo - 1e-9 <= v <= hi + 1e-9
