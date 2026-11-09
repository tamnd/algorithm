# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unit-resolution/. The authors are listed in prov/HX313Y.jsonl.

import itertools
import random

from unit_resolution import SATURATED, UNKNOWN, UNSAT, make_clause, unit_resolution

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


def tvars(t):
    return [t] if isinstance(t, str) else [v for a in t[1:] for v in tvars(a)]


def check_mgu(a, b, s):
    assert app(a, s) == app(b, s)
    t = mm_unify(a, b)
    assert t is not None and variant([app(a, s)], [app(a, t)])


def check_refutation(proof, unit_parent=True):
    table = {}
    for k, c, rule, parents, info in proof:
        if rule == "input":
            table[k] = c
            continue
        i, j, s = info
        p = table[parents[0]]
        if rule == "factor":
            assert p[i][0] == p[j][0]
            check_mgu(p[i][1], p[j][1], s)
            expect = {(sg, app(a, s)) for sg, a in p}
        else:
            q = [(sg, app(a, {v: v + "'" for v in tvars(a)})) for sg, a in table[parents[1]]]
            if unit_parent:
                assert len(p) == 1 or len(q) == 1
            assert p[i][0] != q[j][0]
            check_mgu(p[i][1], q[j][1], s)
            expect = {(sg, app(a, s)) for n, (sg, a) in enumerate(p) if n != i}
            expect |= {(sg, app(a, s)) for n, (sg, a) in enumerate(q) if n != j}
        assert clause_variant(sorted(expect, key=repr), c)
        table[k] = c
    assert proof[-1][1] == ()


# ---------------------------------------------------------------- oracles


def brute_force_sat(clauses, n):
    return any(all(any(bits[a[0]] == sg for sg, a in c) for c in clauses) for bits in itertools.product([False, True], repeat=n))


def propagation_conflict(clauses):
    """Plain unit propagation, written apart from the code under test."""
    val = {}
    while True:
        unit = None
        for c in clauses:
            if any(val.get(a) == sg for sg, a in c):
                continue
            open_lits = [(sg, a) for sg, a in c if a not in val]
            if not open_lits:
                return True
            if len(open_lits) == 1:
                unit = open_lits[0]
                break
        if unit is None:
            return False
        val[unit[1]] = unit[0]


def random_clauses(rng, n, m, horn, min_width=1):
    out = []
    for _ in range(m):
        w = rng.randint(min_width, 3)
        atoms = [rng.randrange(n) for _ in range(w)]
        signs = [rng.random() < 0.5 for _ in range(w)]
        if horn and signs.count(True) > 1:
            first = signs.index(True)
            signs = [k == first for k in range(w)]
        out.append([(sg, (a,)) for sg, a in zip(signs, atoms)])
    return out


def pos(*atom):
    return (True, atom)


def neg(*atom):
    return (False, atom)


# ---------------------------------------------------------------- tests


def test_example_of_the_page():
    s = [[neg("p"), neg("q"), pos("r")], [neg("r"), pos("s")], [pos("p")], [pos("q")], [neg("s")]]
    res, proof = unit_resolution(s)
    assert res == UNSAT
    check_refutation(proof)


def test_counterexample_has_no_unit_refutation():
    s = [[pos("p"), pos("q")], [neg("p"), pos("q")], [pos("p"), neg("q")], [neg("p"), neg("q")]]
    assert unit_resolution(s)[0] == SATURATED
    assert not any(all(any((sg == (b[0] if a == ("p",) else b[1])) for sg, a in c) for c in s) for b in itertools.product([False, True], repeat=2))


def test_horn_sets_against_brute_force():
    rng = random.Random(1974)
    seen = set()
    for _ in range(600):
        n = rng.randint(1, 6)
        clauses = random_clauses(rng, n, rng.randint(1, 12), horn=True)
        res, out = unit_resolution(clauses)
        sat = brute_force_sat([make_clause(c) for c in clauses], n)
        assert res == (SATURATED if sat else UNSAT)
        seen.add(res)
        if res == UNSAT:
            check_refutation(out)
    assert seen == {SATURATED, UNSAT}


def test_general_sets_match_unit_propagation():
    rng = random.Random(1970)
    misses = 0
    for _ in range(600):
        n = rng.randint(2, 4)
        clauses = random_clauses(rng, n, rng.randint(4, 16), horn=False, min_width=rng.randint(1, 2))
        res, out = unit_resolution(clauses)
        cl = [make_clause(c) for c in clauses]
        assert (res == UNSAT) == propagation_conflict(cl)
        if res == UNSAT:
            assert not brute_force_sat(cl, n)
            check_refutation(out)
        elif not brute_force_sat(cl, n):
            misses += 1
    assert misses > 0


def test_first_order_horn():
    a, b, c, d = ("a",), ("b",), ("c",), ("d",)
    problems = [
        [[neg("Man", "x"), pos("Mortal", "x")], [pos("Man", ("socrates",))], [neg("Mortal", ("socrates",))]],
        [[neg("L", "x", "y"), neg("L", "y", "z"), pos("L", "x", "z")], [pos("L", a, b)], [pos("L", b, c)], [pos("L", c, d)], [neg("L", a, d)]],
        [[pos("P", a)], [neg("P", "x"), pos("P", ("f", "x"))], [neg("P", ("f", ("f", a)))]],
        [[pos("P", "x")], [neg("P", "u"), neg("P", "v")]],
    ]
    for clauses in problems:
        res, proof = unit_resolution(clauses)
        assert res == UNSAT
        check_refutation(proof)
    assert unit_resolution([[pos("P", a)], [neg("P", "x"), pos("P", ("f", "x"))]], limit=60)[0] == UNKNOWN
    assert unit_resolution([[pos("P", a)], [neg("P", "x"), pos("Q", "x")], [neg("Q", b)]])[0] == SATURATED


def test_edges():
    assert unit_resolution([])[0] == SATURATED
    assert unit_resolution([[]])[0] == UNSAT
    assert unit_resolution([[pos("p")], [neg("p")]])[0] == UNSAT
