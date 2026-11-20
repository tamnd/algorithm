# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterated-elimination-of-dominated-strategies/. The authors are listed in prov/M509ET.jsonl.

import random
from fractions import Fraction as F

import agtgame
from agtgame import (deviation_payoffs, expected_utility, from_bimatrix, is_coarse_correlated,
                     is_correlated, is_distribution, is_epsilon_nash, is_nash, max_gain, profiles,
                     pure_best_responses, pure_nash_brute, random_game)
from iterated_elimination_of_dominated_strategies import (
    dominated_by_mixed, dominated_by_pure, iterated_elimination, maximin, mixed_dominance,
    weakly_dominated_by_pure)

H = F(1, 2)
T3 = F(1, 3)

PD = from_bimatrix([[3, 0], [5, 1]], [[3, 5], [0, 1]])  # 0 = cooperate, 1 = defect
PENNIES = from_bimatrix([[1, -1], [-1, 1]], [[-1, 1], [1, -1]])
RPS_A = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
RPS = from_bimatrix(RPS_A, [[-x for x in row] for row in RPS_A])
BOS = from_bimatrix([[2, 0], [0, 1]], [[1, 0], [0, 2]])
# Chicken, strategy 0 = dare (D), 1 = chicken (C).
CHICKEN = from_bimatrix([[0, 7], [2, 6]], [[0, 2], [7, 6]])


# ---------------------------------------------------------------- the helper agtgame


