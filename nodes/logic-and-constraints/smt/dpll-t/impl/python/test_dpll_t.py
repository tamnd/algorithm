# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dpll-t/. The authors are listed in prov/R9CQRP.jsonl.
"""Tests against brute force over interpretations on a small domain.

By the small model property of EUF, a satisfiable formula whose atoms use m
distinct subterms has a model with at most m elements: keep only the values
of the subterms. So it is enough to try all ways to give values to the
subterms that respect functional consistency, up to a renaming of values.
"""

import itertools
import random

from dpll_t import DPLLT, EUFTheory, dpll_t


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
    return out  # each term after its arguments


def valuations(pool):
    """All maps from the pool to values that some interpretation gives,
    with values numbered in order of first use."""
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
    """The set of truth vectors of the atoms over all interpretations."""
    pool = pool_of([x for st in atoms.values() for x in st])
    vs = sorted(atoms)
    out = set()
    for val in valuations(pool):
        out.add(tuple(val[atoms[v][0]] == val[atoms[v][1]] for v in vs))
    return vs, out


def brute_force(clauses, atoms, vectors=None):
    vs, vecs = vectors or achievable(atoms)
    boolean = sorted({abs(l) for c in clauses for l in c} - set(atoms))
    for vec in vecs:
        a = dict(zip(vs, vec))
        for bits in itertools.product([False, True], repeat=len(boolean)):
            a.update(zip(boolean, bits))
            if all(any(a.get(abs(l), False) == (l > 0) for l in c) for c in clauses):
                return True
    return False


def f(n, x="a"):
    for _ in range(n):
        x = ("f", x)
    return x


def check_model(clauses, atoms, model, vecs):
    vs, achievable_vectors = vecs
    for c in clauses:
        assert any(model[abs(l)] == (l > 0) for l in c)
    assert tuple(model[v] for v in vs) in achievable_vectors


def check_lemma(lemma, atoms):
    """The negation of a lemma is a set of theory literals with no model, and
    each literal is needed (the theory solver returns minimal conflicts)."""
    lits = [(atoms[abs(l)][0], atoms[abs(l)][1], l < 0) for l in lemma]
    th = EUFTheory()
    assert not th.consistent(lits)
    for i in range(len(lits)):
        assert th.consistent(lits[:i] + lits[i + 1:])


def test_page_example():
    # (a = b or a = c) and f(a) != f(b) and f(a) != f(c)
    atoms = {1: ("a", "b"), 2: ("a", "c"), 3: (("f", "a"), ("f", "b")), 4: (("f", "a"), ("f", "c"))}
    solver = DPLLT([[1, 2], [-3], [-4]], atoms)
    assert solver.solve() == (False, None)
    for lemma in solver.lemmas:
        check_lemma(lemma, atoms)
    # (a = b or b = c) and f(a) != f(c) is satisfiable
    atoms = {1: ("a", "b"), 2: ("b", "c"), 3: (("f", "a"), ("f", "c"))}
    ok, model = dpll_t([[1, 2], [-3]], atoms)
    assert ok and model[3] is False
    check_model([[1, 2], [-3]], atoms, model, achievable(atoms))


def test_cycle_example():
    atoms = {1: (f(3), "a"), 2: (f(5), "a"), 3: (f(1), "a")}
    assert dpll_t([[1], [2], [-3]], atoms) == (False, None)
    ok, model = dpll_t([[1], [-3]], atoms)
    assert ok and model[1] and not model[3]


def test_boolean_variables_and_empty_inputs():
    assert dpll_t([], {}) == (True, {})
    assert dpll_t([[]], {}) == (False, None)
    atoms = {1: ("a", "b")}
    # variable 2 is a plain Boolean variable
    ok, model = dpll_t([[2, -1], [-2, 1], [1]], atoms)
    assert ok and model == {1: True, 2: True}


POOLS = [
    ["a", "b", "c", ("f", "a"), ("f", "b"), ("f", ("f", "a"))],
    [f(i) for i in range(6)],
    ["a", "b", ("g", "a", "b"), ("g", "b", "a"), ("f", "a"), ("f", "b")],
    ["x", "y", "z", ("h", "x"), ("h", "y"), ("h", ("h", "z"))],
]


def random_instance(rng, pool):
    pairs = [(s, t) for s, t in itertools.combinations(pool, 2)]
    chosen = rng.sample(pairs, rng.randint(2, 6))
    atoms = {i + 1: st for i, st in enumerate(chosen)}
    nv = len(atoms)
    clauses = []
    for _ in range(rng.randint(1, 8)):
        k = rng.randint(1, 3)
        clauses.append([rng.choice([1, -1]) * rng.randint(1, nv) for _ in range(k)])
    return clauses, atoms


def test_random_against_brute_force():
    rng = random.Random(2006)
    counts = {True: 0, False: 0}
    for trial in range(500):
        pool = POOLS[trial % len(POOLS)]
        clauses, atoms = random_instance(rng, pool)
        vecs = achievable(atoms)
        expected = brute_force(clauses, atoms, vecs)
        for tp in (True, False):
            solver = DPLLT(clauses, atoms, theory_propagate=tp)
            ok, model = solver.solve()
            assert ok == expected
            if ok:
                check_model(clauses, atoms, model, vecs)
            for lemma in solver.lemmas:
                check_lemma(lemma, atoms)
        counts[expected] += 1
    assert counts[True] > 50 and counts[False] > 50


def test_minimal_conflict():
    th = EUFTheory()
    lits = [("b", ("f", "b"), True), (("f", "a"), "a", True), (("f", "b"), "a", True),
            ("c", "d", True), ("b", ("f", "a"), False)]
    core = th.conflict(lits)
    # c = d is not needed, and each kept literal is needed
    assert 3 not in core and 4 in core
    kept = [lits[j] for j in core]
    assert not th.consistent(kept)
    for i in range(len(kept)):
        assert th.consistent(kept[:i] + kept[i + 1:])
