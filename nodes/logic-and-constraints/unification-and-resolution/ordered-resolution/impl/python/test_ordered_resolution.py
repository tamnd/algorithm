# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ordered-resolution/. The authors are listed in prov/HD62FE.jsonl.

import itertools
import random

from ordered_resolution import SATURATED, UNKNOWN, UNSAT, kbo_greater, lit_greater, make_clause, no_selection, ordered_resolution, subsumes

# ---------------------------------------------------------------- an independent checker


def app(t, s):
    if isinstance(t, str):
        return app(s[t], s) if t in s and s[t] != t else t
    return (t[0],) + tuple(app(a, s) for a in t[1:])


def has_var(t, v):
    return t == v if isinstance(t, str) else any(has_var(a, v) for a in t[1:])


def mm_unify(a, b):
    eqs, s = [(a, b)], {}
    while eqs:
        x, y = eqs.pop()
        x, y = app(x, s), app(y, s)
        if x == y:
            continue
        if not isinstance(x, str) and isinstance(y, str):
            x, y = y, x
        if isinstance(x, str):
            if has_var(y, x):
                return None
            s = {v: app(t, {x: y}) for v, t in s.items()}
            s[x] = y
        elif x[0] == y[0] and len(x) == len(y):
            eqs.extend(zip(x[1:], y[1:]))
        else:
            return None
    return s


def variant(xs, ys):
    fw, bw = {}, {}

    def go(a, b):
        if isinstance(a, str) or isinstance(b, str):
            return isinstance(a, str) and isinstance(b, str) and fw.setdefault(a, b) == b and bw.setdefault(b, a) == a
        return a[0] == b[0] and len(a) == len(b) and all(go(p, q) for p, q in zip(a[1:], b[1:]))

    return len(xs) == len(ys) and all(go(a, b) for a, b in zip(xs, ys))


def clause_variant(c, d):
    c = list(c)
    return len(c) == len(d) and any(variant([("L", x) for x in c], [("L", y) for y in p]) for p in itertools.permutations(d))


def apply_once(t, s):
    if isinstance(t, str):
        return s.get(t, t)
    return (t[0],) + tuple(apply_once(a, s) for a in t[1:])


def tvars(t):
    return [t] if isinstance(t, str) else [v for a in t[1:] for v in tvars(a)]


def check_mgu(a, b, s):
    assert app(a, s) == app(b, s)
    t = mm_unify(a, b)
    assert t is not None and variant([app(a, s)], [app(a, t)])


def check_refutation(proof, prec, select):
    """Check each step, with the order and selection conditions."""
    table = {}
    for k, c, rule, parents, info in proof:
        if rule == "input":
            table[k] = c
            continue
        i, j, s = info
        p = table[parents[0]]
        ps = [(sg, app(a, s)) for sg, a in p]
        if rule == "factor":
            assert p[i][0] and p[j][0] and select(p) is None
            check_mgu(p[i][1], p[j][1], s)
            assert not any(lit_greater(x, ps[i], prec) for x in ps)
            expect = set(ps)
        else:
            q = [(sg, app(a, {v: v + "'" for v in tvars(a)})) for sg, a in table[parents[1]]]
            qs = [(sg, app(a, s)) for sg, a in q]
            assert p[i][0] != q[j][0]
            check_mgu(p[i][1], q[j][1], s)
            for clause, inst, n in ((p, ps, i), (table[parents[1]], qs, j)):
                others = [x for m, x in enumerate(inst) if m != n]
                if inst[n][0]:
                    assert select(clause) is None
                    assert not any(x == inst[n] or lit_greater(x, inst[n], prec) for x in others)
                elif select(clause) is not None:
                    assert select(clause) == n
                else:
                    assert not any(lit_greater(x, inst[n], prec) for x in others)
            expect = {x for m, x in enumerate(ps) if m != i} | {x for m, x in enumerate(qs) if m != j}
        assert clause_variant(sorted(expect, key=repr), c)
        table[k] = c
    assert proof[-1][1] == ()


# ---------------------------------------------------------------- oracles and helpers


def brute_force_sat(clauses, atoms):
    atoms = sorted(atoms)
    for bits in itertools.product([False, True], repeat=len(atoms)):
        val = dict(zip(atoms, bits))
        if all(any(val[a] == sg for sg, a in c) for c in clauses):
            return True
    return False


def select_last_negative(c):
    negs = [k for k, (sg, _) in enumerate(c) if not sg]
    return negs[-1] if negs else None


def select_first_negative_if_two(c):
    negs = [k for k, (sg, _) in enumerate(c) if not sg]
    return negs[0] if len(negs) >= 2 else None


SELECTIONS = [no_selection, select_last_negative, select_first_negative_if_two]


def pos(*atom):
    return (True, atom)


def neg(*atom):
    return (False, atom)


def random_ground_term(rng, depth):
    if depth == 0 or rng.random() < 0.3:
        return (rng.choice("abc"),)
    f = rng.choice(["f", "g", "h"])
    arity = {"f": 1, "g": 2, "h": 2}[f]
    return (f,) + tuple(random_ground_term(rng, depth - 1) for _ in range(arity))


def random_term(rng, depth):
    if depth == 0 or rng.random() < 0.3:
        return rng.choice(["x", "y", ("a",), ("b",)])
    f = rng.choice(["f", "g"])
    return (f,) + tuple(random_term(rng, depth - 1) for _ in range({"f": 1, "g": 2}[f]))


# ---------------------------------------------------------------- tests


