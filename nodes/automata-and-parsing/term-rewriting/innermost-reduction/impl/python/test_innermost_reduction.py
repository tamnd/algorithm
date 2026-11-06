# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/innermost-reduction/. The authors are listed in prov/KTF62M.jsonl.

import random

import pytest

from innermost_reduction import innermost_normalize, term_eq

# Peano addition and multiplication, the example of the page.
ARITH = [
    (("add", ("0",), "y"), "y"),
    (("add", ("s", "x"), "y"), ("s", ("add", "x", "y"))),
    (("mul", ("0",), "y"), ("0",)),
    (("mul", ("s", "x"), "y"), ("add", ("mul", "x", "y"), "y")),
]


def num(k):
    t = ("0",)
    for _ in range(k):
        t = ("s", t)
    return t


# ---------- an independent, naive oracle (recursive, for small terms) ----------

def o_match(p, t, s):
    if isinstance(p, str):
        if p in s:
            return s[p] == t
        s[p] = t
        return True
    if isinstance(t, str) or p[0] != t[0] or len(p) != len(t):
        return False
    return all(o_match(a, b, s) for a, b in zip(p[1:], t[1:]))


def o_subst(t, s):
    if isinstance(t, str):
        return s.get(t, t)
    return (t[0],) + tuple(o_subst(a, s) for a in t[1:])


def o_positions(t, p=()):
    yield p, t
    if not isinstance(t, str):
        for i, a in enumerate(t[1:], 1):
            yield from o_positions(a, p + (i,))


def o_replace(t, p, u):
    if not p:
        return u
    i = p[0]
    return t[:i] + (o_replace(t[i], p[1:], u),) + t[i + 1:]


def o_rule_at(u, rules):
    for k, (l, r) in enumerate(rules):
        s = {}
        if o_match(l, u, s):
            return k, o_subst(r, s)
    return None


def o_innermost(t, rules, bound):
    """Leftmost-innermost by brute force: list all redexes, keep those with no
    redex strictly below, take the leftmost."""
    trace = []
    while True:
        if sum(1 for _ in o_positions(t)) > 300:
            return "big", trace
        redexes = [p for p, u in o_positions(t) if o_rule_at(u, rules) is not None]
        if not redexes:
            return t, trace
        inner = [p for p in redexes if not any(q != p and q[:len(p)] == p for q in redexes)]
        p = min(inner)
        if len(trace) == bound:
            return None, trace
        u = dict(o_positions(t))[p]
        k, v = o_rule_at(u, rules)
        trace.append((p, k))
        t = o_replace(t, p, v)


def o_successors(t, rules):
    out = []
    for p, u in o_positions(t):
        for l, r in rules:
            s = {}
            if o_match(l, u, s):
                out.append(o_replace(t, p, o_subst(r, s)))
    return out


def o_reach(t, rules, limit=300):
    seen, todo = {t}, [t]
    while todo and len(seen) < limit:
        u = todo.pop()
        for v in o_successors(u, rules):
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return seen


# ---------- tests ----------

def test_page_example():
    t = ("mul", num(2), num(1))
    trace = []
    nf, steps = innermost_normalize(t, ARITH, trace=trace)
    assert term_eq(nf, num(2))
    assert steps == 6
    assert trace == [((), 3), ((1,), 3), ((1, 1), 2), ((1,), 0), ((), 1), ((1,), 0)]


def test_empty_system_and_normal_forms():
    t = ("f", "x", ("g", ("a",)))
    assert innermost_normalize(t, []) == (t, 0)
    assert innermost_normalize("x", ARITH) == ("x", 0)
    assert innermost_normalize(num(3), ARITH) == (num(3), 0)


def test_not_normalizing():
    rules = [(("f", "x"), ("a",)), (("b",), ("b",))]
    nf, steps = innermost_normalize(("f", ("b",)), rules, max_steps=100)
    assert nf is None and steps == 100
    # the term has the normal form a, reached by one outermost step
    assert ("a",) in o_reach(("f", ("b",)), rules)


def test_nonlinear_and_shared_variables():
    rules = [(("eq", "x", "x"), ("t",)), (("d", "x"), ("p", "x", "x"))]
    nf, _ = innermost_normalize(("eq", ("d", ("a",)), ("p", ("a",), ("a",))), rules)
    assert nf == ("t",)
    nf, _ = innermost_normalize(("eq", ("a",), ("b",)), rules)
    assert nf == ("eq", ("a",), ("b",))


def test_bad_rules():
    with pytest.raises(ValueError):
        innermost_normalize(("a",), [("x", ("a",))])
    with pytest.raises(ValueError):
        innermost_normalize(("a",), [(("a",), "y")])


def test_deep_terms():
    n = 20000
    nf, steps = innermost_normalize(("add", num(n), num(n)), ARITH)
    assert steps == n + 1
    assert term_eq(nf, num(2 * n))
    deep = ("a",)
    for _ in range(n):
        deep = ("g", deep)
    rules = [(("g", ("a",)), ("a",))]
    nf, steps = innermost_normalize(deep, rules)
    assert nf == ("a",) and steps == n


SIG = [("f", 2), ("g", 1), ("h", 1), ("a", 0), ("b", 0)]


def rand_term(rng, depth, vs):
    if depth == 0 or rng.random() < 0.3:
        if vs and rng.random() < 0.5:
            return rng.choice(vs)
        return (rng.choice(["a", "b"]),)
    f, n = rng.choice(SIG[:3])
    return (f,) + tuple(rand_term(rng, depth - 1, vs) for _ in range(n))


def rand_rules(rng):
    rules = []
    for _ in range(rng.randint(0, 4)):
        while True:
            l = rand_term(rng, 2, ["x", "y"])
            if not isinstance(l, str):
                break
        lv = sorted({u for _, u in o_positions(l) if isinstance(u, str)})
        r = rand_term(rng, 2, lv)
        rules.append((l, r))
    return rules


def test_random_against_oracle():
    rng = random.Random(20261106)
    bound = 30
    compared = 0
    for _ in range(1500):
        rules = rand_rules(rng)
        t = rand_term(rng, 3, ["x", "y"])
        trace = []
        nf, steps = innermost_normalize(t, rules, max_steps=bound, trace=trace)
        o_nf, o_trace = o_innermost(t, rules, bound)
        if o_nf == "big":
            assert trace[:len(o_trace)] == o_trace
            continue
        compared += 1
        assert trace == o_trace
        assert nf == o_nf
        if nf is not None:
            assert steps == len(trace)
            assert not o_successors(nf, rules)
            reach = o_reach(t, rules, 200)
            if len(reach) < 200:
                assert nf in reach
    assert compared >= 1000
