# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-rules-algorithm/. The authors are listed in prov/TPC6ZK.jsonl.

import itertools
import random

from inverse_rules_algorithm import cq_as_program, fixpoint, inverse_rules, inverse_rules_answers

# The example of Pottinger and Levy (VLDB 2000), Section 3.
Q1 = (("x",), [("cites", ("x", "y")), ("cites", ("y", "x")), ("sameTopic", ("x", "y"))])
PAPER_VIEWS = {
    "V4": (("a",), [("cites", ("a", "b")), ("cites", ("b", "a"))]),
    "V5": (("c", "d"), [("sameTopic", ("c", "d"))]),
    "V6": (("f", "h"), [("cites", ("f", "g")), ("cites", ("g", "h")), ("sameTopic", ("f", "g"))]),
}

# Transitive closure over e, a recursive query.
TC = (
    [
        (("path", ("x", "y")), [("e", ("x", "y"))]),
        (("path", ("x", "y")), [("e", ("x", "z")), ("path", ("z", "y"))]),
    ],
    "path",
)


def variables(atoms):
    seen = {}
    for _, args in atoms:
        for a in args:
            seen.setdefault(a, None)
    return list(seen)


def all_maps(atoms, index, binding=None):
    binding = {} if binding is None else binding
    if not atoms:
        yield binding
        return
    pred, args = atoms[0]
    for tup in index.get(pred, ()):
        if len(tup) != len(args):
            continue
        new = dict(binding)
        if all(new.setdefault(a, v) == v for a, v in zip(args, tup)):
            yield from all_maps(atoms[1:], index, new)


def naive_datalog(rules, db):
    """Oracle evaluation: apply every rule until nothing changes (no function terms)."""
    model = {p: set(ts) for p, ts in db.items()}
    while True:
        before = sum(len(v) for v in model.values())
        for (hp, ha), body in rules:
            for m in list(all_maps(body, model)):
                model.setdefault(hp, set()).add(tuple(m[a] for a in ha))
        if sum(len(v) for v in model.values()) == before:
            return model


def canonical_db(views, view_instance):
    """Oracle: chase the view facts with labeled nulls, one fresh null per existential and view fact."""
    db = {}
    k = 0
    for name in sorted(view_instance):
        vhead, vbody = views[name]
        for t in sorted(view_instance[name]):
            k += 1
            m = dict(zip(vhead, t))
            for pred, args in vbody:
                db.setdefault(pred, set()).add(tuple(m.setdefault(u, ("null", k, u)) for u in args))
    return db


def certain_by_chase(query, views, view_instance):
    rules, goal = query
    model = naive_datalog(rules, canonical_db(views, view_instance))
    return {t for t in model.get(goal, set()) if not any(isinstance(v, tuple) for v in t)}


def expand(body, views):
    out = []
    for k, (name, args) in enumerate(body):
        vhead, vbody = views[name]
        ren = dict(zip(vhead, args))
        for pred, us in vbody:
            out.append((pred, tuple(ren.setdefault(u, "%s#%d" % (u, k)) for u in us)))
    return out


def brute_rewriting_answers(query, views, view_instance):
    """Oracle for a conjunctive query: evaluate every contained rewriting with at
    most n view atoms (n the number of subgoals) on the view instance."""
    qhead, qbody = query
    qvars = variables(qbody)
    atoms = []
    for name in sorted(views):
        for args in itertools.product(qvars + [None], repeat=len(views[name][0])):
            atoms.append((name, args))
    out = set()
    for size in range(1, len(qbody) + 1):
        for combo in itertools.combinations_with_replacement(atoms, size):
            fresh = itertools.count()
            body = [(n, tuple(a if a is not None else "_f%d" % next(fresh) for a in args)) for n, args in combo]
            index = {}
            for pred, args in expand(body, views):
                index.setdefault(pred, set()).add(args)
            rvars = set(variables(body))
            heads = set()
            for h in all_maps(qbody, index):
                t = tuple(h[x] for x in qhead)
                if all(v in rvars for v in t):
                    heads.add(t)
            for t in heads:
                for m in all_maps(body, view_instance):
                    out.add(tuple(m[v] for v in t))
    return out


def view_image(views, db):
    out = {}
    for name, (vhead, vbody) in views.items():
        out[name] = {tuple(m[y] for y in vhead) for m in all_maps(vbody, db)}
    return out


