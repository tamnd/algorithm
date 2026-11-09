# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boolean-constraint-satisfaction/. The authors are listed in prov/3NGE2G.jsonl.

import itertools
import random

import pytest

from boolean_constraint_satisfaction import (POLYMORPHISM, closed_under, count_affine, is_in_class,
                                             schaefer_classes, solve)


def all_relations(r: int):
    tuples = list(itertools.product((0, 1), repeat=r))
    for mask in range(1 << len(tuples)):
        yield {t for k, t in enumerate(tuples) if mask >> k & 1}


def brute(n, instance):
    return [t for t in itertools.product((0, 1), repeat=n)
            if all(tuple(t[v] for v in s) in rel for s, rel in instance)]


def check_class_equals_closure(r: int, rel: set) -> None:
    for name, (k, op) in POLYMORPHISM.items():
        if name in ("0-valid", "1-valid") and not rel:
            continue  # the empty relation is closed under a constant, but it is not 0-valid
        assert is_in_class(name, r, rel) == closed_under(rel, k, op), (name, r, sorted(rel))


def test_recognizers_match_polymorphisms_up_to_arity_3() -> None:
    for r in (1, 2, 3):
        for rel in all_relations(r):
            check_class_equals_closure(r, rel)


def test_recognizers_match_polymorphisms_arity_4_sample() -> None:
    rng = random.Random(10)
    tuples = list(itertools.product((0, 1), repeat=4))
    for _ in range(400):
        p = rng.random()
        check_class_equals_closure(4, {t for t in tuples if rng.random() < p})


def test_counts_of_ternary_relations() -> None:
    rels = list(all_relations(3))
    count = {name: sum(1 for rel in rels if is_in_class(name, 3, rel)) for name in POLYMORPHISM}
    assert count == {"0-valid": 128, "1-valid": 128, "horn": 122, "dual-horn": 122,
                     "bijunctive": 166, "affine": 52}
    none = [rel for rel in rels if not schaefer_classes([(3, rel)])]
    assert len(none) == 15
    assert {(1, 0, 0), (0, 1, 0), (0, 0, 1)} in none  # one-in-three
    nae = {t for t in itertools.product((0, 1), repeat=3) if len(set(t)) == 2}
    assert nae in none


def relations_in(name: str):
    return [(r, rel) for r in (1, 2, 3) for rel in all_relations(r) if is_in_class(name, r, rel)]


def test_solvers_against_brute_force() -> None:
    rng = random.Random(11)
    for name in POLYMORPHISM:
        pool = relations_in(name)
        for _ in range(150):
            n = rng.randint(3, 8)
            instance = []
            for _ in range(rng.randint(1, 10)):
                r, rel = rng.choice(pool)
                instance.append((tuple(rng.sample(range(n), r)), rel))
            sols = brute(n, instance)
            got = solve(n, instance)
            if sols:
                assert got is not None and tuple(got) in set(sols), name
            else:
                assert got is None, name
            if name == "affine":
                assert count_affine(n, instance) == len(sols)


def test_hard_language_is_rejected() -> None:
    one_in_three = {(1, 0, 0), (0, 1, 0), (0, 0, 1)}
    with pytest.raises(ValueError):
        solve(3, [((0, 1, 2), one_in_three)])


def test_examples() -> None:
    # (x0 or x1) and (not x0 or x1) and (not x1 or x2): 2-SAT, solved by x1 = x2 = 1
    two = solve(3, [((0, 1), {(0, 1), (1, 0), (1, 1)}), ((0, 1), {(0, 0), (0, 1), (1, 1)}),
                    ((1, 2), {(0, 0), (0, 1), (1, 1)})])
    assert two is not None and two[1] == two[2] == 1
    # x0 xor x1 xor x2 = 1 and x0 xor x1 = 0 have 2 solutions over 3 variables
    odd = {t for t in itertools.product((0, 1), repeat=3) if sum(t) % 2 == 1}
    assert count_affine(3, [((0, 1, 2), odd), ((0, 1), {(0, 0), (1, 1)})]) == 2
