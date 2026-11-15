# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alc-tableau-algorithm/. The authors are listed in prov/W9NV76.jsonl.
"""Tests of the ALC tableau against the semantics.

Two kinds of reference are used.
1. Evaluation over every interpretation with at most 3 elements (dl.interpretations). When the
   tableau says "satisfiable", the test checks the model that the tableau returns, by evaluation.
   When the tableau says "unsatisfiable", the test checks that no interpretation with at most 3
   elements is a model. A failed search over small domains is not a proof of unsatisfiability: a
   satisfiable ALC concept can need more elements (test_small_search_is_not_a_proof). So this check
   can catch a wrong "unsatisfiable", but it cannot confirm a right one. The proof is in
   proofs/correctness.md.
2. Known subsumptions from the textbooks, with and without a general TBox.
"""

import random
from itertools import permutations

import pytest

import dl
from alc_tableau_algorithm import NonTermination, is_satisfiable, subsumes, tableau
from dl import TOP, BOTTOM, atom, conj, disj, exists, forall, neg

A, B, C = atom("A"), atom("B"), atom("C")


def rand_concept(rng: random.Random, depth: int, atoms=("A", "B"), roles=("r",)) -> tuple:
    if depth == 0 or rng.random() < 0.25:
        x = rng.random()
        if x < 0.06:
            return TOP
        if x < 0.09:
            return BOTTOM
        a = atom(rng.choice(atoms))
        return neg(a) if rng.random() < 0.4 else a
    op = rng.choice(["not", "and", "and", "or", "or", "some", "some", "all"])
    if op == "not":
        return neg(rand_concept(rng, depth - 1, atoms, roles))
    if op in ("and", "or"):
        f = conj if op == "and" else disj
        return f(rand_concept(rng, depth - 1, atoms, roles), rand_concept(rng, depth - 1, atoms, roles))
    q = exists if op == "some" else forall
    return q(rng.choice(roles), rand_concept(rng, depth - 1, atoms, roles))


def _canonical(i: dl.Interpretation, cn, rn) -> tuple:
    n = len(i.domain)
    best = None
    for p in permutations(range(n)):
        key = (n,
               tuple(tuple(sorted(p[x] for x in i.concepts.get(a, ()))) for a in cn),
               tuple(tuple(sorted((p[x], p[y]) for x, y in i.roles.get(r, ()))) for r in rn))
        if best is None or key < best:
            best = key
    return best


_SMALL: dict = {}


def small_interpretations(cn=("A", "B"), rn=("r",), max_size=3) -> list:
    """All interpretations with at most max_size elements, one from each isomorphism class.
    ALC concepts and inclusions do not change under a renaming of the elements."""
    key = (cn, rn, max_size)
    if key not in _SMALL:
        seen = set()
        out = []
        for i in dl.interpretations(cn, rn, max_size):
            k = _canonical(i, cn, rn)
            if k not in seen:
                seen.add(k)
                out.append(i)
        _SMALL[key] = out
    return _SMALL[key]


def small_model_exists(c, tbox=(), cn=("A", "B"), rn=("r",), max_size=3) -> bool:
    return any(dl.evaluate(c, i) and dl.is_model_of_tbox(i, tbox) for i in small_interpretations(cn, rn, max_size))


def check_result(c, tbox=(), cn=("A", "B"), rn=("r",), max_size=3) -> bool:
    res = tableau(c, tbox)
    if res.satisfiable:
        m = res.model
        assert 0 in dl.evaluate(c, m), dl.show(c)
        assert dl.is_model_of_tbox(m, tbox), dl.show(c)
    else:
        assert not small_model_exists(c, tbox, cn, rn, max_size), dl.show(c)
    return res.satisfiable


def test_small_search_is_not_a_proof() -> None:
    # Four elements with four different types along an r-chain: satisfiable, but no model has 3 elements.
    c = conj(A, neg(B), exists("r", conj(neg(A), B, exists("r", conj(neg(A), neg(B), exists("r", conj(A, B)))))))
    res = tableau(c)
    assert res.satisfiable and len(res.model.domain) == 4
    assert not small_model_exists(c)


