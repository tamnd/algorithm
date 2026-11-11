# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-pagerank/. The authors are listed in prov/S5R1H6.jsonl.

import math
import random

from distributed_pagerank import (
    median_estimate,
    power_iteration,
    return_probability,
    rounds_needed,
    walk_pagerank,
)

EXAMPLE = [[1], [2], [0, 3], [0]]  # arcs 0->1, 1->2, 2->0, 2->3, 3->0


def random_digraph(n: int, p: float, rng: random.Random) -> list[list[int]]:
    out = [[u for u in range(n) if u != v and rng.random() < p] for v in range(n)]
    for v in range(n):
        if not out[v]:
            out[v].append((v + 1 + rng.randrange(n - 1)) % n)
    return out


def test_example() -> None:
    pi = power_iteration(4, EXAMPLE, 0.2)
    assert [round(x, 4) for x in pi] == [0.2871, 0.2797, 0.2737, 0.1595]
    st = walk_pagerank(4, EXAMPLE, 0.2, 1000, random.Random(7))
    assert st["rounds"] == 49 == rounds_needed(4, 1000, 0.2)
    assert st["alive"] == 0
    assert all(abs(e - p) <= 0.1 * p for e, p in zip(st["est"], pi))


def test_unbiased() -> None:
    rng = random.Random(5)
    pi = power_iteration(4, EXAMPLE, 0.2)
    total = [0.0] * 4
    for _ in range(200):
        for v, e in enumerate(walk_pagerank(4, EXAMPLE, 0.2, 200, rng)["est"]):
            total[v] += e
    assert all(abs(t / 200 - p) <= 0.02 * p for t, p in zip(total, pi))


def test_variance_and_tail_bound() -> None:
    # Var(visits) <= mu (1 + r) / (1 - r), and P(|est - pi| >= d pi) <= 2 exp(-(1 - r) d^2 mu / 10)
    rng = random.Random(11)
    n, eps, k, d, trials = 10, 0.25, 150, 0.3, 40
    for _ in range(3):
        out = random_digraph(n, 0.3, rng)
        pi = power_iteration(n, out, eps)
        r = [return_probability(n, out, eps, v) for v in range(n)]
        mu = [n * k * p / eps for p in pi]
        runs = [walk_pagerank(n, out, eps, k, rng)["visits"] for _ in range(trials)]
        for v in range(n):
            xs = [run[v] for run in runs]
            mean = sum(xs) / trials
            var = sum((x - mean) ** 2 for x in xs) / (trials - 1)
            assert mu[v] >= k  # since pi(v) >= eps / n
            assert var <= 1.6 * mu[v] * (1 + r[v]) / (1 - r[v])
            bad = sum(abs(x - mu[v]) >= d * mu[v] for x in xs)
            bound = 2 * math.exp(-(1 - r[v]) * d * d * mu[v] / 10)
            assert bad <= trials * bound + 1


def test_high_probability_choice_of_k() -> None:
    # K = ceil(10 ln(2 n^2) / (eps d^2)) puts every node within d with probability >= 1 - 1/n
    rng = random.Random(3)
    n, eps, d = 10, 0.25, 0.3
    k = math.ceil(10 * math.log(2 * n * n) / (eps * d * d))
    for _ in range(4):
        out = random_digraph(n, 0.3, rng)
        pi = power_iteration(n, out, eps)
        st = walk_pagerank(n, out, eps, k, rng)
        assert all(abs(e - p) <= d * p for e, p in zip(st["est"], pi))
        arcs = sum(len(o) for o in out)
        assert st["messages"] <= arcs * st["rounds"]
        assert st["max_bits"] <= (n * k).bit_length()


def test_median_of_groups() -> None:
    rng = random.Random(9)
    n, eps, d = 8, 0.3, 0.3
    out = random_digraph(n, 0.4, rng)
    pi = power_iteration(n, out, eps)
    # with K >= 4 (2 - eps) / (eps d^2) each group misses with probability <= 1/4
    k = math.ceil(4 * (2 - eps) / (eps * d * d))
    est = median_estimate(n, out, eps, k, 25, rng)
    assert all(abs(e - p) <= d * p for e, p in zip(est, pi))
