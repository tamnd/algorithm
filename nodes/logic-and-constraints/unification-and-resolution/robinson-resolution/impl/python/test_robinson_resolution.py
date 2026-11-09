# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robinson-resolution/. The authors are listed in prov/ZY28KR.jsonl.

import itertools
import random

from robinson_resolution import SATURATED, UNKNOWN, UNSAT, clausal_form, make_clause, prove

# ---------------------------------------------------------------- an independent checker


def app(t, s):
    if isinstance(t, str):
        return app(s[t], s) if t in s and s[t] != t else t
    return (t[0],) + tuple(app(a, s) for a in t[1:])


def mm_unify(a, b):
    """Martelli-Montanari unification on a list of equations, written apart from the prover."""
    eqs, s = [(a, b)], {}
    while eqs:
        x, y = eqs.pop()
        x, y = app(x, s), app(y, s)
        if x == y:
            continue
        if not isinstance(x, str) and isinstance(y, str):
            x, y = y, x
        if isinstance(x, str):
            if _has_var(y, x):
                return None
            s = {v: app(t, {x: y}) for v, t in s.items()}
            s[x] = y
        elif x[0] == y[0] and len(x) == len(y):
            eqs.extend(zip(x[1:], y[1:]))
        else:
            return None
    return s


def _has_var(t, v):
    return t == v if isinstance(t, str) else any(_has_var(a, v) for a in t[1:])


def same_up_to_renaming(xs, ys):
    """True if a bijection of variables maps the sequence xs onto ys, item by item."""
    fw, bw = {}, {}

    def go(a, b):
        if isinstance(a, str) or isinstance(b, str):
            if not (isinstance(a, str) and isinstance(b, str)):
                return False
            if fw.setdefault(a, b) != b or bw.setdefault(b, a) != a:
                return False
            return True
        return a[0] == b[0] and len(a) == len(b) and all(go(p, q) for p, q in zip(a[1:], b[1:]))

    return len(xs) == len(ys) and all(go(a, b) for a, b in zip(xs, ys))


def clause_variant(c, d):
    """True if the literal sets c and d are equal up to a renaming of variables."""
    c, d = list(c), list(d)
    if len(c) != len(d):
        return False
    return any(
        same_up_to_renaming([("L", (sg, a)) for sg, a in c], [("L", (sg, a)) for sg, a in perm]) and all(x[0] == y[0] for x, y in zip(c, perm))
        for perm in itertools.permutations(d)
    )


def check_mgu(a, b, s):
    assert app(a, s) == app(b, s), "the stated substitution is not a unifier"
    t = mm_unify(a, b)
    assert t is not None
    assert same_up_to_renaming([app(a, s)], [app(a, t)]), "the stated unifier is not most general"


def check_refutation(proof):
    table = {}
    for k, c, rule, parents, info in proof:
        if rule == "input":
            table[k] = c
            continue
        i, j, s = info
        if rule == "factor":
            p = table[parents[0]]
            assert p[i][0] == p[j][0]
            check_mgu(p[i][1], p[j][1], s)
            expect = {(sg, app(a, s)) for sg, a in p}
        else:
            p = table[parents[0]]
            q = [(sg, app(a, {v: v + "'" for v in _vars(a)})) for sg, a in table[parents[1]]]
            assert p[i][0] != q[j][0]
            check_mgu(p[i][1], q[j][1], s)
            expect = {(sg, app(a, s)) for n, (sg, a) in enumerate(p) if n != i}
            expect |= {(sg, app(a, s)) for n, (sg, a) in enumerate(q) if n != j}
        assert clause_variant(sorted(expect, key=repr), c), (expect, c)
        table[k] = c
    assert proof[-1][1] == ()


def _vars(t):
    return [t] if isinstance(t, str) else [v for a in t[1:] for v in _vars(a)]


# ---------------------------------------------------------------- helpers


def pos(*atom):
    return (True, atom)


def neg(*atom):
    return (False, atom)


def brute_force_sat(clauses, n):
    for bits in itertools.product([False, True], repeat=n):
        if all(any(bits[int(a[0][1:])] == sg for sg, a in c) for c in clauses):
            return True
    return False


# ---------------------------------------------------------------- tests


def test_example_of_the_page():
    s = [[neg("P", "x"), pos("Q", "x")], [pos("P", ("a",))], [neg("Q", ("a",))]]
    res, proof = prove(s)
    assert res == UNSAT
    check_refutation(proof)
    assert len(proof) == 5


def test_propositional_against_brute_force():
    rng = random.Random(1965)
    seen = {UNSAT: 0, SATURATED: 0}
    for _ in range(500):
        n = rng.randint(1, 6)
        m = rng.randint(1, 16)
        clauses = []
        for _ in range(m):
            w = rng.randint(1, 3)
            clauses.append([(rng.random() < 0.5, ("p%d" % rng.randrange(n),)) for _ in range(w)])
        res, out = prove(clauses)
        sat = brute_force_sat([make_clause(c) for c in clauses], n)
        assert res == (SATURATED if sat else UNSAT)
        seen[res] += 1
        if res == UNSAT:
            check_refutation(out)
    assert min(seen.values()) > 100