def test_helper_counts_and_nnf() -> None:
    # 2^(n*2 + n*n) interpretations for each n: 8 + 256 + 32768.
    assert sum(1 for _ in dl.interpretations(("A", "B"), ("r",), 3)) == 8 + 256 + 32768
    rng = random.Random(7)
    small = small_interpretations(max_size=2)
    for _ in range(200):
        c = rand_concept(rng, 4)
        n = dl.nnf(c)
        assert dl.is_nnf(n)
        assert all(dl.evaluate(c, i) == dl.evaluate(n, i) for i in small)


def test_basic_cases() -> None:
    assert is_satisfiable(A)
    assert not is_satisfiable(conj(A, neg(A)))
    assert not is_satisfiable(BOTTOM)
    assert is_satisfiable(TOP)
    assert not is_satisfiable(conj(exists("r", A), forall("r", neg(A))))
    assert is_satisfiable(conj(exists("r", A), forall("r", B)))
    assert is_satisfiable(conj(forall("r", BOTTOM), A))  # no successor at all
    assert not is_satisfiable(conj(exists("r", TOP), forall("r", BOTTOM)))
    # The worked example of the page: one or-choice fails, the other succeeds.
    ex = conj(exists("r", A), forall("r", disj(neg(A), B)), forall("r", neg(B)))
    assert not is_satisfiable(ex)
    ex2 = conj(disj(A, exists("r", B)), neg(A), forall("r", disj(neg(B), C)))
    res = tableau(ex2)
    assert res.satisfiable and len(res.model.domain) == 2


def test_textbook_subsumptions_empty_tbox() -> None:
    # Equivalences and subsumptions of ALC (Baader et al. 2017, chapter 2; Handbook, chapter 2).
    def equiv(x, y):
        return subsumes(x, y) and subsumes(y, x)

    assert equiv(forall("r", conj(A, B)), conj(forall("r", A), forall("r", B)))
    assert equiv(exists("r", disj(A, B)), disj(exists("r", A), exists("r", B)))
    assert equiv(neg(exists("r", A)), forall("r", neg(A)))
    assert subsumes(conj(exists("r", A), forall("r", B)), exists("r", conj(A, B)))
    assert subsumes(exists("r", conj(A, B)), exists("r", A))
    assert not subsumes(exists("r", A), exists("r", conj(A, B)))
    assert not subsumes(forall("r", A), exists("r", A))  # an element with no successor
    assert subsumes(conj(forall("r", A), exists("r", TOP)), exists("r", A))
    assert subsumes(disj(forall("r", A), forall("r", B)), forall("r", disj(A, B)))
    assert not subsumes(forall("r", disj(A, B)), disj(forall("r", A), forall("r", B)))
    assert subsumes(BOTTOM, A) and subsumes(A, TOP)


FAMILY_NAMES = ["Person", "Female", "Woman", "Man", "Mother", "Father", "Parent", "Grandmother", "MotherWithoutDaughter", "Wife"]
P = {n: atom(n) for n in FAMILY_NAMES}


def family_tbox() -> list:
    """The family TBox of the Description Logic Handbook, chapter 2, without the number restriction.
    Each definition A = D gives two inclusions."""
    hc = "hasChild"
    defs = [
        ("Woman", conj(P["Person"], P["Female"])),
        ("Man", conj(P["Person"], neg(P["Woman"]))),
        ("Mother", conj(P["Woman"], exists(hc, P["Person"]))),
        ("Father", conj(P["Man"], exists(hc, P["Person"]))),
        ("Parent", disj(P["Father"], P["Mother"])),
        ("Grandmother", conj(P["Mother"], exists(hc, P["Parent"]))),
        ("MotherWithoutDaughter", conj(P["Mother"], forall(hc, neg(P["Woman"])))),
        ("Wife", conj(P["Woman"], exists("hasHusband", P["Man"]))),
    ]
    out = []
    for a, d in defs:
        out.append((P[a], d))
        out.append((d, P[a]))
    return out


