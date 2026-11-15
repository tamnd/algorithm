# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/el-classification/. The authors are listed in prov/JW3S50.jsonl.
"""Tests of EL classification against the semantics.

1. "No" answers: the canonical model built from S and R must be a model of the TBox (checked by
   evaluation with dl.py), and its element for A must not be in B. This check is exact.
2. "Yes" answers and unsatisfiable names: the ALC tableau of alc_reference.py must agree. EL with
   bottom is a part of ALC, so the tableau decides the same question by a different method.
3. Brute force over every interpretation with at most 2 elements: a small model of the TBox with an
   element in A and not in B would refute a "yes". This direction is sound; a failed search cannot
   confirm a "no", so the canonical model does that.
"""

import random

import alc_reference
import dl
from dl import BOTTOM, TOP, atom, conj, exists, neg
from el_classification import BOTN, NotEL, classify, complete, normalize, subsumes

NAMES = ["A", "B", "C"]
ROLES = ["r", "s"]


def rand_el(rng: random.Random, depth: int, names=NAMES, roles=ROLES) -> tuple:
    if depth == 0 or rng.random() < 0.35:
        x = rng.random()
        if x < 0.08:
            return TOP
        if x < 0.11:
            return BOTTOM
        return atom(rng.choice(names))
    if rng.random() < 0.5:
        return conj(rand_el(rng, depth - 1, names, roles), rand_el(rng, depth - 1, names, roles))
    return exists(rng.choice(roles), rand_el(rng, depth - 1, names, roles))


def rand_tbox(rng: random.Random, k: int, names=NAMES, roles=ROLES) -> list:
    return [(rand_el(rng, 2, names, roles), rand_el(rng, 2, names, roles)) for _ in range(k)]


def check_against_semantics(tbox: list, small: bool) -> tuple[int, int]:
    cn = NAMES
    comp = complete(tbox + [(atom(a), atom(a)) for a in cn])
    model = comp.canonical_model()
    small_models = []
    if small:
        rn = sorted({c[1] for gci in tbox for x in gci for c in dl.subconcepts(x) if c[0] == "some"})
        small_models = [i for i in dl.interpretations(cn, rn, 2) if dl.is_model_of_tbox(i, tbox)]
    if model is None:
        assert not alc_reference.satisfiable(TOP, tbox)
        return 0, 0
    assert dl.is_model_of_tbox(model, tbox)
    yes = no = 0
    for a in cn:
        if comp.unsatisfiable(a):
            assert not alc_reference.satisfiable(atom(a), tbox)
        for b in cn:
            if comp.subsumes(a, b):
                yes += 1
                assert alc_reference.subsumes(atom(a), atom(b), tbox), (a, b, tbox)
                for i in small_models:
                    assert dl.evaluate(atom(a), i) <= dl.evaluate(atom(b), i)
            else:
                no += 1
                x = comp.element(a)
                assert x in dl.evaluate(atom(a), model) and x not in dl.evaluate(atom(b), model)
    return yes, no


def test_page_example() -> None:
    P, I, D, Pc, H, HD = (atom(x) for x in ("Pericarditis", "Inflammation", "Disease", "Pericardium", "Heart", "HeartDisease"))
    tbox = [
        (P, conj(I, exists("loc", Pc))),
        (I, D),
        (Pc, exists("part", H)),
        (conj(D, exists("loc", exists("part", H))), HD),
    ]
    got = classify(tbox)
    assert got["Pericarditis"] == {"Pericarditis", "Inflammation", "Disease", "HeartDisease"}
    assert got["Inflammation"] == {"Inflammation", "Disease"}
    assert got["Pericardium"] == {"Pericardium"}
    assert not subsumes(tbox, I, HD)
    assert subsumes(tbox, conj(I, exists("loc", Pc)), HD)
    assert alc_reference.subsumes(P, HD, tbox)
    comp = complete(tbox)
    assert dl.is_model_of_tbox(comp.canonical_model(), tbox)


def test_normal_form_shapes() -> None:
    A, B, C = atom("A"), atom("B"), atom("C")
    axioms = normalize([(conj(A, exists("r", conj(B, C))), exists("s", conj(A, exists("r", TOP))))])
    for ax in axioms:
        assert ax[0] in ("sub", "conj", "ex_r", "ex_l")
        for x in ax[1:]:
            assert isinstance(x, str)
    assert len(axioms) == 8


def test_bottom_propagates_back() -> None:
    A, B = atom("A"), atom("B")
    tbox = [(A, exists("r", B)), (B, BOTTOM)]
    got = classify(tbox)
    assert got["A"] == {"A", "B"}  # A is unsatisfiable, so it is below every name
    comp = complete(tbox)
    assert BOTN in comp.S["A"]
    assert not alc_reference.satisfiable(A, tbox)


def test_inconsistent_tbox() -> None:
    A = atom("A")
    tbox = [(TOP, exists("r", A)), (A, BOTTOM)]
    comp = complete(tbox)
    assert comp.canonical_model() is None
    assert not alc_reference.satisfiable(TOP, tbox)


def test_rejects_other_constructors() -> None:
    for c in (neg(atom("A")), dl.disj(atom("A"), atom("B")), dl.forall("r", atom("A"))):
        try:
            normalize([(c, atom("B"))])
        except NotEL:
            pass
        else:
            raise AssertionError("expected NotEL")


def test_random_tboxes_brute_force_and_tableau() -> None:
    rng = random.Random(2024)
    yes = no = 0
    for _ in range(40):
        tbox = rand_tbox(rng, rng.randint(2, 4), roles=["r"])
        y, n = check_against_semantics(tbox, small=True)
        yes += y
        no += n
    assert yes > 120 and no > 60


def test_random_tboxes_two_roles() -> None:
    rng = random.Random(99)
    yes = no = 0
    for _ in range(80):
        tbox = rand_tbox(rng, rng.randint(2, 6))
        y, n = check_against_semantics(tbox, small=False)
        yes += y
        no += n
    assert yes > 250 and no > 150


def test_complex_subsumption_against_tableau() -> None:
    rng = random.Random(5)
    yes = 0
    for _ in range(150):
        tbox = rand_tbox(rng, rng.randint(1, 4))
        c, d = rand_el(rng, 3), rand_el(rng, 2)
        got = subsumes(tbox, c, d)
        assert got == alc_reference.subsumes(c, d, tbox), (dl.show(c), dl.show(d), tbox)
        yes += got
    assert 20 < yes < 130
