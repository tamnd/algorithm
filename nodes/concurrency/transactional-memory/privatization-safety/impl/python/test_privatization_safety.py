# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/privatization-safety/. The authors are listed in prov/9NJC6P.jsonl.

import random

from privatization_safety import ALLOWED, X, allowed, privatization
from sched import explore, random_run, run_schedule
from stm import TL2, EagerSTM, NOrec


def outcomes(make):
    out = {}
    for mem, sys in explore(make, 80):
        assert sys.finished()
        assert sys.error == [None] * len(sys.error)
        out.setdefault(mem.val[X], sys.trace)
    return out


def first_bad(make):
    for mem, sys in explore(make, 80):
        if mem.val[X] not in ALLOWED:
            return mem.val[X], sys.trace, sys.result[0]
    return None


def test_tl2_delayed_cleanup():
    bad = first_bad(privatization(TL2))
    assert bad is not None
    value, trace, seen = bad
    # the worker commits before the flag is set, but writes X back after the
    # privatizer has read 0 and written 1
    assert value == 100 and seen == 0


def test_tl2_delayed_cleanup_schedule():
    # worker: begin, read PRIV, lock X, clock (now it is logically committed);
    # privatizer: begin, lock PRIV, clock, write back PRIV, read X, write X;
    # worker: write back X
    sched = [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1]
    mem, sys = run_schedule(privatization(TL2), sched)
    assert mem.val[X] == 100
    assert sys.result[0] == 0


def test_eager_doomed_transaction():
    bad = first_bad(privatization(EagerSTM))
    assert bad is not None
    assert bad[0] == 0   # the abort of the worker restores X = 0 over the privatizer's write


def test_fence_makes_tl2_and_eager_safe():
    for cls in (TL2, EagerSTM):
        assert set(outcomes(privatization(cls, fence=True))) <= ALLOWED


def test_norec_is_safe_without_fence():
    assert set(outcomes(privatization(NOrec))) == ALLOWED


def test_random_schedules_two_workers():
    rng = random.Random(2007)
    seen_bad = {TL2: 0, EagerSTM: 0}
    for i in range(600):
        cls = (TL2, EagerSTM, NOrec)[i % 3]
        fence = i % 2 == 0
        mem, sys = random_run(privatization(cls, fence, workers=2), rng, 2000)
        assert sys.finished()
        ok = mem.val[X] in allowed(2)
        if fence or cls is NOrec:
            assert ok
        elif not ok:
            seen_bad[cls] += 1
    assert seen_bad[TL2] > 0 and seen_bad[EagerSTM] > 0
