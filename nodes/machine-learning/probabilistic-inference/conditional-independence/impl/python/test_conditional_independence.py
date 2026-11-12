# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conditional-independence/. The authors are listed in prov/VZMJS0.jsonl.

import random
from fractions import Fraction as F
from itertools import product

from conditional_independence import (
    contraction_holds,
    decomposition_holds,
    intersection_holds,
    is_ci,
    symmetry_holds,
    table,
    weak_union_holds,
)

X, Y, W, Z = (0,), (1,), (2,), (3,)


def test_chain_and_collider_examples() -> None:
    # chain A -> B -> C: A _||_ C | B but not marginally
    pa = {0: F(1, 2), 1: F(1, 2)}
    pb = {(0, 0): F(9, 10), (0, 1): F(1, 10), (1, 0): F(2, 10), (1, 1): F(8, 10)}
    j = {(a, b, c): pa[a] * pb[a, b] * pb[b, c] for a, b, c in product((0, 1), repeat=3)}
    assert is_ci(j, (0,), (2,), (1,))
    assert not is_ci(j, (0,), (2,), ())
    # collider A -> C <- B with C = A xor B: pairwise independent, dependent given C
    k = {(a, b, a ^ b): F(1, 4) for a, b in product((0, 1), repeat=2)}
    assert is_ci(k, (0,), (1,), ())
    assert is_ci(k, (0,), (2,), ())
    assert not is_ci(k, (0,), (1,), (2,))


def test_semigraphoid_axioms_over_all_supports() -> None:
    # Every 0/1 weighting of the 8 cells of three binary variables (Z empty),
    # in every assignment of the roles X, Y, W.
    nontrivial = {"dec": 0, "con": 0}
    roles = [((0,), (1,), (2,)), ((1,), (2,), (0,)), ((2,), (0,), (1,))]
    for mask in range(1, 1 << 8):
        j = table([(mask >> i) & 1 for i in range(8)], 3)
        for a, b, c in roles:
            assert symmetry_holds(j, a, b, ())
            assert decomposition_holds(j, a, b, c, ())
            assert weak_union_holds(j, a, b, c, ())
            assert contraction_holds(j, a, b, c, ())
            nontrivial["dec"] += is_ci(j, a, b + c, ())
            nontrivial["con"] += is_ci(j, a, b, ()) and is_ci(j, a, c, b)
    # the hypotheses hold for many tables, so the implications were tested
    assert nontrivial["dec"] > 50 and nontrivial["con"] > 50


def test_semigraphoid_axioms_on_random_supports_with_z() -> None:
    # 0/1 weightings of the 16 cells of four binary variables, sampled
    rng = random.Random(1988)
    for _ in range(1500):
        w = [1 if rng.random() < 0.35 else 0 for _ in range(16)]
        if sum(w) == 0:
            continue
        j = table(w, 4)
        assert symmetry_holds(j, X, Y, Z)
        assert decomposition_holds(j, X, Y, W, Z)
        assert weak_union_holds(j, X, Y, W, Z)
        assert contraction_holds(j, X, Y, W, Z)


def test_axioms_on_random_weighted_joints() -> None:
    rng = random.Random(1979)
    for _ in range(300):
        # plant the hypothesis X _||_ (Y, W) | Z, with random zeros
        pz = [rng.randint(0, 3) for _ in range(2)]
        px = [[rng.randint(0, 3) for _ in range(2)] for _ in range(2)]
        pyw = [[rng.randint(0, 3) for _ in range(4)] for _ in range(2)]
        w = [px[z][x] * pyw[z][2 * y + ww] * pz[z] for x, y, ww, z in product((0, 1), repeat=4)]
        if sum(w) == 0:
            continue
        j = table(w, 4)
        assert is_ci(j, X, Y + W, Z)
        assert is_ci(j, X, Y, Z) and is_ci(j, X, Y, Z + W)
        assert contraction_holds(j, X, Y, W, Z)


def test_intersection_fails_without_positivity() -> None:
    # X = Y = W, a fair bit; Z is empty
    j = {(b, b, b): F(1, 2) for b in (0, 1)}
    assert is_ci(j, (0,), (1,), (2,))
    assert is_ci(j, (0,), (2,), (1,))
    assert not is_ci(j, (0,), (1, 2), ())


def test_intersection_over_small_tables() -> None:
    # all weightings in {0,1,2} of three binary variables X, Y, W (Z empty)
    failures = 0
    for w in product((0, 1, 2), repeat=8):
        if sum(w) == 0:
            continue
        j = table(list(w), 3)
        if not intersection_holds(j, (0,), (1,), (2,), ()):
            failures += 1
            assert 0 in w  # every failure has a zero cell
    assert failures > 0
    # with all weights positive the property always holds
    for w in product((1, 2), repeat=8):
        assert intersection_holds(table(list(w), 3), (0,), (1,), (2,), ())
