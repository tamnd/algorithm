# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-averaging/. The authors are listed in prov/XNYGXK.jsonl.

import math
import random

from distributed_averaging import (converges, cycle, deviation, grid, metropolis_weights,
                                   random_connected_graph, run, slem)


def test_metropolis_weights_are_doubly_stochastic() -> None:
    for adj in (cycle(7), grid(3, 4), random_connected_graph(12, 0.3, 5)):
        w = metropolis_weights(adj)
        n = len(adj)
        for i in range(n):
            assert abs(sum(w[i]) - 1.0) < 1e-12
            assert abs(sum(w[k][i] for k in range(n)) - 1.0) < 1e-12
            assert w[i][i] > 0.0
            for j in range(n):
                assert w[i][j] == w[j][i]
                assert w[i][j] >= 0.0
                if i != j and j not in adj[i]:
                    assert w[i][j] == 0.0


def test_slem_of_the_cycle_matches_the_closed_form() -> None:
    # Metropolis on a cycle puts 1/3 on each neighbour and on the node itself.
    # The eigenvalues are (1 + 2 cos(2 pi k / n)) / 3.
    for n in (5, 8, 10, 13):
        exact = max(abs((1 + 2 * math.cos(2 * math.pi * k / n)) / 3) for k in range(1, n))
        assert abs(slem(metropolis_weights(cycle(n))) - exact) < 1e-9


def test_the_mean_is_kept_and_the_values_converge() -> None:
    rng = random.Random(3)
    for adj in (cycle(9), grid(4, 4), random_connected_graph(15, 0.2, 9)):
        w = metropolis_weights(adj)
        x0 = [rng.uniform(-5, 5) for _ in adj]
        xs = run(w, x0, 400)
        avg = sum(x0) / len(x0)
        for x in xs:
            assert abs(sum(x) / len(x) - avg) < 1e-9
        assert deviation(xs[-1]) < 1e-6 * deviation(x0)


def test_the_measured_rate_equals_the_slem() -> None:
    rng = random.Random(2004)
    for seed in range(12):
        adj = random_connected_graph(rng.randint(8, 16), 0.25, seed) if seed % 3 else grid(3, 2 + seed % 4)
        w = metropolis_weights(adj)
        lam = slem(w)
        x0 = [rng.gauss(0, 1) for _ in adj]
        xs = run(w, x0, 400)
        # The error never shrinks slower than the SLEM in one step.
        for a, b in zip(xs, xs[1:]):
            if deviation(a) > 1e-10:
                assert deviation(b) <= lam * deviation(a) * (1 + 1e-6)
        # The asymptotic rate equals the SLEM. Stop before the error reaches
        # the rounding floor of floating point.
        t1 = min(400, int(math.log(1e-11) / math.log(lam)))
        t0 = t1 // 2
        rate = (deviation(xs[t1]) / deviation(xs[t0])) ** (1.0 / (t1 - t0))
        assert abs(rate - lam) < 2e-3, (seed, rate, lam)


def test_a_bipartite_graph_without_self_weight_does_not_converge() -> None:
    # W = A/2 on an even cycle has the eigenvalue -1: the values oscillate.
    n = 6
    w = [[0.0] * n for _ in range(n)]
    for i in range(n):
        w[i][(i + 1) % n] = w[i][(i - 1) % n] = 0.5
    assert not converges(w)
    x0 = [1.0, 0.0, 1.0, 0.0, 1.0, 0.0]
    xs = run(w, x0, 50)
    assert xs[-1] == [0.0, 1.0, 0.0, 1.0, 0.0, 1.0] or xs[-1] == x0
    assert converges(metropolis_weights(cycle(n)))
