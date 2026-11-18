# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conservative-two-phase-locking/. The authors are listed in prov/CS6AB2.jsonl.

import itertools
import random

import pytest

import conservative_two_phase_locking as c2pl
import dbsched


# Tests of the shared helper dbsched.py.


def test_helper_self_test() -> None:
    assert dbsched._self_test()


def test_helper_parse_format_round_trip() -> None:
    text = "r1(x) w2(y) a2 w1(x) c1"
    s = dbsched.parse(text)
    assert s == (("r", 1, "x"), ("w", 2, "y"), ("a", 2, None), ("w", 1, "x"), ("c", 1, None))
    assert dbsched.format(s) == text
    for bad in ("r1", "c1(x)", "q1(x)", "c1 r1(x)", "c1 a1"):
        with pytest.raises(ValueError):
            dbsched.parse(bad)


def test_helper_conflicts() -> None:
    assert dbsched.conflicts(("r", 1, "x"), ("w", 2, "x"))
    assert dbsched.conflicts(("w", 1, "x"), ("w", 2, "x"))
    assert not dbsched.conflicts(("r", 1, "x"), ("r", 2, "x"))
    assert not dbsched.conflicts(("w", 1, "x"), ("w", 1, "x"))
    assert not dbsched.conflicts(("w", 1, "x"), ("w", 2, "y"))
    assert not dbsched.conflicts(("c", 1, None), ("w", 2, "x"))


def test_helper_standard_examples() -> None:
    # Two serial orders when T3 is independent of T2 and T1 is after T2.
    s = dbsched.parse("r1(x) r2(y) r3(z) w1(y) c1 c2 c3")
    assert dbsched.conflict_serializable_orders(s) == [(2, 1, 3), (2, 3, 1), (3, 2, 1)]
    # A read between two writes of the same transaction is not serializable.
    s = dbsched.parse("w1(x) r2(x) w1(x) c1 c2")
    assert not dbsched.is_view_serializable(s)
    # Aborted transactions drop out of the committed projection.
    s = dbsched.parse("r1(x) r2(x) w1(x) w2(x) a2 c1")
    assert dbsched.is_conflict_serializable(s)
    assert not dbsched.is_recoverable(dbsched.parse("w1(x) r2(x) c2 a1"))


def _graph_orders(s):
    """Independent oracle: the topological orders of the conflict graph."""
    cp = dbsched.committed_projection(s)
    txns = sorted(dbsched.committed(cp))
    edges = {(p[1], q[1]) for i, p in enumerate(cp) for q in cp[i + 1:] if dbsched.conflicts(p, q)}
    return [o for o in itertools.permutations(txns) if all(o.index(a) < o.index(b) for a, b in edges)]


def test_helper_classes_on_all_interleavings() -> None:
    txns = ["r1(x) w1(y) c1", "r2(y) w2(x) c2", "w3(x) a3"]
    seen = set()
    for s in dbsched.interleavings(txns):
        seen.add(s)
        st = dbsched.is_strict(s)
        aca = dbsched.avoids_cascading_aborts(s)
        rc = dbsched.is_recoverable(s)
        assert (not st or aca) and (not aca or rc)
        csr = dbsched.is_conflict_serializable(s)
        assert not csr or dbsched.is_view_serializable(s)
        assert dbsched.conflict_serializable_orders(s) == _graph_orders(s)
    assert len(seen) == 560  # 8! / (3! 3! 2!)


def test_helper_random_schedule_is_uniform_enough() -> None:
    rng = random.Random(7)
    txns = ["r1(x) w1(x)", "w2(x) c2"]
    counts = {}
    for _ in range(3000):
        s = dbsched.random_schedule(rng, txns)
        counts[s] = counts.get(s, 0) + 1
    assert set(counts) == set(dbsched.interleavings(txns))
    assert min(counts.values()) > 400  # 6 interleavings, 500 expected each


def test_helper_limit() -> None:
    s = dbsched.parse(" ".join("w%d(x) c%d" % (i, i) for i in range(1, 8)))
    with pytest.raises(ValueError):
        dbsched.is_conflict_serializable(s)


# Tests of conservative two-phase locking.


def _acyclic(edges):
    succ = {}
    for a, b in edges:
        succ.setdefault(a, set()).add(b)
    state = {}

    def visit(v):
        state[v] = 1
        for w in succ.get(v, ()):
            if state.get(w) == 1 or (w not in state and not visit(w)):
                return False
        state[v] = 2
        return True

    return all(v in state or visit(v) for v in list(succ))


