# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-granularity-locking/. The authors are listed in prov/ZVVV9H.jsonl.

import itertools
import random

import pytest

import dbsched
import multiple_granularity_locking as mgl
from multiple_granularity_locking import IS, IX, MODES, S, SIX, X


def make_tree(rows_per_table=2, tables="AB"):
    parent = {"db": None}
    for t in tables:
        parent[t] = "db"
        for r in range(1, rows_per_table + 1):
            parent["%s%d" % (t, r)] = t
    return mgl.Hierarchy(parent)


# What each mode says: (access to the whole subtree, access that it announces below).
MEANING = {IS: (None, "r"), IX: (None, "w"), S: ("r", None), SIX: ("r", "w"), X: ("w", None)}


def _clash(a, b):
    return a is not None and b is not None and (a == "w" or b == "w")


def test_matrix_follows_from_the_meaning_of_the_modes() -> None:
    for a, b in itertools.product(MODES, repeat=2):
        (ea, ia), (eb, ib) = MEANING[a], MEANING[b]
        # Two modes clash if their subtree accesses clash, or if a subtree access
        # of one clashes with an access that the other announces below.
        clash = _clash(ea, eb) or _clash(ea, ib) or _clash(ia, eb)
        assert mgl.COMPAT[a][b] == (not clash), (a, b)
        assert mgl.COMPAT[a][b] == mgl.COMPAT[b][a]


def test_sup_is_the_least_upper_bound() -> None:
    # m is at least as strong as n when every mode compatible with m is compatible with n.
    def ok_with(m):
        return {k for k in MODES if mgl.COMPAT[m][k]}

    def geq(m, n):
        return ok_with(m) <= ok_with(n)

    for a, b in itertools.product(MODES, repeat=2):
        u = mgl.sup(a, b)
        assert geq(u, a) and geq(u, b)
        assert all(geq(m, u) for m in MODES if geq(m, a) and geq(m, b))
        for m in MODES:  # one sup test replaces two compatibility tests
            assert mgl.COMPAT[u][m] == (mgl.COMPAT[a][m] and mgl.COMPAT[b][m])
    assert mgl.sup(IX, S) == SIX


def test_rules_are_enforced() -> None:
    tree = make_tree()
    mgr = mgl.MGLLockManager(tree)
    with pytest.raises(ValueError):
        mgr.lock(1, "A1", S)  # no intention lock on A
    assert mgr.lock(1, "db", IS) and mgr.lock(1, "A", IS)
    with pytest.raises(ValueError):
        mgr.lock(1, "A1", X)  # X needs IX on the parent
    assert mgr.lock(1, "A1", S)
    with pytest.raises(ValueError):
        mgr.unlock(1, "A")  # the child A1 is still locked
    mgr.release_all(1)
    assert mgr.locks == {}


def test_coarse_and_fine_locks() -> None:
    tree = make_tree()
    mgr = mgl.MGLLockManager(tree)
    # T1 updates table A: IX on db, SIX on A, then X on row A1.
    assert mgr.lock(1, "db", IX) and mgr.lock(1, "A", SIX) and mgr.lock(1, "A1", X)
    # T2 reads row A2: IS on A is compatible with SIX.
    assert mgr.lock(2, "db", IS) and mgr.lock(2, "A", IS) and mgr.lock(2, "A2", S)
    # T3 scans table A: S on A is not compatible with SIX.
    assert mgr.lock(3, "db", IS) and not mgr.lock(3, "A", S)
    # T4 writes row B1: no conflict on table B.
    assert mgr.lock(4, "db", IX) and mgr.lock(4, "B", IX) and mgr.lock(4, "B1", X)
    assert mgr.waits_for() == {(3, 1)}
    # T2 now wants to write A2: IX on A conflicts with SIX.
    assert mgr.lock(2, "db", IX) and not mgr.lock(2, "A", IX)
    assert mgr.waits_for() == {(3, 1), (2, 1)}
    mgr.release_all(1)
    assert mgr.lock(2, "A", IX) and not mgr.lock(3, "A", S)
    assert mgr.covers(4, "B1", "w") and not mgr.covers(4, "B2", "r")


