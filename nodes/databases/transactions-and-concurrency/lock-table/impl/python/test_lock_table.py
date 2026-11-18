# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-table/. The authors are listed in prov/J4XAN4.jsonl.

import random

import pytest

import dbsched
from lock_table import COMPAT_SX, S, X, LockTable, find_cycle


def check_invariants(lt):
    for item, entry in lt.table.items():
        modes = list(entry.granted.items())
        for a in range(len(modes)):
            for b in range(a + 1, len(modes)):
                assert COMPAT_SX[modes[a][1]][modes[b][1]], (item, modes)
        if entry.queue:
            # No lost wake-up: the head of the queue cannot be granted now.
            head = entry.queue[0]
            others = [m for t, m in entry.granted.items() if t != head.txn]
            assert any(not COMPAT_SX[m][head.mode] for m in others)
        for r in entry.queue:
            assert lt.waiting[r.txn] == item
    assert sum(len(e.queue) for e in lt.table.values()) == len(lt.waiting)


def run_strict_2pl(txns, arrival):
    """Strict 2PL on top of the lock table. arrival is the order in which the
    transactions offer their next action; a blocked transaction keeps its place.
    A deadlock aborts the largest transaction id on a cycle of the wait-for graph."""
    progs = {}
    for text in txns:
        acts = dbsched.parse(text)
        progs[acts[0][1]] = list(acts)
    lt = LockTable()
    out, pos, blocked = [], {t: 0 for t in progs}, set()
    pending = list(arrival)
    while pending:
        k = next((k for k, t in enumerate(pending) if t not in blocked), None)
        if k is None:
            cycle = find_cycle(lt.waits_for())
            assert cycle is not None, "every transaction waits but there is no cycle"
            assert all(t in blocked for t in cycle)
            victim = max(cycle)
            out.append(("a", victim, None))
            grants = lt.release_all(victim)
            blocked.discard(victim)
            pending = [t for t in pending if t != victim]
        else:
            t = pending[k]
            kind, _, item = progs[t][pos[t]]
            grants = []
            if kind in "rw":
                if not lt.request(t, item, S if kind == "r" else X):
                    blocked.add(t)
                    check_invariants(lt)
                    continue
            out.append(progs[t][pos[t]])
            pos[t] += 1
            pending.pop(k)
            if kind in "ca":
                grants = lt.release_all(t)
        for g in grants:
            blocked.discard(g[0])
        check_invariants(lt)
        for cycle_txn in blocked:
            assert cycle_txn in lt.waiting
    assert not lt.table and not lt.waiting
    return tuple(out)


def test_example():
    lt = LockTable()
    assert lt.request(1, "x", S) and lt.request(2, "x", S)
    assert not lt.request(3, "x", X)  # waits behind two readers
    assert not lt.request(4, "x", S)  # FIFO: does not pass the writer
    assert lt.queue("x") == [(3, X), (4, S)]
    assert not lt.request(1, "x", X)  # conversion goes to the front
    assert lt.queue("x") == [(1, X), (3, X), (4, S)]
    assert lt.waits_for() == {(1, 2), (3, 1), (3, 2), (4, 1), (4, 3)}
    assert lt.release(2, "x") == [(1, "x", X)]
    assert lt.holders("x") == {1: X}
    assert lt.release(1, "x") == [(3, "x", X)]
    assert lt.release(3, "x") == [(4, "x", S)]
    check_invariants(lt)


def test_upgrade_and_reentry():
    lt = LockTable()
    assert lt.request(1, "x", S)
    assert lt.request(1, "x", S)  # already held
    assert lt.request(1, "x", X)  # sole holder upgrades at once
    assert lt.request(1, "x", S)  # X covers S
    assert lt.mode(1, "x") == X
    with pytest.raises(ValueError):
        lt.release(2, "x")


def test_upgrade_deadlock_is_a_cycle():
    lt = LockTable()
    assert lt.request(1, "x", S) and lt.request(2, "x", S)
    assert not lt.request(1, "x", X)
    assert not lt.request(2, "x", X)
    assert sorted(find_cycle(lt.waits_for())) == [1, 2]
    with pytest.raises(ValueError):
        lt.request(1, "y", S)  # a waiting transaction cannot ask again
    assert lt.release_all(2) == [(1, "x", X)]
    assert find_cycle(lt.waits_for()) is None


def test_cancel_wakes_followers():
    lt = LockTable()
    assert lt.request(1, "x", X)
    assert not lt.request(2, "x", X)
    assert not lt.request(3, "x", S)
    assert lt.release_all(1) == [(2, "x", X)]
    assert lt.cancel(2) == []  # 2 holds now; nothing waits for it to cancel
    assert lt.release_all(2) == [(3, "x", S)]


SETS = [
    ["r1(x) w1(x) c1", "r2(x) w2(x) c2"],
    ["r1(x) w1(y) c1", "r2(y) w2(x) c2", "r3(x) r3(y) c3"],
    ["w1(x) w1(y) c1", "r2(y) r2(x) c2", "w3(x) a3"],
]


@pytest.mark.parametrize("txns", SETS)
def test_strict_2pl_on_all_interleavings(txns):
    outcomes = set()
    for s in dbsched.interleavings(txns):
        out = run_strict_2pl(txns, [a[1] for a in s])
        assert dbsched.is_conflict_serializable(out)
        assert dbsched.is_strict(out)
        outcomes.add(out)
    assert len(outcomes) > 1


def test_strict_2pl_on_random_interleavings():
    rng = random.Random(11)
    items = "xyz"
    for n in [4] * 40 + [6] * 15:
        txns = []
        for t in range(1, n + 1):
            acts = ["%s%d(%s)" % (rng.choice("rw"), t, rng.choice(items)) for _ in range(rng.randint(1, 3))]
            txns.append(" ".join(acts + ["c%d" % t]))
        s = dbsched.random_schedule(rng, txns)
        out = run_strict_2pl(txns, [a[1] for a in s])
        assert dbsched.is_conflict_serializable(out)
        assert dbsched.is_strict(out)
