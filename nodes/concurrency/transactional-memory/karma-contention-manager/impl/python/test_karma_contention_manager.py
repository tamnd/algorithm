# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karma-contention-manager/. The authors are listed in prov/GCR25F.jsonl.

import random

from cmsim import ABORTED, Tx, enabled, lasso, random_run, replay
from karma_contention_manager import Karma


def test_trace_of_the_example():
    progs = [[0, 1], [1, 0]]
    st, events = replay(progs, Karma(), [0, 1, 1, 0, 1, 1])
    assert events == ["open", "open", "wait", "wait", "backoff", "abort"]
    assert st[1][0].status == ABORTED and st[0] == (1, 1)
    # T1 has opened two objects, T0 one; T0 keeps its priority when it restarts
    assert st[1][1].prio - st[1][0].prio == 1
    st, events = replay(progs, Karma(), [0, 1, 0, 0, 0], st)
    assert events == ["restart", "commit", "open", "open", "commit"]
    assert not enabled(st)


def test_priority_kept_on_abort_and_reset_on_commit():
    k = Karma()
    t = Tx(prio=5, tries=2)
    assert k.restarted(t).prio == 5
    assert k.committed(t).prio == 0
    assert k.opened(t).prio == 6 and k.opened(t).tries == 0


def test_lower_priority_waits_difference_plus_one_times():
    k = Karma(interval=3)
    for mine in range(4):
        for theirs in range(6):
            me, enemy = Tx(prio=mine), Tx(prio=theirs)
            waits = 0
            while True:
                kill, me = k.resolve(me, enemy)
                if kill:
                    break
                assert me.left == 3
                waits += 1
            assert waits == max(0, theirs - mine + 1)


def test_karma_can_livelock_under_an_adversarial_schedule():
    for progs in ([[0, 1], [1, 0]], [[0, 1], [0, 1]]):
        found = lasso(progs, Karma(), limit=20_000)
        assert found is not None
        prefix, cycle = found
        start, _ = replay(progs, Karma(), prefix)
        st = start
        for _ in range(3):
            st, events = replay(progs, Karma(), cycle, st)
            assert st == start and "commit" not in events
            assert set(cycle) == set(enabled(start))


def test_random_runs_commit_all():
    rng = random.Random(2004)
    for _ in range(600):
        n = rng.randint(2, 4)
        progs = [rng.sample(range(4), rng.randint(1, 3)) for _ in range(n)]
        c = random_run(progs, Karma(), rng, 20_000)
        assert c["done"] and c["commit"] == n