def check_state(mgr):
    tree = mgr.tree
    holders = {t for h in mgr.locks.values() for t in h}
    # The parent rule holds for every lock at every moment.
    for node, h in mgr.locks.items():
        p = tree.parent[node]
        for t, m in h.items():
            assert p is None or mgl.at_least(mgr.mode(t, p), mgl.PARENT_NEEDS[m])
    # The oracle: the implicit locks on the leaves never conflict.
    for leaf in tree.leaves("db"):
        for t, u in itertools.permutations(sorted(holders), 2):
            if mgr.covers(t, leaf, "w"):
                assert not mgr.covers(u, leaf, "r"), (leaf, t, u)


def _plans(tree, programs):
    return {t: mgl.plan(tree, t, ops) for t, ops in programs.items()}


def _check_output(out, plans, brute_force):
    assert dbsched.is_strict(out)
    cp = dbsched.committed_projection(out)
    commit_order = [a[1] for a in out if a[0] == "c"]
    assert dbsched.conflict_equivalent(cp, dbsched.serial_schedule(cp, commit_order))
    if brute_force:
        assert tuple(commit_order) in dbsched.conflict_serializable_orders(out)
    ended = {a[1] for a in out if a[0] in "ca"}
    assert ended == set(plans)


PAIRS = [
    (2, {1: [("scan", "A")], 2: [("write", "A1")]}),
    (2, {1: [("update", "A", ["A1"])], 2: [("read", "A2")]}),
    (1, {1: [("rewrite", "A"), ("rewrite", "B")], 2: [("rewrite", "B"), ("rewrite", "A")]}),
    (1, {1: [("read", "A1"), ("write", "A1")], 2: [("read", "A1")]}),
]


@pytest.mark.parametrize("rows,programs", PAIRS)
def test_all_interleavings_of_two(rows, programs) -> None:
    tree = make_tree(rows)
    plans = _plans(tree, programs)
    seqs = [[t] * len(plans[t]) for t in sorted(plans)]
    aborts = 0
    for arrival in dbsched.interleavings([[("r", t, "x")] * len(s) for t, s in zip(sorted(plans), seqs)]):
        out = mgl.run(tree, plans, [a[1] for a in arrival], check_state)
        _check_output(out, plans, brute_force=True)
        aborts += any(a[0] == "a" for a in out)
    if programs[1][0][0] == "rewrite":
        assert aborts > 0  # the opposite order of tables gives deadlocks


def test_random_interleavings_of_up_to_six() -> None:
    rng = random.Random(3)
    tree = make_tree(2, "ABC")
    rows = [v for v in tree.parent if len(v) == 2]
    tables = ["A", "B", "C"]
    deadlocks = 0
    for n in [3] * 150 + [6] * 100:
        programs = {}
        for t in range(1, n + 1):
            ops = []
            for _ in range(rng.randint(1, 2)):
                kind = rng.choice(["read", "read", "write", "write", "scan", "update", "rewrite"])
                if kind in ("read", "write"):
                    ops.append((kind, rng.choice(rows)))
                elif kind == "update":
                    tab = rng.choice(tables)
                    ops.append((kind, tab, [tab + rng.choice("12")]))
                else:
                    ops.append((kind, rng.choice(tables)))
            programs[t] = ops
        plans = _plans(tree, programs)
        arrival = [t for t in plans for _ in plans[t]]
        rng.shuffle(arrival)
        out = mgl.run(tree, plans, arrival, check_state)
        _check_output(out, plans, brute_force=(n <= 3))
        deadlocks += any(a[0] == "a" for a in out)
    assert deadlocks > 0
