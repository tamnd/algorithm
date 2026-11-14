# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clustered-voltage-scaling/. The authors are listed in prov/STT7KY.jsonl.

import itertools
import random

import pytest

from clustered_voltage_scaling import Net, cvs, is_legal, meets_timing, random_net, saving, worst_output_time


def page_net():
    # a -> g1 -> g2 -> g4 (output); b -> g3 -> g4; g3 -> g5 (output). Delays (high, low), cap.
    return Net(
        ["a", "b"],
        [
            ("g1", ["a"], 2, 3, 2),
            ("g2", ["g1"], 2, 3, 2),
            ("g3", ["b"], 1, 2, 3),
            ("g4", ["g2", "g3"], 2, 3, 2),
            ("g5", ["g3"], 1, 2, 1),
        ],
        ["g4", "g5"],
    )


def all_feasible(net, period, lc):
    for r in range(len(net.gates) + 1):
        for s in itertools.combinations(net.gates, r):
            s = set(s)
            if is_legal(net, s) and meets_timing(net, s, period, lc):
                yield s


def test_page_example():
    net = page_net()
    assert worst_output_time(net, set(), 1) == 6
    low = cvs(net, 8, 1)
    assert low == {"g4", "g5", "g3"}
    assert worst_output_time(net, low, 1) == 8
    best = max(all_feasible(net, 8, 1), key=lambda s: saving(net, s))
    assert saving(net, best) == saving(net, low) == 6


def test_legal_timed_and_maximal_against_brute_force():
    rng = random.Random(31)
    for _ in range(150):
        net = random_net(rng, rng.randint(1, 3), rng.randint(2, 8))
        lc = rng.randint(0, 1)
        period = worst_output_time(net, set(), lc) + rng.randint(0, 4)
        low = cvs(net, period, lc)
        assert is_legal(net, low)
        assert meets_timing(net, low, period, lc)
        # maximal: no single high gate can join and keep both properties
        for g in net.gates:
            if g not in low:
                s = low | {g}
                assert not (is_legal(net, s) and meets_timing(net, s, period, lc))
        best = max(saving(net, s) for s in all_feasible(net, period, lc))
        assert saving(net, low) <= best


def test_result_contains_every_legal_timed_set():
    # Under the additive delay model the legal timed sets are closed under union,
    # and the pass returns the largest one, so it is optimal for any weights.
    rng = random.Random(32)
    for _ in range(200):
        net = random_net(rng, rng.randint(1, 3), rng.randint(2, 9))
        lc = rng.randint(0, 2)
        period = worst_output_time(net, set(), lc) + rng.randint(0, 5)
        low = cvs(net, period, lc)
        feasible = list(all_feasible(net, period, lc))
        for s in feasible:
            assert s <= low
        for s, t in itertools.combinations(feasible[:40], 2):
            u = s | t
            assert is_legal(net, u) and meets_timing(net, u, period, lc)


def test_fanout_stem_goes_low_only_after_all_its_fanouts():
    # g1 drives g2 and g3. With period 3 only the two outputs fit at the low
    # supply; with period 4 the stem g1 joins them.
    net = Net(["a"], [("g1", ["a"], 1, 2, 5), ("g2", ["g1"], 1, 2, 1), ("g3", ["g1"], 1, 2, 1)], ["g2", "g3"])
    assert cvs(net, 3, 0) == {"g2", "g3"}
    assert cvs(net, 4, 0) == {"g1", "g2", "g3"}


def test_infeasible_period_raises():
    with pytest.raises(ValueError):
        cvs(page_net(), 5, 1)
