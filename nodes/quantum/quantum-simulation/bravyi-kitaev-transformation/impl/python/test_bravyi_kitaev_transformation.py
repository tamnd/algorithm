# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bravyi-kitaev-transformation/. The authors are listed in prov/P3HDKS.jsonl.

import random

from bravyi_kitaev_transformation import (
    bk_ladder,
    bk_matrix,
    bravyi_kitaev,
    encode,
    flip_set,
    parity_set,
    remainder_set,
    update_set,
)
from qsim import (
    annihilation_matrix,
    close,
    eigvalsh,
    fermion_matrix,
    pauli_on,
    qop_add,
    qop_matrix,
    qop_mul,
    weight,
    zeros,
)


def anti(a, b):
    return qop_add(qop_mul(a, b), qop_mul(b, a))


def test_beta_on_four_modes():
    assert bk_matrix(4) == [[1, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0], [1, 1, 1, 1]]


def rows_sum(beta, rows, n):
    s = [0] * n
    for r in rows:
        s = [(a + b) % 2 for a, b in zip(s, beta[r])]
    return s


def test_sets_follow_from_beta():
    for n in range(1, 17):
        beta = bk_matrix(n)
        for j in range(n):
            assert update_set(n, j) == [i for i in range(n) if i != j and beta[i][j]]
            assert rows_sum(beta, parity_set(n, j), n) == [1 if k < j else 0 for k in range(n)]
            child = rows_sum(beta, flip_set(n, j), n)
            child[j] = (child[j] + 1) % 2
            assert child == beta[j]
            assert set(flip_set(n, j)) <= set(parity_set(n, j))
            assert set(remainder_set(n, j)) == set(parity_set(n, j)) - set(flip_set(n, j))


def test_four_mode_images():
    assert bk_ladder(4, 0, False) == {"XIXX": 0.5, "XIXY": 0.5j}
    assert bk_ladder(4, 1, False) == {"XIXZ": 0.5, "XIYI": 0.5j}
    assert bk_ladder(4, 2, False) == {"XXZI": 0.5, "XYZI": 0.5j}
    assert bk_ladder(4, 3, False) == {"XZZI": 0.5, "YIII": 0.5j}


def test_anticommutation_relations_exactly():
    for n in (3, 4, 5):
        one = {"I" * n: 1}
        a = [bk_ladder(n, j, False) for j in range(n)]
        ad = [bk_ladder(n, j, True) for j in range(n)]
        for i in range(n):
            for j in range(n):
                assert anti(a[i], ad[j]) == (one if i == j else {})
                assert anti(a[i], a[j]) == {}
                assert anti(ad[i], ad[j]) == {}


def test_images_are_the_encoded_fock_matrices():
    for n in range(1, 6):
        d = 1 << n
        perm = [encode(n, x) for x in range(d)]
        assert sorted(perm) == list(range(d))
        for j in range(n):
            a = annihilation_matrix(n, j)
            w = zeros(d)
            for x in range(d):
                for y in range(d):
                    w[perm[y]][perm[x]] = a[y][x]
            assert qop_matrix(bk_ladder(n, j, False), n) == w


def jw_ladder(n, j, is_dagger):
    z = {q: "Z" for q in range(j)}
    return {pauli_on(n, {**z, j: "X"}): 0.5, pauli_on(n, {**z, j: "Y"}): (-0.5j if is_dagger else 0.5j)}


def test_same_spectrum_as_jordan_wigner_and_fock():
    rng = random.Random(7)
    n = 4
    terms = []
    for p in range(n):
        terms.append((rng.uniform(-1, 1), ((p, True), (p, False))))
        for q in range(p + 1, n):
            h = complex(rng.uniform(-1, 1), rng.uniform(-1, 1))
            terms += [(h, ((p, True), (q, False))), (h.conjugate(), ((q, True), (p, False)))]
            terms.append((rng.uniform(-1, 1), ((p, True), (p, False), (q, True), (q, False))))
    jw = {}
    for coef, word in terms:
        w = {"I" * n: 1}
        for j, dg in word:
            w = qop_mul(w, jw_ladder(n, j, dg))
        jw = qop_add(jw, {s: coef * c for s, c in w.items()})
    e_bk = eigvalsh(qop_matrix(bravyi_kitaev(n, terms), n))
    e_jw = eigvalsh(qop_matrix(jw, n))
    e_f = eigvalsh(fermion_matrix(n, terms))
    assert close(e_bk, e_jw, 1e-9) and close(e_bk, e_f, 1e-9)


def test_weight_table():
    # the largest Pauli weight in the image of a_j, maximized over j
    for k in range(1, 11):
        n = 1 << k
        bk = [max(weight(s) for s in bk_ladder(n, j, False)) for j in range(n)]
        assert max(bk) == k + 1 and min(bk) == k + 1
    for n in list(range(1, 130)) + [1000]:
        bk = max(max(weight(s) for s in bk_ladder(n, j, False)) for j in range(n))
        assert bk == n.bit_length()
