# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-locking-protocol/. The authors are listed in prov/AV253P.jsonl.

import random

import pytest

import dbsched
import tree_locking_protocol as tlp

#         a
#       /   \
#      b     c
#     / \   / \
#    d   e f   g
TREE = {"a": None, "b": "a", "c": "a", "d": "b", "e": "b", "f": "c", "g": "c"}


def test_rules_are_enforced() -> None:
    mgr = tlp.TreeLockManager(TREE)
    assert mgr.lock(1, "b")  # the first lock may be on any node
    with pytest.raises(ValueError):
        mgr.lock(1, "f")  # T1 does not hold c
    with pytest.raises(ValueError):
        mgr.lock(1, "a")  # the parent of b is above, not held
    assert mgr.lock(1, "d")
    mgr.unlock(1, "d")
    with pytest.raises(ValueError):
        mgr.lock(1, "d")  # no lock again after an unlock
    with pytest.raises(ValueError):
        mgr.unlock(1, "d")
    assert mgr.lock(2, "d") and not mgr.lock(3, "d")
    assert mgr.waits_for() == {(3, 2)}


def test_plan() -> None:
    assert tlp.plan(TREE, 1, [("w", "d"), ("w", "e")]) == [
        ("lock", "b"), ("lock", "d"), ("w", 1, "d"), ("unlock", "d"),
        ("lock", "e"), ("unlock", "b"), ("w", 1, "e"), ("unlock", "e"), ("c", 1, None)]
    assert tlp.plan(TREE, 2, [("r", "b"), ("r", "d")]) == [
        ("lock", "b"), ("r", 2, "b"), ("lock", "d"), ("unlock", "b"),
        ("r", 2, "d"), ("unlock", "d"), ("c", 2, None)]
    assert tlp.plan(TREE, 3, [("r", "f")])[0] == ("lock", "f")


def test_example() -> None:
    plans = {1: tlp.plan(TREE, 1, [("w", "d"), ("w", "e")]),
             2: tlp.plan(TREE, 2, [("r", "b"), ("r", "d")])}
    arrival = [1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1]
    out, log = tlp.run(TREE, plans, arrival, check_state)
    assert dbsched.format(out) == "w1(d) r2(b) r2(d) c2 w1(e) c1"
    assert dbsched.conflict_serializable_orders(out) == [(1, 2)]
    assert not dbsched.is_recoverable(out)  # T2 read d from T1 and committed first
    assert ("unlock", 1, "d") in log and log.index(("unlock", 1, "d")) < log.index(("lock", 1, "e"))


def test_a_schedule_that_two_phase_locking_cannot_give() -> None:
    plans = {1: tlp.plan(TREE, 1, [("w", "d"), ("w", "e")]),
             2: tlp.plan(TREE, 2, [("w", "d")]),
             3: tlp.plan(TREE, 3, [("w", "e")])}
    arrival = [1, 1, 1, 1] + [2] * 4 + [3] * 4 + [1] * 5
    out, _ = tlp.run(TREE, plans, arrival, check_state)
    # Under 2PL, T1 would hold e from before w2(d) until w1(e), so w3(e) could not run.
    assert dbsched.format(out) == "w1(d) w2(d) c2 w3(e) c3 w1(e) c1"
    assert dbsched.conflict_serializable_orders(out) == [(3, 1, 2)]


def check_state(mgr):
    for t, done in mgr.locked.items():
        # The nodes that t has locked form a subtree: all but one have their parent in it.
        assert sum(1 for v in done if mgr.parent[v] not in done) == 1
        assert mgr.held(t) <= done
    for t, x in mgr.waiting.items():
        # A waiter holds the parent of the node it waits for, unless it holds nothing.
        assert mgr.holder.get(x) != t
        assert not mgr.locked.get(t) or mgr.holder.get(mgr.parent[x]) == t


def lock_order_edges(log):
    """(T, U) when T and U lock a common node and T locks it first."""
    first = {}
    for kind, t, v in log:
        if kind == "lock":
            first.setdefault(v, []).append(t)
    return {(ts[i], ts[j]) for ts in first.values()
            for i in range(len(ts)) for j in range(i + 1, len(ts))}


