# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transaction-chopping/. The authors are listed in prov/G7FCSD.jsonl.

import itertools
import random

import dbsched
from transaction_chopping import (
    ROLLBACK, conflict, finest_chopping, has_sc_cycle, is_correct,
    is_rollback_safe, parse_txn, private_chopping,
)

ITEMS = "xyz"


def gen(rng, n, m):
    out = []
    for _ in range(n):
        t = [(rng.choice("rw"), rng.choice(ITEMS)) for _ in range(rng.randint(1, m))]
        if rng.random() < 0.2:
            t.insert(rng.randrange(len(t) + 1), (ROLLBACK,))
        out.append(t)
    return out


def all_choppings(t):
    n = len(t)
    out = []
    for mask in range(1 << (n - 1)):
        b = [0] + [p + 1 for p in range(n - 1) if mask >> p & 1] + [n]
        out.append([(b[k], b[k + 1]) for k in range(len(b) - 1)])
    return out


def coarser(c, f):
    """Every cut of c is a cut of f, so each piece of c is a union of pieces of f."""
    return {b for _, b in c} <= {b for _, b in f}


def sc_cycle_brute(txns, chop):
    """Search every simple cycle of the chopping graph for one with an S edge
    and a C edge."""
    nodes = [(i, k) for i, c in enumerate(chop) for k in range(len(c))]

    def label(u, v):
        if u[0] == v[0]:
            return "S"
        a, b = chop[u[0]][u[1]], chop[v[0]][v[1]]
        if any(conflict(p, q) for p in txns[u[0]][a[0]:a[1]]
               for q in txns[v[0]][b[0]:b[1]]):
            return "C"
        return None

    adj = {u: [(v, label(u, v)) for v in nodes if v != u and label(u, v)] for u in nodes}

    def dfs(start, u, seen, kinds):
        for v, lab in adj[u]:
            if v == start and len(seen) >= 3 and kinds | {lab} == {"S", "C"}:
                return True
            if v not in seen and v > start:
                seen.add(v)
                if dfs(start, v, seen, kinds | {lab}):
                    return True
                seen.discard(v)
        return False

    return any(dfs(s, s, {s}, frozenset()) for s in nodes)


def executions(txns, chop):
    """Every execution that runs each piece as one atomic step, the pieces of a
    transaction in their order, as a dbsched schedule with the commit of a
    transaction after its last piece."""
    seqs = [[(i, k) for k in range(len(c))] for i, c in enumerate(chop)]
    for order in dbsched.interleavings(seqs):
        s = []
        for i, k in order:
            a, b = chop[i][k]
            s.extend((op[0], i + 1, op[1]) for op in txns[i][a:b] if op[0] != ROLLBACK)
            if k == len(chop[i]) - 1:
                s.append(("c", i + 1, None))
        yield tuple(s)


def all_executions_serializable(txns, chop):
    return all(dbsched.is_conflict_serializable(s) for s in executions(txns, chop))


def test_transfer_example():
    transfer = parse_txn("r(a) w(a) r(b) w(b)")
    dep_b = parse_txn("r(b) w(b)")
    dep_a = parse_txn("r(a) w(a)")
    audit = parse_txn("r(a) r(b)")
    txns = [transfer, dep_b, dep_a]
    assert finest_chopping(txns) == [[(0, 2), (2, 4)], [(0, 2)], [(0, 2)]]
    assert all_executions_serializable(txns, finest_chopping(txns))
    # The audit joins the two deposits into one component: no cut is allowed.
    txns = [transfer, dep_b, dep_a, audit]
    assert finest_chopping(txns) == [[(0, 4)], [(0, 2)], [(0, 2)], [(0, 2)]]
    bad = [[(0, 2), (2, 4)], [(0, 2)], [(0, 2)], [(0, 2)]]
    assert has_sc_cycle(txns, bad) and not is_correct(txns, bad)
    # The audit runs between the two pieces and sees a debited and b not yet credited.
    s = dbsched.parse("r1(a) w1(a) r2(a) r2(b) c2 r1(b) w1(b) c1")
    assert s in set(executions([transfer, audit], [[(0, 2), (2, 4)], [(0, 2)]]))
    assert not dbsched.is_conflict_serializable(s)


def test_rollback_safety():
    # A check on a before the write: the first piece must hold the rollback.
    t1 = parse_txn("r(a) rollback w(a) r(b) w(b)")
    txns = [t1, parse_txn("r(b) w(b)"), parse_txn("r(a) w(a)")]
    assert finest_chopping(txns)[0] == [(0, 3), (3, 5)]
    # A check on b at the end forces the whole transaction into one piece.
    t1 = parse_txn("r(a) w(a) r(b) w(b) rollback")
    txns = [t1, parse_txn("r(b) w(b)"), parse_txn("r(a) w(a)")]
    assert finest_chopping(txns)[0] == [(0, 5)]
    assert not is_rollback_safe(t1, [(0, 2), (2, 5)])
    assert not is_correct(txns, [[(0, 2), (2, 5)], [(0, 2)], [(0, 2)]])


def test_no_conflict_means_one_piece_per_statement():
    txns = [parse_txn("r(x) w(y) w(z)"), parse_txn("r(x) r(y)")]
    # w(y) of T1 conflicts with T2; r(x) and w(z) conflict with nothing.
    assert finest_chopping(txns)[0] == [(0, 1), (1, 2), (2, 3)]


def test_component_test_matches_brute_force():
    rng = random.Random(11)
    for _ in range(150):
        txns = gen(rng, rng.randint(2, 3), 3)
        for chop in itertools.product(*[all_choppings(t) for t in txns]):
            chop = list(chop)
            assert has_sc_cycle(txns, chop) == sc_cycle_brute(txns, chop)


def test_finest_is_correct_and_below_every_correct_chopping():
    rng = random.Random(12)
    for _ in range(300):
        txns = gen(rng, rng.randint(2, 4), 4)
        fine = finest_chopping(txns)
        assert is_correct(txns, fine)
        for i, t in enumerate(txns):
            for c in all_choppings(t):
                trial = [fine[j] if j != i else c for j in range(len(txns))]
                # A private chopping is correct if and only if it is coarser.
                assert is_correct(txns, trial) == coarser(c, fine[i])
            assert fine[i] == private_chopping(txns, i)
        everything = list(itertools.product(*[all_choppings(t) for t in txns]))
        if len(everything) <= 64:
            for chop in everything:
                chop = list(chop)
                ok = all(coarser(c, f) for c, f in zip(chop, fine))
                assert is_correct(txns, chop) == ok


def test_correct_choppings_give_serializable_executions():
    rng = random.Random(13)
    for _ in range(25):
        txns = gen(rng, 3, 3)
        fine = finest_chopping(txns)
        assert all_executions_serializable(txns, fine)
        # Any chopping with an SC-cycle, on these sizes, has a bad execution.
        for chop in itertools.product(*[all_choppings(t) for t in txns]):
            chop = list(chop)
            if has_sc_cycle(txns, chop):
                assert not all_executions_serializable(txns, chop)
                break


def test_two_pieces_against_one_transaction():
    # The simplest SC-cycle: p and p' of T1 both conflict with T2.
    t1, t2 = parse_txn("r(x) r(y)"), parse_txn("w(x) w(y)")
    chop = [[(0, 1), (1, 2)], [(0, 2)]]
    assert has_sc_cycle([t1, t2], chop)
    s = dbsched.parse("r1(x) w2(x) w2(y) c2 r1(y) c1")
    assert not dbsched.is_conflict_serializable(s)
    assert s in set(executions([t1, t2], chop))
