# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anderson-lock/. The authors are listed in prov/SV4NZH.jsonl.

from anderson_lock import client, home, init, lines
from interleave import explore, max_passage_rmr, no_progress, run, starvation


def explore_lock(n, rounds, padded=True):
    return explore([client(n, rounds)] * n, init(n), home=home(n), lines=lines(n, padded), cache=True)


def test_mutual_exclusion_fifo_and_cc_cost_two_processes() -> None:
    g = explore_lock(2, 2)
    assert g.violation is None and not g.stuck
    assert [max_passage_rmr(g, p, "cc") for p in range(2)] == [6, 6]


def test_mutual_exclusion_fifo_and_cc_cost_three_processes() -> None:
    g = explore_lock(3, 1)
    assert g.violation is None and not g.stuck
    assert [max_passage_rmr(g, p, "cc") for p in range(3)] == [5, 5, 5]


def test_dsm_cost_is_unbounded() -> None:
    # a process may get a slot that lives with another process and spin on it
    g = explore_lock(2, 2)
    assert max_passage_rmr(g, 0, "dsm") == float("inf")


def test_starvation_free_forever() -> None:
    g = explore([client(2, None)] * 2, init(2))
    assert g.violation is None
    assert no_progress(g) == []
    assert starvation(g, 0) == [] and starvation(g, 1) == []


def take_places_then_round_robin(n):
    def policy(t, enabled, rng):
        return t // 2 if t < 2 * n else enabled[t % len(enabled)]
    return policy


def test_padding_keeps_the_cost_constant_and_false_sharing_makes_it_grow() -> None:
    for n in range(2, 9):
        costs = []
        for padded in (True, False):
            m = run([client(n, 1)] * n, init(n), lines=lines(n, padded), policy=take_places_then_round_robin(n))
            assert m.violations == [] and m.entries == list(range(n))
            costs.append(max(cc for p in range(n) for cc, _ in m.passages[p]))
        assert costs == [5, 2 * n + 2]


def test_random_runs() -> None:
    for seed in range(40):
        n = 2 + seed % 6
        m = run([client(n, 3)] * n, init(n), lines=lines(n, True), seed=seed)
        assert m.violations == [] and len(m.entries) == 3 * n
        assert all(cc <= 6 for p in range(n) for cc, _ in m.passages[p])