def topological_order(nodes, edges):
    indeg = {v: 0 for v in nodes}
    for _, b in edges:
        indeg[b] += 1
    ready = sorted(v for v in nodes if indeg[v] == 0)
    order = []
    while ready:
        v = ready.pop(0)
        order.append(v)
        for a, b in sorted(edges):
            if a == v:
                indeg[b] -= 1
                if indeg[b] == 0:
                    ready.append(b)
    return order if len(order) == len(nodes) else None


def check_output(out, log, plans, brute_force):
    rho = lock_order_edges(log)
    order = topological_order(sorted(plans), rho)
    assert order is not None  # Theorem 1: the lock order relation has no cycle
    for i in range(len(out)):
        for j in range(i + 1, len(out)):
            if dbsched.conflicts(out[i], out[j]):
                assert (out[i][1], out[j][1]) in rho
    assert dbsched.conflict_equivalent(out, dbsched.serial_schedule(out, order))
    if brute_force:
        assert tuple(order) in dbsched.conflict_serializable_orders(out)
    assert dbsched.committed(out) == set(plans)


def unlock_then_lock(log):
    """True if some transaction locks a node after it unlocked another one."""
    unlocked = set()
    for kind, t, _ in log:
        if kind == "unlock":
            unlocked.add(t)
        elif t in unlocked:
            return True
    return False


PAIRS = [
    {1: [("w", "d"), ("w", "e")], 2: [("r", "b"), ("r", "d")]},
    {1: [("w", "b"), ("w", "d")], 2: [("w", "d")]},
]


@pytest.mark.parametrize("programs", PAIRS)
def test_all_interleavings_of_two(programs) -> None:
    plans = {t: tlp.plan(TREE, t, acc) for t, acc in programs.items()}
    seqs = [[("r", t, "x")] * len(plans[t]) for t in sorted(plans)]
    orders = set()
    for arrival in dbsched.interleavings(seqs):
        out, log = tlp.run(TREE, plans, [a[1] for a in arrival], check_state)
        check_output(out, log, plans, brute_force=True)
        orders.add(tuple(topological_order(sorted(plans), lock_order_edges(log))))
    assert orders == {(1, 2), (2, 1)}


def test_opposite_orders_do_not_deadlock() -> None:
    # Under 2PL, w(d) w(e) against w(e) w(d) can deadlock. Here both start at b.
    plans = {1: tlp.plan(TREE, 1, [("w", "d"), ("w", "e")]),
             2: tlp.plan(TREE, 2, [("w", "e"), ("w", "d")])}
    seqs = [[("r", t, "x")] * len(plans[t]) for t in sorted(plans)]
    rng = random.Random(2)
    for _ in range(3000):
        arrival = [a[1] for a in dbsched.random_schedule(rng, seqs)]
        out, log = tlp.run(TREE, plans, arrival, check_state)
        check_output(out, log, plans, brute_force=True)


def heap_tree(n):
    return {"n%d" % i: ("n%d" % (i // 2) if i > 1 else None) for i in range(1, n + 1)}


def test_random_interleavings_of_up_to_six() -> None:
    rng = random.Random(7)
    tree = heap_tree(15)
    nodes = sorted(tree)
    early, unrecoverable = 0, 0
    for n in [3] * 400 + [6] * 300:
        programs = {t: [(rng.choice("rw"), rng.choice(nodes)) for _ in range(rng.randint(1, 3))]
                    for t in range(1, n + 1)}
        plans = {t: tlp.plan(tree, t, acc) for t, acc in programs.items()}
        arrival = [t for t in plans for _ in plans[t]]
        rng.shuffle(arrival)
        out, log = tlp.run(tree, plans, arrival, check_state)  # never a deadlock
        check_output(out, log, plans, brute_force=(n <= 3))
        early += unlock_then_lock(log)
        unrecoverable += not dbsched.is_recoverable(out)
    assert early > 0 and unrecoverable > 0  # not two-phase, and not recoverable