def test_first_order_problems():
    a, b, c, d = ("a",), ("b",), ("c",), ("d",)
    problems = [
        ([[neg("Man", "x"), pos("Mortal", "x")], [pos("Man", ("socrates",))], [neg("Mortal", ("socrates",))]], UNSAT),
        ([[neg("S", b, "y"), neg("S", "y", "y")], [pos("S", b, "y"), pos("S", "y", "y")]], UNSAT),
        ([[pos("P", "x"), pos("P", "y")], [neg("P", "u"), neg("P", "v")]], UNSAT),
        ([[neg("L", "x", "y"), neg("L", "y", "z"), pos("L", "x", "z")], [pos("L", a, b)], [pos("L", b, c)], [pos("L", c, d)], [neg("L", a, d)]], UNSAT),
        ([[pos("P", a)], [neg("P", "x"), pos("P", ("f", "x"))], [neg("P", ("f", ("f", ("f", a))))]], UNSAT),
        ([[pos("P", a)], [neg("P", "x"), pos("Q", "x")], [neg("Q", b)]], SATURATED),
        ([[pos("P", a)], [neg("P", "x"), pos("P", ("f", "x"))]], UNKNOWN),
        ([[pos("E", "x", ("g", "x"))], [neg("E", "x", "y"), neg("E", "y", "x")], [neg("E", "x", "y"), pos("E", "y", "x")]], UNSAT),
    ]
    for clauses, expected in problems:
        res, out = prove(clauses, limit=300)
        assert res == expected, (clauses, res)
        if res == UNSAT:
            check_refutation(out)


def test_factoring_is_needed():
    s = [[pos("P", "x"), pos("P", "y")], [neg("P", "u"), neg("P", "v")]]
    assert prove(s, use_factoring=False)[0] == SATURATED
    res, proof = prove(s)
    assert res == UNSAT
    assert any(step[2] == "factor" for step in proof)
    check_refutation(proof)


def test_without_subsumption_same_answers():
    rng = random.Random(70)
    for _ in range(100):
        n = rng.randint(1, 3)
        clauses = [[(rng.random() < 0.5, ("p%d" % rng.randrange(n),)) for _ in range(rng.randint(1, 3))] for _ in range(rng.randint(1, 6))]
        assert prove(clauses)[0] == prove(clauses, use_subsumption=False)[0]


def test_empty_input_and_empty_clause():
    assert prove([])[0] == SATURATED
    res, proof = prove([[]])
    assert res == UNSAT and proof[-1][1] == ()


# ---------------------------------------------------------------- clausal form against finite models


def signature(clauses):
    funcs, preds = {}, {}
    for c in clauses:
        for _, atom in c:
            preds[atom[0]] = len(atom) - 1
            stack = list(atom[1:])
            while stack:
                t = stack.pop()
                if not isinstance(t, str):
                    funcs[t[0]] = len(t) - 1
                    stack.extend(t[1:])
    return funcs, preds


def clauses_have_model(clauses, k):
    """Search all structures with domain 0..k-1 by backtracking over the table cells."""
    funcs, preds = signature(clauses)
    cells = [("f", f, args) for f, r in sorted(funcs.items()) for args in itertools.product(range(k), repeat=r)]
    cells += [("p", p, args) for p, r in sorted(preds.items()) for args in itertools.product(range(k), repeat=r)]
    ground = []
    for c in clauses:
        vs = sorted({v for _, a in c for v in _vars(a)})
        for vals in itertools.product(range(k), repeat=len(vs)):
            ground.append((c, dict(zip(vs, vals))))
    val = {}

    def term(t, env):
        if isinstance(t, str):
            return env[t]
        args = []
        for x in t[1:]:
            y = term(x, env)
            if y is None:
                return None
            args.append(y)
        return val.get(("f", t[0], tuple(args)))

    def propagate(trail):
        """Unit propagation on the ground clauses. Return False on a conflict."""
        changed = True
        while changed:
            changed = False
            for c, env in ground:
                open_cell, n_open, done = None, 0, False
                for sg, atom in c:
                    args = [term(x, env) for x in atom[1:]]
                    if None in args:
                        n_open += 2
                        continue
                    cell = ("p", atom[0], tuple(args))
                    v = val.get(cell)
                    if v is None:
                        n_open += 1
                        open_cell = (cell, sg)
                    elif v == sg:
                        done = True
                        break
                if done:
                    continue
                if n_open == 0:
                    return False
                if n_open == 1:
                    val[open_cell[0]] = open_cell[1]
                    trail.append(open_cell[0])
                    changed = True
        return True

    def search():
        trail = []
        ok = propagate(trail)
        if ok:
            free = [cell for cell in cells if cell not in val]
            if not free:
                return True
            cell = free[0]
            for x in range(k) if cell[0] == "f" else (False, True):
                val[cell] = x
                if search():
                    return True
                del val[cell]
        for cell in trail:
            del val[cell]
        return False

    return search()


