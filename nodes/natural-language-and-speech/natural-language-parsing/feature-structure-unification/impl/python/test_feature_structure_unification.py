# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feature-structure-unification/. The authors are listed in prov/W1EW4J.jsonl.

import random

from feature_structure_unification import (
    Node,
    build,
    canonical,
    copy,
    get_path,
    subsumes,
    to_spec,
    unify,
    unify_copy,
)


def reference_unify(a, b):
    """Least congruence by naive fixed-point iteration, without union-find.

    Number all nodes of the two graphs, start with the two roots in one class,
    and merge the classes of x.f and y.f whenever x and y are in one class and
    both have the feature f, until nothing changes. Return the canonical form
    of the quotient graph, or None if a class holds two atoms or an atom and a
    feature.
    """
    nodes = []
    index = {}

    def collect(x):
        stack = [x]
        while stack:
            y = stack.pop()
            if id(y) in index:
                continue
            index[id(y)] = len(nodes)
            nodes.append(y)
            stack.extend(y.arcs.values())

    collect(a)
    collect(b)
    n = len(nodes)
    arcs = [{f: index[id(v)] for f, v in x.arcs.items()} for x in nodes]
    cls = list(range(n))

    def merge(i, j):
        ci, cj = cls[i], cls[j]
        if ci == cj:
            return False
        for k in range(n):
            if cls[k] == cj:
                cls[k] = ci
        return True

    merge(index[id(a)], index[id(b)])
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(n):
                if cls[i] != cls[j]:
                    continue
                for f in arcs[i]:
                    if f in arcs[j] and merge(arcs[i][f], arcs[j][f]):
                        changed = True
    atoms = {}
    has_arcs = set()
    for i in range(n):
        c = cls[i]
        if nodes[i].atom is not None:
            atoms.setdefault(c, set()).add(nodes[i].atom)
        if arcs[i]:
            has_arcs.add(c)
    for c, s in atoms.items():
        if len(s) > 1 or c in has_arcs:
            return None
    quotient = {c: Node() for c in set(cls)}
    for c, s in atoms.items():
        quotient[c].atom = next(iter(s))
    for i in range(n):
        for f, j in arcs[i].items():
            quotient[cls[i]].arcs[f] = quotient[cls[j]]
    return canonical(quotient[cls[index[id(a)]]])


def random_structure(rng, size):
    """A random structure with up to size nodes, reentrancy and possible cycles."""
    feats = ["a", "b", "c"]
    root = Node()
    made = [root]
    frontier = [root]
    while frontier and len(made) < size:
        x = frontier.pop(0)
        for f in feats:
            if rng.random() < 0.5:
                continue
            r = rng.random()
            if r < 0.2 and len(made) > 1:
                x.arcs[f] = rng.choice(made)
            elif r < 0.5:
                x.arcs[f] = Node(atom=rng.choice(["x", "y"]))
                made.append(x.arcs[f])
            else:
                y = Node()
                x.arcs[f] = y
                made.append(y)
                frontier.append(y)
    # An atom node must have no arcs; drop the arcs of any atom node.
    for x in made:
        if x.atom is not None:
            x.arcs = {}
    return root


SHIEBER_A = {"agreement": ("#1", {"number": "singular"}), "subject": {"agreement": "#1"}}
SHIEBER_B = {"subject": {"agreement": {"person": "third"}}}


def test_shieber_reentrancy_example():
    r = unify(build(SHIEBER_A), build(SHIEBER_B))
    assert r is not None
    assert to_spec(r) == {
        "agreement": ("#1", {"number": "singular", "person": "third"}),
        "subject": {"agreement": "#1"},
    }
    assert get_path(r, ["agreement"]) is get_path(r, ["subject", "agreement"])


def test_without_reentrancy_the_information_does_not_spread():
    a = build({"agreement": {"number": "singular"}, "subject": {"agreement": {"number": "singular"}}})
    r = unify(a, build(SHIEBER_B))
    assert get_path(r, ["agreement", "person"]) is None
    assert get_path(r, ["subject", "agreement", "person"]).atom == "third"


def test_clash_on_atoms():
    assert unify(build({"number": "singular"}), build({"number": "plural"})) is None


def test_clash_atom_against_complex():
    assert unify(build({"f": "x"}), build({"f": {"g": "x"}})) is None
    assert unify(build("x"), build({"g": "x"})) is None


def test_clash_found_through_reentrancy():
    a = build({"f": ("#1", None), "g": "#1"})
    b = build({"f": "x", "g": "y"})
    assert unify(a, b) is None


