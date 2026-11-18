# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/data-exchange-core-computation/. The authors are listed in prov/6E0XMM.jsonl.

import itertools
import random

from data_exchange_core_computation import (
    Null,
    chase,
    core,
    core_solution,
    is_null,
    null_blocks,
)

D1 = ([("Flight", ("x", "y"))], [("Leg", ("x", "z")), ("Leg", ("z", "y"))])
D2 = ([("Flight", ("x", "y"))], [("Leg", ("x", "u"))])
I = {("Flight", ("a", "b")), ("Flight", ("b", "c"))}


def nulls_of(inst):
    return sorted({v for _, t in inst for v in t if is_null(v)}, key=lambda n: n.id)


def adom(inst):
    return sorted({v for _, t in inst for v in t}, key=repr)


def image(h, inst):
    return {(r, tuple(h.get(v, v) for v in t)) for r, t in inst}


def endomorphisms(inst):
    """All maps from the nulls to the values of inst that map inst into itself, by brute force."""
    ns, vals = nulls_of(inst), adom(inst)
    for combo in itertools.product(vals, repeat=len(ns)):
        h = dict(zip(ns, combo))
        if image(h, inst) <= inst:
            yield h


def maps_into(src, dst):
    ns, vals = nulls_of(src), adom(dst)
    return any(image(dict(zip(ns, c)), src) <= dst for c in itertools.product(vals, repeat=len(ns)))


def isomorphic(c1, c2):
    n1, n2 = nulls_of(c1), nulls_of(c2)
    if len(c1) != len(c2) or len(n1) != len(n2):
        return False
    return any(image(dict(zip(n1, p)), c1) == c2 for p in itertools.permutations(n2))


def satisfies(source, tgds, target):
    """Brute force: each match of a body in the source has a witness for the head in the target."""
    vals_s = sorted({v for _, t in source for v in t})
    vals_t = adom(target)
    for body, head in tgds:
        bv = sorted({x for _, ts in body for x in ts})
        ev = sorted({x for _, ts in head for x in ts} - set(bv))
        for c in itertools.product(vals_s, repeat=len(bv)):
            m = dict(zip(bv, c))
            if all((r, tuple(m[x] for x in ts)) in source for r, ts in body):
                if not any(all((r, tuple({**m, **dict(zip(ev, d))}[x] for x in ts)) in target for r, ts in head)
                           for d in itertools.product(vals_t, repeat=len(ev))):
                    return False
    return True


def naive_eval(query, inst):
    """The null-free answers of a CQ (head variables, body atoms) by brute force."""
    hv, body = query
    vs = sorted({x for _, ts in body for x in ts})
    vals = adom(inst)
    out = set()
    for c in itertools.product(vals, repeat=len(vs)):
        m = dict(zip(vs, c))
        if all((r, tuple(m[x] for x in ts)) in inst for r, ts in body):
            ans = tuple(m[x] for x in hv)
            if not any(is_null(v) for v in ans):
                out.add(ans)
    return out


def random_setting(rng):
    """Small random source instance and s-t tgds over S(2), P(1) into T(2), U(1)."""
    consts = ["a", "b", "c"]
    source = set()
    for _ in range(rng.randint(1, 3)):
        source.add(("S", (rng.choice(consts), rng.choice(consts))))
    if rng.random() < 0.5:
        source.add(("P", (rng.choice(consts),)))
    tgds = []
    for _ in range(rng.randint(1, 3)):
        body = [("S", ("x0", "x1"))] if rng.random() < 0.8 else [("P", ("x0",))]
        bvars = sorted({x for _, ts in body for x in ts})
        terms = bvars + ["y0", "y1"][: rng.randint(0, 2)]
        head = []
        for _ in range(rng.randint(1, 3)):
            if rng.random() < 0.7:
                head.append(("T", (rng.choice(terms), rng.choice(terms))))
            else:
                head.append(("U", (rng.choice(terms),)))
        tgds.append((body, head))
    return source, tgds


def random_query(rng):
    vs = ["v0", "v1", "v2"]
    body = []
    for _ in range(rng.randint(1, 3)):
        if rng.random() < 0.75:
            body.append(("T", (rng.choice(vs), rng.choice(vs))))
        else:
            body.append(("U", (rng.choice(vs),)))
    used = sorted({x for _, ts in body for x in ts})
    return (used[: rng.randint(0, len(used))], body)


def test_example():
    j = chase(I, [D1, D2])
    n = {k: Null(k) for k in range(1, 5)}
    assert j == {("Leg", ("a", n[1])), ("Leg", (n[1], "b")), ("Leg", ("b", n[2])), ("Leg", (n[2], "c")),
                 ("Leg", ("a", n[3])), ("Leg", ("b", n[4]))}
    assert null_blocks(j) == [[n[1]], [n[2]], [n[3]], [n[4]]]
    c = core(j)
    assert c == {("Leg", ("a", n[1])), ("Leg", (n[1], "b")), ("Leg", ("b", n[2])), ("Leg", (n[2], "c"))}
    assert core_solution(I, [D1, D2]) == c
    q2 = (["x", "y"], [("Leg", ("x", "z")), ("Leg", ("z", "y"))])
    assert naive_eval(q2, c) == {("a", "b"), ("b", "c")}
    assert naive_eval((["x", "y"], [("Leg", ("x", "y"))]), c) == set()


def test_constant_absorbs_null():
    # S(x, y) -> exists z T(x, z), and S(x, y) -> T(x, y): the null folds onto the constant.
    tgds = [([("S", ("x", "y"))], [("T", ("x", "z"))]), ([("S", ("x", "y"))], [("T", ("x", "y"))])]
    c = core_solution({("S", ("a", "b"))}, tgds)
    assert c == {("T", ("a", "b"))}


def test_against_brute_force():
    rng = random.Random(2024)
    checked = 0
    while checked < 60:
        source, tgds = random_setting(rng)
        j = chase(source, tgds)
        if len(nulls_of(j)) > 4:
            continue
        checked += 1
        c = core(j)
        assert c <= j
        assert satisfies(source, tgds, c)
        assert maps_into(j, c)
        # The smallest image of an endomorphism of j is the core, so its size is |c|.
        assert min(len(image(h, j)) for h in endomorphisms(j)) == len(c)
        # c has no proper endomorphism.
        assert all(image(h, c) == c for h in endomorphisms(c))
        # A different universal solution has an isomorphic core.
        j2 = chase(source, list(reversed(tgds)) + tgds[:1], first_null=100)
        assert isomorphic(core(j2), c)
        # Certain answers of CQs by naive evaluation agree on j and on its core.
        for _ in range(3):
            q = random_query(rng)
            assert naive_eval(q, j) == naive_eval(q, c)


def test_edges():
    assert chase(set(), [D1]) == set()
    assert core(set()) == set()
    ground = {("T", ("a", "b"))}
    assert core(ground) == ground
    # A block of two nulls that folds onto a constant, and a block that is already a core.
    n1, n2 = Null(1), Null(2)
    inst = {("T", ("a", n1)), ("T", (n1, n2)), ("T", ("a", "b")), ("T", ("b", "b"))}
    assert core(inst) == {("T", ("a", "b")), ("T", ("b", "b"))}
    loop = {("T", ("a", n1)), ("T", (n1, n2)), ("T", (n2, n2))}
    assert core(loop) == loop