def random_views(rng):
    views = {}
    for k in range(rng.randint(1, 3)):
        vv = ["a", "b", "c"]
        vbody = []
        for _ in range(rng.randint(1, 2)):
            if rng.random() < 0.8:
                atom = ("e", (rng.choice(vv), rng.choice(vv)))
            else:
                atom = ("p", (rng.choice(vv),))
            if atom not in vbody:
                vbody.append(atom)
        vused = variables(vbody)
        views["V%d" % k] = (tuple(rng.sample(vused, rng.randint(1, len(vused)))), vbody)
    return views


def random_cq(rng):
    qv = ["x", "y", "z"]
    body = []
    for _ in range(rng.randint(1, 2)):
        if rng.random() < 0.75:
            atom = ("e", (rng.choice(qv), rng.choice(qv)))
        else:
            atom = ("p", (rng.choice(qv),))
        if atom not in body:
            body.append(atom)
    used = variables(body)
    return (tuple(rng.sample(used, rng.randint(0, min(2, len(used))))), body)


def random_db(rng):
    dom = ["1", "2", "3", "4"]
    db = {"e": set(), "p": set()}
    for _ in range(rng.randint(0, 6)):
        db["e"].add((rng.choice(dom), rng.choice(dom)))
    for _ in range(rng.randint(0, 2)):
        db["p"].add((rng.choice(dom),))
    return db


def test_paper_rules():
    rules = inverse_rules(PAPER_VIEWS)
    f1 = ("f", "V4", "b", ("a",))
    f2 = ("f", "V6", "g", ("f", "h"))
    assert rules == [
        (("cites", ("a", f1)), [("V4", ("a",))]),
        (("cites", (f1, "a")), [("V4", ("a",))]),
        (("sameTopic", ("c", "d")), [("V5", ("c", "d"))]),
        (("cites", ("f", f2)), [("V6", ("f", "h"))]),
        (("cites", (f2, "h")), [("V6", ("f", "h"))]),
        (("sameTopic", ("f", f2)), [("V6", ("f", "h"))]),
    ]


def test_paper_answers():
    inst = {"V4": {("p1",)}, "V5": {("p1", "p2")}, "V6": {("p3", "p3"), ("p4", "p5")}}
    # Only V6(p3, p3) gives a paper that cites and is cited by a paper on its topic.
    assert inverse_rules_answers(cq_as_program(Q1), PAPER_VIEWS, inst) == {("p3",)}
    model = fixpoint(list(cq_as_program(Q1)[0]) + inverse_rules(PAPER_VIEWS), inst)
    sk = ("f", "V4", "b", ("p1",))
    assert ("p1", sk) in model["cites"] and (sk, "p1") in model["cites"]


def test_recursive_query():
    # Hop(a, c) hides the middle stop of a two-leg trip. Direct(a, b) shows one leg.
    views = {
        "Hop": (("a", "c"), [("e", ("a", "b")), ("e", ("b", "c"))]),
        "Direct": (("a", "b"), [("e", ("a", "b"))]),
    }
    inst = {"Hop": {("1", "3")}, "Direct": {("3", "4"), ("5", "1")}}
    got = inverse_rules_answers(TC, views, inst)
    assert got == {("1", "3"), ("1", "4"), ("3", "4"), ("5", "1"), ("5", "3"), ("5", "4")}
    assert got == certain_by_chase(TC, views, inst)


def test_conjunctive_queries_against_rewritings():
    rng = random.Random(5)
    for _ in range(80):
        views, query = random_views(rng), random_cq(rng)
        for _ in range(3):
            inst = view_image(views, random_db(rng))
            got = inverse_rules_answers(cq_as_program(query), views, inst)
            assert got == brute_rewriting_answers(query, views, inst)


def test_recursive_queries_against_chase_and_sound():
    rng = random.Random(9)
    for _ in range(80):
        views = random_views(rng)
        db = random_db(rng)
        inst = view_image(views, db)
        got = inverse_rules_answers(TC, views, inst)
        assert got == certain_by_chase(TC, views, inst)
        # Sound: each answer holds in the database the views came from.
        assert got <= naive_datalog(TC[0], db).get("path", set())


def test_empty_and_boolean():
    views = {"V": (("a",), [("e", ("a", "b"))])}
    assert inverse_rules_answers(cq_as_program(((), [("e", ("x", "y"))])), views, {"V": set()}) == set()
    assert inverse_rules_answers(cq_as_program(((), [("e", ("x", "y"))])), views, {"V": {("1",)}}) == {()}
    # The hidden value never shows up in an answer.
    assert inverse_rules_answers(cq_as_program((("y",), [("e", ("x", "y"))])), views, {"V": {("1",)}}) == set()