def _check_state(sched):
    # Safety: conflicting locks of different transactions are never held together.
    for item, holders in sched.locks.items():
        modes = list(holders.values())
        assert all(not c2pl.conflict(a, b) for i, a in enumerate(modes) for b in modes[i + 1:]), item
    # A waiting transaction holds nothing, so the wait-for graph has no cycle.
    for t in sched.wait:
        assert not sched.held.get(t)
    edges = sched.waits_for()
    assert _acyclic(edges)
    assert all(u not in sched.wait or sched.wait.index(u) < sched.wait.index(t) for t, u in edges)


def _run(txns, arrival, strict=True):
    progs = [dbsched.parse(t) for t in txns]
    out, lps = c2pl.run(progs, arrival, strict, _check_state)
    assert sorted(dbsched.transactions(out)) == sorted(p[0][1] for p in progs)
    assert len(out) == sum(len(p) for p in progs)  # every transaction finishes
    return out, lps


def _lock_point_order_is_serial(out, lps):
    done = dbsched.committed(out)
    order = tuple(t for t in lps if t in done)
    cp = dbsched.committed_projection(out)
    assert dbsched.conflict_equivalent(cp, dbsched.serial_schedule(cp, order))


def test_the_deadlock_of_basic_2pl_does_not_happen() -> None:
    # Under basic 2PL this arrival order deadlocks (see the two-phase-locking page).
    txns = ["r1(x) w1(y) c1", "r2(y) w2(x) c2"]
    out, lps = _run(txns, [1, 2, 1, 2, 1, 2])
    assert dbsched.format(out) == "r1(x) w1(y) c1 r2(y) w2(x) c2"
    assert lps == (1, 2)


def test_all_or_nothing_and_fifo() -> None:
    sched = c2pl.ConservativeScheduler()
    assert sched.begin(1, dbsched.parse("r1(x) c1"))
    assert not sched.begin(2, dbsched.parse("r2(y) w2(x) c2"))
    assert sched.held.get(2) is None and "y" not in sched.locks  # nothing is held
    # S on x fits the holder T1, but T3 must not pass the earlier waiter T2.
    assert not sched.begin(3, dbsched.parse("r3(x) c3"))
    assert sched.waits_for() == {(2, 1), (3, 2)}
    # T4 conflicts with nobody and is admitted at once.
    assert sched.begin(4, dbsched.parse("w4(z) c4"))
    assert sched.end(1) == [2]
    assert sched.end(2) == [3]
    assert sched.lock_points == [1, 4, 2, 3]
    with pytest.raises(ValueError):
        sched.access(4, "r", "x")


SETS = [
    ["r1(x) w1(y) c1", "r2(y) w2(x) c2"],
    ["r1(x) w1(x) c1", "r2(x) w2(x) c2", "r3(y) c3"],
    ["r1(x) w1(y) c1", "r2(y) w2(z) c2", "r3(z) w3(x) c3"],
    ["w1(x) r1(y) c1", "r2(x) c2", "w3(y) a3"],
]


@pytest.mark.parametrize("txns", SETS)
def test_strict_on_all_interleavings(txns) -> None:
    for s in dbsched.interleavings(txns):
        out, lps = _run(txns, [a[1] for a in s], strict=True)
        _lock_point_order_is_serial(out, lps)
        assert dbsched.is_strict(out)


@pytest.mark.parametrize("txns", SETS)
def test_early_release_on_all_interleavings(txns) -> None:
    for s in dbsched.interleavings(txns):
        out, lps = _run(txns, [a[1] for a in s], strict=False)
        _lock_point_order_is_serial(out, lps)


def test_early_release_can_give_a_schedule_that_is_not_recoverable() -> None:
    txns = ["w1(x) r1(y) c1", "r2(x) c2"]
    out, _ = _run(txns, [1, 2, 2, 1, 1], strict=False)
    assert dbsched.format(out) == "w1(x) r2(x) c2 r1(y) c1"
    assert dbsched.is_conflict_serializable(out) and not dbsched.is_recoverable(out)
    out, _ = _run(txns, [1, 2, 2, 1, 1], strict=True)
    assert dbsched.format(out) == "w1(x) r1(y) c1 r2(x) c2"


def test_random_interleavings_of_up_to_six() -> None:
    rng = random.Random(5)
    for n in [4] * 30 + [6] * 20:
        txns = []
        for t in range(1, n + 1):
            acts = ["%s%d(%s)" % (rng.choice("rw"), t, rng.choice("xyzu")) for _ in range(rng.randint(1, 3))]
            txns.append(" ".join(acts + ["c%d" % t]))
        arrival = [a[1] for a in dbsched.random_schedule(rng, txns)]
        for strict in (True, False):
            out, lps = _run(txns, arrival, strict)
            _lock_point_order_is_serial(out, lps)
            if strict:
                assert dbsched.is_strict(out)
