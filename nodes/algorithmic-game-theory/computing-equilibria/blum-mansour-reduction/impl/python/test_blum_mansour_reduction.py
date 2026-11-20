# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blum-mansour-reduction/. The authors are listed in prov/FWT8FT.jsonl.
"""Tests of the Blum-Mansour reduction: the stationary step, the regret decomposition, the
swap regret bound at every round against several adversaries, and self-play in games."""

import math
import random

import pytest

from agtgame import deviation_payoffs, from_bimatrix, profiles, random_game
from blum_mansour_reduction import BlumMansour, Hedge, external_regret, regret_bound, run, stationary, swap_regret


def tuned_eta(k, T):
    return math.sqrt(2 * k * math.log(k) / T) if k > 1 else 1.0


def test_stationary_distribution():
    rng = random.Random(11)
    for _ in range(200):
        k = rng.randint(1, 6)
        Q = []
        for _ in range(k):
            row = [rng.random() + 1e-3 for _ in range(k)]
            s = sum(row)
            Q.append([x / s for x in row])
        p = stationary(Q)
        assert all(x >= 0 for x in p) and abs(sum(p) - 1) < 1e-12
        for i in range(k):
            assert abs(sum(p[j] * Q[j][i] for j in range(k)) - p[i]) < 1e-12


def test_hedge_distribution_and_validation():
    h = Hedge(3, 0.5)
    assert h.distribution() == [1 / 3] * 3
    h.update([1.0, 0.0, 2.0])
    d = h.distribution()
    assert abs(d[1] / d[0] - math.exp(0.5)) < 1e-12 and abs(d[0] / d[2] - math.exp(0.5)) < 1e-12
    with pytest.raises(ValueError):
        Hedge(0, 1.0)
    with pytest.raises(ValueError):
        Hedge(2, 0.0)


def test_decomposition_into_copies():
    """The loss of the learner is the sum of the losses of the copies, and its swap regret is at
    most the sum of their external regrets on the scaled losses."""
    rng = random.Random(3)
    for k in (2, 3, 5):
        ps, losses, Qs = run(k, 150, 0.3, lambda t, p: [rng.random() for _ in range(k)])
        mine = sum(sum(x * v for x, v in zip(p, l)) for p, l in zip(ps, losses))
        theirs = 0.0
        copy_regret = 0.0
        for j in range(k):
            scaled = [[p[j] * v for v in l] for p, l in zip(ps, losses)]
            qs = [Q[j] for Q in Qs]
            theirs += sum(sum(x * v for x, v in zip(q, l)) for q, l in zip(qs, scaled))
            copy_regret += external_regret(qs, scaled)
        assert abs(mine - theirs) < 1e-9
        assert swap_regret(ps, losses) <= copy_regret + 1e-9
        assert external_regret(ps, losses) <= swap_regret(ps, losses) + 1e-9


def adversaries(rng, k):
    yield lambda t, p: [rng.random() for _ in range(k)]
    yield lambda t, p: [1.0 if a == max(range(k), key=lambda b: p[b]) else 0.0 for a in range(k)]
    # A sequence that rewards a shifted copy of the last action: good for swaps, bad for Hedge alone.
    yield lambda t, p: [0.0 if a == (t // 7) % k else (1.0 if a == (t // 7 + 1) % k else 0.5) for a in range(k)]
    yield lambda t, p: [float((a + t) % 2) for a in range(k)]


def test_swap_regret_bound_at_every_round():
    rng = random.Random(2024)
    T = 400
    for k in (1, 2, 3, 4):
        eta = tuned_eta(k, T)
        for adv in adversaries(rng, k):
            learner = BlumMansour(k, eta)
            W = [[0.0] * k for _ in range(k)]  # W[j][a] = sum_t p_t(j) loss_t(a)
            for t in range(1, T + 1):
                p = learner.distribution()
                loss = adv(t, p)
                learner.update(loss)
                for j in range(k):
                    for a in range(k):
                        W[j][a] += p[j] * loss[a]
                swap = sum(W[j][j] - min(W[j]) for j in range(k))
                bound = regret_bound(k, t, eta) if k > 1 else 0.0
                assert swap <= bound + 1e-9
        if k > 1:
            assert abs(regret_bound(k, T, eta) - math.sqrt(2 * T * k * math.log(k))) < 1e-9


def test_one_action():
    ps, losses, _ = run(1, 20, 1.0, lambda t, p: [0.3])
    assert all(p == [1.0] for p in ps) and swap_regret(ps, losses) == 0


def self_play(game, T, eta):
    sizes, pay = game
    n = len(sizes)
    lo = [min(pay[s][i] for s in pay) for i in range(n)]
    hi = [max(pay[s][i] for s in pay) for i in range(n)]
    span = [float(hi[i] - lo[i]) or 1.0 for i in range(n)]
    learners = [BlumMansour(k, eta) for k in sizes]
    history = []
    z = {s: 0.0 for s in profiles(sizes)}
    for _ in range(T):
        sigma = [L.distribution() for L in learners]
        for s in z:
            w = 1.0
            for i, a in enumerate(s):
                w *= sigma[i][a]
            z[s] += w / T
        losses = []
        for i in range(n):
            d = deviation_payoffs(game, i, sigma)
            losses.append([(float(hi[i]) - float(v)) / span[i] for v in d])
        for L, l in zip(learners, losses):
            L.update(l)
        history.append((sigma, losses))
    return z, history, span


def ce_gap(game, z, i):
    sizes, pay = game
    gap = 0.0
    for j in range(sizes[i]):
        best = 0.0
        for l in range(sizes[i]):
            g = sum(q * float(pay[s[:i] + (l,) + s[i + 1:]][i] - pay[s][i]) for s, q in z.items() if s[i] == j)
            best = max(best, g)
        gap += best
    return gap


def test_self_play_gives_an_approximate_correlated_equilibrium():
    chicken = from_bimatrix([[0, 7], [2, 6]], [[0, 2], [7, 6]])
    rps = from_bimatrix([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], [[0, 1, -1], [-1, 0, 1], [1, -1, 0]])
    three = random_game(random.Random(8), (2, 2, 3), -2, 2)
    for game, T in ((chicken, 300), (rps, 300), (three, 120)):
        k = max(game[0])
        eta = tuned_eta(k, T)
        z, history, span = self_play(game, T, eta)
        for i in range(len(game[0])):
            ps = [sigma[i] for sigma, _ in history]
            losses = [l[i] for _, l in history]
            swap = swap_regret(ps, losses)
            # The swap regret in losses is the correlated equilibrium gap of z, scaled.
            assert abs(ce_gap(game, z, i) - span[i] * swap / T) < 1e-9
            assert swap <= regret_bound(game[0][i], T, eta) + 1e-9
            assert ce_gap(game, z, i) <= span[i] * regret_bound(k, T, eta) / T + 1e-9


def test_regret_definitions_on_small_cases():
    ps = [[1.0, 0.0], [0.0, 1.0]]
    losses = [[1.0, 0.0], [1.0, 0.0]]
    # The swap 0 -> 1 saves 1 in round 1, and the learner already plays action 1 in round 2.
    assert swap_regret(ps, losses) == 1.0 and external_regret(ps, losses) == 1.0
    losses = [[1.0, 0.0], [0.0, 1.0]]
    # The learner loses 2 and each fixed action loses 1, but the swap 0 <-> 1 loses 0.
    assert external_regret(ps, losses) == 1.0 and swap_regret(ps, losses) == 2.0
