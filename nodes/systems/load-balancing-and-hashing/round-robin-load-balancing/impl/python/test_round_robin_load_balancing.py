# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/round-robin-load-balancing/. The authors are listed in prov/JZRZJJ.jsonl.

import random
from statistics import mean

from round_robin_load_balancing import (RoundRobin, fcfs_farm, pareto_sizes, percentile,
                                        poisson_arrivals)


def test_cycle_and_empty() -> None:
    assert RoundRobin(0).pick() is None
    rr = RoundRobin(3)
    assert [rr.pick() for _ in range(7)] == [0, 1, 2, 0, 1, 2, 0]


def test_every_window_is_balanced() -> None:
    for n in range(1, 7):
        rr = RoundRobin(n)
        seq = [rr.pick() for _ in range(40)]
        for a in range(len(seq)):
            for b in range(a + 1, len(seq) + 1):
                k = b - a
                counts = [seq[a:b].count(j) for j in range(n)]
                assert all(k // n <= c <= -(-k // n) for c in counts)


def test_skips_down_backends() -> None:
    rr = RoundRobin(4)
    rr.up[1] = False
    assert [rr.pick() for _ in range(6)] == [0, 2, 3, 0, 2, 3]
    rr.up = [False] * 4
    assert rr.pick() is None
    rr.up[2] = True
    assert [rr.pick() for _ in range(3)] == [2, 2, 2]


def test_random_against_oracle() -> None:
    rng = random.Random(7)
    for _ in range(500):
        n = rng.randint(1, 6)
        rr = RoundRobin(n)
        i = 0
        for _ in range(30):
            if rng.random() < 0.3:
                rr.up[rng.randrange(n)] = rng.random() < 0.6
            # oracle: the first up index at or after i, cyclically
            cand = [(i + d) % n for d in range(n) if rr.up[(i + d) % n]]
            want = cand[0] if cand else None
            assert rr.pick() == want
            if want is not None:
                i = (want + 1) % n
            else:
                i = i  # a full scan leaves the index where it was


def test_farm_by_hand() -> None:
    # one server: arrivals 0, 1, 2 with sizes 3, 1, 1 give finishes 3, 4, 5
    assert fcfs_farm(lambda a: 0, [0, 1, 2], [3, 1, 1], 1) == [3, 3, 3]
    # two servers, round robin: 0 -> s0 (done 3), 1 -> s1 (done 2), 2 -> s0 (done 4)
    rr = RoundRobin(2)
    assert fcfs_farm(lambda a: rr.pick(), [0, 1, 2], [3, 1, 1], 2) == [3, 1, 2]


def test_heavy_tail_round_robin_loses_to_least_connections() -> None:
    for seed in (1, 2, 3):
        rng = random.Random(seed)
        n, m, rho = 4, 20000, 0.8
        arr = poisson_arrivals(rng, rho * n, m)
        size = pareto_sizes(rng, 1.5, 1.0, m)
        rr = RoundRobin(n)
        r_rr = fcfs_farm(lambda a: rr.pick(), arr, size, n)
        r_lc = fcfs_farm(lambda a: min(range(n), key=lambda j: (a[j], j)), arr, size, n)
        assert mean(r_lc) * 2 < mean(r_rr)
        assert percentile(r_lc, 99) * 2 < percentile(r_rr, 99)


def test_exact_balance_by_count_not_by_work() -> None:
    rng = random.Random(11)
    n, m = 4, 4000
    arr = poisson_arrivals(rng, 3.2, m)
    size = pareto_sizes(rng, 1.5, 1.0, m)
    rr = RoundRobin(n)
    picks = []
    fcfs_farm(lambda a: picks.append(rr.pick()) or picks[-1], arr, size, n)
    counts = [picks.count(j) for j in range(n)]
    assert counts == [1000] * 4
    work = [sum(s for s, j in zip(size, picks) if j == k) for k in range(n)]
    assert max(work) > 1.2 * min(work)
