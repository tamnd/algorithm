# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lossless-join-test/. The authors are listed in prov/R7WCET.jsonl.

import random
from itertools import product

import pytest

from lossless_join_test import chase_fds, lossless_join_test, start_tableau


def closure(x, fds):
    res = set(x)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if set(lhs) <= res and not set(rhs) <= res:
                res |= set(rhs)
                changed = True
    return res


def satisfies(rel, fds):
    """rel is a set of tuples over the columns 0 .. a - 1; fds use column indexes."""
    for lhs, rhs in fds:
        seen = {}
        for t in rel:
            key = tuple(t[j] for j in lhs)
            val = tuple(t[j] for j in rhs)
            if seen.setdefault(key, val) != val:
                return False
    return True


def join_of_projections(rel, parts, a):
    """The natural join of the projections of rel on parts, built one part at a time."""
    partial = {tuple([None] * a)}
    for p in parts:
        cols = sorted(p)
        proj = {tuple(t[j] for j in cols) for t in rel}
        nxt = set()
        for u in partial:
            for v in proj:
                if all(u[j] is None or u[j] == x for j, x in zip(cols, v)):
                    w = list(u)
                    for j, x in zip(cols, v):
                        w[j] = x
                    nxt.add(tuple(w))
        partial = nxt
    return partial


def rgs(k):
    """All set partitions of k rows, as restricted growth strings."""
    out = []

    def rec(prefix, top):
        if len(prefix) == k:
            out.append(tuple(prefix))
            return
        for x in range(top + 2):
            rec(prefix + [x], max(top, x))

    rec([], -1)
    return out


def all_small_relations(a, k):
    """Each relation with at most k tuples over a columns, up to a renaming of each column."""
    cols = rgs(k)
    for choice in product(cols, repeat=a):
        yield {tuple(choice[j][i] for j in range(a)) for i in range(k)}


def random_instance(rng, a, k, nfd):
    attrs = [chr(ord("A") + j) for j in range(a)]
    fds = []
    for _ in range(nfd):
        lhs = rng.sample(attrs, rng.randint(0 if rng.random() < 0.1 else 1, 2))
        rhs = rng.sample(attrs, rng.randint(1, 2))
        fds.append(("".join(lhs), "".join(rhs)))
    parts = [set(rng.sample(attrs, rng.randint(1, a - 1))) for _ in range(k)]
    for x in attrs:
        if not any(x in p for p in parts):
            parts[rng.randrange(k)].add(x)
    return attrs, fds, ["".join(sorted(p)) for p in parts]


def to_cols(attrs, fds, parts):
    col = {x: j for j, x in enumerate(attrs)}
    f = [([col[x] for x in lhs], [col[x] for x in rhs]) for lhs, rhs in fds]
    p = [{col[x] for x in q} for q in parts]
    return f, p


def brute_lossless(attrs, fds, parts):
    a, k = len(attrs), len(parts)
    f, p = to_cols(attrs, fds, parts)
    for rel in all_small_relations(a, k):
        if satisfies(rel, f) and join_of_projections(rel, p, a) != rel:
            return False
    return True


def test_ullman_five_parts():
    attrs = "ABCDE"
    fds = [("A", "C"), ("B", "C"), ("C", "D"), ("DE", "C"), ("CE", "A")]
    parts = ["AD", "AB", "BE", "CDE", "AE"]
    ok, t = lossless_join_test(attrs, fds, parts)
    assert ok
    assert t[2] == [0, 0, 0, 0, 0]
    assert t == [[0, 1, 0, 0, 1], [0, 0, 0, 0, 2], [0, 0, 0, 0, 0], [0, 4, 0, 0, 0], [0, 5, 0, 0, 0]]
    for drop in range(len(fds)):
        assert not lossless_join_test(attrs, fds[:drop] + fds[drop + 1:], parts)[0]


def test_abcd_cases():
    fds = [("A", "B"), ("C", "D")]
    ok, t = lossless_join_test("ABCD", fds, ["AB", "CD", "AC"])
    assert ok and [0, 0, 0, 0] in t
    ok, t = lossless_join_test("ABCD", fds, ["AB", "CD", "BD"])
    assert not ok
    assert t == [[0, 0, 1, 1], [2, 2, 0, 0], [3, 0, 3, 0]]


