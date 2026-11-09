# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-resolution/. The authors are listed in prov/4MCTF6.jsonl.

import itertools
import random

from linear_resolution import UNKNOWN, UNSAT, input_sides, linear_resolution, make_clause

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


def check_linear(inputs, top, steps, sides):
    """Each center is a factor of the last center, or a resolvent of it with an input clause, a factor of one, or an earlier center."""
    s = [make_clause(c) for c in inputs]
    for k, (c, origin) in enumerate(sides):
        if origin is None:
            assert c == s[k]
        else:
            q, i, j, sb = origin
            assert q < k
            p = sides[q][0]
            assert p[i][0] == p[j][0]
            check_mgu(p[i][1], p[j][1], sb)
            assert clause_variant(sorted({(sg, app(a, sb)) for sg, a in p}, key=repr), c)
    s = [c for c, _ in sides]
    centers = [s[top]]
    for r, rule, side, (i, j, sb) in steps:
        p = centers[-1]
        if rule == "factor":
            assert p[i][0] == p[j][0]
            check_mgu(p[i][1], p[j][1], sb)
            expect = {(sg, app(a, sb)) for sg, a in p}
        else:
            kind, k = side
            assert kind == "input" or k < len(centers) - 1
            d = s[k] if kind == "input" else centers[k]
            q = [(sg, app(a, {v: v + "'" for v in tvars(a)})) for sg, a in d]
            assert p[i][0] != q[j][0]
            check_mgu(p[i][1], q[j][1], sb)
            expect = {(sg, app(a, sb)) for n, (sg, a) in enumerate(p) if n != i}
            expect |= {(sg, app(a, sb)) for n, (sg, a) in enumerate(q) if n != j}
        assert clause_variant(sorted(expect, key=repr), r)
        centers.append(r)
    assert centers[-1] == ()


# ---------------------------------------------------------------- oracles


def satisfiable(clauses, n):
    return any(all(any(bits[a[0]] == sg for sg, a in c) for c in clauses) for bits in itertools.product([False, True], repeat=n))


def minimal_core(clauses, n):
    """Delete clauses one at a time while the rest stays unsatisfiable."""
    core = list(clauses)
    k = 0
    while k < len(core):
        rest = core[:k] + core[k + 1:]
        if not satisfiable(rest, n):
            core = rest
        else:
            k += 1
    return core


def pos(*atom):
    return (True, atom)


def neg(*atom):
    return (False, atom)


# ---------------------------------------------------------------- tests


def test_example_of_the_page():
    s = [[pos("p"), pos("q")], [neg("p"), pos("q")], [pos("p"), neg("q")], [neg("p"), neg("q")]]
    res, (top, steps, sides) = linear_resolution(s, top=0)
    assert res == UNSAT and len(steps) == 4
    check_linear(s, top, steps, sides)
    assert [r for r, *_ in steps] == [((True, ("q",)),), ((True, ("p",)),), ((False, ("q",)),), ()]
    assert steps[-1][2] == ("center", 1)
    # No refutation of three steps exists, from any top clause.
    for t in range(4):
        assert linear_resolution(s, max_depth=3, top=t)[0] == UNKNOWN


def test_propositional_against_brute_force():
    # Unsatisfiable sets must be refuted; on satisfiable sets a short search must not claim a refutation.
    rng = random.Random(1970)
    found = 0
    for _ in range(500):
        n = rng.randint(1, 3)
        clauses = [[(rng.random() < 0.5, (rng.randrange(n),)) for _ in range(rng.randint(1, 3))] for _ in range(rng.randint(2, 10))]
        cl = [make_clause(c) for c in clauses]
        if satisfiable(cl, n):
            assert linear_resolution(clauses, max_depth=3)[0] == UNKNOWN
        else:
            res, out = linear_resolution(clauses, max_depth=10)
            assert res == UNSAT
            check_linear(clauses, *out)
            found += 1
    assert found > 100


def test_top_clause_from_a_minimal_core():
    # Loveland 1970: if S is unsatisfiable and S minus C is satisfiable, some linear refutation has top clause C.
    rng = random.Random(1978)
    tried = 0
    while tried < 150:
        n = rng.randint(2, 3)
        clauses = [make_clause([(rng.random() < 0.5, (rng.randrange(n),)) for _ in range(rng.randint(1, 3))]) for _ in range(rng.randint(3, 7))]
        if satisfiable(clauses, n):
            continue
        tried += 1
        core = minimal_core(clauses, n)
        for c in core:
            res, out = linear_resolution(core, max_depth=7, top=core.index(c))
            assert res == UNSAT
            check_linear(core, *out)


def test_a_bad_top_clause_fails():
    s = [[pos("p")], [neg("p")], [pos("q")]]
    assert linear_resolution(s, max_depth=6, top=2)[0] == UNKNOWN
    assert linear_resolution(s, max_depth=6, top=0)[0] == UNSAT


def test_first_order():
    a, b, c = ("a",), ("b",), ("c",)
    problems = [
        [[pos("P", "x"), pos("P", "y")], [neg("P", "u"), neg("P", "v")]],
        [[neg("S", b, "y"), neg("S", "y", "y")], [pos("S", b, "y"), pos("S", "y", "y")]],
        [[neg("L", "x", "y"), neg("L", "y", "z"), pos("L", "x", "z")], [pos("L", a, b)], [pos("L", b, c)], [neg("L", a, c)]],
        [[pos("P", a), pos("Q", a)], [neg("P", "x"), pos("Q", "x")], [pos("P", "x"), neg("Q", "x")], [neg("P", a), neg("Q", "y")]],
    ]
    for clauses in problems:
        res, out = linear_resolution(clauses, max_depth=6)
        assert res == UNSAT
        check_linear(clauses, *out)
    assert linear_resolution([[pos("P", a)], [neg("P", "x"), pos("P", ("f", "x"))]], max_depth=4)[0] == UNKNOWN


def test_factors_of_input_clauses_are_side_clauses():
    s = [make_clause([pos("P", "x", "y"), pos("P", "y", "x"), pos("P", "u", "v")])]
    sides = input_sides(s)
    assert sides[0] == (s[0], None)
    assert ((True, ("P", "X0", "X0")),) in [c for c, _ in sides]
    for k, (c, origin) in enumerate(sides[1:], 1):
        assert origin[0] < k and len(c) < len(sides[origin[0]][0])
    assert input_sides([make_clause([pos("p"), pos("q")])]) == [(make_clause([pos("p"), pos("q")]), None)]


def test_edges():
    assert linear_resolution([], max_depth=3)[0] == UNKNOWN
    assert linear_resolution([[]])[0] == UNSAT
