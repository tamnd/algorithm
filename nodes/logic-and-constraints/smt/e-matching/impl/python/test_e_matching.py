# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/e-matching/. The authors are listed in prov/5EARHB.jsonl.
"""Tests of E-matching against brute force.

The brute force tries every substitution of classes for the pattern
variables. For each one it builds the ground term p(sigma), with one term per
class, and decides E |= p(sigma) = t by a naive congruence closure computed
from scratch over all subterms. It shares no code with the matcher.
"""

import random
from itertools import product

from e_matching import EGraph, instantiate, is_var, match_all, match_multi


def subterms(t, out):
    if isinstance(t, tuple):
        for a in t[1:]:
            subterms(a, out)
    if t not in out:
        out.append(t)


def naive_closure(eqs, terms):
    """Union-find over all subterms, closed under congruence by fixpoint."""
    all_terms = []
    for s, t in eqs:
        subterms(s, all_terms)
        subterms(t, all_terms)
    for t in terms:
        subterms(t, all_terms)
    rep = {t: t for t in all_terms}

    def find(t):
        while rep[t] != t:
            t = rep[t]
        return t

    for s, t in eqs:
        rep[find(s)] = find(t)
    apps = [t for t in all_terms if isinstance(t, tuple)]
    changed = True
    while changed:
        changed = False
        for i, s in enumerate(apps):
            for t in apps[i + 1:]:
                if (s[0] == t[0] and len(s) == len(t) and find(s) != find(t)
                        and all(find(a) == find(b) for a, b in zip(s[1:], t[1:]))):
                    rep[find(s)] = find(t)
                    changed = True
    return find


def pattern_vars(p, out):
    if is_var(p):
        if p not in out:
            out.append(p)
    elif isinstance(p, tuple):
        for a in p[1:]:
            pattern_vars(a, out)
    return out


def plug(p, env):
    if is_var(p):
        return env[p]
    if isinstance(p, str):
        return p
    return (p[0],) + tuple(plug(a, env) for a in p[1:])


def brute_matches(eqs, terms, g, p):
    """All (class, substitution) with E |= p(sigma) = t for a term t of the class."""
    classes = g.classes()
    xs = pattern_vars(p, [])
    out = []
    for choice in product(classes, repeat=len(xs)):
        env = {x: g.term[c] for x, c in zip(xs, choice)}
        inst = plug(p, env)
        find = naive_closure(eqs, terms + [inst] + [g.term[c] for c in classes])
        for c in classes:
            if find(inst) == find(g.term[c]):
                out.append((c, dict(zip(xs, choice))))
    return out


def build(eqs, terms):
    g = EGraph()
    for t in terms:
        g.add(t)
    for s, t in eqs:
        g.merge(g.add(s), g.add(t))
    return g


def same(a, b):
    key = lambda m: (m[0], sorted(m[1].items()))
    return sorted(map(key, a)) == sorted(map(key, b))


def test_simple_match_modulo_equality():
    # E = {f(a) = b}; pattern g(f(?x)) matches g(b) with ?x = a
    eqs = [(("f", "a"), "b")]
    terms = [("g", "b")]
    g = build(eqs, terms)
    ms = match_all(g, ("g", ("f", "?x")))
    assert len(ms) == 1
    c, s = ms[0]
    assert c == g.find(g.add(("g", "b"))) and s == {"?x": g.find(g.add("a"))}
    # syntactic matching would find nothing: g(b) has no f below it
    assert same(ms, brute_matches(eqs, terms, g, ("g", ("f", "?x"))))


def test_shared_variable():
    # pattern h(?x, ?x) matches h(a, b) only when a = b
    terms = [("h", "a", "b")]
    assert match_all(build([], terms), ("h", "?x", "?x")) == []
    g = build([("a", "b")], terms)
    assert len(match_all(g, ("h", "?x", "?x"))) == 1


