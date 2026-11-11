# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polka-contention-manager/. The authors are listed in prov/D8YGK7.jsonl.

import random

from cmsim import ABORTED, DONE, Tx, enabled, lasso, random_run, replay, step
from polka_contention_manager import Polka


def test_trace_of_the_example():
    # T0 opens three objects first, so T1 has a priority gap of 3: three rounds of backoff
    progs = [[0, 1, 2], [2]]
    st, events = replay(progs, Polka(), [0, 0, 0, 1, 1, 1, 1, 1, 1])
    assert events == ["open", "open", "open", "wait", "backoff", "wait", "backoff", "backoff",
                      "wait"]
    assert st[1][1].tries == 3 and st[1][1].left == 4
    st, events = replay(progs, Polka(), [1, 1, 1, 1, 1], st)
    assert events == ["backoff"] * 4 + ["abort"]
    assert st[1][0].status == ABORTED
    st, events = replay(progs, Polka(), [1, 0, 0, 0, 0, 0], st)
    assert events == ["commit", "restart", "open", "open", "open", "commit"]
    assert not enabled(st)


def test_backoff_rounds_equal_the_priority_gap():
    p = Polka()
    for mine in range(4):
        for theirs in range(7):
            me, enemy = Tx(prio=mine), Tx(prio=theirs)
            intervals = []
            while True:
                kill, me = p.resolve(me, enemy)
                if kill:
                    break
                intervals.append(me.left)
            gap = max(0, theirs - mine)
            assert intervals == [2 ** i for i in range(gap)]


def test_priority_kept_on_abort_and_reset_on_commit():
    p = Polka()
    t = Tx(prio=4, tries=1)
    assert p.restarted(t).prio == 4 and p.committed(t).prio == 0
    assert p.opened(t).prio == 5 and p.opened(t).tries == 0


def test_obstruction_freedom_against_a_stopped_enemy():
    for k in range(1, 5):
        progs = [[k], list(range(k + 1))]       # T1 opens k + 1 objects, then stops
        st, _ = replay(progs, Polka(), [1] * (k + 1))
        steps = 0
        while st[1][0].status != DONE:
            st, _ = step(progs, Polka(), st, 0)
            steps += 1
        gap = k + 1
        assert steps == gap + (2 ** gap - 1) + 2


def test_polka_can_livelock_under_an_adversarial_schedule():
    for progs in ([[0, 1], [1, 0]], [[0, 1], [0, 1]]):
        found = lasso(progs, Polka(), limit=20_000)
        assert found is not None
        prefix, cycle = found
        start, _ = replay(progs, Polka(), prefix)
        st = start
        for _ in range(3):
            st, events = replay(progs, Polka(), cycle, st)
            assert st == start and "commit" not in events
            assert set(cycle) == set(enabled(start))


def test_random_runs_commit_all():
    rng = random.Random(2005)
    for _ in range(600):
        n = rng.randint(2, 4)
        progs = [rng.sample(range(4), rng.randint(1, 3)) for _ in range(n)]
        c = random_run(progs, Polka(), rng, 20_000)
        assert c["done"] and c["commit"] == n
