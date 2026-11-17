# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elementary-flux-mode-enumeration/. The authors are listed in prov/E5TT1K.jsonl.
"""Tests of efm_enumeration() against brute force over all supports."""

import random
from fractions import Fraction as F

from elementary_flux_mode_enumeration import (REV_E, S_E, brute_force_efms,
                                              diamond_chain, efm_enumeration,
                                              primitive)
from sy3lp import solve_lp

S_N = [
    [1, -1, -1, -1, 0, -1],
    [0, 2, 2, 1, 0, -1],
    [0, 0, 0, 1, -1, 0],
]


def is_steady(S, v):
    return all(sum(a * b for a, b in zip(row, v)) == 0 for row in S)


def test_network_e():
    modes = efm_enumeration(S_E, REV_E)
    assert modes == sorted([
        (1, 1, 0, 0, 0, 1),    # R1 + R2 + R6
        (1, 0, 1, 0, 1, 0),    # R1 + R3 + R5
        (1, 1, 0, 1, 1, 0),    # R1 + R2 + R4 + R5
        (0, 1, -1, 1, 0, 0),   # the cycle R2 + R4 - R3
    ])
    # R1 + R2 + R4 + R5 is the sum of two other modes, yet it is a mode.
    assert tuple(a + b for a, b in zip((1, 0, 1, 0, 1, 0), (0, 1, -1, 1, 0, 0))) \
        == (1, 1, 0, 1, 1, 0)
    # The sum of the first two modes is steady but not elementary.
    s = tuple(a + b for a, b in zip((1, 1, 0, 0, 0, 1), (1, 0, 1, 0, 1, 0)))
    assert is_steady(S_E, s) and primitive([F(x) for x in s]) not in modes


def test_network_n():
    modes = efm_enumeration(S_N, [False] * 6)
    assert modes == [(2, 0, 0, 1, 1, 1), (3, 0, 1, 0, 0, 2), (3, 1, 0, 0, 0, 2)]


def test_diamond_chain_doubles():
    for k in range(1, 6):
        S, rev = diamond_chain(k)
        assert len(efm_enumeration(S, rev)) == 2 ** k


def test_all_reversible_cycle_counts_both_directions():
    # A <-> B <-> C <-> A: one cycle, in two directions.
    S = [[-1, 0, 1], [1, -1, 0], [0, 1, -1]]
    assert efm_enumeration(S, [True] * 3) == [(-1, -1, -1), (1, 1, 1)]


def random_network(rng):
    n, m = rng.randint(1, 3), rng.randint(3, 7)
    S = [[rng.choice([-1, -1, 0, 0, 0, 1, 1, 2]) for _ in range(m)]
         for _ in range(n)]
    rev = [rng.random() < 0.3 for _ in range(m)]
    return S, rev


def test_random_against_brute_force():
    rng = random.Random(31)
    for _ in range(60):
        S, rev = random_network(rng)
        modes = efm_enumeration(S, rev)
        assert modes == brute_force_efms(S, rev)
        for e in modes:
            assert is_steady(S, e)
            assert all(rev[j] or x >= 0 for j, x in enumerate(e))


def test_modes_generate_the_cone():
    # Every sign-feasible steady state is a non-negative combination of modes.
    rng = random.Random(32)
    for _ in range(20):
        S, rev = random_network(rng)
        modes = efm_enumeration(S, rev)
        if not modes:
            continue
        m = len(rev)
        weights = [rng.randint(0, 3) for _ in modes]
        v = [sum(w * e[j] for w, e in zip(weights, modes)) for j in range(m)]
        A = [[e[j] for e in modes] for j in range(m)]
        res = solve_lp([0] * len(modes), A_eq=A, b_eq=v)
        assert res.status == "optimal"
