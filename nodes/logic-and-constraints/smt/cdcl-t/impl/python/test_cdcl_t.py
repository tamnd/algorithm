# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cdcl-t/. The authors are listed in prov/R7T2R4.jsonl.
"""Tests against brute force over interpretations on a small domain.

A satisfiable EUF formula whose atoms use m distinct subterms has a model
with at most m elements (keep only the values of the subterms). So the
oracle tries every way to give values to the subterms that respects
functional consistency, up to a renaming of the values.
"""

import itertools
import random

from cdcl_t import CDCLT, CongruenceClosure, cdcl_t


def pool_of(terms):
    out = []

    def add(t):
        if t in out:
            return
        if isinstance(t, tuple):
            for a in t[1:]:
                add(a)
        out.append(t)

    for t in terms:
        add(t)
    return out


def valuations(pool):
    n = len(pool)
    val, fun = {}, {}

    def rec(i, top):
        if i == n:
            yield dict(val)
            return
        t = pool[i]
        key = (t[0], tuple(val[a] for a in t[1:])) if isinstance(t, tuple) else ("const", t)
        if key in fun:
            val[t] = fun[key]
            yield from rec(i + 1, top)
            del val[t]
            return
        for v in range(top + 1):
            val[t] = v
            fun[key] = v
            yield from rec(i + 1, top + 1 if v == top else top)
            del fun[key]
            del val[t]

    yield from rec(0, 0)


def achievable(atoms):
    pool = pool_of([x for st in atoms.values() for x in st])
    vs = sorted(atoms)
    return vs, {tuple(val[atoms[v][0]] == val[atoms[v][1]] for v in vs) for val in valuations(pool)}


def satisfiable(clauses, atoms, vecs):
    vs, vectors = vecs
    boolean = sorted({abs(l) for c in clauses for l in c} - set(atoms))
    for vec in vectors:
        a = dict(zip(vs, vec))
        for bits in itertools.product([False, True], repeat=len(boolean)):
            a.update(zip(boolean, bits))
            if all(any(a.get(abs(l), False) == (l > 0) for l in c) for c in clauses):
                return True
    return False


def theory_valid(clause, atoms):
    """The negation of the clause, a conjunction of EUF literals, has no model."""
    sub = {abs(l): atoms[abs(l)] for l in clause}
    vecs = achievable(sub)
    return not satisfiable([[l] for l in (-x for x in clause)], sub, vecs)


def f(n, x="a"):
    for _ in range(n):
        x = ("f", x)
    return x


def test_page_example():
    # x, w, y, q are Boolean; 5 is a = b, 6 is b = c, 7 is f(a) = f(c)
    atoms = {5: ("a", "b"), 6: ("b", "c"), 7: (("f", "a"), ("f", "c"))}
    clauses = [[-1, 5], [-3, 6], [-7, 4], [-7, -4], [1, 2]]
    s = CDCLT(clauses, atoms, restart_first=100)
    ok, model = s.solve()
    assert ok
    assert model == {1: True, 2: True, 3: False, 4: True, 5: True, 6: False, 7: False}
    # the first UIP of the first conflict is the theory-propagated f(a) = f(c)
    assert s.learned == [[-7], [-6, -5]]
    assert s.theory_clauses == [[7, -5, -6], [7, -5, -6]]
    assert s.stats["t_propagations"] == 1 and s.stats["theory_conflicts"] == 1


def test_split_example():
    # (a = b or a = c) and f(a) != f(b) and f(a) != f(c)
    atoms = {1: ("a", "b"), 2: ("a", "c"), 3: (("f", "a"), ("f", "b")), 4: (("f", "a"), ("f", "c"))}
    s = CDCLT([[1, 2], [-3], [-4]], atoms)
    assert s.solve() == (False, None)
    assert s.learned == [[-1]]
    assert sorted(s.theory_clauses) == sorted([[3, -1], [4, -2]])


def test_learning_across_theory_reasons():
    # x1 -> a = b, x2 -> b = c, and f(a) != f(c); the conflict is at the theory
    atoms = {3: ("a", "b"), 4: ("b", "c"), 5: (("f", "a"), ("f", "c"))}
    clauses = [[-1, 3], [-2, 4], [-5], [1, 6], [2, 6], [-6, 7], [-6, -7]]
    s = CDCLT(clauses, atoms)
    ok, model = s.solve()
    assert not ok
    assert s.learned  # a clause was learned through a theory reason


def test_cycle_and_boolean():
    atoms = {1: (f(3), "a"), 2: (f(5), "a"), 3: (f(1), "a")}
    assert cdcl_t([[1], [2], [-3]], atoms) == (False, None)
    assert cdcl_t([], {}) == (True, {})
    assert cdcl_t([[]], {}) == (False, None)
    ok, model = cdcl_t([[2, -1], [-2, 1], [1]], {1: ("a", "b")})
    assert ok and model == {1: True, 2: True}


POOLS = [
    ["a", "b", "c", ("f", "a"), ("f", "b"), ("f", ("f", "a"))],
    [f(i) for i in range(6)],
    ["a", "b", ("g", "a", "b"), ("g", "b", "a"), ("f", "a"), ("f", "b")],
    ["x", "y", "z", ("h", "x"), ("h", "y"), ("h", ("h", "z"))],
]


def random_instance(rng, pool):
    pairs = list(itertools.combinations(pool, 2))
    chosen = rng.sample(pairs, rng.randint(2, 7))
    atoms = {i + 1: st for i, st in enumerate(chosen)}
    nv = len(atoms) + rng.randint(0, 2)  # some plain Boolean variables
    clauses = []
    for _ in range(rng.randint(1, 10)):
        k = rng.randint(1, 3)
        clauses.append([rng.choice([1, -1]) * rng.randint(1, nv) for _ in range(k)])
    return clauses, atoms


def test_random_against_brute_force():
    rng = random.Random(2004)
    counts = {True: 0, False: 0}
    learned_checked = 0
    for trial in range(500):
        pool = POOLS[trial % len(POOLS)]
        clauses, atoms = random_instance(rng, pool)
        vecs = achievable(atoms)
        expected = satisfiable(clauses, atoms, vecs)
        s = CDCLT(clauses, atoms, restart_first=2, restart_growth=1.3)
        ok, model = s.solve()
        assert ok == expected
        counts[expected] += 1
        if ok:
            for c in clauses:
                assert any(model[abs(l)] == (l > 0) for l in c)
            assert tuple(model[v] for v in vecs[0]) in vecs[1]
        # every explanation and theory conflict is a valid theory lemma
        for c in s.theory_clauses:
            assert theory_valid(c, atoms)
        # every learned clause follows from the input in the theory
        for c in s.learned:
            assert not satisfiable(clauses + [[-l] for l in c], atoms, vecs)
            learned_checked += 1
    assert counts[True] > 50 and counts[False] > 50
    assert learned_checked > 20


def test_explanations_are_conflicts():
    rng = random.Random(9)
    for _ in range(200):
        pool = POOLS[rng.randrange(len(POOLS))]
        eqs = [tuple(rng.sample(pool, 2)) for _ in range(3)]
        s, t = rng.sample(pool, 2)
        cc = CongruenceClosure()
        for i, (x, y) in enumerate(eqs):
            cc.merge(x, y, i)
        if cc.equal(s, t):
            core = {i: eqs[i] for i in cc.explain(s, t)}
            atoms = dict(core)
            atoms[-1] = (s, t)
            vs, vecs = achievable(atoms)
            # the explanation with s != t has no model
            assert not any(all(vec[vs.index(i)] for i in core) and not vec[vs.index(-1)] for vec in vecs)
