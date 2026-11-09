# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/e-graph/. The authors are listed in prov/S6Y6MV.jsonl.

import itertools
import random

from e_graph import EGraph


def subterms(t, out):
    stack = [t]
    while stack:
        u = stack.pop()
        if u not in out:
            out.add(u)
            if isinstance(u, tuple):
                stack.extend(u[1:])
    return out


def naive_closure(terms, eqs):
    """Apply the input equations and congruence until nothing changes."""
    terms = list(terms)
    cls = {t: i for i, t in enumerate(terms)}

    def join(x, y):
        a, b = cls[x], cls[y]
        if a == b:
            return False
        for t in terms:
            if cls[t] == b:
                cls[t] = a
        return True

    for s, t in eqs:
        join(s, t)
    changed = True
    while changed:
        changed = False
        apps = [t for t in terms if isinstance(t, tuple)]
        for p in apps:
            for q in apps:
                if p[0] == q[0] and len(p) == len(q) and cls[p] != cls[q]:
                    if all(cls[x] == cls[y] for x, y in zip(p[1:], q[1:])):
                        join(p, q)
                        changed = True
    return cls


def f(n, x="a"):
    for _ in range(n):
        x = ("f", x)
    return x


def size(t):
    return 1 if isinstance(t, str) else 1 + sum(size(a) for a in t[1:])


def random_term(rng, depth):
    if depth == 0 or rng.random() < 0.35:
        return rng.choice("abc")
    if rng.random() < 0.6:
        return ("f", random_term(rng, depth - 1))
    return ("g", random_term(rng, depth - 1), random_term(rng, depth - 1))


def test_page_example():
    g = EGraph()
    for t in [("g", ("f", "a")), ("g", ("f", "b")), ("f", "c")]:
        g.add_term(t)
    assert len(g.classes()) == 8
    g.merge(g.add_term("a"), g.add_term("b"))
    g.merge(g.add_term("b"), g.add_term("c"))
    # the parents f(a) and f(c) of the two classes that were linked below
    assert sorted(n[0] for n, _ in g.pending) == ["f", "f"]
    assert len(g.pending) == 2
    assert g.rebuild() == 3
    assert len(g.classes()) == 3
    assert g.lookup(("g", ("f", "c"))) == g.lookup(("g", ("f", "a")))
    assert g.lookup(("g", "c")) is None


def test_cyclic_class_represents_infinitely_many_terms():
    g = EGraph()
    a = g.add_term("a")
    fa = g.add_term(("f", "a"))
    g.merge(fa, a)
    g.rebuild()
    assert len(g.classes()) == 1
    assert g.lookup(f(25)) == g.find(a)
    assert g.lookup(("f", "b")) is None
    assert g.extract()[g.find(a)] == (1, "a")


def test_hash_cons_shares_nodes():
    g = EGraph()
    x = g.add_term(("g", "a", ("f", "a")))
    count = len(g.uf)
    assert g.add_term(("g", "a", ("f", "a"))) == x
    assert len(g.uf) == count == 3
    g.merge(g.lookup("a"), g.lookup(("f", "a")))
    g.rebuild()
    # g(a, f(a)) and g(f(a), a) are now congruent, so adding one creates nothing
    assert g.add_term(("g", ("f", "a"), "a")) == g.find(x)
    assert len(g.classes()) == 2


def test_random_operations_against_naive_closure():
    rng = random.Random(2021)
    for _ in range(400):
        g = EGraph()
        added, eqs = [], []
        for _ in range(rng.randint(3, 12)):
            r = rng.random()
            if r < 0.5 or len(added) < 2:
                t = random_term(rng, 3)
                g.add_term(t)
                added.append(t)
            elif r < 0.85:
                s, t = rng.choice(added), rng.choice(added)
                eqs.append((s, t))
                # find() never needs a rebuild, so merging is always allowed
                g.merge(g.add_term(s), g.add_term(t))
            else:
                g.rebuild()
            # before a rebuild, the classes are a refinement of the closure
            terms = set()
            for t in added:
                subterms(t, terms)
            ref = naive_closure(terms, eqs)
            ids = {t: g.find(g.add_term(t)) for t in terms}
            for x in terms:
                for y in terms:
                    if ids[x] == ids[y]:
                        assert ref[x] == ref[y]
        g.rebuild()
        terms = set()
        for t in added:
            subterms(t, terms)
        ref = naive_closure(terms, eqs)
        for x in terms:
            assert g.lookup(x) is not None
            for y in terms:
                assert (g.lookup(x) == g.lookup(y)) == (ref[x] == ref[y])
        # the congruence invariant on all e-nodes
        canon = {}
        for c in g.classes():
            for n in g.enodes(c):
                assert canon.setdefault(n, c) == c


def all_terms(max_size):
    """All terms over a, b, f/1, g/2 with at most max_size symbols."""
    by_size = {1: ["a", "b"]}
    for s in range(2, max_size + 1):
        out = [("f", t) for t in by_size[s - 1]]
        for i in range(1, s - 1):
            out += [("g", x, y) for x in by_size[i] for y in by_size[s - 1 - i]]
        by_size[s] = out
    return [t for s in range(1, max_size + 1) for t in by_size[s]]


def test_lookup_and_extract_against_enumeration():
    rng = random.Random(7)
    universe = all_terms(6)
    for _ in range(60):
        g = EGraph()
        pool = [random_term(rng, 2) for _ in range(6)]
        pool = [t for t in pool if "'c'" not in repr(t) and t != "c"] or ["a"]
        eqs = [(rng.choice(pool), rng.choice(pool)) for _ in range(2)]
        for t in pool:
            g.add_term(t)
        for s, t in eqs:
            g.merge(g.add_term(s), g.add_term(t))
        g.rebuild()
        best = g.extract(cost=lambda n: 1)
        # brute force: the smallest enumerated term that each class represents
        smallest = {}
        for t in universe:
            c = g.lookup(t)
            if c is not None and c not in smallest:
                smallest[c] = size(t)
        for c, (cost, term) in best.items():
            assert g.lookup(term) == c
            assert cost == size(term)
            if c in smallest:
                assert cost == smallest[c]
            else:
                assert cost > 6