def test_profiles_and_shapes():
    assert profiles((2, 3)) == [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    assert len(profiles((2, 3, 4))) == 24
    sizes, pay = from_bimatrix([[1, 2, 3]], [[4, 5, 6]])
    assert sizes == (1, 3) and pay[(0, 2)] == (F(3), F(6))
    g1 = random_game(random.Random(7), (2, 2, 2), -3, 3)
    g2 = random_game(random.Random(7), (2, 2, 2), -3, 3)
    assert g1 == g2 and all(-3 <= v <= 3 and isinstance(v, F) for t in g1[1].values() for v in t)


def test_expected_utility_matches_brute_force():
    rng = random.Random(11)
    for _ in range(30):
        sizes = tuple(rng.randint(1, 3) for _ in range(rng.randint(2, 3)))
        game = random_game(rng, sizes, -5, 5)
        sigma = []
        for k in sizes:
            w = [rng.randint(0, 4) for _ in range(k)]
            if sum(w) == 0:
                w[0] = 1
            sigma.append([F(x, sum(w)) for x in w])
        for i in range(len(sizes)):
            brute = sum(F(1) * game[1][s][i] * _prod(sigma[k][s[k]] for k in range(len(s)))
                        for s in profiles(sizes))
            assert expected_utility(game, i, sigma) == brute
            d = deviation_payoffs(game, i, sigma)
            assert sum(p * v for p, v in zip(sigma[i], d)) == brute
            best = max(d)
            assert pure_best_responses(game, i, sigma) == [a for a in range(sizes[i]) if d[a] == best]
        assert max_gain(game, sigma) >= 0


def _prod(xs):
    out = F(1)
    for x in xs:
        out *= x
    return out


def test_check_values_of_nash():
    assert is_nash(PENNIES, [[H, H], [H, H]])
    assert not is_nash(PENNIES, [[F(1), F(0)], [H, H]])
    assert pure_nash_brute(PENNIES) == []
    assert is_nash(RPS, [[T3] * 3, [T3] * 3]) and expected_utility(RPS, 0, [[T3] * 3, [T3] * 3]) == 0
    mixed = [[F(2, 3), T3], [T3, F(2, 3)]]
    assert is_nash(BOS, mixed)
    assert expected_utility(BOS, 0, mixed) == F(2, 3) == expected_utility(BOS, 1, mixed)
    assert pure_nash_brute(BOS) == [(0, 0), (1, 1)]
    chick = [[T3, F(2, 3)], [T3, F(2, 3)]]
    assert is_nash(CHICKEN, chick) and expected_utility(CHICKEN, 0, chick) == F(14, 3)
    assert pure_nash_brute(PD) == [(1, 1)]


def test_epsilon_nash_and_distributions():
    sigma = [[F(1), F(0)], [F(1), F(0)]]  # both cooperate in the prisoner's dilemma
    assert max_gain(PD, sigma) == 2
    assert is_epsilon_nash(PD, sigma, F(2)) and not is_epsilon_nash(PD, sigma, F(199, 100))
    assert not is_nash(PD, [[H, F(1, 3)], [H, H]])  # not a distribution
    assert is_distribution([H, H]) and not is_distribution([H, F(2, 3)])
    assert not is_distribution({(0, 0): F(3, 2), (1, 1): -H})


def test_correlated_and_coarse_correlated():
    third = {(1, 1): T3, (0, 1): T3, (1, 0): T3}
    assert is_correlated(CHICKEN, third) and is_coarse_correlated(CHICKEN, third)
    assert all(sum(q * CHICKEN[1][s][i] for s, q in third.items()) == 5 for i in (0, 1))
    best = {(0, 1): F(1, 4), (1, 0): F(1, 4), (1, 1): H}
    assert is_correlated(CHICKEN, best)
    assert all(sum(q * CHICKEN[1][s][i] for s, q in best.items()) == F(21, 4) for i in (0, 1))
    assert not is_correlated(CHICKEN, {(1, 1): F(1)})
    # The product of the mixed equilibrium is a correlated equilibrium.
    x = [T3, F(2, 3)]
    prod = {(r, c): x[r] * x[c] for r in range(2) for c in range(2)}
    assert is_correlated(CHICKEN, prod)
    # Rock-paper-scissors: uniform on the six profiles without a tie is a CCE but not a CE.
    six = {(r, c): F(1, 6) for r in range(3) for c in range(3) if r != c}
    assert is_coarse_correlated(RPS, six) and not is_correlated(RPS, six)
    assert not is_correlated(CHICKEN, {(5, 5): F(1)})


def test_every_ce_is_a_cce_on_random_games():
    rng = random.Random(3)
    for _ in range(200):
        game = random_game(rng, (rng.randint(2, 3), rng.randint(2, 3)), 0, 4)
        ps = profiles(game[0])
        w = [rng.randint(0, 3) for _ in ps]
        if sum(w) == 0:
            continue
        dist = {s: F(x, sum(w)) for s, x in zip(ps, w)}
        if is_correlated(game, dist):
            assert is_coarse_correlated(game, dist)
        # Pure equilibria are correlated equilibria.
        for s in pure_nash_brute(game):
            assert is_correlated(game, {s: F(1)})


# ---------------------------------------------------------------- the elimination


def test_prisoners_dilemma_is_solved():
    alive, log = iterated_elimination(PD)
    assert alive == [[1], [1]]
    assert [(i, a) for i, a, _ in log] == [(0, 0), (1, 0)]


THREE = from_bimatrix([[4, 5, 6], [2, 8, 3], [3, 9, 2]], [[3, 1, 2], [1, 4, 6], [0, 6, 8]])


def test_trace_of_the_page():
    alive, log = iterated_elimination(THREE)
    assert alive == [[0], [0]]
    assert [(i, a, w) for i, a, w in log] == [(1, 1, 2), (0, 1, 0), (0, 2, 0), (1, 2, 0)]


MIXED_ONLY = from_bimatrix([[3, 0], [0, 3], [1, 1]], [[1, 0], [0, 1], [1, 0]])


def test_mixed_dominance_without_pure_dominance():
    alive = [[0, 1, 2], [0, 1]]
    assert dominated_by_pure(MIXED_ONLY, alive, 0, 2) is None
    assert dominated_by_mixed(MIXED_ONLY, alive, 0, 2) == {0: H, 1: H}
    kind, belief = mixed_dominance(MIXED_ONLY, alive, 0, 0)
    assert kind == "best response"
    assert iterated_elimination(MIXED_ONLY, "pure")[0] == [[0, 1, 2], [0, 1]]
    assert iterated_elimination(MIXED_ONLY, "mixed")[0][0] == [0, 1]


def _check_certificate(game, alive, i, a):
    _, pay = game
    kind, cert = mixed_dominance(game, alive, i, a)
    others = [b for b in alive[i] if b != a]
    ctx = agt_contexts(alive, i)
    if kind == "dominated":
        assert is_distribution(cert) and set(cert) <= set(others)
        for t in ctx:
            assert sum(p * pay[put(t, i, b)][i] for b, p in cert.items()) > pay[put(t, i, a)][i]
    else:
        assert is_distribution(cert) and set(cert) <= set(ctx)
        ua = sum(q * pay[put(t, i, a)][i] for t, q in cert.items())
        for b in others:
            assert sum(q * pay[put(t, i, b)][i] for t, q in cert.items()) <= ua
    return kind


def agt_contexts(alive, i):
    from iterated_elimination_of_dominated_strategies import _contexts
    return _contexts(alive, i)


def put(t, i, a):
    return t[:i] + (a,) + t[i + 1:]


def test_certificates_on_random_games():
    rng = random.Random(5)
    for _ in range(120):
        sizes = (rng.randint(2, 4), rng.randint(2, 3)) if rng.random() < 0.7 else (2, 2, 2)
        game = random_game(rng, sizes, 0, 6)
        alive = [list(range(k)) for k in sizes]
        for i in range(len(sizes)):
            for a in alive[i]:
                kind = _check_certificate(game, alive, i, a)
                if dominated_by_pure(game, alive, i, a) is not None:
                    assert kind == "dominated"


def test_maximin_value_against_a_grid():
    rng = random.Random(9)
    for _ in range(40):
        cols = rng.randint(1, 4)
        D = [[F(rng.randint(-4, 4)) for _ in range(cols)] for _ in range(2)]
        z, x = maximin(D)
        grid = max(min(F(k, 60) * D[0][c] + F(60 - k, 60) * D[1][c] for c in range(len(D[0])))
                   for k in range(61))
        assert z >= grid and is_distribution(x)


def _restricted_pure_nash(game, alive):
    sizes, pay = game
    out = []
    import itertools
    for s in itertools.product(*alive):
        if all(pay[s][i] >= pay[put(s, i, b)][i] for i in range(len(sizes)) for b in alive[i]):
            out.append(s)
    return out


def test_order_does_not_matter_for_strict_dominance():
    rng = random.Random(1)
    for trial in range(60):
        sizes = (rng.randint(2, 4), rng.randint(2, 4)) if trial % 3 else (2, 3, 2)
        game = random_game(rng, sizes, 0, 5)
        for rule in ("pure", "mixed"):
            base, _ = iterated_elimination(game, rule)
            for seed in range(3):
                r = random.Random(seed)
                other, _ = iterated_elimination(game, rule, pick=lambda c: r.choice(c))
                assert other == base
            # Every pure Nash equilibrium survives, and the equilibria of the reduced game
            # are exactly the pure equilibria of the original game.
            pne = pure_nash_brute(game)
            assert all(all(s[i] in base[i] for i in range(len(sizes))) for s in pne)
            assert _restricted_pure_nash(game, base) == pne
        assert all(set(m) <= set(p) for m, p in zip(iterated_elimination(game, "mixed")[0],
                                                     iterated_elimination(game, "pure")[0]))


WEAK = from_bimatrix([[1, 0], [1, 2], [0, 2]], [[1, 0], [1, 1], [0, 1]])


def _priority(order):
    return lambda c: min(c, key=lambda p: order.index(p) if p in order else len(order))


def test_weak_dominance_depends_on_the_order():
    # Rows T, M, B are 0, 1, 2 and columns L, R are 0, 1.
    first, _ = iterated_elimination(WEAK, "weak", pick=_priority([(0, 0), (1, 0)]))
    assert first == [[1, 2], [1]]
    assert all(WEAK[1][(r, 1)] == (F(2), F(1)) for r in first[0])
    other, _ = iterated_elimination(WEAK, "weak", pick=_priority([(0, 2), (1, 1)]))
    assert other == [[0, 1], [0]]
    assert all(WEAK[1][(r, 0)] == (F(1), F(1)) for r in other[0])
    third, _ = iterated_elimination(WEAK, "weak")
    assert third == [[1], [0, 1]]
    assert weakly_dominated_by_pure(WEAK, [[0, 1, 2], [0, 1]], 0, 0) == 1
    assert dominated_by_pure(WEAK, [[0, 1, 2], [0, 1]], 0, 0) is None


def test_nothing_to_remove():
    for g in (PENNIES, RPS, BOS, CHICKEN):
        for rule in ("pure", "mixed", "weak"):
            alive, log = iterated_elimination(g, rule)
            assert alive == [list(range(k)) for k in g[0]] and log == []


def test_helper_has_no_algorithm():
    names = {n for n in dir(agtgame) if not n.startswith("_")}
    assert names >= {"profiles", "from_bimatrix", "random_game", "expected_utility",
                     "deviation_payoffs", "pure_best_responses", "max_gain", "is_nash",
                     "is_epsilon_nash", "is_distribution", "is_correlated",
                     "is_coarse_correlated", "pure_nash_brute"}
