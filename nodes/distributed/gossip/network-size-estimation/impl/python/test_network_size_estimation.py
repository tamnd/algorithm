# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/network-size-estimation/. The authors are listed in prov/RJGWTH.jsonl.

import random
import statistics

from network_size_estimation import (averaging_count, exp_direct, exp_minima, hyperloglog, kmin_direct,
                                     kmin_uniform, random_graph, random_tour, sample_collide)


def mean_and_se(xs):
    return statistics.mean(xs), statistics.stdev(xs) / len(xs) ** 0.5


def test_averaging_count_is_exact_in_the_limit():
    for seed in range(3):
        est = averaging_count(1000, 40, seed)
        assert max(abs(e - 1000) for e in est) < 1e-3


def test_kmin_gossip_reaches_the_global_value():
    for seed in range(3):
        est = kmin_uniform(500, 10, 15, seed)
        assert len(set(est)) == 1
        est = exp_minima(500, 10, 15, seed)
        assert len(set(est)) == 1


def test_kmin_and_exponential_estimators_are_unbiased():
    rng = random.Random(11)
    n = 1000
    m, se = mean_and_se([kmin_direct(n, 20, rng) for _ in range(1500)])
    assert abs(m - n) < 4 * se
    m, se = mean_and_se([exp_direct(n, 20, rng) for _ in range(10000)])
    assert abs(m - n) < 4 * se


def test_random_tour_is_unbiased():
    adj = random_graph(200, 4, 1)
    assert len({len(a) for a in adj}) > 1        # degrees vary
    rng = random.Random(5)
    for start in (0, 7):
        m, se = mean_and_se([random_tour(adj, start, rng) for _ in range(1500)])
        assert abs(m - 200) < 4 * se


def test_sample_and_collide():
    adj = random_graph(2000, 4, 2)
    est = [sample_collide(adj, 20, 10.0, seed) for seed in range(30)]
    assert abs(statistics.mean(est) / 2000 - 1) < 0.15
    # a timer that is too short gives samples near the start node
    short = [sample_collide(adj, 20, 0.5, seed) for seed in range(10)]
    assert statistics.mean(short) < 0.5 * 2000


def test_hyperloglog_merged_by_gossip():
    for seed in range(2):
        est = hyperloglog(2000, 64, 15, seed)
        assert len(set(est)) == 1
        assert abs(est[0] / 2000 - 1) < 3 * 1.04 / 8
