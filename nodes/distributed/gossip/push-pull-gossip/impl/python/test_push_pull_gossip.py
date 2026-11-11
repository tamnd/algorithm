# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/push-pull-gossip/. The authors are listed in prov/JCK6B9.jsonl.

import math
import random

from push_pull_gossip import (barbell, conductance, cycle, is_connected, median_counter, normalized_laplacian,
                              push_pull_with_age, random_regular_cycles, spread, star, symmetric_eigenvalues,
                              two_stars)


def test_small_cases_and_determinism() -> None:
    assert spread(1, "push-pull", random.Random(0)) == (0, 0, [1])
    assert spread(2, "push-pull", random.Random(0))[0] == 1
    assert spread(500, "push-pull", random.Random(3)) == spread(500, "push-pull", random.Random(3))


def test_first_round_triples_on_average() -> None:
    # The source pushes along its own call and pulls along each call it gets.
    # The expected number of callers is 1, so the expected count after round 1 is 3.
    firsts = []
    for seed in range(200):
        _, _, hist = spread(300, "push-pull", random.Random(seed))
        firsts.append(hist[1])
        assert all(hist[t] >= hist[t - 1] for t in range(1, len(hist)))
    assert 2.7 <= sum(firsts) / len(firsts) <= 3.3


def test_push_pull_rounds_fit_log3_plus_loglog() -> None:
    # Karp et al. 2000: log3 n + O(log log n). Fitted: the extra term is about log2 ln n.
    for n, trials in ((256, 30), (1024, 20)):
        rounds = [spread(n, "push-pull", random.Random(n + s))[0] for s in range(trials)]
        mean = sum(rounds) / trials
        low = math.log(n, 3)
        high = math.log(n, 3) + math.log2(math.log(n)) + 1.0
        assert low <= mean <= high, (n, mean, low, high)
        push = [spread(n, "push", random.Random(n + s))[0] for s in range(10)]
        assert mean < sum(push) / 10 - 4


def test_age_rule_is_sensitive_to_the_stopping_time() -> None:
    n = 1024
    early, _ = push_pull_with_age(n, random.Random(1), math.floor(math.log(n, 3)))
    assert early < 0.6 * n
    full, tx = push_pull_with_age(n, random.Random(1), math.ceil(math.log(n, 3) + math.log2(math.log(n))) + 1)
    assert full == n and tx < 10 * n


def test_median_counter_informs_all_and_its_cost_stays_flat() -> None:
    cost = {}
    for n, trials in ((256, 8), (1024, 6)):
        total = 0
        for s in range(trials):
            rounds, tx, informed = median_counter(n, random.Random(10 * n + s))
            assert informed == n
            assert rounds <= 4 * math.log2(n)
            total += tx
        cost[n] = total / trials / n
    push = {n: sum(spread(n, "push", random.Random(n + s))[1] for s in range(6)) / 6 / n for n in (256, 1024)}
    # Push grows by about ln 4 per process when n grows by 4; the median counter does not.
    assert push[1024] - push[256] > 1.0
    assert abs(cost[1024] - cost[256]) < 0.5
    assert cost[1024] < 11


def test_star_push_pull_fast_push_slow() -> None:
    n = 60
    for seed in range(10):
        src = random.Random(seed).randrange(n)
        assert spread(n, "push-pull", random.Random(seed), adj=star(n), source=src)[0] <= 2
        assert spread(n, "push", random.Random(seed), adj=star(n), source=src)[0] >= n - 1
    # Pull from a leaf waits for the center to call that leaf.
    waits = [spread(n, "pull", random.Random(s), adj=star(n), source=5)[0] for s in range(40)]
    assert sum(waits) / 40 > (n - 1) / 3


def test_time_against_log_n_over_conductance() -> None:
    # Giakkoupis 2011: O(log n / phi) rounds for push-pull, on every graph.
    cases = [(barbell(16), 1 / (16 * 15 + 1)), (cycle(64), 1 / 32), (two_stars(20, 300), 1 / 39), (star(100), 1.0)]
    for adj, phi in cases:
        n = len(adj)
        for seed in range(15):
            src = random.Random(seed).randrange(n)
            rounds = spread(n, "push-pull", random.Random(seed), adj=adj, source=src)[0]
            assert rounds <= 4 * math.log(n) / phi + 4


def test_two_stars_need_about_one_over_phi_rounds() -> None:
    # The lower bound example: the centers talk with probability about 1/a per round.
    n = 300
    means = []
    for a in (10, 40):
        r = [spread(n, "push-pull", random.Random(s), adj=two_stars(a, n), source=1)[0] for s in range(40)]
        means.append(sum(r) / 40)
    assert means[1] > 2 * means[0]
    assert means[1] > 0.3 * 40


def test_expanders_take_logarithmic_time() -> None:
    for n in (256, 1024):
        adj = random_regular_cycles(n, 2, random.Random(n))
        rounds = [spread(n, "push-pull", random.Random(s), adj=adj, source=s)[0] for s in range(8)]
        assert max(rounds) <= 2.5 * math.log(n)


def test_cheeger_inequality_on_random_small_graphs() -> None:
    checked = 0
    for s in range(120):
        rng = random.Random(s)
        n = rng.randrange(4, 10)
        p = rng.uniform(0.25, 0.8)
        adj: list[list[int]] = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < p:
                    adj[i].append(j)
                    adj[j].append(i)
        if not is_connected(adj):
            continue
        phi = conductance(adj)
        lam2 = symmetric_eigenvalues(normalized_laplacian(adj))[1]
        assert lam2 / 2 <= phi + 1e-9 <= math.sqrt(2 * lam2) + 2e-9, (s, lam2, phi)
        checked += 1
    assert checked > 60


def test_known_conductances_and_eigenvalues() -> None:
    for n in (6, 7, 8):
        complete = [[j for j in range(n) if j != i] for i in range(n)]
        assert abs(conductance(complete) - math.ceil(n / 2) / (n - 1)) < 1e-12
        assert abs(symmetric_eigenvalues(normalized_laplacian(complete))[1] - n / (n - 1)) < 1e-9
        assert abs(conductance(cycle(n)) - 1 / (n // 2)) < 1e-12
        assert abs(symmetric_eigenvalues(normalized_laplacian(cycle(n)))[1] - (1 - math.cos(2 * math.pi / n))) < 1e-9
    assert conductance(star(8)) == 1.0
    assert abs(conductance(barbell(4)) - 1 / 13) < 1e-12
