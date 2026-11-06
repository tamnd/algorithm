# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hoffmann-odonnell-matching/. The authors are listed in prov/R5TC80.jsonl.

import random

import pytest

from hoffmann_odonnell_matching import Matcher

A, B = ("a",), ("b",)


def f(s, t):
    return ("f", s, t)


def g(t):
    return ("g", t)


# ---------- an independent, naive oracle (recursive, for small terms) ----------

def o_var(t):
    return isinstance(t, str)


def o_match(p, t, s):
    if o_var(p):
        if p in s:
            return s[p] == t
        s[p] = t
        return True
    if o_var(t) or p[0] != t[0] or len(p) != len(t):
        return False
    return all(o_match(a, b, s) for a, b in zip(p[1:], t[1:]))


def o_positions(t):
    out = [((), t)]
    if not o_var(t):
        for i in range(1, len(t)):
            out += [((i,) + p, u) for p, u in o_positions(t[i])]
    return out


def o_find_all(patterns, t):
    return sorted((p, j) for p, u in o_positions(t) for j, q in enumerate(patterns) if o_match(q, u, {}))


def find_all(m, t):
    return sorted(m.find_all(t))


# ---------- the examples of the page ----------

def test_page_example():
    m = Matcher([f(A, "x"), f("x", g(A))])
    assert m.num_states() == 6
    assert len(m.table[("f", 2)]) == 36 and len(m.table[("g", 1)]) == 6
    t = f(f(A, B), g(A))
    assert find_all(m, t) == [((), 1), ((1,), 0)]
    assert find_all(m, f(A, g(A))) == [((), 0), ((), 1)]
    nodes, parent, argi, state = m.match_sets(t)
    names = [sorted(m.states[s]) for s in state]
    assert len(names) == 6 and names[nodes.index(B)] == [0]   # b is in no pattern: {v}


def test_exponential_match_sets():
    # h(x, ..., a, ..., x) with a at place i, for i = 1..k: 2^k match sets
    for k in range(1, 4):
        pats = [("h",) + tuple(A if j == i else "x%d" % j for j in range(k)) for i in range(k)]
        m = Matcher(pats)
        # {v} (no pattern), {v, a}, and one set for each nonempty subset of the patterns
        assert m.num_states() == 2 ** k + 1
        assert len(m.table[("h", k)]) == (2 ** k + 1) ** k


def test_edge_cases():
    m = Matcher([])
    assert m.find_all(f(A, B)) == [] and m.num_states() == 1
    m = Matcher(["x"])                                   # a variable matches everywhere
    assert find_all(m, f(A, "y")) == [((), 0), ((1,), 0), ((2,), 0)]
    m = Matcher([("f", A), f(A, A)])                     # same name, two arities
    assert find_all(m, ("f", A)) == [((), 0)]
    assert find_all(m, f(A, A)) == [((), 1)]
    m = Matcher([g(A), g(A)])                            # a pattern given twice
    assert find_all(m, g(A)) == [((), 0), ((), 1)]
    m = Matcher([g("x")])                                # subject variables are constants
    assert find_all(m, g("x")) == [((), 0)]
    assert find_all(m, "x") == []
    with pytest.raises(RuntimeError):
        Matcher([("h",) + tuple(A if j == i else "x%d" % j for j in range(5)) for i in range(5)], max_states=10)


def test_non_linear_patterns():
    m = Matcher([f("x", "x"), f("x", "y")])
    assert find_all(m, f(g(A), g(A))) == [((), 0), ((), 1)]
    assert find_all(m, f(g(A), g(B))) == [((), 1)]
    m = Matcher([("h", "x", g("x"), "y")])
    assert find_all(m, ("h", A, g(A), B)) == [((), 0)]
    assert find_all(m, ("h", A, g(B), B)) == []


def test_deep_terms():
    n = 50000
    t = A
    for _ in range(n):
        t = g(t)
    m = Matcher([g(g(A)), f("x", "x")])
    assert find_all(m, t) == [((1,) * (n - 2), 0)]
    assert m.find_all(f(t, t))[0] == ((), 1) and len(m.find_all(f(t, t))) == 3
    assert [j for _, j in m.find_all(f(t, g(t)))] == [0, 0]


# ---------- random tests against the oracle ----------

SIG = {"f": 2, "g": 1, "h": 3, "a": 0, "b": 0}


def rand_term(rng, vs, depth):
    if depth == 0 or rng.random() < 0.3:
        if vs and rng.random() < 0.5:
            return rng.choice(vs)
        return (rng.choice(["a", "b"]),)
    name = rng.choice(["f", "g", "h", "f", "g"])
    return (name,) + tuple(rand_term(rng, vs, depth - 1) for _ in range(SIG[name]))


def test_random_against_brute_force():
    rng = random.Random(5)
    hits = 0
    for case in range(700):
        pats = [rand_term(rng, ["x", "y", "z"], rng.randint(0, 3)) for _ in range(rng.randint(0, 5))]
        m = Matcher(pats)
        for _ in range(4):
            t = rand_term(rng, ["x", "u"] if rng.random() < 0.3 else [], rng.randint(0, 5))
            want = o_find_all(pats, t)
            assert find_all(m, t) == want, (pats, t)
            hits += len(want)
    assert hits > 2000


def test_random_match_sets_are_exact():
    """Each state is exactly the set of subpatterns that match the node."""
    rng = random.Random(6)
    for case in range(300):
        pats = [rand_term(rng, ["x", "y"], rng.randint(0, 3)) for _ in range(rng.randint(1, 4))]
        m = Matcher(pats)
        inv = {pid: key for key, pid in m.node_id.items()}

        def build(pid):
            if pid == 0:
                return "v"
            key = inv[pid]
            return (key[0],) + tuple(build(c) for c in key[2:])

        t = rand_term(rng, [], rng.randint(0, 4))
        nodes, parent, argi, state = m.match_sets(t)
        for u, s in zip(nodes, state):
            want = {0} | {pid for pid in inv if _lin_match(build(pid), u)}
            assert set(m.states[s]) == want


def _lin_match(p, t):
    """Match with every occurrence of v a separate variable."""
    if o_var(p):
        return True
    if o_var(t) or p[0] != t[0] or len(p) != len(t):
        return False
    return all(_lin_match(a, b) for a, b in zip(p[1:], t[1:]))
