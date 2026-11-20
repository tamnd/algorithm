# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/security-game/. The authors are listed in prov/ZA3ZMX.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from agtlp import lp_max
from security_game import attacker_response, best_for_target, comb_mixture, strong_stackelberg, utilities

F = Fraction

# Three targets, one resource. Defender: covered / uncovered; attacker: covered / uncovered.
PAGE_GAME = ([1, 1, 0], [-5, -3, -1], [-1, -1, -1], [5, 3, 1])


def normal_form_commitment(game, k, use_all=False):
    """The optimal commitment over all sets of at most k targets (exactly k with use_all),
    by one LP per attacked target on the normal form."""
    dc, du, ac, au = game
    T = len(dc)
    sizes = [k] if use_all else range(k + 1)
    subsets = [S for r in sizes for S in combinations(range(T), r)]
    A = [[dc[t] if t in S else du[t] for t in range(T)] for S in subsets]
    B = [[ac[t] if t in S else au[t] for t in range(T)] for S in subsets]
    m = len(subsets)
    best = None
    for j in range(T):
        A_ub = [[B[i][s] - B[i][j] for i in range(m)] for s in range(T) if s != j]
        status, _, value, _ = lp_max([A[i][j] for i in range(m)], A_ub, [0] * len(A_ub), [[1] * m], [1])
        if status == "optimal" and (best is None or value > best):
            best = value
    return best


def random_game(rng, T):
    dc = [rng.randint(0, 6) for _ in range(T)]
    du = [v - rng.randint(1, 8) for v in dc]
    ac = [rng.randint(-6, 0) for _ in range(T)]
    au = [v + rng.randint(1, 8) for v in ac]
    return dc, du, ac, au


def check(game, k, value, c, t, use_all=False):
    T = len(game[0])
    assert all(0 <= v <= 1 for v in c) and (sum(c) == k if use_all else sum(c) <= k)
    att = [utilities(game, c, s)[1] for s in range(T)]
    assert att[t] == max(att)
    assert utilities(game, c, t)[0] == value
    assert utilities(game, c, attacker_response(game, c))[0] == value


def check_mixture(c, k):
    mix = comb_mixture(c)
    assert sum(p for p, _ in mix) == 1 and all(p > 0 for p, _ in mix)
    for _, S in mix:
        assert len(S) == len(set(S)) and len(S) <= k
    for t in range(len(c)):
        assert sum(p for p, S in mix if t in S) == c[t]


def test_page_example():
    value, c, t = strong_stackelberg(PAGE_GAME, 1)
    assert (value, c, t) == (F(-7, 5), [F(3, 5), F(2, 5), F(0)], 0)
    check(PAGE_GAME, 1, value, c, t)
    assert [utilities(PAGE_GAME, c, s)[1] for s in range(3)] == [F(7, 5), F(7, 5), 1]
    assert [utilities(PAGE_GAME, c, s)[0] for s in range(3)] == [F(-7, 5), F(-7, 5), -1]
    assert best_for_target(PAGE_GAME, 1, 2) is None
    assert normal_form_commitment(PAGE_GAME, 1) == value == normal_form_commitment(PAGE_GAME, 1, True)
    assert comb_mixture(c) == [(F(3, 5), (0,)), (F(2, 5), (1,))]


def test_random_games_against_normal_form():
    rng = random.Random(1123)
    for _ in range(40):
        T = rng.randint(1, 4)
        k = rng.randint(1, T)
        game = random_game(rng, T)
        for use_all in (False, True):
            value, c, t = strong_stackelberg(game, k, use_all)
            check(game, k, value, c, t, use_all)
            check_mixture(c, k)
            assert value == normal_form_commitment(game, k, use_all)


def test_idle_resources_can_help():
    # With 3 resources on 3 targets, using all of them forces the attacker to target 1,
    # while leaving target 0 partly open draws the attack there.
    game = ([6, 1, 0], [0, 0, -4], [-3, 0, 0], [2, 6, 3])
    assert strong_stackelberg(game, 3, use_all=True)[0] == 1
    value, c, t = strong_stackelberg(game, 3)
    assert value == F(12, 5) and t == 0 and c[0] < 1


def test_more_resources_never_hurt():
    rng = random.Random(8)
    for _ in range(30):
        T = rng.randint(2, 5)
        game = random_game(rng, T)
        values = [strong_stackelberg(game, k)[0] for k in range(0, T + 1)]
        assert all(a <= b for a, b in zip(values, values[1:]))


def test_comb_mixture_examples():
    check_mixture([F(1, 2), F(1, 2), F(1, 2), F(1, 2)], 2)
    assert comb_mixture([F(1, 2), F(1, 2), F(1, 2), F(1, 2)]) == [(F(1, 2), (0, 2)), (F(1, 2), (1, 3))]
    check_mixture([F(1), F(1, 3), F(2, 3)], 2)
    rng = random.Random(3)
    for _ in range(200):
        T = rng.randint(1, 6)
        c = [F(rng.randint(0, 6), 6) for _ in range(T)]
        k = -(-sum(c) // 1)
        check_mixture(c, max(k, 0))


def test_no_resources():
    game = ([1, 2], [-4, -1], [-1, -1], [3, 2])
    value, c, t = strong_stackelberg(game, 0)
    assert (value, c, t) == (-4, [0, 0], 0)
    assert best_for_target(game, 0, 1) is None
