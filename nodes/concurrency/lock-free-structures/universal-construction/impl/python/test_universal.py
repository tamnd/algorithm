# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/universal-construction/. The authors are listed in prov/TT2P8N.jsonl.

import pytest

from explorer import World, explore, final_histories, random_run
from lincheck import Queue, is_linearizable
from universal import race, setup_for

WORKLOADS = {
    "enq | enq": [[("enq", "a")], [("enq", "b")]],
    "enq | deq": [[("enq", "a")], [("deq", None)]],
}


@pytest.mark.parametrize("wait_free", [True, False], ids=["wait-free", "lock-free"])
@pytest.mark.parametrize("name", sorted(WORKLOADS))
def test_queue_every_history_is_linearizable(name, wait_free) -> None:
    progs = WORKLOADS[name]
    hs = final_histories(setup_for(progs, Queue(), wait_free), max_depth=400)
    assert hs
    for h in hs:
        assert is_linearizable(list(h), Queue()), h


@pytest.mark.parametrize("name", sorted(WORKLOADS))
def test_wait_free_loop_bound_in_every_run(name) -> None:
    # Each operation threads its node within n + 2 rounds of the loop.
    progs = WORKLOADS[name]
    n = len(progs)
    worst = [0]

    def final(w):
        for r in w.ret:
            worst[0] = max(worst[0], max(r))

    explore(setup_for(progs, Queue(), True), final=final, max_depth=400)
    assert 1 <= worst[0] <= n + 2


@pytest.mark.parametrize("n", [3, 4])
@pytest.mark.parametrize("wait_free", [True, False], ids=["wait-free", "lock-free"])
def test_random_schedules(n, wait_free) -> None:
    # Too many states for the explorer; sample 2000 seeded schedules instead.
    progs = [[("enq", i), ("deq", None)] for i in range(n)]
    for seed in range(2000):
        w = random_run(setup_for(progs, Queue(), wait_free), seed)
        assert all(w.done)
        assert is_linearizable(list(w.history), Queue()), w.history
        if wait_free:
            assert max(max(r) for r in w.ret) <= n + 2


def test_queue_alone() -> None:
    ops = [("enq", "a"), ("enq", "b"), ("deq", None), ("enq", "c"), ("deq", None), ("deq", None), ("deq", None)]
    for wait_free in (True, False):
        w = World(setup_for([ops, []], Queue(), wait_free))
        while not w.done[0]:
            w.step(0)
        results = [e[2] for e in w.history if e[0] == "res"]
        assert results == [None, None, "a", None, "b", "c", None]
        assert w.ret[0] == [1] * len(ops)  # alone, one round of the loop each


@pytest.mark.parametrize("n", [2, 3, 4, 5])
@pytest.mark.parametrize("head_start", [0, 17, 100])
def test_race_wait_free_ends_lock_free_starves(n, head_start) -> None:
    # The others win every consensus they can win.
    done, iters, _ = race(Queue(), True, n, head_start)
    assert done and iters <= n + 2
    done, iters, others = race(Queue(), False, n, head_start, rounds=2000)
    assert not done and iters is None and others > 100
