# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polite-contention-manager/. The authors are listed in prov/6YVCN1.jsonl.

import random

from cmsim import ABORTED, Tx, enabled, lasso, random_run, replay, step
from polite_contention_manager import Polite


def test_trace_of_the_example():
    progs = [[0, 1], [1, 0]]
    st, events = replay(progs, Polite(2), [0, 1, 1, 1, 1, 1, 1, 1])
    assert events == ["open", "open", "wait", "backoff", "wait", "backoff", "backoff", "abort"]
    assert st[1][0].status == ABORTED and st[0] == (1, 1)
    st, events = replay(progs, Polite(2), [0, 1, 0, 0, 0], st)
    assert events == ["restart", "commit", "open", "open", "commit"]
    assert not enabled(st)


def test_m_waits_and_exponential_intervals():
    for m in range(6):
        p = Polite(m)
        me, enemy = Tx(), Tx()
        intervals = []
        while True:
            kill, me = p.resolve(me, enemy)
            if kill:
                break
            intervals.append(me.left)
        assert intervals == [2 ** i for i in range(m)]
        assert sum(intervals) == 2 ** m - 1


def test_obstruction_freedom_against_a_stopped_enemy():
    # T1 holds object 0 and then stops for ever; T0 runs alone
    for m in range(5):
        progs = [[0, 1], [0]]
        st, _ = replay(progs, Polite(m), [1])
        steps = 0
        while st[1][0].status != 2:
            st, _ = step(progs, Polite(m), st, 0)
            steps += 1
        # m waits, 2^m - 1 backoff steps, abort and take, open, commit
        assert steps == m + (2 ** m - 1) + 3


def test_polite_can_livelock_under_an_adversarial_schedule():
    for progs in ([[0, 1], [1, 0]], [[0, 1], [0, 1]], [[0, 1], [1, 2], [2, 0]]):
        found = lasso(progs, Polite(2))
        assert found is not None
        prefix, cycle = found
        start, _ = replay(progs, Polite(2), prefix)
        st = start
        for _ in range(3):
            st, events = replay(progs, Polite(2), cycle, st)
            assert st == start and "commit" not in events
            assert set(cycle) == set(enabled(start))


def test_random_runs_commit_all():
    rng = random.Random(22)
    for _ in range(600):
        n = rng.randint(2, 4)
        progs = [rng.sample(range(4), rng.randint(1, 3)) for _ in range(n)]
        c = random_run(progs, Polite(rng.randint(0, 4)), rng, 20_000)
        assert c["done"] and c["commit"] == n
