# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/congruence-closure/. The authors are listed in prov/QSSXKY.jsonl.

import random

from congruence_closure import CongruenceClosure, euf_satisfiable


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
    """The reference: start from the input equations and apply congruence
    to every pair of terms until nothing changes. Returns a class map."""
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


def test_page_example():
    cc = CongruenceClosure()
    cc.merge(f(3), "a", 1)
    assert not cc.are_equal(f(1), "a")
    cc.merge(f(5), "a", 2)
    assert cc.are_equal(f(1), "a")
    assert cc.explain(f(1), "a") == {1, 2}
    assert len(cc.classes()) == 1
    assert not euf_satisfiable([(f(3), "a"), (f(5), "a")], [(f(1), "a")])
    assert euf_satisfiable([(f(3), "a")], [(f(1), "a")])


def test_binary_and_shared_arguments():
    cc = CongruenceClosure()
    for t in [("g", "a", "b"), ("g", "b", "a"), ("g", "a", "a")]:
        cc.add_term(t)
    cc.merge("a", "b", "ab")
    assert cc.are_equal(("g", "a", "b"), ("g", "b", "a"))
    assert cc.are_equal(("g", "a", "a"), ("g", "b", "a"))
    assert cc.explain(("g", "a", "b"), ("g", "b", "a")) == {"ab"}
    assert not cc.are_equal(("g", "a", "b"), "a")


def test_same_symbol_different_arity_stays_apart():
    cc = CongruenceClosure()
    cc.add_term(("h", "a"))
    cc.add_term(("h", "a", "a"))
    assert not cc.are_equal(("h", "a"), ("h", "a", "a"))


def test_empty_and_reflexive():
    cc = CongruenceClosure()
    assert cc.are_equal("a", "a")
    assert cc.explain("a", "a") == set()
    assert euf_satisfiable([], [])
    assert not euf_satisfiable([], [("a", "a")])


def test_deep_term_has_no_recursion_limit():
    cc = CongruenceClosure()
    cc.merge(f(3000), "a", 0)
    cc.merge(f(1), "a", 1)
    assert cc.are_equal(f(2999), "a")


def random_term(rng, depth):
    if depth == 0 or rng.random() < 0.35:
        return rng.choice("abc")
    if rng.random() < 0.6:
        return ("f", random_term(rng, depth - 1))
    return ("g", random_term(rng, depth - 1), random_term(rng, depth - 1))


def test_random_against_naive_fixpoint():
    rng = random.Random(4242)
    for _ in range(600):
        pool = [random_term(rng, 3) for _ in range(rng.randint(2, 7))]
        eqs = [(rng.choice(pool), rng.choice(pool)) for _ in range(rng.randint(0, 4))]
        terms = set()
        for t in pool:
            subterms(t, terms)
        ref = naive_closure(terms, eqs)
        cc = CongruenceClosure()
        for t in terms:
            cc.add_term(t)
        for i, (s, t) in enumerate(eqs):
            cc.merge(s, t, i)
        tl = sorted(terms, key=repr)
        for x in tl:
            for y in tl:
                assert cc.are_equal(x, y) == (ref[x] == ref[y])
                if ref[x] == ref[y]:
                    expl = cc.explain(x, y)
                    # the explanation alone must give the equality
                    sub = [eqs[i] for i in expl]
                    ref2 = naive_closure(terms, sub)
                    assert ref2[x] == ref2[y]


def test_explanation_is_a_conflict():
    rng = random.Random(77)
    found = 0
    for _ in range(400):
        pool = [random_term(rng, 2) for _ in range(5)]
        eqs = [(rng.choice(pool), rng.choice(pool)) for _ in range(3)]
        s, t = rng.choice(pool), rng.choice(pool)
        cc = CongruenceClosure()
        for i, (x, y) in enumerate(eqs):
            cc.merge(x, y, i)
        cc.add_term(s)
        cc.add_term(t)
        if s != t and cc.are_equal(s, t):
            found += 1
            core = [eqs[i] for i in cc.explain(s, t)]
            assert not euf_satisfiable(core, [(s, t)])
    assert found > 30
