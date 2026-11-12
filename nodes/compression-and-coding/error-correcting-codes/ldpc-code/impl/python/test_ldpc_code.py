# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ldpc-code/. The authors are listed in prov/JDSJ23.jsonl.

import itertools
import random

from ldpc_code import (
    bec_threshold,
    bec_threshold_fixed_point,
    de_bec,
    design_rate,
    gallager_regular,
    gf2_null_space,
    node_to_edge,
)

# Kudekar, Richardson and Urbanke, IEEE Trans. Inf. Theory 57(2), 2011,
# Example 5: the BP threshold of the (3, 6) ensemble on the BEC is about 0.42944.
CITED_36 = 0.42944


def test_bec_threshold_of_3_6() -> None:
    thr = bec_threshold({3: 1.0}, {6: 1.0}, tol=1e-6, iterations=4000)
    assert abs(thr - CITED_36) < 2e-4
    assert abs(bec_threshold_fixed_point({3: 1.0}, {6: 1.0}, grid=20000) - CITED_36) < 1e-4
    assert thr < 0.5  # below the Shannon limit 1 - r of the rate 1/2 ensemble


def test_density_evolution_two_sides() -> None:
    assert de_bec(0.42, {3: 1.0}, {6: 1.0}, 400) < 1e-12
    assert de_bec(0.44, {3: 1.0}, {6: 1.0}, 400) > 0.3


def test_design_rate() -> None:
    assert abs(design_rate({3: 1.0}, {6: 1.0}) - 0.5) < 1e-12
    assert abs(design_rate({3: 1.0}, {4: 1.0}) - 0.25) < 1e-12
    lam = node_to_edge({2: 0.5, 3: 0.3, 8: 0.2})
    assert abs(sum(lam.values()) - 1) < 1e-12
    assert abs(lam[2] - 2 / 7) < 1e-12
    assert abs(design_rate(lam, {6: 1.0}) - 5 / 12) < 1e-12


def test_gallager_matrix_is_regular_and_rate_at_least_design() -> None:
    rng = random.Random(8)
    for n, dv, dc in ((12, 3, 4), (24, 3, 6), (40, 4, 8), (60, 3, 6)):
        h = gallager_regular(n, dv, dc, rng)
        assert len(h) == n * dv // dc
        assert all(sum(r) == dc for r in h)
        assert all(sum(r[j] for r in h) == dv for j in range(n))
        basis = gf2_null_space(h)
        assert len(basis) >= n - len(h) + (dv - 1)  # each band adds to all ones
        for v in basis:
            assert all(sum(a * b for a, b in zip(r, v)) % 2 == 0 for r in h)


def test_null_space_against_brute_force() -> None:
    rng = random.Random(4)
    for _ in range(500):
        n = rng.randrange(1, 9)
        h = [[rng.randrange(2) for _ in range(n)] for _ in range(rng.randrange(1, 6))]
        words = {c for c in itertools.product((0, 1), repeat=n)
                 if all(sum(a * b for a, b in zip(r, c)) % 2 == 0 for r in h)}
        basis = gf2_null_space(h)
        span = set()
        for m in itertools.product((0, 1), repeat=len(basis)):
            span.add(tuple(sum(m[i] * basis[i][j] for i in range(len(basis))) % 2 for j in range(n)))
        assert span == words and len(words) == 2 ** len(basis)