def test_empty_structure_is_the_identity():
    rng = random.Random(1)
    for _ in range(50):
        d = random_structure(rng, 8)
        assert canonical(unify(Node(), copy(d))) == canonical(d)
        assert canonical(unify(copy(d), Node())) == canonical(d)


def test_atoms():
    assert unify(build("x"), build("x")).atom == "x"
    assert unify(build("x"), build(None)).atom == "x"
    assert unify(build("x"), build("y")) is None


def test_idempotent():
    rng = random.Random(2)
    for _ in range(200):
        d = random_structure(rng, 10)
        assert canonical(unify(copy(d), copy(d))) == canonical(d)


def test_commutative():
    rng = random.Random(3)
    for _ in range(300):
        a = random_structure(rng, 7)
        b = random_structure(rng, 7)
        ab = unify_copy(a, b)
        ba = unify_copy(b, a)
        assert (ab is None) == (ba is None)
        if ab is not None:
            assert canonical(ab) == canonical(ba)


def test_associative():
    rng = random.Random(4)
    for _ in range(200):
        a, b, c = (random_structure(rng, 6) for _ in range(3))
        ab = unify_copy(a, b)
        left = None if ab is None else unify_copy(ab, c)
        bc = unify_copy(b, c)
        right = None if bc is None else unify_copy(a, bc)
        assert (left is None) == (right is None)
        if left is not None:
            assert canonical(left) == canonical(right)


def test_against_naive_least_congruence():
    rng = random.Random(5)
    fails = 0
    for _ in range(400):
        a = random_structure(rng, 7)
        b = random_structure(rng, 7)
        want = reference_unify(copy(a), copy(b))
        got = unify_copy(a, b)
        if want is None:
            fails += 1
            assert got is None
        else:
            assert got is not None
            assert canonical(got) == want
    assert 20 < fails < 380


def test_result_is_subsumed_by_both_inputs():
    rng = random.Random(6)
    for _ in range(300):
        a = random_structure(rng, 7)
        b = random_structure(rng, 7)
        r = unify_copy(a, b)
        if r is None:
            continue
        assert subsumes(a, r) and subsumes(b, r)


def test_most_general_common_extension():
    # Any structure subsumed by both inputs is subsumed by their unification.
    rng = random.Random(7)
    checked = 0
    for _ in range(400):
        a = random_structure(rng, 5)
        b = random_structure(rng, 5)
        r = unify_copy(a, b)
        if r is None:
            continue
        extra = random_structure(rng, 5)
        bigger = unify_copy(r, extra)
        if bigger is None:
            continue
        assert subsumes(a, bigger) and subsumes(b, bigger)
        assert subsumes(r, bigger)
        checked += 1
    assert checked > 50


def test_inputs_unchanged_by_unify_copy():
    a = build(SHIEBER_A)
    b = build(SHIEBER_B)
    ca, cb = canonical(a), canonical(b)
    unify_copy(a, b)
    assert canonical(a) == ca and canonical(b) == cb


def test_cycle_without_occurs_check():
    a = build({"a": ("#1", None), "b": "#1"})
    b = build({"a": {"h": ("#2", None)}, "b": "#2"})
    r = unify(a, b)
    assert r is not None
    x = get_path(r, ["a"])
    assert get_path(r, ["a", "h"]) is x
    assert get_path(r, ["b", "h", "h", "h"]) is x


def test_subsumption_chain():
    chain = [
        None,
        {"cat": "np"},
        {"cat": "np", "agreement": {"number": "singular"}},
        {"cat": "np", "agreement": {"number": "singular", "person": "third"}},
        {"cat": "np", "agreement": ("#1", {"number": "singular", "person": "third"}), "subject": {"agreement": "#1"}},
    ]
    built = [build(s) for s in chain]
    for i in range(len(built)):
        for j in range(len(built)):
            assert subsumes(built[i], built[j]) == (i <= j)


def test_long_lists_need_no_recursion():
    n = 3000
    a = build(None)
    b = build(None)
    x, y = a, b
    for i in range(n):
        x.arcs["rest"] = Node()
        y.arcs["rest"] = Node()
        x.arcs["first"] = Node(atom="w" + str(i))
        x, y = x.arcs["rest"], y.arcs["rest"]
    r = unify(a, b)
    assert r is not None
    assert get_path(r, ["rest"] * (n - 1) + ["first"]).atom == "w" + str(n - 1)
