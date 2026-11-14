# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fractional-factorial-design/. The authors are listed in prov/2RTF2Q.jsonl.

import random
from itertools import combinations, product
from string import ascii_uppercase

import pytest

from fractional_factorial_design import (
    alias_set, column, defining_relation, design, estimate, name, resolution, word,
    wordlength_pattern,
)


def all_effects(k: int) -> list[str]:
    letters = ascii_uppercase[:k]
    return [name(frozenset(c)) for r in range(1, k + 1) for c in combinations(letters, r)]


def brute_force_aliases(runs: list[tuple[int, ...]], k: int) -> dict[str, set[str]]:
    """Group the effects whose columns in the fraction are equal or opposite."""
    cols = {e: tuple(column(runs, e)) for e in ["I"] + all_effects(k)}
    out = {}
    for e, c in cols.items():
        neg = tuple(-v for v in c)
        out[e] = {f for f, d in cols.items() if f != e and (d == c or d == neg)}
    return out


CASES = [
    (4, {"D": "ABC"}),
    (5, {"E": "ABCD"}),
    (5, {"D": "AB", "E": "AC"}),
    (6, {"E": "ABC", "F": "BCD"}),
    (7, {"D": "AB", "E": "AC", "F": "BC", "G": "ABC"}),
    (7, {"F": "ABCD", "G": "ABDE"}),
]


@pytest.mark.parametrize("k, gens", CASES)
def test_alias_structure_against_column_products(k: int, gens: dict[str, str]) -> None:
    runs = design(k, gens)
    assert len(runs) == 2 ** (k - len(gens))
    relation = defining_relation(gens)
    assert len(relation) == 2 ** len(gens) - 1
    brute = brute_force_aliases(runs, k)
    # the defining words are the effects aliased with the mean
    assert brute["I"] == {name(w) for w in relation}
    for e in all_effects(k):
        assert set(alias_set(e, relation)) - {"I"} == brute[e] - {"I"}
        assert ("I" in alias_set(e, relation)) == ("I" in brute[e])


@pytest.mark.parametrize("k, gens", CASES)
def test_columns_of_distinct_alias_sets_are_orthogonal(k: int, gens: dict[str, str]) -> None:
    runs = design(k, gens)
    relation = defining_relation(gens)
    for e, f in combinations(all_effects(k), 2):
        dot = sum(a * b for a, b in zip(column(runs, e), column(runs, f)))
        aliased = (word(e) ^ word(f)) in relation
        assert abs(dot) == (len(runs) if aliased else 0)


def test_resolution_and_patterns() -> None:
    assert resolution(defining_relation({"D": "ABC"})) == 4
    assert resolution(defining_relation({"E": "ABCD"})) == 5
    assert resolution(defining_relation({"D": "AB", "E": "AC", "F": "BC", "G": "ABC"})) == 3
    rel = defining_relation({"E": "ABC", "F": "BCD"})
    assert [name(w) for w in rel] == ["ABCE", "ADEF", "BCDF"]
    assert wordlength_pattern(rel, 6) == (0, 3, 0, 0)


def test_minimum_aberration_two_to_the_seven_minus_two() -> None:
    # Search every choice of two generator words on A..E (each of length >= 2).
    words = ["".join(c) for r in range(2, 6) for c in combinations("ABCDE", r)]
    best = None
    for w1, w2 in combinations(words, 2):
        pattern = wordlength_pattern(defining_relation({"F": w1, "G": w2}), 7)
        best = pattern if best is None or pattern < best else best
    assert best == (0, 1, 2, 0, 0)
    assert wordlength_pattern(defining_relation({"F": "ABCD", "G": "ABDE"}), 7) == best
    assert wordlength_pattern(defining_relation({"F": "ABC", "G": "ADE"}), 7) == (0, 2, 0, 1, 0)


def test_half_fraction_estimates_sums_of_aliased_effects() -> None:
    rng = random.Random(1)
    full = design(4, {})
    y_full = [rng.uniform(0.0, 100.0) for _ in full]
    half_idx = [i for i, r in enumerate(full) if r[0] * r[1] * r[2] * r[3] == 1]
    runs = [full[i] for i in half_idx]
    y = [y_full[i] for i in half_idx]
    assert sorted(runs) == sorted(design(4, {"D": "ABC"}))
    rel = defining_relation({"D": "ABC"})
    for e in all_effects(4):
        partner = alias_set(e, rel)[0]
        if partner == "I":
            continue
        assert abs(estimate(runs, y, e) - (estimate(full, y_full, e) + estimate(full, y_full, partner))) < 1e-9


