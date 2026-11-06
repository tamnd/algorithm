# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/narrowing/. The authors are listed in prov/4TKTY0.jsonl.

import random

from narrowing import narrow, show

Z = ("0",)


def S(t):
    return ("s", t)


def num(k, base=Z):
    t = base
    for _ in range(k):
        t = S(t)
    return t


ADD = [(("add", Z, "y"), "y"), (("add", S("x"), "y"), S(("add", "x", "y")))]
MUL = ADD + [(("mul", Z, "y"), Z), (("mul", S("x"), "y"), ("add", ("mul", "x", "y"), "y"))]
NIL = ("nil",)
APP = [(("app", NIL, "y"), "y"), (("app", ("cons", "x", "y"), "z"), ("cons", "x", ("app", "y", "z")))]
BOOL = [
    (("not", ("true",)), ("false",)), (("not", ("false",)), ("true",)),
    (("and", ("true",), "x"), "x"), (("and", ("false",), "x"), ("false",)),
]


def shown(answers):
    return [{x: show(v) for x, v in a.items()} for a in answers]


# ---------- an independent, naive oracle (recursive, for small terms) ----------

def o_var(t):
    return isinstance(t, str)


def o_vars(t):
    if o_var(t):
        return {t}
    out = set()
    for a in t[1:]:
        out |= o_vars(a)
    return out


def o_sub(t, s):
    return s.get(t, t) if o_var(t) else (t[0],) + tuple(o_sub(a, s) for a in t[1:])


def o_match(p, t, s):
    if o_var(p):
        if p in s:
            return s[p] == t
        s[p] = t
        return True
    if o_var(t) or p[0] != t[0] or len(p) != len(t):
        return False
    return all(o_match(a, b, s) for a, b in zip(p[1:], t[1:]))


def o_steps(t, rules):
    out = []
    for l, r in rules:
        s = {}
        if o_match(l, t, s):
            out.append(o_sub(r, s))
    if not o_var(t):
        for i in range(1, len(t)):
            for u in o_steps(t[i], rules):
                out.append(t[:i] + (u,) + t[i + 1:])
    return out


def o_reach(t, rules, k):
    seen = {t}
    frontier = [t]
    for _ in range(k):
        frontier = [v for u in frontier for v in o_steps(u, rules) if v not in seen]
        seen.update(frontier)
    return seen


def o_innermost(t, rules):
    """(normal form, number of innermost steps) for a terminating system."""
    if o_var(t):
        return t, 0
    n = 0
    args = []
    for a in t[1:]:
        v, k = o_innermost(a, rules)
        args.append(v)
        n += k
    u = (t[0],) + tuple(args)
    for l, r in rules:
        s = {}
        if o_match(l, u, s):
            v, k = o_innermost(o_sub(r, s), rules)
            return v, n + 1 + k
    return u, n


def instance_of(answer, theta, xs):
    """Is theta(x) an instance of answer(x), with one matcher for all x in xs?"""
    s = {}
    return all(o_match(answer[x], theta[x], s) for x in xs)


# ---------- the examples of the page ----------

def test_page_example():
    goal = (("add", "x", S(Z)), num(2))
    assert narrow(*goal, ADD, 1) == []
    assert narrow(*goal, ADD, 2) == [{"x": S(Z)}]
    assert narrow(*goal, ADD, 5) == [{"x": S(Z)}]


def test_all_solutions_of_a_sum():
    assert shown(narrow(("add", "x", "y"), num(2), ADD, 4)) == [
        {"x": "0", "y": "s(s(0))"}, {"x": "s(0)", "y": "s(0)"}, {"x": "s(s(0))", "y": "0"},
    ]
    assert len(narrow(("add", "x", "y"), num(2), ADD, 4, max_answers=2)) == 2


def test_partial_answers_keep_variables():
    # add(x, y) = s(z): x = 0 and y = s(z), or x = s(x') and z = add(x', y) for any x', y
    answers = shown(narrow(("add", "x", "y"), S("z"), ADD, 1))
    assert answers == [{"x": "0", "y": "s(z)", "z": "z"}, {"x": "s(_1)", "y": "_2", "z": "add(_1,_2)"}]


def test_empty_system_is_syntactic_unification():
    assert narrow(("f", "x", ("b",)), ("f", ("a",), "y"), [], 3) == [{"x": ("a",), "y": ("b",)}]
    assert narrow(("f", "x"), "x", [], 3) == []
    assert narrow("x", "x", [], 0) == [{"x": "x"}]


