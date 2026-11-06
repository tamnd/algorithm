# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unfailing-completion/. The authors are listed in prov/FECHPF.jsonl.

import itertools
import random

from unfailing_completion import canonical, equal, lpo_gt, normal_form, unfailing_completion

A, B = ("a",), ("b",)


def f(s, t):
    return ("f", s, t)


def g(t):
    return ("g", t)


# ---------- independent oracles (recursive, for small terms) ----------

def o_match(p, t, s):
    if isinstance(p, str):
        if p in s:
            return s[p] == t
        s[p] = t
        return True
    if isinstance(t, str) or p[0] != t[0] or len(p) != len(t):
        return False
    return all(o_match(a, b, s) for a, b in zip(p[1:], t[1:]))


def o_apply(t, s):
    if isinstance(t, str):
        return s.get(t, t)
    return (t[0],) + tuple(o_apply(a, s) for a in t[1:])


def o_size(t):
    return 1 if isinstance(t, str) else 1 + sum(o_size(a) for a in t[1:])


def o_steps(t, E):
    """All terms reachable from t by one replacement step with E, in either direction."""
    out = []
    stack = [(t, lambda r: r)]
    while stack:
        u, ctx = stack.pop()
        for l, r in E:
            for x, y in ((l, r), (r, l)):
                s = {}
                if o_match(x, u, s):
                    out.append(ctx(o_apply(y, s)))
        if not isinstance(u, str):
            for i in range(1, len(u)):
                stack.append((u[i], lambda r, u=u, i=i, ctx=ctx: ctx(u[:i] + (r,) + u[i + 1:])))
    return out


def o_class(t, E, max_size, rounds):
    """The ground terms of size at most max_size that are E-equal to t by at most rounds steps."""
    seen = {t}
    frontier = [t]
    for _ in range(rounds):
        nxt = []
        for u in frontier:
            for v in o_steps(u, E):
                if v not in seen and o_size(v) <= max_size:
                    seen.add(v)
                    nxt.append(v)
        frontier = nxt
    return seen


def o_eval(t, alg, env):
    if isinstance(t, str):
        return env[t]
    return alg[t[0]][tuple(o_eval(a, alg, env) for a in t[1:])]


def o_vars(t, acc):
    if isinstance(t, str):
        acc.add(t)
    else:
        for a in t[1:]:
            o_vars(a, acc)
    return acc


def holds(alg, eq, dom):
    vs = sorted(o_vars(eq[0], set()) | o_vars(eq[1], set()))
    for vals in itertools.product(dom, repeat=len(vs)):
        env = dict(zip(vs, vals))
        if o_eval(eq[0], alg, env) != o_eval(eq[1], alg, env):
            return False
    return True


ARITY = {"a": 0, "b": 0, "g": 1, "f": 2}


def random_algebra(rng, dom):
    return {s: {args: rng.choice(dom) for args in itertools.product(dom, repeat=k)} for s, k in ARITY.items()}


def rand_term(rng, depth, vars_):
    if depth == 0 or rng.random() < 0.3:
        if vars_ and rng.random() < 0.5:
            return rng.choice(vars_)
        return (rng.choice(["a", "b"]),)
    name = rng.choice(["g", "f", "f"])
    return (name,) + tuple(rand_term(rng, depth - 1, vars_) for _ in range(ARITY[name]))


def ground_terms(max_size):
    """All ground terms of size at most max_size."""
    by = {1: [A, B]}
    for n in range(2, max_size + 1):
        by[n] = [g(t) for t in by[n - 1]]
        for i in range(1, n - 1):
            by[n] += [f(s, t) for s in by[i] for t in by[n - 1 - i]]
    return [t for n in by for t in by[n]]


# ---------- tests ----------

