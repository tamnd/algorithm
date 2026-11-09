# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyperresolution/. The authors are listed in prov/BHQ7B0.jsonl.

import itertools
import random

from hyperresolution import SATURATED, UNKNOWN, UNSAT, hyperresolution, make_clause

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


def check_refutation(proof):
    """Each hyperresolvent clashes all negative literals of an input nucleus with positive electrons."""
    table, inputs = {}, set()
    for k, c, rule, parents, info in proof:
        if rule == "input":
            table[k] = c
            inputs.add(k)
            continue
        if rule == "factor":
            i, j, s = info
            p = table[parents[0]]
            assert all(sg for sg, _ in p) and p[i][0] == p[j][0]
            check_mgu(p[i][1], p[j][1], s)
            expect = {(sg, app(a, s)) for sg, a in p}
        else:
            positions, s = info
            nucleus = table[parents[0]]
            assert parents[0] in inputs
            negs = [a for sg, a in nucleus if not sg]
            assert len(negs) == len(parents) - 1 >= 1
            expect = {(sg, app(a, s)) for sg, a in nucleus if sg}
            left, right = [], []
            for slot, (e_id, p) in enumerate(zip(parents[1:], positions)):
                e = table[e_id]
                assert all(sg for sg, _ in e)
                copy = [(sg, app(a, {v: v + "'%d" % slot for v in tvars(a)})) for sg, a in e]
                left.append(negs[slot])
                right.append(copy[p][1])
                expect |= {(sg, app(a, s)) for q, (sg, a) in enumerate(copy) if q != p}
            check_mgu(("t",) + tuple(left), ("t",) + tuple(right), s)
        assert clause_variant(sorted(expect, key=repr), c)
        assert all(sg for sg, _ in c)
        table[k] = c
    assert proof[-1][1] == ()


# ---------------------------------------------------------------- oracles


def brute_force_sat(clauses, n):
    return any(all(any(bits[a[0]] == sg for sg, a in c) for c in clauses) for bits in itertools.product([False, True], repeat=n))


def pos(*atom):
    return (True, atom)


def neg(*atom):
    return (False, atom)


# ---------------------------------------------------------------- tests


def test_example_of_the_page():
    a, b, c, d = ("a",), ("b",), ("c",), ("d",)
    s = [[neg("L", "x", "y"), neg("L", "y", "z"), pos("L", "x", "z")], [pos("L", a, b)], [pos("L", b, c)], [pos("L", c, d)], [neg("L", a, d)]]
    res, proof = hyperresolution(s)
    assert res == UNSAT
    check_refutation(proof)
    derived = [c for _, c, rule, _, _ in proof if rule == "hyper"]
    assert derived[-1] == ()
    assert all(len(c) <= 1 for c in derived)


def test_propositional_against_brute_force():
    rng = random.Random(1965)
    seen = {SATURATED: 0, UNSAT: 0}
    for _ in range(500):
        n = rng.randint(1, 5)
        clauses = []
        for _ in range(rng.randint(1, 12)):
            w = rng.randint(1, 3)
            clauses.append([(rng.random() < 0.5, (rng.randrange(n),)) for _ in range(w)])
        res, out = hyperresolution(clauses)
        sat = brute_force_sat([make_clause(c) for c in clauses], n)
        assert res == (SATURATED if sat else UNSAT)
        seen[res] += 1
        if res == UNSAT:
            check_refutation(out)
        else:
            # Every saturated set is positive and is implied by the input.
            assert all(all(sg for sg, _ in c) for c in out)
    assert min(seen.values()) > 100


def test_first_order():
    a, b, c = ("a",), ("b",), ("c",)
    problems = [
        [[pos("P", "x"), pos("P", "y")], [neg("P", "u"), neg("P", "v")]],
        [[neg("S", b, "y"), neg("S", "y", "y")], [pos("S", b, "y"), pos("S", "y", "y")]],
        [[neg("L", "x", "y"), neg("L", "y", "z"), pos("L", "x", "z")], [pos("L", a, b)], [pos("L", b, c)], [neg("L", a, c)]],
        [[pos("P", a), pos("Q", a)], [neg("P", "x"), pos("Q", "x")], [pos("P", "x"), neg("Q", "x")], [neg("P", a), neg("Q", "y")]],
        [[pos("P", a)], [neg("P", "x"), pos("P", ("f", "x"))], [neg("P", ("f", ("f", ("f", a))))]],
        [[pos("D", "x")], [neg("D", ("sk",))]],
    ]
    for clauses in problems:
        res, proof = hyperresolution(clauses)
        assert res == UNSAT
        check_refutation(proof)
    assert hyperresolution([[pos("P", a)], [neg("P", "x"), pos("P", ("f", "x"))]], limit=60)[0] == UNKNOWN
    assert hyperresolution([[pos("P", a)], [neg("P", "x"), pos("Q", "x")], [neg("Q", b)]])[0] == SATURATED


def test_no_positive_clause_saturates_at_once():
    s = [[neg("p"), neg("q")], [neg("p"), pos("q")], [neg("r")]]
    res, active = hyperresolution(s)
    assert res == SATURATED and active == []


def test_edges():
    assert hyperresolution([])[0] == SATURATED
    assert hyperresolution([[]])[0] == UNSAT
    assert hyperresolution([[pos("p")], [neg("p")]])[0] == UNSAT
