# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transactional-boosting/. The authors are listed in prov/BFAFX0.jsonl.

import random

from sched import explore, random_run
from transactional_boosting import BoostedSet, apply, inverse, serializable


def program(txs, initial=(), use_locks=True, inverse_mode="correct"):
    """txs: list of (calls, cancel_first), one process each."""

    def make():
        s = BoostedSet(set(initial), use_locks, inverse_mode)
        return s, [s.transaction(p, calls, cancel) for p, (calls, cancel) in enumerate(txs)]

    return make


def all_serializable(make):
    runs = bad = 0
    for s, sys in explore(make, 200):
        assert sys.finished() and all(e is None for e in sys.error)
        runs += 1
        bad += not serializable(s.initial, s.items, s.committed)
    return runs, bad


T0 = ([("add", 1), ("remove", 2)], True)        # aborts once, then commits
T1 = ([("contains", 1), ("add", 2)], False)
T2 = ([("remove", 1), ("add", 3)], False)


def test_inverse_restores_the_state():
    for start in (set(), {1}, {2}, {1, 2}):
        for calls in ([("add", 1)], [("remove", 1)], [("add", 1), ("remove", 2), ("add", 2)]):
            items = set(start)
            undo = []
            for c in calls:
                r = apply(items, c)
                inv = inverse(c, r)
                if inv:
                    undo.append(inv)
            for c in reversed(undo):
                apply(items, c)
            assert items == start


def test_abort_rolls_back_with_inverses():
    s = BoostedSet({2})
    gen = s.transaction(0, [("add", 1), ("remove", 2)], cancel_first=True)
    snapshots = []
    try:
        while True:
            next(gen)
            snapshots.append(set(s.items))
    except StopIteration as stop:
        assert stop.value == [True, True]
    # after the first attempt and its undo, the set was {2} again
    assert {2} in snapshots[3:]
    assert s.items == {1}


def test_boosting_is_serializable_on_all_schedules():
    for txs, init in (([T0, T1], {2}), ([T0, T2], {1, 2}), ([T1, T2], {1})):
        runs, bad = all_serializable(program(txs, init))
        assert runs > 20 and bad == 0


def test_three_transactions_all_schedules():
    runs, bad = all_serializable(program([([("add", 1)], False), ([("contains", 1)], False),
                                          ([("remove", 1)], False)], set()))
    assert runs > 50 and bad == 0


def test_without_abstract_locks_some_schedule_is_not_serializable():
    runs, bad = all_serializable(program([T0, T1], {2}, use_locks=False))
    assert bad > 0


def test_without_undo_log_aborts_leave_effects():
    runs, bad = all_serializable(program([T0, T1], {2}, inverse_mode="none"))
    assert bad > 0            # T0 aborts once, and its effects stay


def test_blind_inverse_is_wrong():
    # T0 adds 1 though 1 is already there; the blind inverse removes it
    runs, bad = all_serializable(program([([("add", 1)], True), ([("contains", 2)], False)], {1},
                                         inverse_mode="blind"))
    assert bad == runs


def test_random_transactions():
    rng = random.Random(2008)
    methods = ("add", "remove", "contains")
    for _ in range(600):
        n = rng.randint(2, 4)
        txs = []
        for _ in range(n):
            calls = [(rng.choice(methods), rng.randint(0, 3)) for _ in range(rng.randint(1, 3))]
            txs.append((calls, rng.random() < 0.3))
        init = {k for k in range(4) if rng.random() < 0.5}
        s, sys = random_run(program(txs, init), rng, 5000)
        assert sys.finished()
        assert len(s.committed) == n
        assert serializable(s.initial, s.items, s.committed)
