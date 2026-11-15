# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/perfectref-rewriting/. The authors are listed in prov/4TB81W.jsonl.
"""Tests of PerfectRef against certain answers computed by a chase.

The reference builds the restricted chase of the ABox with the TBox, cut at depth
m + 2|P| + 1, where m is the number of query atoms and |P| the number of role names. Concept and
role inclusions are applied to a fixpoint before each new element is made, so the part of the
chase below an anonymous element depends only on the role that made it. A match of a connected
part of the query that uses only anonymous elements can then be moved up to depth at most
2|P| + m, and a part that touches the ABox stays within depth m of it. So the cut chase has a
match exactly when the full chase has one, and the full chase is a universal model: its answers on
named individuals are the certain answers.
"""

import random
from itertools import product

from perfectref_rewriting import UNBOUND, evaluate_cq, evaluate_ucq, perfect_ref, reduce_pair, rewrite_atom, tau


def chase(tbox_ci, tbox_ri, abox, depth_limit: int):
    """The restricted chase, cut at depth_limit. Inclusions without existentials are applied to a
    fixpoint before each new element is made, and new elements are made in order of depth."""
    conc: set = set()
    roles: set = set()
    has: set = set()  # basic concepts that hold: ("A", name, x) and ("E", p, inverse, x)
    depth: dict = {}
    for _, x in abox[0]:
        depth[x] = 0
    for _, x, y in abox[1]:
        depth[x] = depth[y] = 0
    order = {x: k for k, x in enumerate(sorted(depth))}  # the order in which elements were made
    by_lhs: dict = {}
    for lhs, rhs in tbox_ci:
        by_lhs.setdefault(lhs, []).append(rhs)
    queue: list = [("C", a, x) for a, x in abox[0]] + [("R", p, x, y) for p, x, y in abox[1]]
    # Existentials to check later, as (depth of x, order of x, rhs, x). Each element handles its own
    # existentials in a fixed order, so the part below an anonymous element depends only on the
    # role that made it.
    needs: list = []
    fresh = 0

    def basic(b: tuple, x) -> None:
        key = b + (x,)
        if key in has:
            return
        has.add(key)
        for rhs in by_lhs.get(b, ()):
            if rhs[0] == "A":
                queue.append(("C", rhs[1], x))
            else:
                needs.append((depth[x], order[x], rhs, x))

    while True:
        while queue:
            f = queue.pop()
            if f[0] == "C":
                if (f[1], f[2]) in conc:
                    continue
                conc.add((f[1], f[2]))
                basic(("A", f[1]), f[2])
                continue
            _, p, x, y = f
            if (p, x, y) in roles:
                continue
            roles.add((p, x, y))
            basic(("E", p, False), x)
            basic(("E", p, True), y)
            for r1, r2 in tbox_ri:
                if r1[0] != p:
                    continue
                a, b = (x, y) if not r1[1] else (y, x)  # (a, b) is in r1
                queue.append(("R", r2[0], a, b) if not r2[1] else ("R", r2[0], b, a))
        needs.sort(key=lambda t: t[:3])
        while needs:
            d, _, rhs, x = needs.pop(0)
            if d < depth_limit and rhs + (x,) not in has:
                break
        else:
            return conc, roles, depth
        fresh += 1
        y = ("null", fresh)
        depth[y] = d + 1
        order[y] = len(order)
        queue.append(("R", rhs[1], x, y) if not rhs[2] else ("R", rhs[1], y, x))


def certain_answers(query, tbox_ci, tbox_ri, abox) -> set:
    head, body = query
    role_names = {g[1] for g in body if g[0] == "R"} | {b[1] for ci in tbox_ci for b in ci if b[0] == "E"}
    role_names |= {r[0] for ri in tbox_ri for r in ri} | {p for p, _, _ in abox[1]}
    d = len(body) + 2 * len(role_names) + 1
    conc, roles, depth = chase(tbox_ci, tbox_ri, abox, d)
    named = {x for x in depth if depth[x] == 0}
    return {t for t in evaluate_cq(query, (conc, roles)) if all(v in named for v in t)}


def C(a, t):
    return ("C", a, t)


def R(p, t1, t2):
    return ("R", p, t1, t2)


def test_paper_style_example() -> None:
    # Professor is subsumed by some teaches; some teaches^- is subsumed by Course.
    ci = [(("A", "Professor"), ("E", "teaches", False)), (("E", "teaches", True), ("A", "Course"))]
    q = (("x",), frozenset({R("teaches", "x", "y"), C("Course", "y")}))
    ucq = perfect_ref(q, ci)
    bodies = {b for _, b in ucq}
    assert frozenset({R("teaches", "x", UNBOUND)}) in bodies
    assert frozenset({C("Professor", "x")}) in bodies
    assert len(ucq) == 4
    abox = ({("Professor", "ann")}, {("teaches", "bob", "c1")})
    assert evaluate_ucq(ucq, abox) == {("ann",), ("bob",)}
    assert evaluate_cq(q, abox) == set()  # without the TBox, the query finds nothing
    assert certain_answers(q, ci, [], abox) == {("ann",), ("bob",)}


