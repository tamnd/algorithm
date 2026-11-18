# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/holistic-twig-join/. The authors are listed in prov/JKP2FG.jsonl.

import random
from collections import Counter

import dbrel
from holistic_twig_join import Twig, encode, is_ancestor, twig_stack, useless

# The example of the page: a1(b1, a2(b2, c1), c2, a3(b3)).
NAMES = ["a1", "b1", "a2", "b2", "c1", "c2", "a3", "b3"]
PARENT = [-1, 0, 0, 2, 2, 0, 0, 6]


def oracle(twig: Twig, elems: list) -> Counter:
    """The twig as a chain of theta joins over one relation (start, end, level) per query node."""
    db = {}
    for q, tag in enumerate(twig.tag):
        db["E%d" % q] = dbrel.Relation(("s%d" % q, "e%d" % q, "l%d" % q),
                                       [(e.start, e.end, e.level) for e in elems if e.tag == tag])
    expr = ("scan", "E0")
    for q in range(1, len(twig.tag)):
        p, pc = twig.parent[q], twig.axis[q] == "/"

        def edge(r, p=p, q=q, pc=pc):
            inside = r["s%d" % p] < r["s%d" % q] and r["e%d" % q] < r["e%d" % p]
            return inside and (not pc or r["l%d" % q] == r["l%d" % p] + 1)

        expr = ("theta_join", edge, expr, ("scan", "E%d" % q))
    rel = dbrel.evaluate(expr, db)
    rel = dbrel.project(rel, ["s%d" % q for q in range(len(twig.tag))])
    return Counter(rel.rows)


def as_starts(matches: list) -> Counter:
    return Counter(tuple(e.start for e in m) for m in matches)


def random_doc(rng: random.Random, n: int) -> list:
    tags = [rng.choice("abc") for _ in range(n)]
    parent = [-1] + [rng.randrange(i) for i in range(1, n)]
    return encode(tags, parent[:n])


def random_twig(rng: random.Random, k: int, pc_rate: float) -> Twig:
    nodes = [(rng.choice("abc"), -1, None)]
    for q in range(1, k):
        nodes.append((rng.choice("abc"), rng.randrange(q), "/" if rng.random() < pc_rate else "//"))
    return Twig(nodes)


def test_region_encoding() -> None:
    elems = encode([n[0] for n in NAMES], PARENT)
    assert [(e.start, e.end, e.level) for e in elems[:3]] == [(0, 15, 0), (1, 2, 1), (3, 8, 1)]

    def anc(u, v):
        while PARENT[v] >= 0:
            v = PARENT[v]
            if v == u:
                return True
        return False

    for u in range(len(NAMES)):
        for v in range(len(NAMES)):
            assert is_ancestor(elems[u], elems[v]) == anc(u, v)


def test_example() -> None:
    elems = encode([n[0] for n in NAMES], PARENT)
    name = {e: NAMES[i] for i, e in enumerate(elems)}
    twig = Twig([("a", -1, None), ("b", 0, "//"), ("c", 0, "//")])
    matches, stats = twig_stack(twig, elems)
    steps = [(twig.tag[q], name[e], act) for q, e, act in stats["steps"]]
    assert steps == [("a", "a1", "push"), ("b", "b1", "push"), ("a", "a2", "push"), ("b", "b2", "push"),
                     ("c", "c1", "push"), ("c", "c2", "push"), ("a", "a3", "drop"), ("b", "b3", "push")]
    paths = {leaf: [tuple(name[e] for e in s) for s in sols] for leaf, sols in stats["path_solutions"].items()}
    assert paths == {1: [("a1", "b1"), ("a1", "b2"), ("a2", "b2"), ("a1", "b3")],
                     2: [("a1", "c1"), ("a2", "c1"), ("a1", "c2")]}
    assert len(matches) == 7 and ("a2", "b2", "c1") in [tuple(name[e] for e in m) for m in matches]
    assert useless(twig, stats["path_solutions"], matches) == 0


def test_random_against_dbrel() -> None:
    rng = random.Random(2)
    for trial in range(150):
        elems = random_doc(rng, rng.randrange(0, 31))
        twig = random_twig(rng, rng.randrange(1, 5), rng.choice([0.0, 0.5, 1.0]))
        matches, _ = twig_stack(twig, elems)
        assert as_starts(matches) == oracle(twig, elems)


def test_ancestor_descendant_twigs_have_no_useless_path_solutions() -> None:
    rng = random.Random(3)
    for trial in range(400):
        elems = random_doc(rng, rng.randrange(1, 60))
        twig = random_twig(rng, rng.randrange(1, 6), 0.0)
        matches, stats = twig_stack(twig, elems)
        assert useless(twig, stats["path_solutions"], matches) == 0
        used = {(q, m[q]) for m in matches for q in range(len(twig.tag))}
        taken = [(q, e) for q, e, act in stats["steps"]]
        assert all(act == "push" for q, e, act in stats["steps"] if (q, e) in used)
        assert used <= set(taken)


def test_parent_child_edge_gives_useless_path_solution() -> None:
    elems = encode(["a", "b", "c"], [-1, 0, 1])
    twig = Twig([("a", -1, None), ("b", 0, "//"), ("c", 0, "/")])
    matches, stats = twig_stack(twig, elems)
    assert matches == []
    assert [tuple(e.tag for e in s) for s in stats["path_solutions"][1]] == [("a", "b")]
    assert useless(twig, stats["path_solutions"], matches) == 1


def test_edges() -> None:
    one = Twig([("a", -1, None)])
    assert twig_stack(one, [])[0] == []
    elems = encode(["a", "a", "b"], [-1, 0, 1])
    assert [tuple(e.start for e in m) for m in twig_stack(one, elems)[0]] == [(0,), (1,)]
    assert twig_stack(Twig([("a", -1, None), ("c", 0, "//")]), elems)[0] == []
    # Two query nodes with the same tag on one path: a//a.
    assert as_starts(twig_stack(Twig([("a", -1, None), ("a", 0, "//")]), elems)[0]) == Counter({(0, 1): 1})
    # Two sibling query nodes may map to the same element.
    sib = Twig([("a", -1, None), ("b", 0, "//"), ("b", 0, "//")])
    assert as_starts(twig_stack(sib, elems)[0]) == Counter({(0, 2, 2): 1, (1, 2, 2): 1})
