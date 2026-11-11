# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lpbcast/. The authors are listed in prov/DD2C6C.jsonl.

import statistics

from lpbcast import Lpbcast, infect_and_die_reach


def ratios(l: int, retrieve: bool = False, n: int = 300, fanout: int = 4) -> list[float]:
    out = []
    for seed in range(2):
        s = Lpbcast(n, l, fanout, seed, retrieve=retrieve)
        s.run(3)
        for k in range(3):
            s.broadcast(s.rng.randrange(n), 10 ** 6 + k)
        s.run(12)
        out += [s.delivery_ratio(10 ** 6 + k) for k in range(3)]
        for p in s.alive:
            assert len(s.view[p]) <= l and p not in s.view[p]
    return out


def test_infect_and_die_fixed_point():
    assert abs(infect_and_die_reach(4) - 0.9802) < 1e-3
    assert abs(infect_and_die_reach(2) - 0.7968) < 1e-3


def test_delivery_ratio_against_view_size():
    small = statistics.mean(ratios(4))
    mid = statistics.mean(ratios(15))
    large = statistics.mean(ratios(40))
    want = infect_and_die_reach(4)
    # with views much larger than the fanout, delivery is close to the
    # infect-and-die prediction for uniform targets
    assert abs(large - want) < 0.03
    assert abs(mid - want) < 0.05
    # it depends only mildly on the view size, even when l equals F
    assert large - small < 0.1
    assert small > 0.85


def test_retrieval_of_missing_ids_gives_full_delivery():
    assert min(ratios(15, retrieve=True)) == 1.0


def test_join_spreads_into_views():
    s = Lpbcast(300, 15, 4, 1)
    s.run(5)
    p = s.join(0)
    s.run(12)
    assert len(s.view[p]) == 15
    assert sum(p in s.view[q] for q in s.alive) >= 3


def test_unsubscription_removes_the_process_from_views():
    s = Lpbcast(300, 15, 4, 1)
    s.run(5)
    assert sum(5 in s.view[q] for q in s.alive) > 0
    s.unsubscribe(5)
    s.run(10)
    assert sum(5 in s.view[q] for q in s.alive) == 0