def holds(f, k, fn, pr, env):
    tag = f[0]
    if tag == "atom":
        a = f[1]
        return tuple(ev(t, fn, env) for t in a[1:]) in pr[a[0]]
    if tag == "not":
        return not holds(f[1], k, fn, pr, env)
    if tag in ("and", "or", "imp", "iff"):
        x, y = holds(f[1], k, fn, pr, env), holds(f[2], k, fn, pr, env)
        return {"and": x and y, "or": x or y, "imp": (not x) or y, "iff": x == y}[tag]
    vals = [holds(f[2], k, fn, pr, {**env, f[1]: d}) for d in range(k)]
    return all(vals) if tag == "all" else any(vals)


def ev(t, fn, env):
    if isinstance(t, str):
        return env[t]
    return fn[t[0]][tuple(ev(a, fn, env) for a in t[1:])]


def formula_has_model(f, k):
    for p in itertools.product([False, True], repeat=k):
        for r in itertools.product([False, True], repeat=k * k):
            for a in range(k):
                for fv in itertools.product(range(k), repeat=k):
                    pr = {"P": {(d,) for d in range(k) if p[d]}, "R": {(d, e) for d in range(k) for e in range(k) if r[d * k + e]}}
                    fn = {"a": {(): a}, "f": {(d,): fv[d] for d in range(k)}}
                    if holds(f, k, fn, pr, {}):
                        return True
    return False


def random_formula(rng, depth, bound):
    if depth == 0 or rng.random() < 0.25:
        terms = list(bound) + [("a",)]
        t = rng.choice(terms)
        if rng.random() < 0.2:
            t = ("f", t)
        if rng.random() < 0.5:
            return ("atom", ("P", t))
        return ("atom", ("R", t, rng.choice(terms)))
    op = rng.choice(["not", "and", "or", "imp", "iff", "all", "ex", "all", "ex"])
    if op == "not":
        return ("not", random_formula(rng, depth - 1, bound))
    if op in ("all", "ex"):
        v = rng.choice("xy")
        return (op, v, random_formula(rng, depth - 1, bound | {v}))
    return (op, random_formula(rng, depth - 1, bound), random_formula(rng, depth - 1, bound))


def test_clausal_form_equisatisfiable_on_small_domains():
    rng = random.Random(1930)
    seen = set()
    for i in range(150):
        if i % 3 == 0:
            g = random_formula(rng, 3, frozenset())
            f = ("and", g, ("not", g))
        else:
            parts = [random_formula(rng, d, frozenset()) for d in (3, 2, 2)]
            f = ("and", parts[0], ("and", parts[1], parts[2]))
        naive = clausal_form(f)
        structural = clausal_form(f, structural=True)
        for k in (1, 2):
            want = formula_has_model(f, k)
            seen.add((k, want))
            assert clauses_have_model(naive, k) == want, f
            assert clauses_have_model(structural, k) == want, f
    assert len(seen) == 4


def test_clausal_form_of_the_drinker():
    drinker = ("ex", "x", ("imp", ("atom", ("D", "x")), ("all", "y", ("atom", ("D", "y")))))
    clauses = clausal_form(("not", drinker))
    assert len(clauses) == 2
    res, proof = prove(clauses)
    assert res == UNSAT
    check_refutation(proof)


def test_distribution_is_exponential_and_structural_is_linear():
    for k in range(1, 9):
        f = ("and", ("atom", ("A1",)), ("atom", ("B1",)))
        for i in range(2, k + 1):
            f = ("or", f, ("and", ("atom", ("A%d" % i,)), ("atom", ("B%d" % i,))))
        assert len(clausal_form(f)) == 2 ** k
        assert len(clausal_form(f, structural=True)) == 3 * k


def test_skolem_form_is_not_equivalent():
    # F = for all x there is y with R(x, y). Its Skolem form is R(x, sk1(x)).
    f = ("all", "x", ("ex", "y", ("atom", ("R", "x", "y"))))
    clauses = clausal_form(f)
    assert len(clauses) == 1 and len(clauses[0]) == 1
    atom = clauses[0][0][1]
    sk = atom[2][0]
    fn = {sk: {(0,): 0, (1,): 1}}
    pr = {"R": {(0, 1), (1, 0)}}
    assert holds(f, 2, fn, pr, {})
    assert not all((d, fn[sk][(d,)]) in pr["R"] for d in range(2))
