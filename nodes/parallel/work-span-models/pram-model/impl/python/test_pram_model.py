# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pram-model/. The authors are listed in prov/43RZPV.jsonl.

import math
import random

import pytest

from pram_model import (ARBITRARY, COMBINING, COMMON, CREW, EREW, PRIORITY, AccessError, access_sets, brent_time,
                        run_step, run_step_on_p, tree_sum, write_conflict_step)

ORDER = (EREW, CREW, COMMON, ARBITRARY, PRIORITY)


def test_tree_sum_on_erew():
    rng = random.Random(1)
    for n in list(range(0, 70)) + [128, 129, 1000]:
        xs = [rng.randint(-50, 50) for _ in range(n)]
        total, m = tree_sum(xs, EREW)  # each step runs under the EREW rule, so a conflict would raise
        assert total == sum(xs)
        assert m.time == (math.ceil(math.log2(n)) if n > 1 else 0)
        assert m.work == max(n - 1, 0)


def test_reads_see_the_old_memory():
    mem = {"a": 1, "b": 2}
    swap = {0: (("a",), lambda x: [("b", x[0])]), 1: (("b",), lambda x: [("a", x[0])])}
    assert run_step(mem, swap, EREW) == {"a": 2, "b": 1}
    assert mem == {"a": 1, "b": 2}


def test_read_rules():
    step = {i: (("x",), lambda x, i=i: [(("y", i), x[0])]) for i in range(4)}
    with pytest.raises(AccessError):
        run_step({"x": 7}, step, EREW)
    for rule in ORDER[1:]:
        new = run_step({"x": 7}, step, rule)
        assert all(new[("y", i)] == 7 for i in range(4))


def test_write_rules():
    same, diff = write_conflict_step([5, 5, 5]), write_conflict_step([4, 9, 6])
    for rule in (EREW, CREW):
        for step in (same, diff):
            with pytest.raises(AccessError):
                run_step({}, step, rule)
    assert run_step({}, same, COMMON)["x"] == 5
    with pytest.raises(AccessError):
        run_step({}, diff, COMMON)
    rng = random.Random(2)
    for _ in range(20):
        assert run_step({}, diff, ARBITRARY, choose=rng.choice)["x"] in (4, 9, 6)
    assert run_step({}, diff, PRIORITY)["x"] == 4
    assert run_step({}, diff, COMBINING, combine=lambda a, b: a + b)["x"] == 19
    assert run_step({}, diff, COMBINING, combine=max)["x"] == 9


def random_step(rng, k, cells=4):
    step = {}
    for pid in rng.sample(range(3 * k), k):
        reads = tuple(rng.randrange(cells) for _ in range(rng.randint(0, 2)))
        target = rng.randrange(cells) if rng.random() < 0.7 else None
        c = rng.randint(0, 2)
        step[pid] = (reads, lambda x, t=target, c=c: [] if t is None else [(t, (sum(x) + c) % 3)])
    return step


def legal(mem, step, rule, **kw):
    try:
        return run_step(mem, step, rule, **kw)
    except AccessError:
        return None


def test_order_of_power():
    # A step that is legal under EREW, CREW or common is legal under each later rule, with the
    # same result. Under arbitrary the result depends on the choice, and priority is one choice.
    rng = random.Random(3)
    seen = [0] * len(ORDER)
    for _ in range(3000):
        mem = {a: rng.randint(0, 2) for a in range(4)}
        step = random_step(rng, rng.randint(1, 4))
        for i, rule in enumerate(ORDER):
            res = legal(mem, step, rule, choose=rng.choice)
            if res is not None:
                seen[i] += 1
                if rule == ARBITRARY:
                    assert legal(mem, step, PRIORITY) == legal(mem, step, ARBITRARY, choose=min)
                else:
                    for later in ORDER[i + 1:]:
                        assert legal(mem, step, later, choose=rng.choice) == res
                break
    # each of the first four rules was the weakest legal one for some step; arbitrary never fails
    assert all(s > 0 for s in seen[:4]) and seen[4] == 0


def test_priority_is_combining_with_keep_first():
    rng = random.Random(4)
    for _ in range(500):
        mem = {a: rng.randint(0, 2) for a in range(4)}
        step = random_step(rng, rng.randint(1, 6))
        assert run_step(mem, step, PRIORITY) == run_step(mem, step, COMBINING, combine=lambda a, b: a)


def test_access_sets():
    step = {0: ((1, 2), lambda x: [(3, 0)]), 1: ((2,), lambda x: [(3, 1)])}
    readers, writers, writes = access_sets(step, {})
    assert readers == {1: {0}, 2: {0, 1}}
    assert writers == {3: {0, 1}}
    assert writes == {3: [(0, 0), (1, 1)]}


def test_brent_principle():
    rng = random.Random(5)
    for _ in range(300):
        works = [rng.randint(1, 40) for _ in range(rng.randint(1, 12))]
        w, t = sum(works), len(works)
        for p in (1, 2, 3, 5, 8, 64):
            assert math.ceil(w / p) <= brent_time(works, p) <= w // p + t
            assert max(math.ceil(w / p), t) <= brent_time(works, p)


def test_fewer_processors_give_the_same_step():
    rng = random.Random(6)
    for _ in range(1000):
        mem = {a: rng.randint(0, 2) for a in range(4)}
        step = random_step(rng, rng.randint(1, 7))
        for rule in (CREW, COMMON, PRIORITY):
            full = legal(mem, step, rule)
            if full is None:
                continue
            for p in (1, 2, 3):
                new, rounds = run_step_on_p(mem, step, rule, p)
                assert new == full
                assert rounds == math.ceil(len(step) / p)
