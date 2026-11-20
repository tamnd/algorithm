# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimistic-hedge/. The authors are listed in prov/259HJ8.jsonl.
"""Tests of optimistic Hedge: the closed form, the RVU bound at every round, the bound on the
sum of the regrets in self-play, the duality gap in zero-sum games, and the last iterate."""

import math
import random

import pytest

from agtgame import from_bimatrix, random_game
from optimistic_hedge import OptimisticHedge, play, regret, rvu_bound, self_play

CHICKEN = from_bimatrix([[0, 7], [2, 6]], [[0, 2], [7, 6]])
RPS = from_bimatrix([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], [[0, 1, -1], [-1, 0, 1], [1, -1, 0]])


def softmax(v):
    top = max(v)
    w = [math.exp(a - top) for a in v]
    s = sum(w)
    return [a / s for a in w]


def test_closed_form_and_validation():
    """x_{t+1} is proportional to exp(-eta (L_t + l_t)), with L_t the cumulative loss."""
    rng = random.Random(4)
    k, eta = 4, 0.7
    learner = OptimisticHedge(k, eta)
    cum = [0.0] * k
    assert learner.distribution() == [0.25] * 4
    for _ in range(60):
        loss = [rng.random() for _ in range(k)]
        learner.update(loss)
        cum = [c + v for c, v in zip(cum, loss)]
        want = softmax([-eta * (c + v) for c, v in zip(cum, loss)])
        assert all(abs(a - b) < 1e-12 for a, b in zip(learner.distribution(), want))
    with pytest.raises(ValueError):
        OptimisticHedge(0, 1.0)
    with pytest.raises(ValueError):
        OptimisticHedge(3, -1.0)


def test_no_underflow_on_long_runs():
    xs, _ = play(3, 2000, 5.0, lambda t, x: [0.0, 1.0, 1.0])
    assert abs(sum(xs[-1]) - 1) < 1e-12 and xs[-1][0] > 0.999999


def adversaries(rng, k):
    yield "random", lambda t, x: [rng.random() for _ in range(k)]
    yield "adaptive", lambda t, x: [1.0 if a == max(range(k), key=lambda b: x[b]) else 0.0 for a in range(k)]
    yield "alternating", lambda t, x: [float((a + t) % 2) for a in range(k)]
    yield "slow drift", lambda t, x: [0.5 + 0.5 * math.sin(t / 50 + a) for a in range(k)]


def test_rvu_bound_at_every_round():
    rng = random.Random(99)
    for k in (1, 2, 3, 5):
        for eta in (0.05, 0.3, 1.0):
            for _, adv in adversaries(rng, k):
                xs, losses = play(k, 250, eta, adv)
                for T in range(1, 251, 17):
                    r = regret(xs[:T], losses[:T])
                    assert r <= rvu_bound(xs[:T], losses[:T], eta) + 1e-9
                    var = sum(max(abs(a - b) for a, b in zip(l, p)) ** 2
                              for l, p in zip(losses[:T], [[0.0] * k] + losses[:T - 1]))
                    assert r <= math.log(k) / eta + eta / 2 * var + 1e-9


def test_slowly_changing_losses_give_small_regret():
    """When the losses change slowly, the regret stays far below the sqrt(T) of plain Hedge."""
    xs, losses = play(2, 4000, 0.5, lambda t, x: [0.5 + 0.5 * math.sin(t / 300), 0.5 - 0.5 * math.sin(t / 300)])
    assert regret(xs, losses) <= math.log(2) / 0.5 + 0.5 * (1 + 4000 * (1 / 300) ** 2) + 1e-9
    assert regret(xs, losses) < 3


def test_sum_of_regrets_in_self_play():
    """With eta <= 1 / (sqrt 8 (n - 1)), the sum of the regrets is at most n ln k / eta + n eta for every T."""
    three = random_game(random.Random(6), (2, 3, 2), -3, 3)
    for game, T in ((CHICKEN, 600), (RPS, 600), (three, 200)):
        sizes = game[0]
        n, k = len(sizes), max(sizes)
        eta = 1 / (math.sqrt(8) * (n - 1))
        hist_x, hist_l = self_play(game, T, eta)
        for t in range(1, T + 1, 13):
            total = sum(regret([xs[i] for xs in hist_x[:t]], [ls[i] for ls in hist_l[:t]]) for i in range(n))
            assert total <= n * math.log(k) / eta + n * eta + 1e-9


def test_zero_sum_duality_gap():
    """In a zero-sum game the sum of the two regrets is T times the duality gap of the averages."""
    rng = random.Random(21)
    for _ in range(3):
        m = rng.randint(2, 4)
        A = [[rng.randint(-3, 3) for _ in range(m + 1)] for _ in range(m)]
        game = from_bimatrix(A, [[-v for v in row] for row in A])
        T, eta = 400, 1 / math.sqrt(8)
        hist_x, hist_l = self_play(game, T, eta)
        xbar = [sum(xs[0][r] for xs in hist_x) / T for r in range(m)]
        ybar = [sum(xs[1][c] for xs in hist_x) / T for c in range(m + 1)]
        best_col = min(sum(xbar[r] * A[r][c] for r in range(m)) for c in range(m + 1))
        best_row = max(sum(A[r][c] * ybar[c] for c in range(m + 1)) for r in range(m))
        gap = best_row - best_col
        span = max(max(row) for row in A) - min(min(row) for row in A) or 1
        r1 = regret([xs[0] for xs in hist_x], [ls[0] for ls in hist_l])
        r2 = regret([xs[1] for xs in hist_x], [ls[1] for ls in hist_l])
        assert abs((r1 + r2) * span / T - gap) < 1e-9
        assert 0 <= gap <= span * (2 * math.log(m + 1) / eta + 2 * eta) / T + 1e-9


def test_last_iterate_in_matching_pennies():
    """The last iterate of optimistic Hedge approaches the equilibrium; that of Hedge moves away.
    The row player wants to match: its loss for an action is the chance that the column differs."""
    row, col = OptimisticHedge(2, 0.1), OptimisticHedge(2, 0.1)
    row.z = [0.3, 0.0]
    row.x = softmax(row.z)
    zr, zc = [0.3, 0.0], [0.0, 0.0]
    for _ in range(3000):
        x, y = row.distribution(), col.distribution()
        row.update([y[1], y[0]])
        col.update([x[0], x[1]])
        hx, hy = softmax(zr), softmax(zc)
        zr = [zr[0] - 0.1 * hy[1], zr[1] - 0.1 * hy[0]]
        zc = [zc[0] - 0.1 * hx[0], zc[1] - 0.1 * hx[1]]
    x, y = row.distribution(), col.distribution()
    assert abs(x[0] - 0.5) + abs(y[0] - 0.5) < 0.01
    hx, hy = softmax(zr), softmax(zc)
    assert abs(hx[0] - 0.5) + abs(hy[0] - 0.5) > 0.5
