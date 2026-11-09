# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/superposition/. The authors are listed in prov/8J4M9K.jsonl.

import itertools
import random

from superposition import SATURATED, UNKNOWN, UNSAT, demodulate, equality_factors, kbo_greater, lit_greater, make_clause, superposition

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


def orient(lit):
    sg, (_, s, t) = lit
    return (sg, ("=",) + tuple(sorted((s, t), key=repr)))


def clause_variant(c, d):
    # Equations have no direction: try both directions of each literal of c.
    c, d = list(c), list(d)
    if len(c) != len(d):
        return False
    flips = [[x, (x[0], ("=", x[1][2], x[1][1]))] for x in c]
    return any(variant([("L", x) for x in cc], [("L", y) for y in p]) for cc in itertools.product(*flips) for p in itertools.permutations(d))


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


def get(t, path):
    for k in path:
        t = t[k]
    return t


def ge(s, t, prec):
    return s == t or kbo_greater(s, t, prec)


def inst(c, s):
    return [(sg, ("=", app(a[1], s), app(a[2], s))) for sg, a in c]


def is_max(c, i, prec, strict):
    for k, x in enumerate(c):
        if k == i:
            continue
        if lit_greater(x, c[i], prec):
            return False
        if strict and sorted(x[1][1:], key=repr) == sorted(c[i][1][1:], key=repr) and x[0] == c[i][0]:
            return False
    return True


def ren(c, mark):
    return [(sg, app(a, {v: v + mark for v in tvars(a)})) for sg, a in c]


def check_refutation(proof, prec):
    table = {}
    for k, c, rule, parents, info in proof:
        if rule == "input":
            table[k] = c
            continue
        p = table[parents[0]]
        if rule == "eqres":
            j, s = info
            assert not p[j][0]
            check_mgu(p[j][1][1], p[j][1][2], s)
            assert is_max(inst(p, s), j, prec, False)
            expect = inst([x for n, x in enumerate(p) if n != j], s)
        elif rule == "eqfact":
            i, iside, j, jside, s = info
            a, b = p[i][1][iside], p[i][1][3 - iside]
            a2, b2 = p[j][1][jside], p[j][1][3 - jside]
            assert p[i][0] and p[j][0] and i != j
            check_mgu(a, a2, s)
            assert not ge(app(b, s), app(a, s), prec) and is_max(inst(p, s), i, prec, False)
            expect = inst([x for n, x in enumerate(p) if n not in (i, j)] + [(False, ("=", b, b2)), (True, ("=", a2, b2))], s)
        elif rule == "superpose":
            i, lside, j, path, s = info
            q = ren(table[parents[1]], "'")
            assert p[i][0]
            l, r = p[i][1][lside], p[i][1][3 - lside]
            u = get(q[j][1], path)
            assert not isinstance(u, str) and path[0] in (1, 2)
            check_mgu(l, u, s)
            side_t = q[j][1][3 - path[0]]
            assert not ge(app(r, s), app(l, s), prec)
            assert not ge(app(side_t, s), app(q[j][1][path[0]], s), prec)
            assert is_max(inst(p, s), i, prec, True)
            assert is_max(inst(q, s), j, prec, q[j][0])
            expect = inst([x for n, x in enumerate(p) if n != i] + [x for n, x in enumerate(q) if n != j] + [(q[j][0], put(q[j][1], path, r))], s)
        else:
            lits = list(p)
            for lit, path, uid, lside, m in info:
                unit = ren(table[uid], "'u")[0][1]
                lt, rt = app(unit[lside], m), app(unit[3 - lside], m)
                assert get(lits[lit][1], path) == lt
                assert kbo_greater(lt, rt, prec)
                assert lit_greater(lits[lit], (True, ("=", lt, rt)), prec)
                lits[lit] = (lits[lit][0], put(lits[lit][1], path, rt))
            expect = lits
        expect = sorted({orient(x) for x in expect}, key=repr)
        assert clause_variant(expect, c)
        table[k] = c
    assert proof[-1][1] == ()


# ---------------------------------------------------------------- oracles


