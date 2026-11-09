# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adagrad/. The authors are listed in prov/M591DH.jsonl.

import math
import random

from adagrad import adagrad

TOL = 1e-9


def regret_bound(gs: list[list[float]], d_inf: float, eta: float) -> float:
    """(D_inf^2 / (2 eta) + eta) * sum_i |g_(1:T, i)|_2, the diagonal AdaGrad regret bound."""
    return (d_inf**2 / (2 * eta) + eta) * sum(math.sqrt(sum(g[i] ** 2 for g in gs)) for i in range(len(gs[0])))


def test_example_trace() -> None:
    gs = [[1.0, 0.0], [-1.0, 0.0], [1.0, 2.0], [1.0, 0.0], [1.0, 0.0], [0.5, 0.0]]
    xs = adagrad(lambda t, x: gs[t], [0.0, 0.0], 1.0, 6, [-1.0, -1.0], [1.0, 1.0])
    want = [[0.0, 0.0], [-1.0, 0.0], [-0.29289, 0.0], [-0.87024, -1.0], [-1.0, -1.0], [-1.0, -1.0], [-1.0, -1.0]]
    for x, w in zip(xs, want):
        assert max(abs(a - b) for a, b in zip(x, w)) <= 5e-6
    played = sum(g[0] * x[0] + g[1] * x[1] for g, x in zip(gs, xs))
    best = -sum(abs(sum(g[i] for g in gs)) for i in range(2))
    assert abs(played - best - 3.83686) <= 5e-5
    assert played - best <= regret_bound(gs, 2.0, 1.0)


def test_regret_bound_linear_losses_every_round() -> None:
    # For linear losses the best point in the box is a vertex, so the check covers every comparator u.
    d, rounds = 4, 300
    lo, hi = [-1.0, 0.0, -2.0, -0.5], [1.0, 3.0, 0.0, 0.5]
    d_inf = max(h - l for l, h in zip(lo, hi))
    for seed in range(20):
        r = random.Random(seed)
        density = [1.0, 0.3, 0.05, 0.6]
        gs = [[r.uniform(-2, 2) if r.random() < density[i] else 0.0 for i in range(d)] for _ in range(rounds)]
        eta = r.choice([0.1, 1.0, d_inf / math.sqrt(2), 5.0])
        xs = adagrad(lambda t, x: gs[t], [r.uniform(l, h) for l, h in zip(lo, hi)], eta, rounds, lo, hi)
        played, sums = 0.0, [0.0] * d
        for t in range(rounds):
            played += sum(a * b for a, b in zip(gs[t], xs[t]))
            sums = [a + b for a, b in zip(sums, gs[t])]
            best = sum(min(s * l, s * h) for s, l, h in zip(sums, lo, hi))
            assert played - best <= regret_bound(gs[: t + 1], d_inf, eta) + TOL


def test_regret_bound_quadratic_losses_every_round() -> None:
    # f_t(x) = |x - z_t|^2 / 2; the best fixed point of the first T losses in the box is clip(mean z).
    d, rounds = 3, 200
    lo, hi = [-1.0] * d, [1.0] * d
    d_inf = 2.0
    eta = d_inf / math.sqrt(2)
    for seed in range(10):
        r = random.Random(100 + seed)
        zs = [[r.uniform(-1.5, 1.5) for _ in range(d)] for _ in range(rounds)]
        xs = adagrad(lambda t, x: [a - b for a, b in zip(x, zs[t])], [0.9, -0.9, 0.0], eta, rounds, lo, hi)
        gs, played = [], 0.0
        for t in range(rounds):
            gs.append([a - b for a, b in zip(xs[t], zs[t])])
            played += sum((a - b) ** 2 for a, b in zip(xs[t], zs[t])) / 2
            mean = [sum(z[i] for z in zs[: t + 1]) / (t + 1) for i in range(d)]
            u = [min(max(m, -1.0), 1.0) for m in mean]
            best = sum(sum((a - b) ** 2 for a, b in zip(u, z)) / 2 for z in zs[: t + 1])
            assert played - best <= regret_bound(gs, d_inf, eta) + TOL


def test_sum_lemma() -> None:
    # sum_t a_t / sqrt(S_t) <= 2 sqrt(S_T) with S_t = a_1 + ... + a_t, a_t >= 0 (terms with S_t = 0 count 0).
    r = random.Random(7)
    for _ in range(50):
        a = [r.choice([0.0, r.random() * 10]) for _ in range(100)]
        s, total = 0.0, 0.0
        for v in a:
            s += v
            if s > 0:
                total += v / math.sqrt(s)
            assert total <= 2 * math.sqrt(s) + TOL


def test_online_to_batch_stochastic_average() -> None:
    # F(x) = E|x - xi| with xi ~ U(0, 1) on [-1, 2]: F* = 1/4 at the median. E F(average) - F* <= E R_T / T.
    rounds, seeds, eta, d_inf = 400, 200, 3 / math.sqrt(2), 3.0

    def big_f(x: float) -> float:
        if x <= 0:
            return 0.5 - x
        if x >= 1:
            return x - 0.5
        return x * x - x + 0.5

    gap, bound = 0.0, 0.0
    for t in range(seeds):
        r = random.Random(900 + t)
        xis = [r.random() for _ in range(rounds)]
        xs = adagrad(lambda k, x: [1.0 if x[0] > xis[k] else -1.0], [2.0], eta, rounds, [-1.0], [2.0])
        gap += big_f(sum(x[0] for x in xs[:rounds]) / rounds) - 0.25
        bound += (d_inf**2 / (2 * eta) + eta) * math.sqrt(rounds) / rounds  # |g| = 1 in every round
    assert gap / seeds <= bound / seeds


def test_zero_gradients_do_not_move_and_zero_iterations() -> None:
    xs = adagrad(lambda t, x: [0.0, 1.0], [0.3, 0.3], 0.5, 3)
    assert all(x[0] == 0.3 for x in xs)
    assert adagrad(lambda t, x: x, [1.0], 0.1, 0) == [[1.0]]