def test_shared_variable_and_non_linear_rule():
    assert narrow(("add", "x", "x"), num(2), ADD, 4) == [{"x": S(Z)}]
    rules = [(("eq", "x", "x"), ("true",))]
    assert narrow(("eq", ("f", "y"), ("f", ("a",))), ("true",), rules, 1) == [{"y": ("a",)}]


def test_lists():
    xs = ("cons", ("a",), ("cons", ("b",), NIL))
    answers = shown(narrow(("app", "x", "y"), xs, APP, 3))
    assert answers == [
        {"x": "nil", "y": "cons(a,cons(b,nil))"},
        {"x": "cons(a,nil)", "y": "cons(b,nil)"},
        {"x": "cons(a,cons(b,nil))", "y": "nil"},
    ]


def test_non_terminating_system_with_a_bound():
    rules = [(("f", "x"), ("f", S("x")))]
    assert narrow(("f", Z), ("g", "y"), rules, 6) == []
    # sound even here: f(x) = f(s(s(0))) by x = s(s(0)), or by x = 0 and two steps
    answers = shown(narrow(("f", "x"), ("f", num(2)), rules, 2))
    assert {"x": "s(s(0))"} in answers and {"x": "0"} in answers and {"x": "s(0)"} in answers


def test_deep_terms():
    n = 800
    assert narrow(("add", "x", num(n)), num(n + 1), ADD, 2) == [{"x": S(Z)}]
    assert narrow(("add", num(3), "y"), num(n), ADD, 4) == [{"y": num(n - 3)}]


# ---------- random tests against the oracle ----------

def rand_term(rng, sig, vs, depth):
    if depth == 0 or rng.random() < 0.3:
        consts = [f for f, k in sig.items() if k == 0]
        if vs and (not consts or rng.random() < 0.5):
            return rng.choice(vs)
        return (rng.choice(consts),)
    f = rng.choice(sorted(sig))
    return (f,) + tuple(rand_term(rng, sig, vs, depth - 1) for _ in range(sig[f]))


def test_random_soundness_on_any_system():
    """Every answer joins both sides within depth steps, for any rules at all."""
    rng = random.Random(11)
    sig = {"f": 1, "g": 2, "a": 0, "b": 0}
    total = 0
    for case in range(600):
        rules = []
        for _ in range(rng.randint(0, 3)):
            l = rand_term(rng, sig, ["x", "y"], 2)
            if o_var(l):
                l = ("f", l)
            r = rand_term(rng, sig, sorted(o_vars(l)), 2)
            rules.append((l, r))
        s = rand_term(rng, sig, ["x", "y"], 2)
        t = rand_term(rng, sig, ["x", "y"], 2)
        depth = rng.randint(0, 2)
        for ans in narrow(s, t, rules, depth):
            ss, tt = o_sub(s, ans), o_sub(t, ans)
            assert o_reach(ss, rules, depth) & o_reach(tt, rules, depth), (rules, s, t, ans)
            total += 1
    assert total >= 300


def test_random_completeness_on_convergent_systems():
    """Every normalized solution is an instance of an answer (Hullot)."""
    rng = random.Random(12)
    systems = [
        (ADD, {"add": 2, "s": 1, "0": 0}, {"s": 1, "0": 0}),
        (MUL, {"mul": 2, "add": 2, "s": 1, "0": 0}, {"s": 1, "0": 0}),
        (APP, {"app": 2, "cons": 2, "nil": 0, "a": 0}, {"cons": 2, "nil": 0, "a": 0}),
        (BOOL, {"not": 1, "and": 2, "true": 0, "false": 0}, {"true": 0, "false": 0}),
    ]
    cases = 0
    while cases < 500:
        rules, sig, cons = systems[rng.randrange(len(systems))]
        s = rand_term(rng, sig, ["x", "y"], 3 if rng.random() < 0.3 else 2)
        xs = sorted(o_vars(s))
        theta = {x: rand_term(rng, cons, [], 2) for x in xs}
        if rng.random() < 0.7:
            t = o_innermost(o_sub(s, theta), rules)[0]
        else:
            t = rand_term(rng, sig, [], 2)
        left, n1 = o_innermost(o_sub(s, theta), rules)
        right, n2 = o_innermost(t, rules)
        if left != right or n1 + n2 > 4 or (n1 + n2 == 0 and rng.random() < 0.9):
            continue
        answers = narrow(s, t, rules, n1 + n2)
        assert any(instance_of(a, theta, xs) for a in answers), (s, t, theta, answers)
        for a in answers:  # and they are all sound
            assert o_innermost(o_sub(s, a), rules)[0] == o_innermost(o_sub(t, a), rules)[0]
        cases += 1
