# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rainbow-signature/. The authors are listed in prov/DWHJ3K.jsonl.
"""Tests for toy two-layer Rainbow over GF(31) and the toy key recovery. The
Rainbow known answer tests of the NIST submission use GF(16) or GF(256) and a
fixed encoding, so they do not apply to this toy; there are no official
vectors for it. The tests check a hand example, the linear algebra against
brute force, the layer structure, sign and verify round trips, and the attack,
all with fixed seeds."""

import itertools
import random

from rainbow_signature import (
    Q,
    in_O2,
    inverse,
    keygen,
    layer_system,
    mat_mul,
    mat_vec,
    nullspace,
    quad_form,
    rank,
    recover_key,
    secret_subspaces,
    forge,
    sign,
    solve_any,
    verify,
)


def test_page_example():
    """f1 = x1^2 + 3 x1 x2 and f2 = x2^2 + x1 x3 + 2 x2 x3 over GF(31), with
    target (7, 9). Vinegar x1 = 1 gives 1 + 3 x2 = 7, so x2 = 2; then
    4 + 5 x3 = 9, so x3 = 1."""
    h = pow(2, -1, Q)
    F1 = [[1, 3 * h % Q, 0], [3 * h % Q, 0, 0], [0, 0, 0]]
    F2 = [[0, 0, h], [0, 1, 1], [h, 1, 0]]
    lhs, rhs = layer_system([F1], [1], 1, [7])
    assert lhs == [[3]] and rhs == [6] and solve_any(lhs, rhs, unique=True) == [2]
    lhs, rhs = layer_system([F2], [1, 2], 1, [9])
    assert lhs == [[5]] and rhs == [5] and solve_any(lhs, rhs, unique=True) == [1]
    assert quad_form(F1, [1, 2, 1]) == 7 and quad_form(F2, [1, 2, 1]) == 9


def test_linear_algebra_against_brute_force():
    rng = random.Random(1)
    for _ in range(500):
        rows, cols = rng.randint(1, 2), rng.randint(1, 2)
        a = [[rng.randrange(Q) for _ in range(cols)] for _ in range(rows)]
        b = [rng.randrange(Q) for _ in range(rows)]
        brute = [list(x) for x in itertools.product(range(Q), repeat=cols)
                 if all(sum(r * y for r, y in zip(row, x)) % Q == bi for row, bi in zip(a, b))]
        got = solve_any(a, b)
        assert (got is None) == (not brute)
        if got is not None:
            assert got in brute
        uniq = solve_any(a, b, unique=True)
        assert (uniq is not None) == (len(brute) == 1)
        kernel = sum(1 for x in itertools.product(range(Q), repeat=cols)
                     if all(sum(r * y for r, y in zip(row, x)) % Q == 0 for row in a))
        assert kernel == Q ** len(nullspace(a))
        if rows == cols:
            inv = inverse(a)
            assert (inv is None) == (kernel > 1)
            if inv is not None:
                assert mat_mul(a, inv) == [[int(i == j) for j in range(cols)] for i in range(rows)]


def test_central_map_has_the_layer_shape():
    rng = random.Random(2)
    v1, o1, o2 = 6, 3, 3
    _, sk = keygen(v1, o1, o2, rng)
    n = v1 + o1 + o2
    for k, Fk in enumerate(sk.F):
        assert all(Fk[i][j] == Fk[j][i] for i in range(n) for j in range(n))
        lo, hi = (v1, v1 + o1) if k < o1 else (v1 + o1, n)
        assert all(Fk[i][j] == 0 for i in range(lo, hi) for j in range(lo, hi))
        assert all(Fk[i][j] == 0 for i in range(hi, n) for j in range(n))


def test_public_key_is_the_composition():
    rng = random.Random(3)
    P, sk = keygen(6, 3, 3, rng)
    for _ in range(500):
        s = [rng.randrange(Q) for _ in range(12)]
        f = [quad_form(Fj, mat_vec(sk.S, s)) for Fj in sk.F]
        assert [quad_form(Pk, s) for Pk in P] == mat_vec(sk.T, f)


def test_sign_and_verify():
    rng = random.Random(4)
    for prm in [(4, 2, 2), (6, 3, 3)]:
        P, sk = keygen(*prm, rng)
        for i in range(30):
            msg = b"message %d" % i
            sig = sign(sk, msg, rng)
            assert verify(P, msg, sig)
            assert not verify(P, msg + b"!", sig)
            s, salt = sig
            assert not verify(P, msg, ([(s[0] + 1) % Q] + s[1:], salt))


def test_second_oil_space_is_visible_in_the_public_key():
    """P vanishes on O2, and P'(y, o) lies in the o2-dimensional W for o in O2."""
    rng = random.Random(5)
    P, sk = keygen(6, 3, 3, rng)
    O2, W = secret_subspaces(sk)
    for o in O2:
        assert all(quad_form(Pk, o) == 0 for Pk in P) and in_O2(P, o, 3)
        for _ in range(20):
            y = [rng.randrange(Q) for _ in range(12)]
            image = [2 * sum(a * b for a, b in zip(y, mat_vec(Pk, o))) % Q for Pk in P]
            assert rank(W + [image]) == 3
    assert not any(in_O2(P, [rng.randrange(Q) for _ in range(12)], 3) for _ in range(50))


def test_toy_key_recovery_lets_the_attacker_sign():
    for prm, seed in [((2, 2, 2), 6), ((2, 2, 3), 7)]:
        rng = random.Random(seed)
        P, sk = keygen(*prm, rng)
        key = recover_key(P, prm[1], prm[2], rng)          # public key only
        assert key is not None
        O2, W = secret_subspaces(sk)
        assert rank(key.O2 + O2) == prm[2]                  # the true O2
        assert all(sum(c * w for c, w in zip(cv, wv)) % Q == 0 for cv in key.w_perp for wv in W)
        for i in range(10):
            msg = b"forged %d" % i
            assert verify(P, msg, forge(P, key, msg, rng))