def subterm_closure(terms):
    out, stack = set(), list(terms)
    while stack:
        t = stack.pop()
        if t not in out:
            out.add(t)
            stack.extend(t[1:])
    return out


def congruence_classes(terms, equations):
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


def naive_normal_form(t, rules):
    """Innermost rewriting with ground or non-ground rules l -> r, until no rule applies."""
    if not isinstance(t, str):
        t = (t[0],) + tuple(naive_normal_form(a, rules) for a in t[1:])
    for l, r in rules:
        m = one_way_match(l, t, {})
        if m is not None:
            return naive_normal_form(app(r, m), rules)
    return t


def one_way_match(p, t, m):
    if isinstance(p, str):
        if p in m:
            return m if m[p] == t else None
        return {**m, p: t}
    if isinstance(t, str) or p[0] != t[0] or len(p) != len(t):
        return None
    for a, b in zip(p[1:], t[1:]):
        m = one_way_match(a, b, m)
        if m is None:
            return None
    return m


def random_ground_term(rng, depth, consts="ab"):
    if depth == 0 or rng.random() < 0.5:
        return (rng.choice(consts),)
    if rng.random() < 0.7:
        return ("f", random_ground_term(rng, depth - 1, consts))
    return ("g", random_ground_term(rng, depth - 1, consts), random_ground_term(rng, depth - 1, consts))


def eq(s, t):
    return (True, ("=", s, t))


def ne(s, t):
    return (False, ("=", s, t))


# ---------------------------------------------------------------- tests


def test_example_of_the_page():
    a, b = ("a",), ("b",)
    prec = {"f": 3, "a": 2, "b": 1}
    s = [[eq(("f", ("f", "x")), "x")], [eq(("f", a), b)], [ne(("f", b), a)]]
    res, proof = superposition(s, prec)
    assert res == UNSAT
    check_refutation(proof, prec)
    derived = [(c, rule) for _, c, rule, _, _ in proof if rule != "input"]
    assert derived == [((eq(a, ("f", b)),), "superpose"), ((ne(a, a),), "superpose"), ((), "eqres")]


def test_demodulation_against_naive_rewriting():
    zero = ("0",)
    prec = {"plus": 3, "times": 4, "s": 2, "0": 1}
    rules = [(("plus", zero, "y"), "y"), (("plus", ("s", "x"), "y"), ("s", ("plus", "x", "y")))]
    units = [(k, make_clause([eq(l, r)])) for k, (l, r) in enumerate(rules)]

    def num(n):
        t = zero
        for _ in range(n):
            t = ("s", t)
        return t

    def value(t):
        if t == zero:
            return 0
        if t[0] == "s":
            return value(t[1]) + 1
        return value(t[1]) + value(t[2])

    rng = random.Random(1994)

    def rand(d):
        if d == 0 or rng.random() < 0.3:
            return num(rng.randint(0, 3))
        if rng.random() < 0.3:
            return ("s", rand(d - 1))
        return ("plus", rand(d - 1), rand(d - 1))

    for _ in range(500):
        t = rand(4)
        nf, steps = demodulate(t, units, prec)
        assert nf == naive_normal_form(t, rules) == num(value(t))
        # Replay the trace of rewrite steps.
        u = t
        for uid, lside, path, m in steps:
            unit = units[uid][1][0][1]
            l, r = unit[lside], unit[3 - lside]
            l, r = app(l, {v: v + "'u" for v in tvars(l)}), app(r, {v: v + "'u" for v in tvars(r)})
            assert get(u, path) == app(l, m) and kbo_greater(app(l, m), app(r, m), prec)
            u = put(u, path, app(r, m))
        assert u == nf


