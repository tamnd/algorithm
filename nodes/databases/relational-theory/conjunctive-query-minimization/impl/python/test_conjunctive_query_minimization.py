# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conjunctive-query-minimization/. The authors are listed in prov/PG64E9.jsonl.

import itertools
import random

from conjunctive_query_minimization import (
    evaluate,
    homomorphism,
    is_equivalent,
    is_var,
    minimize,
    variables,
)


def brute_homomorphism(source, target) -> bool:
    """The definition: try every map from the variables of source to the terms of target."""
    head_s, body_s = source
    head_t, body_t = target
    vs = variables(body_s)
    terms = sorted({t for _, ts in body_t for t in ts} | set(head_t), key=repr)
    facts = set(body_t)
    for values in itertools.product(terms, repeat=len(vs)):
        h = dict(zip(vs, values))

        def image(ts):
            return tuple(h[t] if is_var(t) else t for t in ts)

        if image(head_s) != tuple(head_t):
            continue
        if all((name, image(ts)) in facts for name, ts in body_s):
            return True
    return False


def safe(head, body) -> bool:
    return all(not is_var(t) or t in variables(body) for t in head)


def brute_force_minimum(query) -> int:
    """The smallest number of atoms of an equivalent subquery, by trying all subsets."""
    head, body = query
    for size in range(len(body) + 1):
        for sub in itertools.combinations(body, size):
            sub = list(sub)
            if not safe(head, sub):
                continue
            q = (head, sub)
            if brute_homomorphism(query, q) and brute_homomorphism(q, query):
                return size
    return len(body)


def random_query(rng, names=("x", "y", "z", "u", "v")):
    names = list(names)
    k = rng.randint(1, 5)
    body = []
    for _ in range(k):
        if rng.random() < 0.7:
            terms = (rng.choice(names), rng.choice(names))
            body.append(("E", terms))
        else:
            terms = (rng.choice(names), rng.choice(names + [1]))
            body.append(("R", terms))
    vs = variables(body)
    head = tuple(rng.sample(vs, rng.randint(0, min(2, len(vs)))))
    return head, body


def random_db(rng):
    dom = [1, 2, 3]
    return {
        "E": {(rng.choice(dom), rng.choice(dom)) for _ in range(rng.randint(0, 6))},
        "R": {(rng.choice(dom), rng.choice(dom)) for _ in range(rng.randint(0, 4))},
    }


def edge_atoms(edges, prefix):
    body = []
    for a, b in edges:
        body.append(("E", (f"{prefix}{a}", f"{prefix}{b}")))
        body.append(("E", (f"{prefix}{b}", f"{prefix}{a}")))
    return body


def test_page_example():
    q = (("x", "z"), [
        ("E", ("x", "y")), ("E", ("y", "z")), ("E", ("x", "w")), ("E", ("w", "z")), ("E", ("x", "u")),
    ])
    trace = []
    head, body = minimize(q, trace)
    assert body == [("E", ("x", "w")), ("E", ("w", "z"))]
    assert [removed for _, removed in trace] == [True, True, False, False, True]
    assert is_equivalent(q, (head, body))


def test_constants_and_head():
    # The constant 1 blocks the map y -> 2.
    q = (("x",), [("R", ("x", "y")), ("R", ("x", 1))])
    assert minimize(q)[1] == [("R", ("x", 1))]
    q = (("x",), [("R", ("x", 2)), ("R", ("x", 1))])
    assert minimize(q)[1] == q[1]
    # A head variable can not be renamed, so nothing goes.
    q = (("x", "y"), [("E", ("x", "z")), ("E", ("y", "z"))])
    assert minimize(q)[1] == q[1]
    # The Boolean version folds y onto x.
    q = ((), [("E", ("x", "z")), ("E", ("y", "z"))])
    assert len(minimize(q)[1]) == 1
    # Duplicate atoms.
    q = (("x",), [("E", ("x", "y")), ("E", ("x", "y"))])
    assert minimize(q)[1] == [("E", ("x", "y"))]


def test_homomorphism_against_brute_force():
    rng = random.Random(11)
    for _ in range(300):
        q1, q2 = random_query(rng), random_query(rng)
        if len(q1[0]) != len(q2[0]):
            continue
        found = homomorphism(q1, q2)
        assert (found is not None) == brute_homomorphism(q1, q2)
        if found is not None:
            image = lambda ts: tuple(found[t] if is_var(t) else t for t in ts)
            assert image(q1[0]) == q2[0]
            assert all((n, image(ts)) in set(q2[1]) for n, ts in q1[1])


def test_minimize_against_brute_force():
    rng = random.Random(20261118)
    for _ in range(200):
        q = random_query(rng, ("x", "y", "z", "u"))
        head, body = minimize(q)
        rest = list(q[1])
        for atom in body:
            rest.remove(atom)
        assert safe(head, body)
        assert brute_homomorphism(q, (head, body)) and brute_homomorphism((head, body), q)
        assert len(body) == brute_force_minimum(q), q
        # No single atom of the result can go: it is minimal.
        for atom in body:
            smaller = list(body)
            smaller.remove(atom)
            assert not (safe(head, smaller) and brute_homomorphism((head, body), (head, smaller)))


def test_same_answers_on_random_databases():
    rng = random.Random(5)
    for _ in range(150):
        q = random_query(rng)
        m = minimize(q)
        for _ in range(4):
            db = random_db(rng)
            assert evaluate(q, db) == evaluate(m, db)


def test_core_size_decides_three_coloring():
    # The core of Q_G and Q_K3 together has 6 atoms iff G is 3-colorable.
    triangle = [(0, 1), (1, 2), (2, 0)]
    c5 = [(i, (i + 1) % 5) for i in range(5)]
    k4 = [(a, b) for a in range(4) for b in range(a + 1, 4)]
    for edges, colorable in ((c5, True), (k4, False), ([(0, 1), (1, 2)], True)):
        q = ((), edge_atoms(triangle, "t") + edge_atoms(edges, "g"))
        size = len(minimize(q)[1])
        assert (size == 6) == colorable
    q = ((), edge_atoms(k4, "g") + edge_atoms(triangle, "t"))
    assert len(minimize(q)[1]) == 12


def test_order_changes_the_atoms_not_the_size():
    rng = random.Random(9)
    for _ in range(100):
        head, body = random_query(rng)
        sizes = set()
        for _ in range(3):
            shuffled = list(body)
            rng.shuffle(shuffled)
            sizes.add(len(minimize((head, shuffled))[1]))
        assert len(sizes) == 1
