# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrimination-tree/. The authors are listed in prov/R1941B.jsonl.

import random

from discrimination_tree import DiscriminationTree, flatten, key

A, B = ("a",), ("b",)


def g(t):
    return ("g", t)


def f(s, t):
    return ("f", s, t)


PAGE = [f(g("x"), "y"), f(g(A), B), f("x", "x"), g("x"), f("x", B)]


def page_tree():
    d = DiscriminationTree()
    for i, p in enumerate(PAGE, 1):
        d.insert(p, i)
    return d


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


def o_matches(p, t):
    s = {}
    return s if o_match(p, t, s) else None


def o_linear(p, counter):
    if o_var(p):
        counter[0] += 1
        return "v%d" % counter[0]
    return (p[0],) + tuple(o_linear(a, counter) for a in p[1:])


def o_sub(t, s):
    return s.get(t, t) if o_var(t) else (t[0],) + tuple(o_sub(a, s) for a in t[1:])


def o_steps(t, rules):
    out = []
    for l, r in rules:
        s = o_matches(l, t)
        if s is not None:
            out.append(o_sub(r, s))
    if not o_var(t):
        for i in range(1, len(t)):
            for u in o_steps(t[i], rules):
                out.append(t[:i] + (u,) + t[i + 1:])
    return out


def o_subterms(t):
    out = [((), t)]
    if not o_var(t):
        for i in range(1, len(t)):
            out += [((i,) + p, u) for p, u in o_subterms(t[i])]
    return out


def o_replace(t, p, u):
    if not p:
        return u
    i = p[0]
    return t[:i] + (o_replace(t[i], p[1:], u),) + t[i + 1:]


# ---------- the examples of the page ----------

def test_page_example():
    d = page_tree()
    assert d.node_count() == 12
    q = f(g(A), B)
    assert sorted(v for _, v in d.retrieve(q)) == [1, 2, 3, 5]
    assert sorted((v, sorted(s.items())) for v, s in d.match(q)) == [
        (1, [("x", A), ("y", B)]), (2, []), (5, [("x", g(A))]),
    ]
    q2 = f(g(B), g(B))
    assert sorted(v for _, v in d.retrieve(q2)) == [1, 3]
    assert sorted(v for v, _ in d.match(q2)) == [1, 3]
    assert sorted(v for _, v in d.retrieve(g(f(A, A)))) == [4]
    assert d.retrieve(A) == []


def test_keys_and_skip():
    assert key(f(g("x"), "y")) == [("f", 2), ("g", 1), "*", "*"]
    syms, skip = flatten(f(g(A), B))
    assert [s[0] for s in syms] == ["f", "g", "a", "b"]
    assert skip == [4, 3, 3, 4]


def test_delete_prunes():
    d = page_tree()
    assert d.delete(f(g(A), B), 2)
    assert d.node_count() == 10 and len(d) == 4
    assert not d.delete(f(g(A), B), 2)
    assert not d.delete(f(g(A), A), 9)
    assert not d.delete(f("x", "x"), 4)        # right key, wrong value
    assert d.delete(f("u", "v"), 3) is False   # same key, different pattern
    for i, p in enumerate(PAGE, 1):
        if i != 2:
            assert d.delete(p, i)
    assert d.node_count() == 1 and len(d) == 0


def test_edge_cases():
    d = DiscriminationTree()
    assert d.retrieve(A) == [] and d.match("x") == [] and d.node_count() == 1
    d.insert("x", "any")                      # a variable pattern matches everything
    assert [v for v, _ in d.match(f(A, "z"))] == ["any"]
    d.insert(("f", A), "unary")               # same name, other arity
    assert [v for v, _ in d.match(f(A, A))] == ["any"]
    assert sorted(v for v, _ in d.match(("f", A))) == ["any", "unary"]
    d.insert(A, "c1")
    d.insert(A, "c2")                         # two entries with the same pattern
    assert sorted(v for v, _ in d.match(A)) == ["any", "c1", "c2"]
    # a query variable is consumed only by a pattern variable
    d2 = DiscriminationTree()
    d2.insert(g(A), 1)
    d2.insert(g("x"), 2)
    d2.insert(("?", "x"), 3)                  # a function symbol named "?"
    assert [v for v, _ in d2.match(g("x"))] == [2]
    assert [v for v, _ in d2.match(g("a"))] == [2]
    assert [v for v, _ in d2.match(("?", A))] == [3]


def test_deep_terms():
    n = 50000
    t = A
    for _ in range(n):
        t = g(t)
    p = "x"
    for _ in range(n - 1):
        p = g(p)
    d = DiscriminationTree()
    d.insert(p, "deep")
    d.insert(f("x", "x"), "pair")
    assert [(v, s["x"]) for v, s in d.match(t)] == [("deep", g(A))]
    assert [v for v, _ in d.match(f(t, t))] == ["pair"]
    assert d.match(f(t, g(t))) == []
    assert d.delete(p, "deep") and d.node_count() == 4


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
    rng = random.Random(7)
    for case in range(800):
        d = DiscriminationTree()
        entries = []
        for i in range(rng.randint(0, 12)):
            p = rand_term(rng, ["x", "y", "z"], rng.randint(0, 3))
            d.insert(p, i)
            entries.append((p, i))
        for _ in range(rng.randint(0, 4)):     # some deletions
            if entries and rng.random() < 0.7:
                p, i = entries.pop(rng.randrange(len(entries)))
                assert d.delete(p, i)
            else:
                assert not d.delete(rand_term(rng, ["x"], 2), 99)
        assert len(d) == len(entries)
        for _ in range(5):
            t = rand_term(rng, ["x", "u"] if rng.random() < 0.3 else [], rng.randint(0, 4))
            cand = sorted(v for _, v in d.retrieve(t))
            want = sorted(i for p, i in entries if o_matches(o_linear(p, [0]), t) is not None)
            assert cand == want, (entries, t)
            got = sorted((v, sorted(s.items())) for v, s in d.match(t))
            exact = sorted((i, sorted(o_matches(p, t).items())) for p, i in entries
                           if o_matches(p, t) is not None)
            assert got == exact, (entries, t)


def test_random_rewrite_steps_with_index():
    """One-step reducts through the index equal the brute-force reducts.

    The rules include non-linear left sides, variables shared between sides,
    rules that need not terminate, and the empty system.
    """
    rng = random.Random(8)
    for case in range(600):
        rules = []
        for _ in range(rng.randint(0, 5)):
            l = rand_term(rng, ["x", "y"], rng.randint(1, 3))
            if o_var(l):
                l = g(l)
            vs = sorted({u for _, u in o_subterms(l) if o_var(u)})
            rules.append((l, rand_term(rng, vs, 2)))
        d = DiscriminationTree()
        for i, (l, r) in enumerate(rules):
            d.insert(l, i)
        t = rand_term(rng, [], rng.randint(0, 4))
        got = []
        for p, u in o_subterms(t):
            for i, s in d.match(u):
                got.append(o_replace(t, p, o_sub(rules[i][1], s)))
        assert sorted(map(repr, got)) == sorted(map(repr, o_steps(t, rules)))