def test_foldover_clears_main_effects() -> None:
    runs = design(7, {"D": "AB", "E": "AC", "F": "BC", "G": "ABC"})
    folded = runs + [tuple(-v for v in r) for r in runs]
    for main in "ABCDEFG":
        for two in combinations("ABCDEFG", 2):
            dot = sum(a * b for a, b in zip(column(folded, main), column(folded, "".join(two))))
            assert dot == 0
    # before the foldover, A is aliased with BD (D = AB)
    assert abs(sum(a * b for a, b in zip(column(runs, "A"), column(runs, "BD")))) == 8


PILOT = [60, 72, 54, 68, 52, 83, 45, 80]  # the 2^3 example of factorial-design, standard order


def test_example_half_fractions_of_the_pilot_plant() -> None:
    full = design(3, {})
    assert defining_relation({"C": "AB"}) == [word("ABC")]
    assert resolution(defining_relation({"C": "AB"})) == 3
    plus = [i for i, r in enumerate(full) if r[0] * r[1] * r[2] == 1]
    minus = [i for i, r in enumerate(full) if r[0] * r[1] * r[2] == -1]
    assert [PILOT[i] for i in plus] == [72, 54, 52, 80] and [PILOT[i] for i in minus] == [60, 68, 83, 45]
    assert sorted(full[i] for i in plus) == sorted(design(3, {"C": "AB"}))
    est_plus = {e: estimate([full[i] for i in plus], [PILOT[i] for i in plus], e) for e in "ABC"}
    est_minus = {e: estimate([full[i] for i in minus], [PILOT[i] for i in minus], e) for e in "ABC"}
    assert est_plus == {"A": 23.0, "B": 5.0, "C": 3.0}      # A + BC, B + AC, C + AB
    assert est_minus == {"A": 23.0, "B": -15.0, "C": 0.0}   # A - BC, B - AC, C - AB
    true = {e: estimate(full, PILOT, e) for e in ["A", "B", "C", "AB", "AC", "BC"]}
    assert true == {"A": 23.0, "B": -5.0, "C": 1.5, "AB": 1.5, "AC": 10.0, "BC": 0.0}
    # the fold-over: half sum and half difference separate the aliases
    assert (est_plus["B"] + est_minus["B"]) / 2 == true["B"] and (est_plus["B"] - est_minus["B"]) / 2 == true["AC"]
    assert (est_plus["C"] + est_minus["C"]) / 2 == true["C"] and (est_plus["C"] - est_minus["C"]) / 2 == true["AB"]


def test_saturated_seven_factor_design() -> None:
    gens = {"D": "AB", "E": "AC", "F": "BC", "G": "ABC"}
    rel = defining_relation(gens)
    assert len(rel) == 15 and wordlength_pattern(rel, 7) == (7, 7, 0, 0, 1)
    # each main effect is aliased with three two-factor interactions
    for main in "ABCDEFG":
        twos = [a for a in alias_set(main, rel) if len(a) == 2]
        assert len(twos) == 3
    assert sorted(a for a in alias_set("A", rel) if len(a) == 2) == ["BD", "CE", "FG"]
    # as 0/1 vectors the group is a [7, 4] code with weights 0, 3, 4, 7 (the Hamming code), and the
    # runs, with +1 written as bit 0 and -1 as bit 1, are its dual: the [7, 3] simplex code
    letters = "ABCDEFG"
    vec = lambda w: tuple(int(c in w) for c in letters)
    group = [vec(w) for w in rel] + [(0,) * 7]
    assert sorted(sum(v) for v in group) == [0] + [3] * 7 + [4] * 7 + [7]
    runs = [tuple(0 if v == 1 else 1 for v in r) for r in design(7, gens)]
    assert len(set(runs)) == 8 and sorted(sum(r) for r in runs) == [0] + [4] * 7
    assert all(sum(a * b for a, b in zip(r, g)) % 2 == 0 for r in runs for g in group)
    assert all(tuple((a + b) % 2 for a, b in zip(r, s)) in runs for r in runs for s in runs)


def aliased_two_factor_pairs(rel: list[frozenset[str]], k: int) -> int:
    twos = [frozenset(c) for c in combinations(ascii_uppercase[:k], 2)]
    return sum((a ^ b) in rel for a, b in combinations(twos, 2))


def test_aberration_counts_aliased_two_factor_interactions() -> None:
    good = defining_relation({"F": "ABCD", "G": "ABDE"})
    bad = defining_relation({"F": "ABC", "G": "ADE"})
    assert [name(w) for w in good] == ["CEFG", "ABCDF", "ABDEG"]
    assert [name(w) for w in bad] == ["ABCF", "ADEG", "BCDEFG"]
    assert resolution(good) == resolution(bad) == 4
    assert aliased_two_factor_pairs(good, 7) == 3 and aliased_two_factor_pairs(bad, 7) == 6


def test_errors() -> None:
    with pytest.raises(ValueError):
        design(6, {"D": "AB", "E": "AC", "F": "DE"})  # F uses added factors
    with pytest.raises(ValueError):
        design(4, {"D": "AE"})