def test_example_of_the_page():
    prec = {"p": 2, "q": 1}
    s = [[pos("p"), pos("q")], [neg("p"), pos("q")], [pos("p"), neg("q")], [neg("p"), neg("q")]]
    res, proof = ordered_resolution(s, prec)
    assert res == UNSAT
    check_refutation(proof, prec, no_selection)
    assert [c for _, c, rule, _, _ in proof if rule != "input"] == [(pos("q"),), (neg("q"),), ()]
    # Without the last clause the set saturates, and the saturated set is q and (not q or p).
    res, active = ordered_resolution(s[:3], prec)
    assert res == SATURATED and sorted(active) == sorted([(pos("q"),), (neg("q"), pos("p"))])


def test_kbo_properties():
    rng = random.Random(1990)
    prec = {"a": 0, "b": 1, "c": 2, "f": 3, "g": 4, "h": 5}
    terms = [random_ground_term(rng, 3) for _ in range(120)]
    for s, t in itertools.product(terms[:60], repeat=2):
        # Total and irreflexive on ground terms.
        assert (s == t) + kbo_greater(s, t, prec) + kbo_greater(t, s, prec) == 1
    for s, t, u in itertools.product(terms[:25], repeat=3):
        if kbo_greater(s, t, prec) and kbo_greater(t, u, prec):
            assert kbo_greater(s, u, prec)
    for s in terms:
        # Subterm property.
        stack = list(s[1:])
        while stack:
            u = stack.pop()
            assert kbo_greater(s, u, prec)
            stack.extend(u[1:])
    checked = 0
    for _ in range(3000):
        s, t = random_term(rng, 3), random_term(rng, 3)
        if not kbo_greater(s, t, prec):
            continue
        checked += 1
        th = {"x": random_term(rng, 2), "y": random_term(rng, 2)}
        assert kbo_greater(apply_once(s, th), apply_once(t, th), prec)  # stable under substitution
        assert kbo_greater(("g", s, ("a",)), ("g", t, ("a",)), prec)  # compatible with contexts
    assert checked > 500


def test_propositional_against_brute_force():
    rng = random.Random(1994)
    seen = {SATURATED: 0, UNSAT: 0}
    for run in range(600):
        n = rng.randint(1, 5)
        names = ["p%d" % k for k in range(n)]
        order = names[:]
        rng.shuffle(order)
        prec = {x: k for k, x in enumerate(order)}
        select = SELECTIONS[run % 3]
        clauses = [[(rng.random() < 0.5, (rng.choice(names),)) for _ in range(rng.randint(1, 3))] for _ in range(rng.randint(1, 12))]
        res, out = ordered_resolution(clauses, prec, select)
        sat = brute_force_sat([make_clause(c) for c in clauses], {(x,) for x in names})
        assert res == (SATURATED if sat else UNSAT)
        seen[res] += 1
        if res == UNSAT:
            check_refutation(out, prec, select)
    assert min(seen.values()) > 100


def test_first_order():
    a, b, c = ("a",), ("b",), ("c",)
    problems = [
        [[pos("P", "x"), pos("P", "y")], [neg("P", "u"), neg("P", "v")]],
        [[neg("S", b, "y"), neg("S", "y", "y")], [pos("S", b, "y"), pos("S", "y", "y")]],
        [[neg("L", "x", "y"), neg("L", "y", "z"), pos("L", "x", "z")], [pos("L", a, b)], [pos("L", b, c)], [neg("L", a, c)]],
        [[pos("P", a), pos("Q", a)], [neg("P", "x"), pos("Q", "x")], [pos("P", "x"), neg("Q", "x")], [neg("P", a), neg("Q", "y")]],
        [[pos("P", a)], [neg("P", "x"), pos("P", ("f", "x"))], [neg("P", ("f", ("f", ("f", a))))]],
    ]
    for prec in ({}, {"P": 5, "Q": 4, "L": 3, "S": 2, "f": 1}):
        for select in SELECTIONS:
            for clauses in problems:
                res, proof = ordered_resolution(clauses, prec, select)
                assert res == UNSAT
                check_refutation(proof, prec, select)
    # P(f(x)) is above P(x), so no inference applies to the second clause, and the set saturates.
    # Unrestricted resolution runs forever on this set.
    assert ordered_resolution([[pos("P", a)], [neg("P", "x"), pos("P", ("f", "x"))]])[0] == SATURATED
    # When the negative literal is selected, the same set gives P(f(a)), P(f(f(a))), and so on.
    assert ordered_resolution([[pos("P", a)], [neg("P", "x"), pos("P", ("f", "x"))]], select=select_last_negative, limit=60)[0] == UNKNOWN
    assert ordered_resolution([[pos("P", a)], [neg("P", "x"), pos("Q", "x")], [neg("Q", b)]])[0] == SATURATED


def test_order_prunes_inferences():
    # With p above q, the clauses p or q and not p or q give q, but q or q is not resolved on q.
    prec = {"p": 2, "q": 1}
    s = [[pos("p"), pos("q")], [neg("q"), pos("p")]]
    res, active = ordered_resolution(s, prec)
    assert res == SATURATED
    assert len(active) == 2


def test_multiset_subsumption():
    a = ("a",)
    # P(x) or P(y) maps both literals to P(a), so it does not subsume P(a) or Q(a).
    assert not subsumes(make_clause([pos("P", "x"), pos("P", "y")]), make_clause([pos("P", a), pos("Q", a)]))
    assert subsumes(make_clause([pos("P", "x"), pos("P", "y")]), make_clause([pos("P", a), pos("P", ("b",))]))
    assert subsumes(make_clause([pos("P", "x")]), make_clause([pos("P", a), neg("Q", a)]))


def test_edges():
    assert ordered_resolution([])[0] == SATURATED
    assert ordered_resolution([[]])[0] == UNSAT
    assert ordered_resolution([[pos("p")], [neg("p")]])[0] == UNSAT
