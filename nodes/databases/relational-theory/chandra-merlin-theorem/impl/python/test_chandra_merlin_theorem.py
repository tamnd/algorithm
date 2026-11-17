# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chandra-merlin-theorem/. The authors are listed in prov/ZF3N9M.jsonl.

import random
from itertools import combinations, product

from chandra_merlin_theorem import (
    canonical_db,
    contained,
    contained_by_canonical_db,
    equivalent,
    evaluate,
    find_homomorphism,
    minimize,
)


def variables(q):
    return {t for _, terms in q[1] for t in terms if isinstance(t, str)}


def all_graphs(k):
    """Every database with one binary relation E over the values 0, ..., k - 1."""
    pairs = list(product(range(k), repeat=2))
    for mask in range(1 << len(pairs)):
        yield {"E": {p for i, p in enumerate(pairs) if mask >> i & 1}}


GRAPHS = {k: list(all_graphs(k)) for k in (1, 2, 3)}


def brute_contained(q1, q2):
    """Q1 is contained in Q2 on every database. A counterexample, if any, is the image of a
    valuation of Q1, which has at most |vars(Q1)| values, so databases over that many values
    suffice: the answer of Q2 can only shrink on the smaller database."""
    k = max(1, len(variables(q1)))
    return all(evaluate(q1, db) <= evaluate(q2, db) for db in GRAPHS[k])


def random_cq(rng, nvars, natoms, arity):
    names = "xyzw"[:nvars]
    body = [("E", (rng.choice(names), rng.choice(names))) for _ in range(natoms)]
    used = sorted({t for _, ts in body for t in ts})
    head = tuple(rng.choice(used) for _ in range(arity))
    return head, body


def test_path_examples() -> None:
    path2 = (("x", "z"), [("E", ("x", "y")), ("E", ("y", "z"))])
    edge_loop = (("x", "x"), [("E", ("x", "x"))])
    # A loop is a path of length 2 from x to x, so loop-answers are path-answers.
    assert contained(edge_loop, path2) and not contained(path2, edge_loop)
    # The Boolean query "there is a path of length 2" contains "there is a triangle".
    triangle = ((), [("E", ("a", "b")), ("E", ("b", "c")), ("E", ("c", "a"))])
    p2 = ((), [("E", ("x", "y")), ("E", ("y", "z"))])
    assert contained(triangle, p2) and not contained(p2, triangle)
    assert brute_contained(triangle, p2) and not brute_contained(p2, triangle)


def test_page_example() -> None:
    # Q1(x) :- E(x, y), E(y, y).  Q2(x) :- E(x, u), E(u, v).
    q1 = (("x",), [("E", ("x", "y")), ("E", ("y", "y"))])
    q2 = (("x",), [("E", ("x", "u")), ("E", ("u", "v"))])
    assert find_homomorphism(q2, q1) == {"x": "x", "u": "y", "v": "y"}
    assert contained(q1, q2) and not contained(q2, q1)
    assert evaluate(q2, canonical_db(q1)) == {("x",), ("y",)}


def test_minimize_example() -> None:
    # Q(x) :- E(x, y), E(x, z), E(z, w) has the core Q(x) :- E(x, z), E(z, w).
    q = (("x",), [("E", ("x", "y")), ("E", ("x", "z")), ("E", ("z", "w"))])
    core = minimize(q)
    assert len(core[1]) == 2 and equivalent(core, q)


def test_constants() -> None:
    q1 = (("x",), [("E", ("x", 1))])
    q2 = (("x",), [("E", ("x", "y"))])
    assert contained(q1, q2) and not contained(q2, q1)
    assert evaluate(q1, {"E": {(0, 1), (2, 3)}}) == {(0,)}


def test_random_against_all_databases() -> None:
    rng = random.Random(21)
    yes = no = 0
    for _ in range(600):
        arity = rng.randint(0, 2)
        q1 = random_cq(rng, rng.randint(1, 3), rng.randint(1, 3), arity)
        q2 = random_cq(rng, rng.randint(1, 4), rng.randint(1, 3), arity)
        answer = contained(q1, q2)
        assert answer == contained_by_canonical_db(q1, q2)
        assert answer == brute_contained(q1, q2)
        yes += answer
        no += not answer
    assert yes > 50 and no > 50


def test_minimize_random() -> None:
    rng = random.Random(22)
    for _ in range(500):
        q = random_cq(rng, rng.randint(1, 4), rng.randint(1, 5), rng.randint(0, 2))
        core = minimize(q)
        assert equivalent(core, q)
        # No single atom of the core can be removed.
        for i in range(len(core[1])):
            smaller = (core[0], core[1][:i] + core[1][i + 1:])
            heads = {t for t in core[0]}
            if heads <= variables(smaller):
                assert not contained(smaller, core)
        # The core has the fewest atoms of all equivalent subqueries of q.
        body = list(dict.fromkeys(q[1]))
        best = min(
            size
            for size in range(1, len(body) + 1)
            for sub in combinations(body, size)
            if set(q[0]) <= variables((q[0], list(sub))) and equivalent((q[0], list(sub)), q)
        )
        assert len(core[1]) == best