def test_family_tbox() -> None:
    t = family_tbox()
    yes = [("Woman", "Person"), ("Mother", "Person"), ("Mother", "Parent"), ("Father", "Parent"),
           ("Grandmother", "Parent"), ("Grandmother", "Mother"), ("Parent", "Person"),
           ("MotherWithoutDaughter", "Mother"), ("Wife", "Woman")]
    no = [("Person", "Woman"), ("Parent", "Mother"), ("Mother", "Grandmother"), ("Man", "Father"),
          ("Wife", "Mother"), ("Mother", "MotherWithoutDaughter")]
    for x, y in yes:
        assert subsumes(P[x], P[y], t), (x, y)
    for x, y in no:
        res = tableau(conj(P[x], neg(P[y])), t)
        assert res.satisfiable, (x, y)
        m = res.model
        assert dl.is_model_of_tbox(m, t)
        assert 0 in dl.evaluate(P[x], m) and 0 not in dl.evaluate(P[y], m)
    assert not is_satisfiable(conj(P["Man"], P["Woman"]), t)
    assert subsumes(P["Parent"], exists("hasChild", P["Person"]), t)
    assert subsumes(P["Grandmother"], exists("hasChild", exists("hasChild", P["Person"])), t)
    # Without the TBox the names are unrelated.
    assert not subsumes(P["Mother"], P["Person"])


def test_general_tbox_needs_blocking() -> None:
    t = [(A, exists("r", A))]
    res = tableau(A, t)
    assert res.satisfiable and res.stats.blocked >= 1
    assert dl.is_model_of_tbox(res.model, t) and 0 in dl.evaluate(A, res.model)
    with pytest.raises(NonTermination):
        tableau(A, t, blocking=False)
    # A is subsumed by C. The first inclusion is cyclic, so the search for A and not C needs blocking.
    t2 = [(A, exists("r", A)), (A, B), (exists("r", B), C)]
    assert subsumes(A, C, t2)
    assert not subsumes(C, A, t2)
    # Every A has an A-successor that is not A: A is unsatisfiable.
    t3 = [(A, exists("r", A)), (A, forall("r", neg(A)))]
    assert not is_satisfiable(A, t3)
    assert is_satisfiable(neg(A), t3)
    # The universal TBox axiom top subsumed by all r.A.
    t4 = [(TOP, forall("r", A))]
    assert subsumes(exists("r", TOP), exists("r", A), t4)
    assert subsumes(exists("r", exists("r", TOP)), exists("r", conj(A, exists("r", A))), t4)
    # A cycle through two names: A needs a B-successor and B needs an A-successor.
    t5 = [(A, exists("r", B)), (B, exists("r", A)), (A, neg(B))]
    res = tableau(A, t5)
    assert res.satisfiable and dl.is_model_of_tbox(res.model, t5)
    assert subsumes(A, exists("r", exists("r", exists("r", B))), t5)


def test_empty_tbox_random_against_semantics() -> None:
    rng = random.Random(2024)
    seen = {True: 0, False: 0}
    for _ in range(300):
        c = rand_concept(rng, 4)
        res = tableau(c)
        seen[check_result(c)] += 1
        # Without a TBox the tree is no deeper than the role depth of the concept.
        assert res.stats.depth <= dl.role_depth(dl.nnf(c))
        assert res.stats.blocked == 0
    assert seen[True] > 50 and seen[False] > 20, seen


def test_general_tbox_random_against_semantics() -> None:
    rng = random.Random(99)
    seen = {True: 0, False: 0}
    for _ in range(150):
        tbox = [(rand_concept(rng, 2), rand_concept(rng, 2)) for _ in range(rng.randint(1, 2))]
        c = rand_concept(rng, 3)
        seen[check_result(c, tbox)] += 1
    assert seen[True] > 20 and seen[False] > 20, seen


def test_subsumption_by_reduction() -> None:
    rng = random.Random(5)
    for k in range(100):
        tbox = [] if k % 2 == 0 else [(rand_concept(rng, 2), rand_concept(rng, 2))]
        c, d = rand_concept(rng, 3), rand_concept(rng, 3)
        res = tableau(conj(c, neg(d)), tbox)
        assert subsumes(c, d, tbox) == (not res.satisfiable)
        if res.satisfiable:  # a countermodel: element 0 is in c and not in d
            m = res.model
            assert 0 in dl.evaluate(c, m) and 0 not in dl.evaluate(d, m)
        else:
            small = small_interpretations()
            assert all(dl.evaluate(c, i) <= dl.evaluate(d, i) for i in small if dl.is_model_of_tbox(i, tbox))


def test_two_roles() -> None:
    # With two roles the brute force uses domains of at most 2 elements (1024 interpretations for n = 2).
    rng = random.Random(11)
    for _ in range(120):
        c = rand_concept(rng, 3, atoms=("A",), roles=("r", "s"))
        check_result(c, (), cn=("A",), rn=("r", "s"), max_size=2)
