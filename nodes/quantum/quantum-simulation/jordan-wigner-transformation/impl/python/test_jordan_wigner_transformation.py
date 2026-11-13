# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jordan-wigner-transformation/. The authors are listed in prov/HV0RT2.jsonl.

import random

from jordan_wigner_transformation import jordan_wigner, jw_ladder, no_string_map
from qsim import (
    annihilation_matrix,
    close,
    eigvalsh,
    fermion_matrix,
    qop_add,
    qop_matrix,
    qop_mul,
    weight,
)


def anti(a, b):
    return qop_add(qop_mul(a, b), qop_mul(b, a))


def test_images_on_three_modes():
    assert jw_ladder(3, 0, False) == {"IIX": 0.5, "IIY": 0.5j}
    assert jw_ladder(3, 1, False) == {"IXZ": 0.5, "IYZ": 0.5j}
    assert jw_ladder(3, 2, False) == {"XZZ": 0.5, "YZZ": 0.5j}
    assert jw_ladder(3, 2, True) == {"XZZ": 0.5, "YZZ": -0.5j}


def test_anticommutation_relations_exactly():
    for n in (3, 4):
        one = {"I" * n: 1}
        a = [jw_ladder(n, j, False) for j in range(n)]
        ad = [jw_ladder(n, j, True) for j in range(n)]
        for i in range(n):
            for j in range(n):
                assert anti(a[i], ad[j]) == (one if i == j else {})
                assert anti(a[i], a[j]) == {}
                assert anti(ad[i], ad[j]) == {}


def test_images_equal_the_fock_matrices():
    for n in (3, 4):
        for j in range(n):
            assert qop_matrix(jw_ladder(n, j, False), n) == annihilation_matrix(n, j)


def test_pauli_weight_is_j_plus_one():
    for n in (8, 64):
        for j in range(n):
            assert all(weight(s) == j + 1 for s in jw_ladder(n, j, False))


def test_number_and_hopping_terms():
    assert jordan_wigner(3, [(1.0, ((1, True), (1, False)))]) == {"III": 0.5, "IZI": -0.5}
    hop = [(1.0, ((0, True), (2, False))), (1.0, ((2, True), (0, False)))]
    assert jordan_wigner(3, hop) == {"XZX": 0.5, "YZY": 0.5}


def random_hamiltonian(n, rng):
    """A Hermitian number-conserving operator: hopping h_pq a_p^dag a_q and interactions u_pq n_p n_q."""
    terms = []
    for p in range(n):
        terms.append((rng.uniform(-1, 1), ((p, True), (p, False))))
        for q in range(p + 1, n):
            h = complex(rng.uniform(-1, 1), rng.uniform(-1, 1))
            terms.append((h, ((p, True), (q, False))))
            terms.append((h.conjugate(), ((q, True), (p, False))))
            terms.append((rng.uniform(-1, 1), ((p, True), (p, False), (q, True), (q, False))))
    return terms


def test_same_spectrum_as_the_fock_matrix():
    rng = random.Random(2024)
    n = 4
    terms = random_hamiltonian(n, rng)
    f = fermion_matrix(n, terms)
    q = qop_matrix(jordan_wigner(n, terms), n)
    assert close(f, q, 1e-12)
    assert close(eigvalsh(f), eigvalsh(q), 1e-9)


def sector(m, n, k):
    idx = [x for x in range(1 << n) if bin(x).count("1") == k]
    return [[m[a][b] for b in idx] for a in idx]


def test_dropping_the_string_gives_the_wrong_spectrum():
    ring = []
    for i in range(3):
        k = (i + 1) % 3
        ring += [(-1.0, ((i, True), (k, False))), (-1.0, ((k, True), (i, False)))]
    right = qop_matrix(jordan_wigner(3, ring), 3)
    wrong = qop_matrix(no_string_map(3, ring), 3)
    assert close(eigvalsh(sector(right, 3, 2)), [-1.0, -1.0, 2.0])
    assert close(eigvalsh(sector(wrong, 3, 2)), [-2.0, 1.0, 1.0])
    assert close(eigvalsh(sector(right, 3, 1)), eigvalsh(sector(wrong, 3, 1)))
