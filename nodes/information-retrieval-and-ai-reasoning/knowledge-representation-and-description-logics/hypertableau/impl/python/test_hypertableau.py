# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hypertableau/. The authors are listed in prov/974KXE.jsonl.
"""Tests of the hypertableau calculus against the plain ALC tableau of alc_reference.py.

Every "satisfiable" answer is also checked on its own: the model built from the open branch must
put the root in the concept and satisfy every inclusion of the TBox, by the semantics in dl.py.
"""

import random

import alc_reference as ref
from dl import BOTTOM, atom, conj, disj, evaluate, exists, forall, is_model_of_tbox, neg
from hypertableau import clausify, model_of, satisfiable, satisfiable_count, subsumes

A, B, C, D, E, W = (atom(x) for x in "ABCDEW")


def check(c, tbox) -> bool:
    ok, _, s = satisfiable_count(c, tbox)
    assert ok == ref.satisfiable(c, tbox)
    if ok:
        m = model_of(s)
        assert 0 in evaluate(c, m) and is_model_of_tbox(m, tbox)
    return ok


def test_page_example() -> None:
    # not A and some r.some r.A, with some r.A subsumed by A: unsatisfiable without any choice.
    c = conj(neg(A), exists("r", exists("r", A)))
    tbox = [(exists("r", A), A)]
    root, clauses = clausify(c, tbox)
    assert len(clauses) == 4
    assert (frozenset(), ("r",), (frozenset({"A"}),), (("x", "A"),)) in clauses
    ok, cnt, _ = satisfiable_count(c, tbox)
    assert not ok and cnt.nodes == 2 and cnt.branches == 0 and cnt.hyp == 5
    r_ok, r_cnt = ref.satisfiable_count(c, tbox)
    assert not r_ok and r_cnt.nodes == 3 and r_cnt.branches == 7


def test_clause_shapes() -> None:
    # A and B subsumed by C or for all r.D: one clause, two head atoms, one successor variable.
    _, clauses = clausify(A, [(conj(A, B), disj(C, forall("r", D)))])
    assert (frozenset({"A", "B"}), ("r",), (frozenset(),), (("x", "C"), ("y", 0, "D"))) in clauses
    # for all r.not A in a head goes to the body as A(y).
    _, clauses = clausify(A, [(B, forall("r", neg(A)))])
    assert (frozenset({"B"}), ("r",), (frozenset({"A"}),), ()) in clauses


def test_cyclic_tbox_needs_blocking() -> None:
    ok, cnt, s = satisfiable_count(A, [(A, exists("r", A))])
    assert ok and cnt.nodes == 1
    m = model_of(s)
    assert m.domain == [0] and m.roles["r"] == {(0, 0)}
    assert check(A, [(A, exists("r", A))])


def test_subset_blocking_is_unsound() -> None:
    # The child made for some r.W has the label {W, some r.B}, a subset of the root label. Subset
    # blocking stops there and misses that its B-successor forces A, which the root forbids.
    c = conj(A, W, exists("r", W), forall("r", neg(A)))
    tbox = [(W, exists("r", B)), (exists("r", B), A)]
    assert not ref.satisfiable(c, tbox)
    assert not satisfiable_count(c, tbox, "equal")[0]
    assert satisfiable_count(c, tbox, "subset")[0]


def test_backjumping() -> None:
    # m independent choices, then a choice whose both sides clash on their own.
    for m in range(1, 9):
        c = conj(*[disj(atom(f"B{i}"), atom(f"C{i}")) for i in range(m)], disj(D, E), neg(D), neg(E))
        ok, cnt, _ = satisfiable_count(c)
        assert not ok and cnt.branches == m + 2


def test_or_branching_family() -> None:
    # B_i subsumed by C_i for i < m, and A subsumed by some r.D with D unsatisfiable. The plain
    # tableau adds not B_i or C_i to every node and tries 2^m completions of the root; the
    # clauses B_i(x) -> C_i(x) never fire.
    last = 0
    for m in range(0, 6):
        tbox = [(atom(f"B{i}"), atom(f"C{i}")) for i in range(m)] + [(A, exists("r", D)), (D, E), (E, BOTTOM)]
        ok, cnt, _ = satisfiable_count(A, tbox)
        assert not ok and cnt.nodes == 1 and cnt.branches == 0 and cnt.hyp == 3
        r_ok, r_cnt = ref.satisfiable_count(A, tbox)
        assert not r_ok and r_cnt.nodes == 2 ** m + 1 and r_cnt.branches > last
        last = r_cnt.branches


def rand_concept(rng: random.Random, d: int, cn, rn):
    if d == 0 or rng.random() < 0.3:
        a = atom(rng.choice(cn))
        return neg(a) if rng.random() < 0.4 else a
    k = rng.random()
    if k < 0.25:
        return conj(rand_concept(rng, d - 1, cn, rn), rand_concept(rng, d - 1, cn, rn))
    if k < 0.5:
        return disj(rand_concept(rng, d - 1, cn, rn), rand_concept(rng, d - 1, cn, rn))
    if k < 0.75:
        return exists(rng.choice(rn), rand_concept(rng, d - 1, cn, rn))
    if k < 0.9:
        return forall(rng.choice(rn), rand_concept(rng, d - 1, cn, rn))
    return neg(rand_concept(rng, d - 1, cn, rn))


def run_random(seed: int, count: int, cn, rn) -> list[int]:
    rng = random.Random(seed)
    seen = [0, 0]
    for _ in range(count):
        c = rand_concept(rng, 3, cn, rn)
        tbox = [(rand_concept(rng, 2, cn, rn), rand_concept(rng, 2, cn, rn)) for _ in range(rng.randint(0, 3))]
        seen[check(c, tbox)] += 1
    return seen


def test_random_one_role() -> None:
    unsat, sat = run_random(1, 2000, ["A", "B"], ["r"])
    assert unsat >= 150 and sat >= 1500


def test_random_two_roles() -> None:
    unsat, sat = run_random(6, 1000, ["A", "B", "C"], ["r", "s"])
    assert unsat >= 40 and sat >= 800


def test_subsumption() -> None:
    tbox = [(exists("r", A), A)]
    assert subsumes(exists("r", exists("r", A)), A, tbox)
    assert not subsumes(A, exists("r", A), tbox)
