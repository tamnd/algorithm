# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horizontal-fragmentation/. The authors are listed in prov/XH9D31.jsonl.

import random
from collections import Counter
from functools import reduce

import pytest

import dbrel
from horizontal_fragmentation import (derived_fragments, is_complete, is_disjoint, minterms, naive_fragments,
                                      primary_fragments, reconstruct)

ACCOUNT = ("id", "branch", "balance")
ACCOUNT_ROWS = Counter({(1, "Paris", 500): 1, (2, "Paris", 2500): 1, (3, "Lyon", 800): 1,
                        (4, "Lyon", None): 1, (5, "Nice", 1200): 1})
P1 = lambda r: dbrel.cmp3("=", r["branch"], "Paris")
P2 = lambda r: dbrel.cmp3("<", r["balance"], 1000)
TXN = ("tid", "id", "amount")
TXN_ROWS = Counter({(10, 1, 20): 1, (11, 1, 30): 1, (12, 3, 5): 1, (13, 4, 7): 1, (14, 5, 9): 1})


def rel(schema, rows):
    return dbrel.Relation(schema, rows)


def bag_union(schema, frags):
    return reduce(dbrel.union, (rel(schema, f) for f in frags), rel(schema, ()))


def test_page_example_primary():
    frags = primary_fragments(ACCOUNT, ACCOUNT_ROWS, [P1, P2])
    ids = {m: sorted(t[0] for t in f) for m, f in frags.items()}
    assert ids == {(True, True): [1], (True, False): [2], (False, True): [3], (False, False): [4, 5]}
    assert reconstruct(frags) == ACCOUNT_ROWS and is_disjoint(frags)


def test_page_example_naive_minterms_lose_the_null_row():
    frags = naive_fragments(ACCOUNT, ACCOUNT_ROWS, [P1, P2])
    lost = ACCOUNT_ROWS - reconstruct(frags)
    assert lost == Counter({(4, "Lyon", None): 1})
    assert not is_complete(ACCOUNT_ROWS, frags)


def test_page_example_derived():
    owner = primary_fragments(ACCOUNT, ACCOUNT_ROWS, [P1, P2])
    frags = derived_fragments(TXN, TXN_ROWS, ACCOUNT, owner)
    tids = {m: sorted(t[0] for t in f) for m, f in frags.items()}
    assert tids == {(True, True): [10, 11], (True, False): [], (False, True): [12], (False, False): [13, 14]}
    assert reconstruct(frags) == TXN_ROWS and is_disjoint(frags)


def random_preds(rng, schema, k):
    preds = []
    for _ in range(k):
        a = rng.choice(schema)
        op = rng.choice(["=", "<>", "<", "<=", ">", ">="])
        v = rng.randint(0, 3)
        preds.append(lambda r, a=a, op=op, v=v: dbrel.cmp3(op, r[a], v))
    return preds


@pytest.mark.parametrize("seed", range(80))
def test_minterm_fragments_are_complete_disjoint_and_reconstruct(seed):
    rng = random.Random(seed)
    schema = ("A", "B", "C")
    r = dbrel.random_relation(rng, schema, rng.randint(0, 25), domain=4, null_rate=0.2)
    preds = random_preds(rng, schema, rng.randint(0, 4))
    frags = primary_fragments(schema, r.rows, preds)
    assert len(frags) <= min(2 ** len(preds), max(1, len(r.rows)))
    assert is_disjoint(frags) and is_complete(r.rows, frags)
    assert bag_union(schema, frags.values()) == r
    for m, f in frags.items():
        want = dbrel.select(r, lambda row: all(dbrel.is_true(p(row)) == s for p, s in zip(preds, m)))
        assert rel(schema, f) == want
    # The naive fragments keep exactly the rows on which no predicate is UNKNOWN.
    naive = reconstruct(naive_fragments(schema, r.rows, preds))
    assert rel(schema, naive) == dbrel.select(r, lambda row: all(p(row) is not None for p in preds))


@pytest.mark.parametrize("seed", range(60))
def test_derived_fragments(seed):
    rng = random.Random(1000 + seed)
    keys = rng.sample(range(10), rng.randint(1, 6))
    owner = rel(("K", "G"), [(k, rng.randint(0, 3)) for k in keys])  # K is a key of the owner
    preds = random_preds(rng, ("G",), rng.randint(1, 3))
    ofr = primary_fragments(owner.schema, owner.rows, preds)
    member = dbrel.random_relation(rng, ("M", "K"), rng.randint(0, 15), domain={"M": 5, "K": keys + [None, 99]})
    frags = derived_fragments(member.schema, member.rows, owner.schema, ofr)
    for m, f in frags.items():
        assert rel(member.schema, f) == dbrel.semijoin(member, rel(owner.schema, ofr[m]))
    # K is a key of the owner, so the fragments are disjoint.
    assert is_disjoint(frags)
    # A member row is lost exactly when it has no owner row: a NULL or a dangling key.
    assert rel(member.schema, member.rows - reconstruct(frags)) == dbrel.antijoin(member, owner)
    ok = dbrel.semijoin(member, owner)
    clean = derived_fragments(member.schema, ok.rows, owner.schema, ofr)
    assert reconstruct(clean) == ok.rows and is_complete(ok.rows, clean)


def test_derived_fragments_overlap_without_a_key():
    owner = Counter({(1, 0): 1, (1, 1): 1})         # K = 1 appears twice, in two fragments
    ofr = primary_fragments(("K", "G"), owner, [lambda r: dbrel.cmp3("=", r["G"], 0)])
    frags = derived_fragments(("M", "K"), Counter({(7, 1): 1}), ("K", "G"), ofr)
    assert not is_disjoint(frags)
    assert reconstruct(frags) == Counter({(7, 1): 2})   # the union counts the row twice


def test_minterm_count_and_duplicates():
    assert len(minterms(0)) == 1 and len(minterms(3)) == 8
    rows = Counter({(1, 2): 3, (2, 2): 2})
    frags = primary_fragments(("A", "B"), rows, [lambda r: dbrel.cmp3("=", r["A"], 1)])
    assert frags == {(True,): Counter({(1, 2): 3}), (False,): Counter({(2, 2): 2})}
    assert primary_fragments(("A", "B"), Counter(), [lambda r: True]) == {}