def test_no_fds():
    rng = random.Random(1)
    for _ in range(200):
        a = rng.randint(1, 6)
        k = rng.randint(1, 4)
        attrs, _, parts = random_instance(rng, a, k, 0) if a > 1 else (["A"], [], ["A"] * k)
        if rng.random() < 0.2:
            parts.append("".join(attrs))
        ok, _ = lossless_join_test(attrs, [], parts)
        assert ok == any(set(p) == set(attrs) for p in parts)


def test_two_parts_match_closure():
    rng = random.Random(2)
    for _ in range(400):
        a = rng.randint(2, 6)
        attrs, fds, parts = random_instance(rng, a, 2, rng.randint(0, 5))
        common = set(parts[0]) & set(parts[1])
        c = closure(common, fds)
        expect = set(parts[0]) <= c or set(parts[1]) <= c
        assert lossless_join_test(attrs, fds, parts)[0] == expect


def test_lossy_tableau_is_counterexample():
    rng = random.Random(3)
    seen = 0
    for _ in range(300):
        a = rng.randint(2, 6)
        k = rng.randint(2, 5)
        attrs, fds, parts = random_instance(rng, a, k, rng.randint(0, 6))
        ok, t = lossless_join_test(attrs, fds, parts)
        if ok:
            continue
        seen += 1
        f, p = to_cols(attrs, fds, parts)
        rel = {tuple(row) for row in t}
        assert satisfies(rel, f)
        zero = tuple([0] * a)
        assert zero not in rel
        assert zero in join_of_projections(rel, p, a)
    assert seen > 50


@pytest.mark.parametrize("a,k,count,seed", [(3, 3, 40, 4), (4, 2, 60, 5), (4, 3, 15, 6), (5, 2, 40, 7)])
def test_brute_force_small(a, k, count, seed):
    rng = random.Random(seed)
    for _ in range(count):
        attrs, fds, parts = random_instance(rng, a, k, rng.randint(0, 4))
        assert lossless_join_test(attrs, fds, parts)[0] == brute_lossless(attrs, fds, parts)


def test_random_legal_relations():
    rng = random.Random(8)
    hits = 0
    for _ in range(300):
        a = rng.randint(2, 5)
        k = rng.randint(2, 4)
        attrs, fds, parts = random_instance(rng, a, k, rng.randint(1, 5))
        ok, _ = lossless_join_test(attrs, fds, parts)
        if not ok:
            continue
        f, p = to_cols(attrs, fds, parts)
        rel = set()
        for _ in range(8):
            t = tuple(rng.randrange(3) for _ in range(a))
            if satisfies(rel | {t}, f):
                rel.add(t)
        assert join_of_projections(rel, p, a) == rel
        hits += 1
    assert hits > 30


def test_round_bound_and_fixpoint():
    rng = random.Random(9)
    for _ in range(300):
        a = rng.randint(1, 7)
        k = rng.randint(1, 6)
        if a == 1:
            attrs, fds, parts = ["A"], [("A", "A")], ["A"] * k
        else:
            attrs, fds, parts = random_instance(rng, a, k, rng.randint(0, 8))
        f, p = to_cols(attrs, fds, parts)
        t = start_tableau(attrs, [set(q) for q in parts])
        rounds = chase_fds(t, f)
        assert 1 <= rounds <= a * (k - 1) + 1
        assert satisfies({tuple(row) for row in t}, f)
        assert chase_fds(t, f) == 1


def test_order_does_not_matter():
    rng = random.Random(10)
    for _ in range(300):
        a = rng.randint(2, 6)
        k = rng.randint(2, 5)
        attrs, fds, parts = random_instance(rng, a, k, rng.randint(0, 6))
        ok = lossless_join_test(attrs, fds, parts)[0]
        fds2 = fds[:]
        parts2 = parts[:]
        rng.shuffle(fds2)
        rng.shuffle(parts2)
        assert lossless_join_test(attrs, fds2, parts2)[0] == ok


def test_bad_input():
    with pytest.raises(ValueError):
        lossless_join_test("AAB", [], ["AB"])
    with pytest.raises(ValueError):
        lossless_join_test("ABC", [], ["AB"])
    with pytest.raises(ValueError):
        lossless_join_test("AB", [], ["AB", "BX"])
    with pytest.raises(ValueError):
        lossless_join_test("AB", [("A", "Z")], ["AB"])
    with pytest.raises(ValueError):
        lossless_join_test("AB", [], [])
