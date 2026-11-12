# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yannakakis-algorithm/. The authors are listed in prov/D8JPK9.jsonl.

import random

import pytest

from yannakakis_algorithm import full_reducer, hash_join, semijoin, yannakakis


def nested_loop(attrs, rels):
    cur = [{}]
    for e, r in zip(attrs, rels):
        nxt = []
        for asg in cur:
            for t in r:
                if all(asg.get(v, a) == a for v, a in zip(e, t)):
                    d = dict(asg)
                    d.update(zip(e, t))
                    nxt.append(d)
        cur = nxt
    return cur


def random_tree(rng):
    """A random join tree: each child takes some attributes of its parent and some new ones."""
    n = rng.randrange(1, 7)
    fresh = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    attrs, parent = [], []
    for u in range(n):
        p = rng.randrange(u) if u else -1
        inherit = rng.sample(attrs[p], rng.randrange(0, len(attrs[p]) + 1)) if p >= 0 else []
        new = [next(fresh) for _ in range(rng.randrange(0 if inherit else 1, 3))]
        at = inherit + new
        rng.shuffle(at)
        attrs.append(tuple(at))
        parent.append(p)
    dom = rng.randrange(2, 5)
    rels = [{tuple(rng.randrange(dom) for _ in at) for _ in range(rng.randrange(0, 12))} for at in attrs]
    return attrs, rels, parent


def test_example() -> None:
    # R(A, B) is the root, with children S(B, C) and T(A, D).
    attrs = [("A", "B"), ("B", "C"), ("A", "D")]
    rels = [{(1, 1), (1, 2), (2, 3)}, {(1, 5), (3, 6), (4, 7)}, {(1, 8), (1, 9), (3, 9)}]
    red = full_reducer(attrs, rels, [-1, 0, 0])
    assert red == [{(1, 1)}, {(1, 5)}, {(1, 8), (1, 9)}]
    assert yannakakis(attrs, rels, [-1, 0, 0]) == {(1, 1, 5, 8), (1, 1, 5, 9)}
    assert yannakakis(attrs, rels, [-1, 0, 0], out=["C"]) == {(5,)}


def test_helpers() -> None:
    assert semijoin("AB", {(1, 2), (3, 4)}, "BC", {(2, 0)}) == {(1, 2)}
    assert semijoin("A", {(1,)}, "B", set()) == set()          # no shared attributes, empty right
    assert semijoin("A", {(1,)}, "B", {(7,)}) == {(1,)}
    assert hash_join("AB", {(1, 2)}, "BC", {(2, 3), (2, 4)}) == (["A", "B", "C"], {(1, 2, 3), (1, 2, 4)})
    with pytest.raises(ValueError):
        yannakakis(["A", "B"], [set(), set()], [-1, -1])


def test_random_trees() -> None:
    rng = random.Random(3)
    for _ in range(400):
        attrs, rels, parent = random_tree(rng)
        allattrs = sorted({a for at in attrs for a in at})
        ref = nested_loop(attrs, rels)
        st = {}
        got = yannakakis(attrs, rels, parent, stats=st)
        full = {tuple(d[a] for a in allattrs) for d in ref}
        assert got == full
        assert st["max_intermediate"] <= len(full)       # each J_u is a projection of the result
        # The full reducer leaves no dangling tuple: each R_u is the projection of the join.
        red = full_reducer(attrs, rels, parent)
        for at, r in zip(attrs, red):
            assert r == {tuple(d[a] for a in at) for d in ref}
        # Projections.
        out = rng.sample(allattrs, rng.randrange(0, len(allattrs) + 1))
        proj = {tuple(d[a] for a in out) for d in ref}
        st = {}
        assert yannakakis(attrs, rels, parent, out=out, stats=st) == proj
        assert st["max_intermediate"] <= max(len(r) for r in red) * len(proj)


def test_intermediates_stay_small() -> None:
    # A path R(A, B), S(B, C), T(C, D) where R join S is huge but the result is empty.
    m = 300
    attrs = [("A", "B"), ("B", "C"), ("C", "D")]
    rels = [{(i, 0) for i in range(m)}, {(0, j) for j in range(m)}, {(m + 1, 0)}]
    st = {}
    assert yannakakis(attrs, rels, [1, -1, 1], stats=st) == set()
    assert st["max_intermediate"] == 0
    _, rs = hash_join(attrs[0], rels[0], attrs[1], rels[1])
    assert len(rs) == m * m                                       # what a plain plan builds first
