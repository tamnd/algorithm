# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/argumentation-sat-encoding/. The authors are listed in prov/RCX19M.jsonl.

import itertools
import random

import pytest

import af
from argumentation_sat_encoding import dpll, encode, extensions, preferred_extensions


def random_framework(rng, n, prob):
    args = frozenset(range(n))
    attacks = frozenset((a, b) for a in args for b in args if rng.random() < prob)
    return args, attacks


def brute(args, attacks, semantics):
    if semantics == "conflict-free":
        sets = [s for s in af.subsets(args) if af.conflict_free(attacks, s)]
        return sorted(sets, key=af._key)
    if semantics == "admissible":
        return af.admissible_sets(args, attacks)
    if semantics == "complete":
        return af.complete_extensions(args, attacks)
    return af.stable_extensions(args, attacks)


def satisfiable_by_brute_force(clauses, nvars):
    for bits in itertools.product([False, True], repeat=nvars):
        if all(any(bits[abs(x) - 1] == (x > 0) for x in c) for c in clauses):
            return True
    return False


def satisfies(model, clauses):
    return all(any(model[abs(x)] == (x > 0) for x in c) for c in clauses)


def test_dpll_against_truth_tables():
    rng = random.Random(1)
    for _ in range(400):
        nvars = rng.randrange(1, 7)
        clauses = []
        for _ in range(rng.randrange(0, 14)):
            width = rng.randrange(1, 4)
            clauses.append([rng.randrange(1, nvars + 1) * rng.choice([1, -1]) for _ in range(width)])
        model = dpll(clauses, nvars)
        assert (model is not None) == satisfiable_by_brute_force(clauses, nvars)
        if model is not None:
            assert set(model) == set(range(1, nvars + 1))
            assert satisfies(model, clauses)
    assert dpll([[]], 1) is None
    assert dpll([], 2) == {1: False, 2: False}


SEEDS = {"conflict-free": 11, "admissible": 12, "complete": 13, "stable": 14}


@pytest.mark.parametrize("semantics", ["conflict-free", "admissible", "complete", "stable"])
def test_extensions_match_brute_force(semantics):
    rng = random.Random(SEEDS[semantics])
    for _ in range(120):
        n = rng.randrange(0, 7)
        args, attacks = random_framework(rng, n, rng.choice([0.1, 0.2, 0.35]))
        assert extensions(args, attacks, semantics) == brute(args, attacks, semantics)


def test_models_are_one_to_one_with_extensions():
    # The out variables are fixed by the in variables, so each extension has one model.
    rng = random.Random(2)
    for _ in range(60):
        n = rng.randrange(1, 5)
        args, attacks = random_framework(rng, n, 0.3)
        for semantics in ("admissible", "complete", "stable"):
            clauses, var = encode(args, attacks, semantics)
            nvars = 2 * len(var)
            models = [bits for bits in itertools.product([False, True], repeat=nvars)
                      if all(any(bits[abs(x) - 1] == (x > 0) for x in c) for c in clauses)]
            sets = sorted((frozenset(a for a in var if bits[var[a][0] - 1]) for bits in models), key=af._key)
            assert sets == brute(args, attacks, semantics)
            for bits in models:
                s = frozenset(a for a in var if bits[var[a][0] - 1])
                out = af.attacked_by(attacks, s)
                assert all(bits[var[a][1] - 1] == (a in out) for a in var)


def test_preferred_by_iterated_sat():
    rng = random.Random(3)
    for _ in range(150):
        n = rng.randrange(0, 8)
        args, attacks = random_framework(rng, n, rng.choice([0.1, 0.2, 0.35]))
        assert preferred_extensions(args, attacks) == af.preferred_extensions(args, attacks)


def test_page_example():
    # a <-> b, b -> c, c -> d. The worked example of the page.
    args = frozenset("abcd")
    attacks = frozenset({("a", "b"), ("b", "a"), ("b", "c"), ("c", "d")})
    assert extensions(args, attacks, "admissible") == sorted(
        [frozenset(), frozenset("a"), frozenset("b"), frozenset("ac"), frozenset("bd")], key=af._key)
    assert extensions(args, attacks, "complete") == [frozenset(), frozenset("ac"), frozenset("bd")]
    assert extensions(args, attacks, "stable") == [frozenset("ac"), frozenset("bd")]
    assert preferred_extensions(args, attacks) == [frozenset("ac"), frozenset("bd")]
    assert frozenset("abd") not in extensions(args, attacks, "conflict-free")
    clauses, var = encode(args, attacks, "stable")
    # 4 definitions of out, 4 links in(b) -> out(a), 4 conflict clauses, 4 "in or out" clauses.
    assert len(clauses) == 16
    assert len(var) == 4


def test_self_attack_and_odd_cycle():
    # A self-attacking argument has no stable extension; nor has an odd cycle.
    assert extensions({0}, {(0, 0)}, "stable") == []
    assert extensions({0}, {(0, 0)}, "complete") == [frozenset()]
    cycle = {(0, 1), (1, 2), (2, 0)}
    assert extensions({0, 1, 2}, cycle, "stable") == []
    assert extensions({0, 1, 2}, cycle, "admissible") == [frozenset()]


def test_bad_input():
    with pytest.raises(ValueError):
        encode({0}, {(0, 1)}, "stable")
    with pytest.raises(ValueError):
        encode({0}, set(), "grounded")