def test_demodulation_with_random_ground_units():
    # The result is irreducible and equal to the input modulo the units.
    rng = random.Random(1990)
    prec = {"g": 4, "f": 3, "a": 2, "b": 1, "c": 0}
    for _ in range(500):
        eqs = [(random_ground_term(rng, 2, "abc"), random_ground_term(rng, 2, "abc")) for _ in range(rng.randint(1, 4))]
        units = [(k, make_clause([eq(s, t)])) for k, (s, t) in enumerate(eqs) if s != t]
        t = random_ground_term(rng, 3, "abc")
        nf, _ = demodulate(t, units, prec)
        rules = [(s, t2) if kbo_greater(s, t2, prec) else (t2, s) for s, t2 in eqs if s != t2]
        for _, sub in [(None, x) for x in subterm_closure([nf])]:
            assert all(sub != l for l, _ in rules)
        terms = subterm_closure([t, nf] + [x for e in eqs for x in e])
        find = congruence_classes(terms, eqs)
        assert find(t) == find(nf)


def test_ground_against_congruence_closure():
    rng = random.Random(1969)
    seen = {True: 0, False: 0}
    for _ in range(500):
        clauses = []
        for _ in range(rng.randint(2, 6)):
            width = 1 if rng.random() < 0.7 else rng.randint(2, 3)
            clauses.append([(rng.random() < 0.6, ("=", random_ground_term(rng, 2), random_ground_term(rng, 2))) for _ in range(width)])
        cl = [make_clause(c) for c in clauses]
        sat = ground_equational_sat(cl)
        seen[sat] += 1
        order = ["a", "b", "f", "g"]
        rng.shuffle(order)
        prec = {x: k for k, x in enumerate(order)}
        res, out = superposition(clauses, prec)
        # Ground superposition always stops, so a satisfiable set must saturate.
        assert res == (SATURATED if sat else UNSAT)
        if res == UNSAT:
            check_refutation(out, prec)
    assert min(seen.values()) > 100


def test_first_order():
    a, b, c, e = ("a",), ("b",), ("c",), ("e",)

    def m(x, y):
        return ("m", x, y)

    group = [[eq(m(e, "x"), "x")], [eq(m(("i", "x"), "x"), e)], [eq(m(m("x", "y"), "z"), m("x", m("y", "z")))]]
    problems = [
        [[eq(a, b)], [ne(("f", a), ("f", b))]],
        [[eq(("f", "x"), ("g", "x"))], [ne(("h", ("f", a)), ("h", ("g", a)))]],
        [[eq(("f", ("f", "x")), "x")], [eq(("f", a), b)], [ne(("f", b), a)]],
        [[eq(a, b), eq(a, c)], [ne(a, b)], [ne(a, c)]],
        [[eq("x", a), eq("x", b)], [ne(c, a)], [ne(c, b)]],
        group + [[ne(m(("i", a), m(a, b)), b)]],
        group + [[ne(m(a, e), a)]],
    ]
    prec = {"i": 5, "m": 4, "e": 1}
    for clauses in problems:
        res, proof = superposition(clauses, prec)
        assert res == UNSAT
        check_refutation(proof, prec)
    assert superposition([[eq(("f", ("f", "x")), "x")], [ne(("f", a), a)]], prec)[0] == SATURATED
    assert superposition([[eq(a, b)], [ne(a, c)]])[0] == SATURATED


def test_equality_factoring():
    a, b, c = ("a",), ("b",), ("c",)
    prec = {"a": 3, "b": 2, "c": 1}
    # With a > b > c, only the maximal literal a = b is factored with a = c.
    out = list(equality_factors(make_clause([eq(a, b), eq(a, c)]), prec))
    assert [r for r, *_ in out] == [make_clause([ne(b, c), eq(a, c)])]
    res, proof = superposition([[eq(a, b), eq(a, c)], [ne(b, c)]], prec)
    assert res == SATURATED
    res, proof = superposition([[eq(a, b), eq(a, c)], [eq(b, c)], [ne(a, c)]], prec)
    assert res == UNSAT
    check_refutation(proof, prec)


def test_edges():
    assert superposition([])[0] == SATURATED
    assert superposition([[]])[0] == UNSAT
    assert superposition([[ne("x", "x")]])[0] == UNSAT
    assert superposition([[eq("x", "y")], [ne(("a",), ("b",))]])[0] == UNSAT
    assert superposition([[eq(("f", "x"), ("f", ("f", "x")))], [ne(("a",), ("b",))]], limit=300)[0] in (SATURATED, UNKNOWN)
