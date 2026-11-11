# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-ordering/. The authors are listed in prov/QFVDF2.jsonl.
import random

import pytest

from lock_ordering import Levels, LockOrderValidator, build_parent_child, build_transfers
from procsim import Sim, explore


def has_cycle(g):
    state = {}

    def visit(v):
        state[v] = 1
        for w in g.get(v, ()):
            if state.get(w) == 1 or (w not in state and visit(w)):
                return True
        state[v] = 2
        return False

    return any(v not in state and visit(v) for v in list(g))


def acyclic(sim):
    return "cycle" if has_cycle(sim.waits_for()) else None


def test_transfers_in_opposite_directions():
    bad = explore(lambda: build_transfers(ordered=False))
    assert bad.deadlocks and not bad.truncated
    good = explore(lambda: build_transfers(ordered=True), invariant=acyclic)
    assert good.deadlocks == [] and good.violations == [] and good.finals == 1 and not good.truncated


def test_ordered_runs_keep_the_money():
    res = explore(lambda: build_transfers(ordered=True),
                  invariant=lambda s: None if sum(s.v["bal"]) == 15 else "money lost")
    assert res.violations == []


def test_parent_child_with_trylock():
    assert explore(lambda: build_parent_child(fixed=False)).deadlocks
    res = explore(lambda: build_parent_child(fixed=True), invariant=acyclic)
    assert res.deadlocks == [] and res.violations == [] and res.finals == 1


def ranked(sim, me, locks):
    for m in locks:
        yield ("lock", m)
    for m in reversed(locks):
        yield ("unlock", m)


def test_any_programs_that_follow_the_order_never_deadlock():
    rng = random.Random(31)
    names = ["L0", "L1", "L2", "L3"]
    for _ in range(25):
        programs = {p: sorted(rng.sample(names, rng.randint(1, 3))) for p in "pqr"}

        def build(programs=programs):
            s = Sim()
            for m in names:
                s.mutex(m)
            for p, locks in programs.items():
                s.spawn(p, ranked, locks)
            return s

        res = explore(build, invariant=acyclic)
        assert res.deadlocks == [] and res.violations == [] and not res.truncated
        assert res.finals == 1


def test_validator_flags_an_inversion_in_a_run_that_did_not_deadlock():
    v = LockOrderValidator()
    v.acquire("p", "A")
    assert v.acquire("p", "B") is None
    v.release("p", "B")
    v.release("p", "A")
    v.acquire("q", "B")
    assert v.acquire("q", "A") == ("B", "A")
    # a longer cycle, A before B before C, then C before A
    w = LockOrderValidator()
    for a, b in [("A", "B"), ("B", "C")]:
        w.acquire("t", a)
        assert w.acquire("t", b) is None
        w.release("t", b)
        w.release("t", a)
    w.acquire("u", "C")
    assert w.acquire("u", "A") == ("C", "A")


def test_validator_is_quiet_on_ordered_traces():
    rng = random.Random(32)
    for _ in range(200):
        v = LockOrderValidator()
        for _ in range(10):
            locks = sorted(rng.sample(range(8), rng.randint(1, 4)))
            p = rng.choice("pqr")
            for m in locks:
                assert v.acquire(p, str(m).zfill(2)) is None
            for m in reversed(locks):
                v.release(p, str(m).zfill(2))
        assert v.reports == []


def test_levels():
    lv = Levels({"bucket": 1, "entry": 2, "stats": 3})
    lv.acquire("p", "bucket")
    lv.acquire("p", "entry")
    lv.release("p", "entry")
    lv.acquire("p", "stats")
    with pytest.raises(RuntimeError):
        lv.acquire("p", "entry")
