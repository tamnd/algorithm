# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/substitution-tree/. The authors are listed in prov/6X13J0.jsonl.

import random

from substitution_tree import SubstitutionTree, apply, normalize, term_eq

A, B = ("a",), ("b",)


def g(t):
    return ("g", t)


def f(s, t):
    return ("f", s, t)


PAGE = [f("x", A), f("x", B), f(g("x"), A), f("x", "x")]


def page_tree():
    d = SubstitutionTree()
    for i, p in enumerate(PAGE, 1):
        d.insert(p, i)
    return d


# ---------- a naive, independent oracle (recursive, for small terms) ----------

def o_var(t):
    return isinstance(t, str)


def o_match(p, t, s):
    """Extend s so that p s = t; variables of t are constants."""
    if o_var(p):
        if p in s:
            return s[p] == t
        s[p] = t
        return True
    if o_var(t) or p[0] != t[0] or len(p) != len(t):
        return False
    return all(o_match(a, b, s) for a, b in zip(p[1:], t[1:]))


def o_resolve(t, s):
    while o_var(t) and t in s:
        t = s[t]
    return t


def o_occurs(v, t, s):
    t = o_resolve(t, s)
    if o_var(t):
        return t == v
    return any(o_occurs(v, a, s) for a in t[1:])


def o_unify(a, b, s):
    a, b = o_resolve(a, s), o_resolve(b, s)
    if a == b:
        return True
    if o_var(a):
        if o_occurs(a, b, s):
            return False
        s[a] = b
        return True
    if o_var(b):
        return o_unify(b, a, s)
    if a[0] != b[0] or len(a) != len(b):
        return False
    return all(o_unify(x, y, s) for x, y in zip(a[1:], b[1:]))


def o_rename(t, prefix):
    if o_var(t):
        return prefix + t
    return (t[0],) + tuple(o_rename(a, prefix) for a in t[1:])


def oracle(stored, q, mode):
    out = []
    for t, v in stored:
        if mode == "generalizations":
            ok = o_match(t, q, {})
        elif mode == "instances":
            ok = o_match(q, t, {})
        else:
            ok = o_unify(o_rename(t, "L"), o_rename(q, "R"), {})
        if ok:
            out.append((t, v))
    return out


def key(entries):
    return sorted((repr(t), v) for t, v in entries)


# ---------- structural invariants ----------

def check_invariants(d):
    """Each leaf's composed term is the normalized stored term, each indicator
    variable is bound at most once on a path, inner nodes other than the top
    have at least two children, and the count is right."""
    count = 0
    stack = [(c, {"*0": "*0"}, set()) for c in d.top.children]
    while stack:
        node, comp, bound = stack.pop()
        assert node.subst, "empty substitution"
        assert not (set(node.subst) & bound), "indicator variable bound twice"
        new = {x: apply(t, node.subst) for x, t in comp.items()}
        nb = bound | set(node.subst)
        if node.children:
            assert not node.entries
            assert len(node.children) >= 2
            for c in node.children:
                stack.append((c, new, nb))
        else:
            assert node.entries
            for t, _ in node.entries:
                assert term_eq(new["*0"], normalize(t))
            count += len(node.entries)
    assert count == d.n == len(d.entries())


# ---------- tests ----------

def test_page_example():
    d = page_tree()
    check_invariants(d)
    assert len(d.top.children) == 1
    root = d.top.children[0]
    t = root.subst["*0"]
    assert t[0] == "f" and all(isinstance(a, str) and a[0] == "*" for a in t[1:])
    assert sorted(len(c.children) for c in root.children) == [0, 3]
    r = d.retrieve(f(A, A), "generalizations")
    assert key(r) == key([(PAGE[0], 1), (PAGE[3], 4)])
    r = d.retrieve(f(g(B), A), "generalizations")
    assert key(r) == key([(PAGE[0], 1), (PAGE[2], 3)])
    r = d.retrieve(f(A, "y"), "unifiable")
    assert key(r) == key([(PAGE[0], 1), (PAGE[1], 2), (PAGE[3], 4)])
    r = d.retrieve(f(g("z"), "y"), "instances")
    assert key(r) == key([(PAGE[2], 3)])
    # deleting f(g(x), a) leaves the root with one child, and the two merge
    assert d.delete(f(g("x"), A), 3)
    check_invariants(d)
    root = d.top.children[0]
    assert term_eq(root.subst["*0"], ("f", "#1", root.subst["*0"][2]))
    assert len(root.children) == 3
    assert not d.delete(f(g("x"), A), 3)
    assert d.delete(f("x", B), 2)
    check_invariants(d)
    assert d.n == 2