def test_exponentially_many_matches():
    # one class holding f(c_i) for i < n gives n^k matches of h(f(?x1), ..., f(?xk))
    n, k = 3, 3
    eqs = [(("f", "c0"), ("f", "c%d" % i)) for i in range(1, n)]
    pattern = ("h",) + tuple(("f", "?x%d" % j) for j in range(k))
    g = build(eqs, [("h",) + (("f", "c0"),) * k])
    assert len(match_all(g, pattern)) == n ** k


def test_three_coloring_reduction():
    # the multi-pattern e(?u, ?v) for each edge matches iff the graph is 3-colorable
    colors = ["r", "g", "b"]
    edge_terms = [("e", c, d) for c in colors for d in colors if c != d]
    g = build([], edge_terms)
    triangle = [("e", "?1", "?2"), ("e", "?2", "?3"), ("e", "?1", "?3")]
    assert len(match_multi(g, triangle)) == 6  # 3! colorings
    k4 = [("e", "?%d" % i, "?%d" % j) for i in range(4) for j in range(i + 1, 4)]
    assert match_multi(g, k4) == []


def random_term(rng, depth):
    if depth == 0 or rng.random() < 0.35:
        return rng.choice("abc")
    if rng.random() < 0.6:
        return ("f", random_term(rng, depth - 1))
    return ("g", random_term(rng, depth - 1), random_term(rng, depth - 1))


def random_pattern(rng, depth, top=True):
    if not top and (depth == 0 or rng.random() < 0.4):
        return rng.choice(["?x", "?y", "?x", "a"])
    if rng.random() < 0.6:
        return ("f", random_pattern(rng, depth - 1, False))
    return ("g", random_pattern(rng, depth - 1, False), random_pattern(rng, depth - 1, False))


def test_random_against_brute_force():
    rng = random.Random(4)
    found = 0
    for _ in range(400):
        terms = [random_term(rng, 2) for _ in range(rng.randint(1, 4))]
        eqs = [(random_term(rng, 2), random_term(rng, 1)) for _ in range(rng.randint(0, 2))]
        g = build(eqs, terms)
        if len(g.classes()) > 9:
            continue
        p = random_pattern(rng, 2)
        got = match_all(g, p)
        assert same(got, brute_matches(eqs, terms, g, p)), (eqs, terms, p)
        found += bool(got)
    assert found > 120


def test_incomplete_with_a_bad_trigger():
    # forall x. f(g(x)) = x, with g(a) = g(b) and a != b, is unsatisfiable
    eqs, diseqs = [(("g", "a"), ("g", "b"))], [("a", "b")]
    lhs, rhs = ("f", ("g", "?x")), "?x"
    # the trigger f(g(x)) has no match: the ground part has no f, so nothing happens
    assert instantiate(eqs, diseqs, [([lhs], lhs, rhs)], 10) == ("unknown", 0)
    # the trigger g(x) matches g(a) and g(b), and the two instances refute it
    status, n = instantiate(eqs, diseqs, [([("g", "?x")], lhs, rhs)], 10)
    assert status == "unsat" and n == 2


def test_matching_loop():
    # forall x. f(x) = f(g(x)) with trigger f(x): every instance makes a new f-term
    lhs, rhs = ("f", "?x"), ("f", ("g", "?x"))
    status, n = instantiate([], [(("f", "a"), "b")], [([lhs], lhs, rhs)], 6)
    assert status == "unknown" and n == 6  # one new instance per round, never done
    # the trigger f(g(x)) only matches terms that the instances do not create
    status, n = instantiate([], [(("f", "a"), "b")], [([rhs], lhs, rhs)], 6)
    assert status == "unknown" and n == 0


def test_instantiation_finds_conflict_modulo_equality():
    # forall x. f(x) = x; ground: f(c) = d, c != d.  The match uses E-matching.
    status, n = instantiate([(("f", "c"), "d")], [("c", "d")],
                            [([("f", "?x")], ("f", "?x"), "?x")], 5)
    assert status == "unsat" and n == 1
