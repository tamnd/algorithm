# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-hellman-knapsack/. The authors are listed in prov/TC99QJ.jsonl.

import random
from fractions import Fraction

from lll import lll_reduce
from merkle_hellman_knapsack import (
    cjloss_attack,
    cjloss_basis,
    density,
    lo_attack,
    merkle_hellman_public_key,
    random_instance,
)

EX_A = [1327, 3883, 618, 1618, 2667, 198, 297, 3364, 2195, 386]
EX_X = [1, 0, 0, 1, 0, 1, 1, 0, 1, 0]
EX_S = 5635


def test_worked_example():
    a, x, s = random_instance(10, 12, random.Random(7))
    assert (a, x, s) == (EX_A, EX_X, EX_S)
    assert abs(density(a) - 0.8387) < 1e-4
    assert cjloss_attack(a, s) == EX_X


def test_target_vector_is_in_the_lattice():
    rows = cjloss_basis(EX_A, EX_S)
    n = len(EX_A)
    v = [0] * (n + 1)
    for xi, row in zip(EX_X, rows):
        for j in range(n + 1):
            v[j] += xi * row[j]
    v = [vj - bj for vj, bj in zip(v, rows[n])]
    assert v == [2 * xi - 1 for xi in EX_X] + [0]


def test_cjloss_recovers_random_instances():
    rng = random.Random(2024)
    for _ in range(6):
        a, x, s = random_instance(20, 24, rng)
        assert 0.8 < density(a) < 0.9
        got = cjloss_attack(a, s)
        assert got is not None and sum(g * ai for g, ai in zip(got, a)) == s


def test_cjloss_beats_lagarias_odlyzko():
    rng = random.Random(2024)
    cj = lo = 0
    for _ in range(8):
        a, x, s = random_instance(24, 30, rng)
        cj += cjloss_attack(a, s) is not None
        lo += lo_attack(a, s) is not None
    assert cj == 8 and lo <= 4


def test_breaks_merkle_hellman_without_private_key():
    rng = random.Random(1)
    pk, (w, q, r) = merkle_hellman_public_key(10, rng)
    assert all(w[i] > sum(w[:i]) for i in range(len(w)))
    msg = [1, 1, 0, 1, 0, 0, 1, 0, 1, 1]
    c = sum(m * ai for m, ai in zip(msg, pk))
    # The owner decrypts with the trapdoor: multiply by r^-1 and solve greedily.
    t, out = c * pow(r, -1, q) % q, []
    for wi in reversed(w):
        out.append(1 if t >= wi else 0)
        t -= wi * out[-1]
    assert out[::-1] == msg
    # The attacker uses the public key alone.
    assert cjloss_attack(pk, c) == msg


def test_lll_copy_keeps_the_lattice():
    basis = [[1, 0, 0, 1000], [0, 1, 0, 2001], [0, 0, 1, 2999]]
    red = lll_reduce(basis)
    # Same lattice: each reduced row is an integer combination of the input, and the Gram determinant agrees.
    def gram_det(rows):
        g = [[Fraction(sum(x * y for x, y in zip(u, v))) for v in rows] for u in rows]
        det = Fraction(1)
        for i in range(3):
            piv = g[i][i]
            det *= piv
            for k in range(i + 1, 3):
                f = g[k][i] / piv
                g[k] = [gk - f * gi for gk, gi in zip(g[k], g[i])]
        return det
    assert gram_det(red) == gram_det(basis)
    # The LLL bound with delta = 99/100, against a search of small combinations.
    shortest = min(
        sum((i * basis[0][j] + k * basis[1][j] + m * basis[2][j]) ** 2 for j in range(4))
        for i in range(-4, 5) for k in range(-4, 5) for m in range(-4, 5) if (i, k, m) != (0, 0, 0)
    )
    first = sum(c * c for c in red[0])
    assert first <= (Fraction(400, 296) ** 2) * shortest