def test_commutativity():
    """Knuth-Bendix fails on commutativity; unfailing completion saturates at once."""
    prec = {"f": 3, "b": 2, "a": 1}
    r = unfailing_completion([(f("x", "y"), f("y", "x"))], prec)
    assert r.saturated and len(r.equations) == 1
    assert normal_form(f(B, A), r.equations, prec) == f(A, B)
    assert equal(f(f(B, A), A), f(A, f(A, B)), r, prec)
    assert not equal(f(f(A, B), A), f(A, A), r, prec)


def test_page_example():
    prec = {"f": 3, "b": 2, "a": 1}
    E = [(f("x", "y"), f("y", "x")), (f("x", A), "x")]
    r = unfailing_completion(E, prec)
    assert r.saturated
    assert sorted(map(repr, r.equations)) == sorted(map(repr, [
        (f("x", "y"), f("y", "x")), (f("x", A), "x"), (f(A, "x'"), "x'")]))
    assert normal_form(f(f(A, B), f(B, A)), r.equations, prec) == f(B, B)


def test_groups():
    m = lambda x, y: ("*", x, y)
    i = lambda x: ("i", x)
    e = ("e",)
    prec = {"i": 3, "*": 2, "e": 1}
    G = [(m(e, "x"), "x"), (m(i("x"), "x"), e), (m(m("x", "y"), "z"), m("x", m("y", "z")))]
    r = unfailing_completion(G, prec)
    assert r.saturated and len(r.equations) == 10
    assert all(lpo_gt(s, t, prec) for s, t in r.equations)  # all oriented: a convergent system
    assert normal_form(i(m("a1", i("a2"))), r.equations, {**prec, "a1": 0, "a2": 0}) == m("a2", i("a1"))


def test_empty_system():
    r = unfailing_completion([], {"f": 2, "a": 1})
    assert r.saturated and r.equations == []
    assert not equal(f(A, A), A, r, {"f": 2, "a": 1})


def test_non_terminating_with_bound():
    """h(g(h(x))) = h(g(x)) makes the run add h(g^n(h(x))) = h(g^n(x)) for n = 1, 2, ...;
    the step bound stops it."""
    h = lambda t: ("h", t)

    def gn(n, t):
        for _ in range(n):
            t = g(t)
        return t

    r = unfailing_completion([(h(g(h("x"))), h(g("x")))], {"h": 2, "g": 1}, max_steps=25)
    assert not r.saturated and r.steps == 25
    want = {(h(gn(n, h("v1"))), h(gn(n, "v1"))) for n in range(1, 7)}
    assert {canonical(e) for e in r.equations} == want


def test_random_against_oracles():
    rng = random.Random(5)
    ground = ground_terms(5)
    dom = (0, 1)
    saturated = 0
    for case in range(500):
        E = []
        for _ in range(rng.randint(1, 2)):
            while True:
                s = rand_term(rng, 2, ["x", "y"])
                t = rand_term(rng, 2, ["x", "y"])
                if s != t and o_vars(s, set()) == o_vars(t, set()):
                    break
            E.append((s, t))
        syms = ["a", "b", "g", "f"]
        rng.shuffle(syms)
        prec = {s: k for k, s in enumerate(syms)}
        r = unfailing_completion(E, prec, max_steps=25)
        # soundness: every final equation holds in every 2-element model of E
        models = [alg for alg in (random_algebra(rng, dom) for _ in range(40)) if all(holds(alg, e, dom) for e in E)]
        for alg in models:
            for eq in r.equations:
                assert holds(alg, eq, dom), (E, eq)
        sample = rng.sample(ground, 6)
        for t in sample:
            nf = normal_form(t, r.equations, prec)
            for alg in models:
                assert o_eval(nf, alg, {}) == o_eval(t, alg, {})
        if not r.saturated:
            continue
        saturated += 1
        # completeness on ground terms: E-equal terms found by search have equal normal forms
        for t in sample:
            nf = normal_form(t, r.equations, prec)
            for u in o_class(t, E, 7, 3):
                assert normal_form(u, r.equations, prec) == nf, (E, t, u)
    assert saturated >= 400
