# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-connections/. The authors are listed in prov/MKYZP0.jsonl.

import random
from statistics import mean

import pytest

from least_connections import (LeastConnections, erlang_m1_response, fcfs_farm, jsq_policy,
                               poisson_arrivals)


def test_trace_of_the_page() -> None:
    lc = LeastConnections(3)
    seq = []
    seq.append(lc.pick())          # a = 1 0 0
    seq.append(lc.pick())          # a = 1 1 0
    seq.append(lc.pick())          # a = 1 1 1
    lc.done(1)                     # a = 1 0 1
    seq.append(lc.pick())          # a = 1 1 1
    seq.append(lc.pick())          # a = 2 1 1
    lc.done(0)
    lc.done(0)                     # a = 0 1 1
    seq.append(lc.pick())          # a = 1 1 1
    assert seq == [0, 1, 2, 1, 0, 0]
    assert lc.a == [1, 1, 1]


def test_example_table_of_the_page() -> None:
    arrivals, sizes = list(range(8)), [9, 1, 1, 9, 1, 1, 9, 1]
    lc = fcfs_farm(jsq_policy, arrivals, sizes, 3)
    assert lc == [9, 1, 1, 9, 1, 1, 9, 3] and sum(lc) == 34
    rr = fcfs_farm(lambda a, k=[0]: (k.append(0), (len(k) - 2) % 3)[1], arrivals, sizes, 3)
    assert sum(rr) == 50


def test_down_and_empty() -> None:
    assert LeastConnections(0).pick() is None
    lc = LeastConnections(3)
    lc.up = [False, True, False]
    assert [lc.pick() for _ in range(3)] == [1, 1, 1]
    lc.up[1] = False
    assert lc.pick() is None
    with pytest.raises(ValueError):
        LeastConnections(2).done(0)


def test_random_against_oracle() -> None:
    rng = random.Random(3)
    for _ in range(500):
        n = rng.randint(1, 7)
        lc = LeastConnections(n)
        model = [0] * n
        for _ in range(40):
            if rng.random() < 0.2:
                lc.up[rng.randrange(n)] = rng.random() < 0.7
            busy = [j for j in range(n) if model[j] > 0]
            if busy and rng.random() < 0.4:
                j = rng.choice(busy)
                lc.done(j)
                model[j] -= 1
                continue
            ups = [j for j in range(n) if lc.up[j]]
            want = min(ups, key=lambda j: (model[j], j)) if ups else None
            assert lc.pick() == want
            if want is not None:
                model[want] += 1
            assert lc.a == model


def test_jsq_beats_random_and_round_robin_at_load_09() -> None:
    n, rho, m = 4, 0.9, 40000
    res = {"jsq": [], "random": [], "rr": []}
    for seed in (1, 2, 3):
        rng = random.Random(seed)
        arr = poisson_arrivals(rng, rho * n, m)
        size = [rng.expovariate(1.0) for _ in range(m)]
        g = random.Random(seed + 1000)
        k = [0]

        def rr(active, k=k):
            k[0] += 1
            return (k[0] - 1) % n

        res["jsq"].append(mean(fcfs_farm(jsq_policy, arr, size, n)))
        res["random"].append(mean(fcfs_farm(lambda a: g.randrange(n), arr, size, n)))
        res["rr"].append(mean(fcfs_farm(rr, arr, size, n)))
    jsq, rnd, rr_ = (mean(res[k]) for k in ("jsq", "random", "rr"))
    assert jsq < rr_ < rnd
    assert all(x < y for x, y in zip(res["jsq"], res["rr"]))
    # random splitting gives n M/M/1 queues: mean response 1 / (1 - rho) = 10
    assert abs(rnd - 10.0) < 1.5
    # round robin gives E_n/M/1 queues
    assert abs(rr_ - erlang_m1_response(n, rho)) < 1.0
    assert jsq < 0.6 * rr_


def test_erlang_formula_limits() -> None:
    assert abs(erlang_m1_response(1, 0.9) - 10.0) < 1e-9  # E_1/M/1 is M/M/1
    assert abs(erlang_m1_response(4, 0.9) - 6.383) < 1e-3