def test_tau_and_reduce() -> None:
    q = tau(("x",), [R("r", "x", "y"), R("r", "x", "z"), C("A", "z")])
    assert q[1] == frozenset({R("r", "x", UNBOUND), R("r", "x", "z"), C("A", "z")})
    red = reduce_pair(q, R("r", "x", UNBOUND), R("r", "x", "z"))
    assert red[1] == frozenset({R("r", "x", "z"), C("A", "z")})
    assert reduce_pair(q, R("r", "x", "z"), C("A", "z")) is None


def test_bound_variable_blocks_existential() -> None:
    # A is subsumed by some r. The atom r(x, y) with y bound cannot be rewritten into A(x).
    ci = [(("A", "A"), ("E", "r", False))]
    assert rewrite_atom(R("r", "x", "y"), ci, []) == []
    assert rewrite_atom(R("r", "x", UNBOUND), ci, []) == [C("A", "x")]


def exponential_family(n: int):
    ci = [(("A", f"B{i}"), ("A", f"A{i}")) for i in range(1, n + 1)]
    q = (("x",), frozenset(C(f"A{i}", "x") for i in range(1, n + 1)))
    return q, ci


def test_exponential_rewriting() -> None:
    for n in range(1, 9):
        q, ci = exponential_family(n)
        ucq = perfect_ref(q, ci)
        assert len(ucq) == 2 ** n
    # Every UCQ rewriting needs 2^n queries: the ABox that puts a in one of A_i, B_i for each i
    # has a as an answer, and a CQ that matches it uses exactly those atoms.
    n = 4
    q, ci = exponential_family(n)
    ucq = perfect_ref(q, ci)
    for choice in product((0, 1), repeat=n):
        abox = ({(("A" if c == 0 else "B") + str(i + 1), "a") for i, c in enumerate(choice)}, set())
        hits = [u for u in ucq if evaluate_cq(u, abox)]
        assert len(hits) == 1
        assert certain_answers(q, ci, [], abox) == {("a",)}


def rand_basic(rng: random.Random, cn, rn) -> tuple:
    if rng.random() < 0.5:
        return ("A", rng.choice(cn))
    return ("E", rng.choice(rn), rng.random() < 0.5)


def rand_instance(rng: random.Random):
    cn, rn = ["A", "B", "C"], ["p", "s"]
    ci = [(rand_basic(rng, cn, rn), rand_basic(rng, cn, rn)) for _ in range(rng.randint(2, 5))]
    ri = []
    if rng.random() < 0.5:
        r1 = (rng.choice(rn), rng.random() < 0.5)
        r2 = (rng.choice(rn), rng.random() < 0.5)
        if r1[0] != r2[0] or r1[1] != r2[1]:
            ri.append((r1, r2))
    inds = ["a", "b", "c"]
    conc = {(rng.choice(cn), rng.choice(inds)) for _ in range(rng.randint(0, 3))}
    roles = {(rng.choice(rn), rng.choice(inds), rng.choice(inds)) for _ in range(rng.randint(0, 2))}
    vars_ = ["x", "y", "z"] if rng.random() < 0.3 else ["x", "y"]
    body = set()
    for _ in range(rng.randint(2, 3)):
        if rng.random() < 0.45:
            body.add(C(rng.choice(cn), rng.choice(vars_)))
        else:
            body.add(R(rng.choice(rn), rng.choice(vars_), rng.choice(vars_)))
    used = sorted({t for g in body for t in g[2:]})
    k = rng.randint(0, min(2, len(used)))
    head = tuple(rng.sample(used, k))
    return (head, frozenset(body)), ci, ri, (conc, roles)


def test_random_against_chase() -> None:
    rng = random.Random(31)
    tbox_matters = 0
    for _ in range(1500):
        q, ci, ri, abox = rand_instance(rng)
        got = evaluate_ucq(perfect_ref(q, ci, ri), abox)
        want = certain_answers(q, ci, ri, abox)
        assert got == want, (q, ci, ri, abox)
        if want != evaluate_cq(q, abox):
            tbox_matters += 1  # the TBox adds answers that the ABox alone does not give
    assert tbox_matters >= 100


def test_rewriting_is_finite_on_cycles() -> None:
    # Cyclic inclusions: some p is subsumed by some p^- and back, A is subsumed by some p.
    ci = [(("E", "p", False), ("E", "p", True)), (("E", "p", True), ("E", "p", False)), (("A", "A"), ("E", "p", False))]
    ri = [(("p", False), ("p", True))]
    q = (("x",), frozenset({R("p", "x", "y"), R("p", "y", "z")}))
    ucq = perfect_ref(q, ci, ri)
    assert 0 < len(ucq) < 200
