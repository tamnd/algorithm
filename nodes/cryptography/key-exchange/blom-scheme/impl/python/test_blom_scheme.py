# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blom-scheme/. The authors are listed in prov/809KWA.jsonl.

import itertools
import random
from collections import Counter

import pytest

from blom_scheme import (
    coalition_recovers_matrix,
    dot,
    mat_vec,
    setup,
    shared_key,
    solve_mod,
    vandermonde_column,
)

Q = 2**61 - 1  # a Mersenne prime


def test_keys_are_symmetric() -> None:
    rng = random.Random(1984)
    k = 4
    ids = rng.sample(range(1, Q), 12)
    _, private = setup(ids, k, Q, rng)
    for i, j in itertools.combinations(ids, 2):
        assert shared_key(private[i], j, k, Q) == shared_key(private[j], i, k, Q)


def test_key_is_the_bilinear_form() -> None:
    rng = random.Random(1)
    k = 3
    ids = [5, 9, 11]
    d, private = setup(ids, k, Q, rng)
    gi, gj = vandermonde_column(5, k, Q), vandermonde_column(9, k, Q)
    assert shared_key(private[5], 9, k, Q) == dot(gi, mat_vec(d, gj, Q), Q)


def test_k_plus_1_colluders_recover_every_key() -> None:
    rng = random.Random(2)
    k = 5
    ids = rng.sample(range(1, Q), 10)
    d, private = setup(ids, k, Q, rng)
    coalition = {x: private[x] for x in ids[: k + 1]}
    found = coalition_recovers_matrix(coalition, k, Q)
    assert found == d
    for i, j in itertools.combinations(ids[k + 1 :], 2):
        stolen = dot(vandermonde_column(i, k, Q), mat_vec(found, vandermonde_column(j, k, Q), Q), Q)
        assert stolen == shared_key(private[i], j, k, Q)


def _poly_from_roots(roots: list[int], q: int) -> list[int]:
    """Coefficients (constant first) of the product of (t - r) over the roots."""
    c = [1]
    for r in roots:
        c = [((c[i - 1] if i > 0 else 0) - r * (c[i] if i < len(c) else 0)) % q for i in range(len(c) + 1)]
    return c


def test_k_colluders_cannot_pin_down_a_key() -> None:
    # For a coalition C of k users, w = coefficients of prod (t - x_c) has
    # w . g_c = 0 for c in C. Then D' = D + l w w^T gives the coalition the
    # same vectors, but K_ij moves by l * w(x_i) * w(x_j), which is not 0.
    rng = random.Random(3)
    q = 101
    k = 3
    ids = [1, 2, 3, 50, 60]
    d, private = setup(ids, k, q, rng)
    coalition, (i, j) = ids[:k], ids[k:]
    w = _poly_from_roots(coalition, q)
    assert all(dot(w, vandermonde_column(c, k, q), q) == 0 for c in coalition)
    seen = set()
    for lam in range(q):
        d2 = [[(d[r][s] + lam * w[r] * w[s]) % q for s in range(k + 1)] for r in range(k + 1)]
        for c in coalition:
            assert mat_vec(d2, vandermonde_column(c, k, q), q) == private[c]
        seen.add(dot(vandermonde_column(i, k, q), mat_vec(d2, vandermonde_column(j, k, q), q), q))
    assert seen == set(range(q))  # every key value fits what the coalition knows


def test_exhaustive_one_colluder_learns_nothing_when_k_is_1() -> None:
    # q = 7, k = 1: over all 7^3 symmetric matrices D, the key K_23 is
    # uniform given the private vector of user 1.
    q, k = 7, 1
    views: dict[tuple[int, ...], Counter] = {}
    for d00, d01, d11 in itertools.product(range(q), repeat=3):
        d = [[d00, d01], [d01, d11]]
        a1 = tuple(mat_vec(d, vandermonde_column(1, k, q), q))
        a2 = mat_vec(d, vandermonde_column(2, k, q), q)
        k23 = dot(a2, vandermonde_column(3, k, q), q)
        views.setdefault(a1, Counter())[k23] += 1
    assert len(views) == q * q
    for counts in views.values():
        assert sorted(counts) == list(range(q)) and set(counts.values()) == {1}


def test_solve_mod_and_errors() -> None:
    q = 13
    m = [[2, 3], [5, 7]]
    x = solve_mod(m, [[1], [0]], q)
    assert [sum(m[r][c] * x[c][0] for c in range(2)) % q for r in range(2)] == [1, 0]
    with pytest.raises(ValueError):
        solve_mod([[1, 2], [2, 4]], [[1], [1]], q)
    with pytest.raises(ValueError):
        setup([3, 3], 1, q)
    with pytest.raises(ValueError):
        coalition_recovers_matrix({1: [0, 0]}, 1, q)
