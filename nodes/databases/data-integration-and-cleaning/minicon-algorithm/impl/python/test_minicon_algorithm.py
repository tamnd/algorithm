# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minicon-algorithm/. The authors are listed in prov/Y3KK7E.jsonl.

import itertools
import random

from minicon_algorithm import answer, contained, evaluate, expand, form_mcds, minicon, variables

# The example of Pottinger and Levy (VLDB 2000), Section 3.
Q1 = (("x",), [("cites", ("x", "y")), ("cites", ("y", "x")), ("sameTopic", ("x", "y"))])
PAPER_VIEWS = {
    "V4": (("a",), [("cites", ("a", "b")), ("cites", ("b", "a"))]),
    "V5": (("c", "d"), [("sameTopic", ("c", "d"))]),
    "V6": (("f", "h"), [("cites", ("f", "g")), ("cites", ("g", "h")), ("sameTopic", ("f", "g"))]),
}


def certain_answers(query, views, view_instance):
    """Oracle: chase the view facts into a canonical database with labeled nulls,
    evaluate the query and keep the answers without nulls."""
    db = {}
    k = 0
    for name, tuples in view_instance.items():
        vhead, vbody = views[name]
        for t in sorted(tuples):
            k += 1
            m = dict(zip(vhead, t))
            for pred, args in vbody:
                db.setdefault(pred, set()).add(tuple(m.setdefault(u, ("null", k, u)) for u in args))
    return {t for t in evaluate(query, db) if not any(isinstance(v, tuple) for v in t)}


def view_image(views, db):
    return {name: evaluate(v, db) for name, v in views.items()}


def brute_contained_rewritings(query, views, max_atoms):
    """Oracle: every contained rewriting with at most max_atoms view atoms whose
    variables are query variables or fresh ones, with each possible head."""
    qhead, qbody = query
    qvars = variables(qbody)
    atoms = []
    for name in sorted(views):
        arity = len(views[name][0])
        for args in itertools.product(qvars + [None], repeat=arity):
            atoms.append((name, args))
    for size in range(1, max_atoms + 1):
        for combo in itertools.combinations_with_replacement(atoms, size):
            fresh = itertools.count()
            body = [(n, tuple(a if a is not None else "_f%d" % next(fresh) for a in args)) for n, args in combo]
            ehead, ebody = expand(((), body), views)
            index = {}
            for pred, args in ebody:
                index.setdefault(pred, set()).add(args)
            rvars = set(variables(body))
            heads = set()
            for h in _all_maps(qbody, index):
                t = tuple(h[x] for x in qhead)
                if all(v in rvars for v in t):
                    heads.add(t)
            for t in sorted(heads):
                yield (t, body)


def _all_maps(atoms, index, binding=None):
    binding = {} if binding is None else binding
    if not atoms:
        yield binding
        return
    pred, args = atoms[0]
    for tup in index.get(pred, ()):
        new = dict(binding)
        if all(new.setdefault(a, v) == v for a, v in zip(args, tup)):
            yield from _all_maps(atoms[1:], index, new)


def random_case(rng):
    preds = [("e", 2), ("p", 1)]
    qv = ["x", "y", "z"]
    body = []
    for _ in range(rng.randint(1, 3)):
        p, ar = rng.choice(preds)
        atom = (p, tuple(rng.choice(qv) for _ in range(ar)))
        if atom not in body:
            body.append(atom)
    used = variables(body)
    head = tuple(rng.sample(used, rng.randint(0, min(2, len(used)))))
    views = {}
    for k in range(rng.randint(1, 3)):
        vv = ["a", "b", "c"]
        vbody = []
        for _ in range(rng.randint(1, 2)):
            p, ar = rng.choice(preds)
            atom = (p, tuple(rng.choice(vv) for _ in range(ar)))
            if atom not in vbody:
                vbody.append(atom)
        vused = variables(vbody)
        vhead = tuple(rng.sample(vused, rng.randint(1, len(vused))))
        views["V%d" % k] = (vhead, vbody)
    return (head, body), views


def random_db(rng):
    dom = ["1", "2", "3"]
    db = {"e": set(), "p": set()}
    for _ in range(rng.randint(0, 5)):
        db["e"].add((rng.choice(dom), rng.choice(dom)))
    for _ in range(rng.randint(0, 2)):
        db["p"].add((rng.choice(dom),))
    return db


def test_paper_example():
    mcds = form_mcds(Q1, PAPER_VIEWS)
    # V5 covers sameTopic(x, y) alone. V6 must cover all three subgoals, with f = h.
    assert [(m[0], sorted(m[3])) for m in mcds] == [("V5", [2]), ("V6", [0, 1, 2])]
    v6 = mcds[1]
    assert v6[1] == {"f": "f", "h": "f"}
    assert v6[2] == {"x": "f", "y": "g"}
    assert minicon(Q1, PAPER_VIEWS) == [(("x",), [("V6", ("x", "x"))])]


def test_equivalent_rewriting_found():
    # Q(x, z) :- e(x, y), e(y, z) with the view V(a, b) :- e(a, b).
    q = (("x", "z"), [("e", ("x", "y")), ("e", ("y", "z"))])
    views = {"V": (("a", "b"), [("e", ("a", "b"))])}
    rs = minicon(q, views)
    assert rs == [(("x", "z"), [("V", ("x", "y")), ("V", ("y", "z"))])]
    assert contained(q, expand(rs[0], views)) and contained(expand(rs[0], views), q)


def test_no_rewriting_when_join_variable_is_hidden():
    # The join variable y is existential in each view, so nothing can join the two halves.
    q = (("x", "z"), [("e", ("x", "y")), ("e", ("y", "z"))])
    views = {"L": (("a",), [("e", ("a", "b"))]), "R": (("b",), [("e", ("a", "b"))])}
    assert minicon(q, views) == []


def test_sound_and_maximal_on_random_cases():
    rng = random.Random(7)
    checked = 0
    while checked < 150:
        query, views = random_case(rng)
        if not query[1]:
            continue
        checked += 1
        rs = minicon(query, views)
        for r in rs:
            assert set(r[0]) <= set(variables(r[1]))
            assert contained(expand(r, views), query)
        if len(query[1]) <= 2:
            for b in brute_contained_rewritings(query, views, len(query[1])):
                assert any(contained(b, r) for r in rs), (query, views, b, rs)
        for _ in range(4):
            db = random_db(rng)
            inst = view_image(views, db)
            got = answer(rs, inst)
            assert got <= evaluate(query, db)
            assert got == certain_answers(query, views, inst)


def test_paper_example_maximal():
    rs = minicon(Q1, PAPER_VIEWS)
    for b in brute_contained_rewritings(Q1, PAPER_VIEWS, 2):
        assert any(contained(b, r) for r in rs)


def test_head_variables_can_be_equated():
    # V(a) :- e(a, a) answers Q(x, y) :- e(x, y) only on the diagonal.
    q = (("x", "y"), [("e", ("x", "y"))])
    views = {"V": (("a",), [("e", ("a", "a"))])}
    assert minicon(q, views) == [(("x", "x"), [("V", ("x",))])]
    assert answer(minicon(q, views), {"V": {("1",)}}) == {("1", "1")}


def test_boolean_query():
    q = ((), [("e", ("x", "y"))])
    views = {"V": (("a",), [("e", ("a", "b"))])}
    rs = minicon(q, views)
    assert answer(rs, {"V": {("1",)}}) == {()}
    assert answer(rs, {"V": set()}) == set()
