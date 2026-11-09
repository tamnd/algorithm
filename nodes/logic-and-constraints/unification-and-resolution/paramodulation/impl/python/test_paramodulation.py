# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paramodulation/. The authors are listed in prov/9GTMK7.jsonl.

import itertools
import random

from paramodulation import SATURATED, UNKNOWN, UNSAT, make_clause, paramodulation

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


def put(t, path, new):
    if not path:
        return new
    k = path[0]
    return t[:k] + (put(t[k], path[1:], new),) + t[k + 1:]


def check_refutation(proof):
    table = {}
    for k, c, rule, parents, info in proof:
        if rule == "input":
            table[k] = c
            continue
        p = table[parents[0]]
        if rule == "factor":
            i, j, s = info
            assert p[i][0] == p[j][0]
            check_mgu(p[i][1], p[j][1], s)
            expect = {(sg, app(a, s)) for sg, a in p}
        else:
            q = [(sg, app(a, {v: v + "'" for v in tvars(a)})) for sg, a in table[parents[1]]]
            if rule == "resolve":
                i, j, s = info
                assert p[i][0] != q[j][0]
                check_mgu(p[i][1], q[j][1], s)
                expect = {(sg, app(a, s)) for n, (sg, a) in enumerate(p) if n != i}
                expect |= {(sg, app(a, s)) for n, (sg, a) in enumerate(q) if n != j}
            else:
                i, side, j, path, s = info
                sg, eq = p[i]
                assert sg and eq[0] == "="
                u = q[j][1]
                for x in path:
                    u = u[x]
                assert not isinstance(u, str) and path[0] >= 1
                check_mgu(eq[side], u, s)
                expect = {(g, app(a, s)) for n, (g, a) in enumerate(p) if n != i}
                expect |= {(g, app(a, s)) for n, (g, a) in enumerate(q) if n != j}
                expect.add((q[j][0], app(put(q[j][1], path, eq[3 - side]), s)))
        assert clause_variant(sorted(expect, key=repr), c)
        table[k] = c
    assert proof[-1][1] == ()


# ---------------------------------------------------------------- a ground oracle


def subterm_closure(terms):
    out, stack = set(), list(terms)
    while stack:
        t = stack.pop()
        if t not in out:
            out.add(t)
            stack.extend(t[1:])
    return out


def congruence_classes(terms, equations):
    """Naive congruence closure on the finite set terms."""
    rep = {t: t for t in terms}

    def find(t):
        while rep[t] != t:
            t = rep[t]
        return t

    for s, t in equations:
        rep[find(s)] = find(t)
    changed = True
    while changed:
        changed = False
        for s, t in itertools.combinations(terms, 2):
            if find(s) != find(t) and s[0] == t[0] and len(s) == len(t) and all(find(a) == find(b) for a, b in zip(s[1:], t[1:])):
                rep[find(s)] = find(t)
                changed = True
    return find


def ground_equational_sat(clauses):
    """A set of ground equational clauses is satisfiable iff some choice of true atoms is consistent with congruence."""
    atoms = sorted({a for c in clauses for _, a in c}, key=repr)
    terms = subterm_closure([x for a in atoms for x in a[1:]])
    for bits in itertools.product([False, True], repeat=len(atoms)):
        val = dict(zip(atoms, bits))
        if not all(any(val[a] == sg for sg, a in c) for c in clauses):
            continue
        find = congruence_classes(terms, [(a[1], a[2]) for a in atoms if val[a]])
        if all(find(a[1]) != find(a[2]) for a in atoms if not val[a]):
            return True
    return False


def random_ground_term(rng, depth):
    if depth == 0 or rng.random() < 0.5:
        return (rng.choice("ab"),)
    return ("f", random_ground_term(rng, depth - 1))


def eq(s, t):
    return (True, ("=", s, t))


def ne(s, t):
    return (False, ("=", s, t))


def pos(*atom):
    return (True, atom)


def neg(*atom):
    return (False, atom)


# ---------------------------------------------------------------- tests


def test_example_of_the_page():
    a = ("a",)
    s = [[eq(("f", "x"), ("g", "x"))], [pos("P", ("f", a))], [neg("P", ("g", a))]]
    res, proof = paramodulation(s)
    assert res == UNSAT
    check_refutation(proof)
    assert [c for _, c, rule, _, _ in proof if rule != "input"][-1] == ()


def test_ground_against_congruence_closure():
    rng = random.Random(1969)
    seen = {True: 0, False: 0}
    for _ in range(500):
        clauses = []
        for _ in range(rng.randint(2, 5)):
            width = 1 if rng.random() < 0.7 else 2
            clauses.append([(rng.random() < 0.6, ("=", random_ground_term(rng, 2), random_ground_term(rng, 2))) for _ in range(width)])
        cl = [make_clause(c) for c in clauses]
        sat = ground_equational_sat(cl)
        seen[sat] += 1
        # On a satisfiable set the loop can run forever, so a small limit is enough to check soundness.
        res, out = paramodulation(clauses, limit=100 if sat else 5000)
        if sat:
            assert res != UNSAT
        else:
            assert res == UNSAT
            check_refutation(out)
    assert min(seen.values()) > 100


def test_first_order():
    a, b, c = ("a",), ("b",), ("c",)
    problems = [
        [[eq(a, b)], [ne(("f", a), ("f", b))]],
        [[eq(a, b)], [eq(b, c)], [ne(a, c)]],
        [[eq(a, b)], [ne(b, a)]],
        [[eq(("f", "x"), "x")], [ne(("f", ("f", a)), a)]],
        [[eq(("g", "x", "y"), ("g", "y", "x"))], [pos("P", ("g", a, b))], [neg("P", ("g", b, a))]],
        [[eq(a, b), eq(a, c)], [ne(a, b)], [ne(a, c)]],
        [[pos("P", a)], [neg("P", "x"), eq("x", b)], [ne(a, b)]],
    ]
    for clauses in problems:
        res, proof = paramodulation(clauses)
        assert res == UNSAT
        check_refutation(proof)
    assert paramodulation([[eq(a, b)], [ne(a, c)]], limit=300)[0] != UNSAT
    assert paramodulation([[eq(("f", "x"), ("f", ("f", "x")))], [ne(a, ("f", a))]], limit=300)[0] != UNSAT


def test_without_functional_reflexivity():
    a, b = ("a",), ("b",)
    res, proof = paramodulation([[eq(a, b)], [ne(("f", ("f", a)), ("f", ("f", b)))]], functional_reflexivity=False)
    assert res == UNSAT
    check_refutation(proof)


def test_edges():
    assert paramodulation([[]])[0] == UNSAT
    assert paramodulation([[ne("x", "x")]])[0] == UNSAT
    assert paramodulation([[pos("p")]])[0] == SATURATED
    assert paramodulation([[eq(("f", "x"), ("f", ("f", "x")))], [pos("P", ("a",))]], limit=200)[0] in (SATURATED, UNKNOWN)
    assert UNKNOWN != UNSAT