def test_empty_and_single():
    d = SubstitutionTree()
    assert d.retrieve(A, "unifiable") == []
    assert not d.delete(A, 1)
    d.insert("x", 7)
    check_invariants(d)
    for mode in ("generalizations", "unifiable"):
        assert d.retrieve(f(A, B), mode) == [("x", 7)]
    assert d.retrieve(f(A, B), "instances") == []
    assert d.retrieve("y", "instances") == [("x", 7)]
    assert d.delete("x", 7)
    assert d.n == 0 and d.top.children == []


def test_duplicates_and_variants():
    d = SubstitutionTree()
    d.insert(f("x", "y"), 1)
    d.insert(f("u", "v"), 2)
    d.insert(f("x", "y"), 1)
    check_invariants(d)
    assert len(d.top.children) == 1 and not d.top.children[0].children
    assert len(d.retrieve(f(A, A), "generalizations")) == 3
    assert d.delete(f("x", "y"), 1)
    assert len(d.retrieve(f(A, A), "generalizations")) == 2


def test_occurs_check():
    d = SubstitutionTree()
    d.insert(f("x", g("x")), 1)
    assert d.retrieve(f("y", "y"), "unifiable") == []
    assert d.retrieve(f(A, g(A)), "generalizations") == [(f("x", g("x")), 1)]


def test_deep_terms():
    d = SubstitutionTree()
    t = A
    for _ in range(5000):
        t = g(t)
    u = "x"
    for _ in range(4999):
        u = g(u)
    d.insert(t, 1)
    d.insert(u, 2)
    check_invariants(d)
    assert key(d.retrieve(t, "generalizations")) == key([(t, 1), (u, 2)])
    assert key(d.retrieve(u, "instances")) == key([(t, 1), (u, 2)])
    assert d.delete(t, 1)
    check_invariants(d)


SIG = {"a": 0, "b": 0, "g": 1, "f": 2, "h": 3}


def rand_term(rng, depth, vars_):
    if depth == 0 or rng.random() < 0.3:
        if rng.random() < 0.45:
            return rng.choice(vars_)
        return (rng.choice(["a", "b"]),)
    name = rng.choice(["g", "f", "f", "h"])
    return (name,) + tuple(rand_term(rng, depth - 1, vars_) for _ in range(SIG[name]))


def test_random_against_oracle():
    rng = random.Random(11)
    modes = ("generalizations", "instances", "unifiable")
    for case in range(600):
        d = SubstitutionTree()
        stored = []
        vars_ = ["x", "y"] if case % 2 else ["x", "y", "z"]
        for step in range(rng.randint(0, 14)):
            if stored and rng.random() < 0.25:
                t, v = stored.pop(rng.randrange(len(stored)))
                assert d.delete(t, v)
            else:
                t = rand_term(rng, rng.randint(0, 3), vars_)
                v = rng.randrange(4)
                d.insert(t, v)
                stored.append((t, v))
            check_invariants(d)
        for _ in range(4):
            q = rand_term(rng, rng.randint(0, 3), ["x", "y", "w"])
            for mode in modes:
                assert key(d.retrieve(q, mode)) == key(oracle(stored, q, mode)), (stored, q, mode)
        t = rand_term(rng, 2, vars_)
        present = any(term_eq(s, t) and v == 0 for s, v in stored)
        assert d.delete(t, 0) == present
