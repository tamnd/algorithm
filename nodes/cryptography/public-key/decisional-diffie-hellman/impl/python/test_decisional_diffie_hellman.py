# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decisional-diffie-hellman/. The authors are listed in prov/AE1DRR.jsonl.
"""Tests for the DDH tools. DDH is a problem, not a standard algorithm, so
there are no official test vectors. The tests use toy groups and fixed seeds.
"""

import random
from collections import Counter

from decisional_diffie_hellman import apply_map, is_square, legendre_ddh, rerandomize

# 2 generates Z_2357^* (Handbook of Applied Cryptography, Example 8.19).
P_FULL, G_FULL = 2357, 2
# The safe prime 23 = 2 * 11 + 1; 4 generates the squares, a group of order 11.
P_SMALL, Q_SMALL, G_SMALL = 23, 11, 4
# The smallest safe prime above 2^63 and its subgroup of squares.
P_TOY = 9223372036854778487
Q_TOY = (P_TOY - 1) // 2
G_TOY = 4


def test_generator_of_full_group() -> None:
    n = P_FULL - 1  # 2356 = 2^2 * 19 * 31
    assert all(pow(G_FULL, n // r, P_FULL) != 1 for r in (2, 19, 31))


def test_legendre_attack_has_advantage_one_half() -> None:
    rng = random.Random(1997)
    n = P_FULL - 1
    real = rand = 0
    trials = 4000
    for _ in range(trials):
        x, y, z = rng.randrange(n), rng.randrange(n), rng.randrange(n)
        X, Y = pow(G_FULL, x, P_FULL), pow(G_FULL, y, P_FULL)
        real += legendre_ddh(P_FULL, X, Y, pow(G_FULL, x * y, P_FULL))
        rand += legendre_ddh(P_FULL, X, Y, pow(G_FULL, z, P_FULL))
    assert real == trials
    assert abs(rand / trials - 0.5) < 0.04


def test_exact_advantage_by_enumeration() -> None:
    # Over all (x, y, z) in Z_22^3 for p = 23 and the generator 5:
    # Pr[1 | real] = 1 and Pr[1 | random] = 1/2 exactly.
    p, g, n = 23, 5, 22
    assert all(pow(g, n // r, p) != 1 for r in (2, 11))
    real = sum(legendre_ddh(p, pow(g, x, p), pow(g, y, p), pow(g, x * y, p)) for x in range(n) for y in range(n))
    rand = sum(
        legendre_ddh(p, pow(g, x, p), pow(g, y, p), pow(g, z, p)) for x in range(n) for y in range(n) for z in range(n)
    )
    assert real == n * n
    assert 2 * rand == n**3


def test_subgroup_of_squares_defeats_the_attack() -> None:
    rng = random.Random(8)
    for _ in range(200):
        x, y, z = rng.randrange(Q_TOY), rng.randrange(Q_TOY), rng.randrange(Q_TOY)
        for e in (x, y, x * y, z):
            assert is_square(pow(G_TOY, e, P_TOY), P_TOY)


def test_random_self_reduction_is_exactly_uniform() -> None:
    p, q, g = P_SMALL, Q_SMALL, G_SMALL
    dlog = {pow(g, k, p): k for k in range(q)}
    for x, y, z in [(3, 7, 21 % 11), (0, 5, 0), (3, 7, 4), (2, 0, 9)]:
        X, Y, Z = pow(g, x, p), pow(g, y, p), pow(g, z, p)
        out = Counter()
        for a in range(1, q):
            for b in range(q):
                for c in range(q):
                    X2, Y2, Z2 = apply_map(p, q, g, X, Y, Z, a, b, c)
                    out[(dlog[X2], dlog[Y2], dlog[Z2])] += 1
        if z == x * y % q:
            # Every Diffie-Hellman triple appears q - 1 times.
            assert len(out) == q * q
            assert all(z2 == x2 * y2 % q and n == q - 1 for (x2, y2, z2), n in out.items())
        else:
            # Every triple that is not a Diffie-Hellman triple appears once.
            assert len(out) == q * q * (q - 1)
            assert all(z2 != x2 * y2 % q and n == 1 for (x2, y2, z2), n in out.items())


def test_rerandomize_on_large_group() -> None:
    rng = random.Random(1)
    x, y = rng.randrange(Q_TOY), rng.randrange(Q_TOY)
    X, Y = pow(G_TOY, x, P_TOY), pow(G_TOY, y, P_TOY)
    Z = pow(G_TOY, x * y, P_TOY)
    for _ in range(20):
        X2, Y2, Z2 = rerandomize(P_TOY, Q_TOY, G_TOY, X, Y, Z, rng)
        assert (X2, Y2) != (X, Y)
    # A real triple stays real: check it with the known exponents.
    a, b, c = 5, 6, 7
    X2, Y2, Z2 = apply_map(P_TOY, Q_TOY, G_TOY, X, Y, Z, a, b, c)
    x2, y2 = (a * x + b) % Q_TOY, (y + c) % Q_TOY
    assert X2 == pow(G_TOY, x2, P_TOY) and Y2 == pow(G_TOY, y2, P_TOY)
    assert Z2 == pow(G_TOY, x2 * y2, P_TOY)
