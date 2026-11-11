# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-contention-manager/. The authors are listed in prov/Z33CZD.jsonl.

import random
from itertools import permutations

from cmsim import ABORTED, DONE, Aggressive, enabled, explore, fair_livelocks, initial, lasso, random_run, replay
from greedy_contention_manager import Greedy

WORKLOADS = [
    [[0, 1], [1, 0]],
    [[0, 1], [0, 1]],
    [[0, 1, 2], [2, 1, 0]],
    [[0, 1], [1, 2], [2, 0]],
    [[0], [1, 0], [1]],
    [[0, 1], [1], [0]],
]


def oldest_live(state):
    live = [(t.ts, i) for i, t in enumerate(state[1]) if t.status != DONE]
    return min(live)[1] if live else None


def test_trace_of_the_example():
    progs = [[0, 1], [1, 0]]          # T0 is older (timestamp 0)
    st, events = replay(progs, Greedy(), [0, 1, 1, 0, 0, 1, 1, 1, 1])
    assert events == ["open", "open", "wait", "abort", "commit",
                      "restart", "open", "open", "commit"]
    assert not enabled(st)


def test_no_fair_livelock_on_all_small_workloads():
    for progs in WORKLOADS:
        for order in permutations(range(len(progs))):
            states, edges = explore(progs, Greedy(), list(order))
            assert fair_livelocks(states, edges) == []
            # the only state without a step is the one where all committed
            for st in states:
                assert enabled(st) or all(o == -1 for o in st[0])


def test_oldest_live_transaction_is_never_aborted_once_it_stops_waiting():
    for progs in WORKLOADS:
        for order in permutations(range(len(progs))):
            states, edges = explore(progs, Greedy(), list(order))
            for u, out in enumerate(edges):
                a = oldest_live(states[u])
                if a is None:
                    continue
                ta = states[u][1][a]
                for p, ev, v in out:
                    tb = states[v][1][a]
                    if p == a:
                        assert not tb.waiting      # the oldest never starts to wait
                    elif not ta.waiting and ta.status != ABORTED:
                        assert tb.status != ABORTED


def test_aggressive_livelocks():
    for progs in WORKLOADS[:4]:
        found = lasso(progs, Aggressive())
        assert found is not None
        prefix, cycle = found
        start, _ = replay(progs, Aggressive(), prefix)
        st = start
        for _ in range(3):
            st, events = replay(progs, Aggressive(), cycle, st)
            assert st == start
            assert "commit" not in events
            assert set(cycle) == set(enabled(start))


def test_aggressive_example_cycle():
    progs = [[0, 1], [1, 0]]
    start, _ = replay(progs, Aggressive(), [0])
    st, events = replay(progs, Aggressive(), [0, 1, 0, 1, 0, 1], start)
    assert events == ["open", "abort", "restart", "open", "abort", "restart"]
    assert st == start
    # Greedy on the same schedule: T1 waits for the older T0, and T0 commits
    g_start, _ = replay(progs, Greedy(), [0])
    g_end, g_events = replay(progs, Greedy(), [0, 1, 0, 1, 1, 1], g_start)
    assert g_events == ["open", "wait", "commit", "open", "open", "commit"]
    assert not enabled(g_end)


def test_random_runs_commit_all_and_the_oldest_needs_no_extra_steps():
    rng = random.Random(2005)
    for _ in range(600):
        n = rng.randint(2, 4)
        progs = [rng.sample(range(4), rng.randint(1, 3)) for _ in range(n)]
        order = list(range(n))
        rng.shuffle(order)
        c = random_run(progs, Greedy(), rng, 5000, order)
        assert c["done"] and c["commit"] == n
        first = order.index(0)
        assert c["commit_at"][first] == len(progs[first]) + 1


def test_initial_state():
    st = initial([[0], [0]], Greedy(), [1, 0])
    assert [t.ts for t in st[1]] == [1, 0] and st[0] == (-1,)
