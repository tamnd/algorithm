# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fermion-to-qubit-mapping/. The authors are listed in prov/390342.jsonl.

import random

from fermion_to_qubit_mapping import (
    bravyi_kitaev_matrix,
    encode,
    gf2_inverse,
    jordan_wigner_matrix,
    linear_ladder,
    linear_map,
    parity_matrix,
    random_invertible,
)
from qsim import (
    annihilation_matrix,
    close,
    eigvalsh,
    fermion_matrix,
    qop_add,
    qop_matrix,
    qop_mul,
    weight,
    zeros,
)


def anti(a, b):
    return qop_add(qop_mul(a, b), qop_mul(b, a))


def encodings(n, rng):
    return [jordan_wigner_matrix(n), parity_matrix(n), bravyi_kitaev_matrix(n), random_invertible(n, rng)]


def test_gf2_inverse():
    rng = random.Random(1)
    for n in range(1, 7):
        beta = random_invertible(n, rng)
        inv = gf2_inverse(beta)
        prod = [[sum(beta[i][k] * inv[k][j] for k in range(n)) % 2 for j in range(n)] for i in range(n)]
        assert prod == jordan_wigner_matrix(n)


def test_anticommutation_relations_for_every_encoding():
    rng = random.Random(11)
    for n in (3, 4):
        one = {"I" * n: 1}
        for beta in encodings(n, rng):
            a = [linear_ladder(beta, j, False) for j in range(n)]
            ad = [linear_ladder(beta, j, True) for j in range(n)]
            for i in range(n):
                for j in range(n):
                    assert anti(a[i], ad[j]) == (one if i == j else {})
                    assert anti(a[i], a[j]) == {}


def test_images_are_the_encoded_fock_matrices():
    rng = random.Random(5)
    n = 4
    d = 1 << n
    for beta in encodings(n, rng):
        perm = [encode(beta, x) for x in range(d)]
        assert sorted(perm) == list(range(d))
        for j in range(n):
            a = annihilation_matrix(n, j)
            w = zeros(d)
            for x in range(d):
                for y in range(d):
                    w[perm[y]][perm[x]] = a[y][x]
            assert close(qop_matrix(linear_ladder(beta, j, False), n), w, 1e-12)


def test_same_spectrum_for_every_encoding():
    rng = random.Random(3)
    n = 4
    terms = []
    for p in range(n):
        terms.append((rng.uniform(-1, 1), ((p, True), (p, False))))
        for q in range(p + 1, n):
            h = complex(rng.uniform(-1, 1), rng.uniform(-1, 1))
            terms += [(h, ((p, True), (q, False))), (h.conjugate(), ((q, True), (p, False)))]
            terms.append((rng.uniform(-1, 1), ((p, True), (p, False), (q, True), (q, False))))
    ref = eigvalsh(fermion_matrix(n, terms))
    for beta in encodings(n, rng):
        assert close(eigvalsh(qop_matrix(linear_map(beta, terms), n)), ref, 1e-9)


def test_parity_encoding_strings():
    # parity encoding on 4 modes: a_j^dagger touches Z on qubit j - 1 and X on qubits j to 3
    n = 4
    beta = parity_matrix(n)
    assert linear_ladder(beta, 0, True) == {"XXXX": 0.5, "XXXY": -0.5j}
    assert linear_ladder(beta, 2, True) == {"XXZI": 0.5, "XYII": -0.5j}
    w = [max(weight(s) for s in linear_ladder(parity_matrix(8), j, True)) for j in range(8)]
    assert w == [8, 8, 7, 6, 5, 4, 3, 2]
