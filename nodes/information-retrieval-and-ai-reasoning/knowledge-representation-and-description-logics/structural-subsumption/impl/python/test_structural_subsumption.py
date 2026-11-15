# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/structural-subsumption/. The authors are listed in prov/DQ8M2F.jsonl.
"""Tests of structural subsumption for FL- against the semantics.

1. Brute force: with one role, when c is not subsumed by d there is a counter-model that is a path
   with at most (larger role depth + 1) elements (proofs/correctness.md, size of the counter-model).
   So for one role and role depth at most k, a search over every interpretation with at most k + 1
   elements decides subsumption. The tests use k = 1 (all 32 normal forms over two names) and
   k = 2 (random concepts).
2. The ALC tableau of alc_reference.py on c and not d, for random FL- concepts with two roles.
3. Every counter-model that the algorithm returns is checked by evaluation.
4. The example where a role restriction breaks the method.
"""

import random
from itertools import product

import alc_reference
import dl
from dl import TOP, atom, conj, disj, exists, forall, neg
from structural_subsumption import NotFLMinus, counter_model, is_fl_minus, normalize, subsumes

A, B = atom("A"), atom("B")


def some(r: str) -> tuple:
    return exists(r, TOP)


def rand_fl(rng: random.Random, depth: int, names=("A", "B"), roles=("r",)) -> tuple:
    if depth == 0 or rng.random() < 0.3:
        return TOP if rng.random() < 0.1 else atom(rng.choice(names))
    op = rng.choice(["and", "and", "some", "all", "all"])
    if op == "and":
        return conj(rand_fl(rng, depth, names, roles), rand_fl(rng, depth - 1, names, roles))
    if op == "some":
        return some(rng.choice(roles))
    return forall(rng.choice(roles), rand_fl(rng, depth - 1, names, roles))


def check_counter(c: tuple, d: tuple) -> None:
    i = counter_model(c, d)
    if subsumes(c, d):
        assert i is None
    else:
        assert i is not None
        assert 0 in dl.evaluate(c, i) and 0 not in dl.evaluate(d, i)


def test_page_example() -> None:
    c = conj(A, some("r"), forall("r", A), forall("r", conj(B, forall("s", A))))
    d = conj(some("r"), forall("r", conj(A, B)), forall("r", forall("s", TOP)))
    assert normalize(c).show() == "(A ⊓ ∃r ⊓ ∀r.(A ⊓ B ⊓ ∀s.A))"
    assert normalize(d).show() == "(∃r ⊓ ∀r.(A ⊓ B))"
    assert subsumes(c, d)
    d2 = forall("r", forall("s", B))
    assert not subsumes(c, d2)
    i = counter_model(c, d2)
    assert len(i.domain) == 3
    assert 0 in dl.evaluate(c, i) and 0 not in dl.evaluate(d2, i)


def test_value_restriction_on_top_is_dropped() -> None:
    # Without line L3, the right side keeps an empty child for r and the answer is wrong.
    assert subsumes(A, forall("r", TOP))
    assert subsumes(TOP, conj(forall("r", forall("s", TOP)), TOP))
    assert normalize(forall("r", conj(TOP, forall("s", TOP)))).is_empty()


def test_value_restrictions_are_merged() -> None:
    # Without the merge of line L8, all r.(A and B) is not found below all r.A and all r.B.
    c = conj(forall("r", A), forall("r", B))
    assert subsumes(c, forall("r", conj(A, B)))
    assert subsumes(forall("r", conj(A, B)), c)


def test_rejects_other_constructors() -> None:
    for c in (neg(A), disj(A, B), exists("r", A), dl.BOTTOM):
        assert not is_fl_minus(c)
        try:
            normalize(c)
        except NotFLMinus:
            pass
        else:
            raise AssertionError("expected NotFLMinus")


def _small_extensions(concepts: list, cn: list, rn: list, max_size: int) -> list:
    """For each concept, the list of its extensions in every interpretation with at most max_size elements."""
    exts: list[list] = [[] for _ in concepts]
    for i in dl.interpretations(cn, rn, max_size):
        for k, c in enumerate(concepts):
            exts[k].append(dl.evaluate(c, i))
    return exts


def _brute_subsumes(ec: list, ed: list) -> bool:
    return all(x <= y for x, y in zip(ec, ed))


def all_depth1_concepts() -> list:
    out = []
    subsets = [(), ("A",), ("B",), ("A", "B")]
    for top_names, e, filler in product(subsets, (False, True), subsets):
        parts = [atom(a) for a in top_names]
        if e:
            parts.append(some("r"))
        if filler:
            parts.append(forall("r", conj(*[atom(a) for a in filler])))
        out.append(conj(*parts))
    return out


def test_all_depth1_pairs_against_brute_force() -> None:
    cs = all_depth1_concepts()
    assert len(cs) == 32
    exts = _small_extensions(cs, ["A", "B"], ["r"], 2)
    agree = holds = 0
    for x, c in enumerate(cs):
        for y, d in enumerate(cs):
            want = _brute_subsumes(exts[x], exts[y])
            assert subsumes(c, d) == want, (dl.show(c), dl.show(d))
            agree += 1
            holds += want
            check_counter(c, d)
    assert agree == 1024
    assert 0 < holds < 1024


def test_random_depth2_against_brute_force() -> None:
    rng = random.Random(7)
    cs = []
    while len(cs) < 24:
        c = rand_fl(rng, 2, names=("A",), roles=("r",))
        if dl.role_depth(c) <= 2:
            cs.append(c)
    exts = _small_extensions(cs, ["A"], ["r"], 3)
    holds = 0
    for x, c in enumerate(cs):
        for y, d in enumerate(cs):
            want = _brute_subsumes(exts[x], exts[y])
            assert subsumes(c, d) == want, (dl.show(c), dl.show(d))
            holds += want
    assert 0 < holds < len(cs) ** 2


def test_random_against_alc_tableau() -> None:
    rng = random.Random(11)
    yes = no = 0
    for _ in range(300):
        c = rand_fl(rng, 3, roles=("r", "s"))
        d = rand_fl(rng, 3, roles=("r", "s"))
        if rng.random() < 0.5:
            c = conj(c, d, rand_fl(rng, 2, roles=("r", "s")))  # make "yes" answers common
        got = subsumes(c, d)
        assert got == alc_reference.subsumes(c, d), (dl.show(c), dl.show(d))
        check_counter(c, d)
        yes += got
        no += not got
    assert yes > 50 and no > 50


def test_role_restriction_breaks_it() -> None:
    # FL adds the restricted role (r : C), the r-successors that are in C.
    # C = some (r : A) and all (r : A).B, D = some (r : B). In ALC: some r.A and all r.(not A or B), some r.B.
    c_alc = conj(exists("r", A), forall("r", disj(neg(A), B)))
    d_alc = exists("r", B)
    assert alc_reference.subsumes(c_alc, d_alc)
    exts = _small_extensions([c_alc, d_alc], ["A", "B"], ["r"], 2)
    assert _brute_subsumes(exts[0], exts[1])
    # Comparing part by part treats (r : A) and (r : B) as two unrelated roles and says no.
    c_naive = conj(some("r:A"), forall("r:A", B))
    d_naive = some("r:B")
    assert not subsumes(c_naive, d_naive)
