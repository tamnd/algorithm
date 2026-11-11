# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unbalanced-oil-and-vinegar/. The authors are listed in prov/PHGT6X.jsonl.
"""Tests for toy UOV over GF(31) and the Kipnis-Shamir attack. The official
UOV known answer tests use GF(256) or GF(16), key compression and a fixed
encoding, so they do not apply to this toy; there are no official vectors for
it. The tests check a hand example, the linear algebra against brute force,
sign and verify round trips, and the attack, all with fixed seeds."""

import itertools
import random

from unbalanced_oil_and_vinegar import (
    Q,
    inverse,
    keygen,
    kipnis_shamir,
    mat_mul,
    mat_vec,
    nullspace,
    oil_space,
    quad_form,
    rank,
    sign,
    sign_with_oil_space,
    solve,
    vanishes,
    verify,
)


def test_page_example():
    """f = x1^2 + 2 x1 x3 + 3 x2 x3 + x1 x2 over GF(31) with vinegar x1, x2
    and oil x3. Fixing x1 = 1, x2 = 2 gives 3 + 8 x3, and x3 = 8 gives 5."""
    f = lambda x1, x2, x3: (x1 * x1 + 2 * x1 * x3 + 3 * x2 * x3 + x1 * x2) % 31
    assert f(1, 2, 0) == 3 and (f(1, 2, 1) - f(1, 2, 0)) % 31 == 8
    assert pow(8, -1, 31) == 4 and f(1, 2, 8) == 5
    # the same polynomial as a symmetric matrix (q odd, so 1/2 exists)
    h = pow(2, -1, 31)
    F = [[1, h, 1], [h, 0, 3 * h % 31], [1, 3 * h % 31, 0]]
    assert quad_form(F, [1, 2, 8]) == 5


def test_linear_algebra_against_brute_force():
    rng = random.Random(1)
    q = 5
    for _ in range(500):
        n = rng.randint(1, 3)
        a = [[rng.randrange(q) for _ in range(n)] for _ in range(n)]
        b = [rng.randrange(q) for _ in range(n)]
        brute = [list(x) for x in itertools.product(range(q), repeat=n)
                 if all(sum(r * y for r, y in zip(row, x)) % q == bi for row, bi in zip(a, b))]
        got = solve(a, b, q)
        if got is None:
            assert len(brute) != 1
        else:
            assert brute == [got]
        kernel = [list(x) for x in itertools.product(range(q), repeat=n)
                  if all(sum(r * y for r, y in zip(row, x)) % q == 0 for row in a)]
        assert len(kernel) == q ** len(nullspace(a, q))
        inv = inverse(a, q)
        assert (inv is None) == (len(kernel) > 1)
        if inv is not None:
            assert mat_mul(a, inv, q) == [[int(i == j) for j in range(n)] for i in range(n)]


def test_public_key_is_the_composition():
    rng = random.Random(2)
    P, sk = keygen(12, 6, rng)
    for _ in range(500):
        s = [rng.randrange(Q) for _ in range(18)]
        x = mat_vec(sk.S, s)
        assert [quad_form(Pk, s) for Pk in P] == [quad_form(Fk, x) for Fk in sk.F]


def test_public_key_vanishes_on_the_oil_space():
    rng = random.Random(3)
    P, sk = keygen(12, 6, rng)
    O = oil_space(sk)
    assert rank(O) == 6 and vanishes(P, O)


def test_sign_and_verify():
    rng = random.Random(4)
    for v, o in [(8, 4), (12, 6)]:
        P, sk = keygen(v, o, rng)
        for i in range(30):
            msg = b"message %d" % i
            sig = sign(sk, msg, rng)
            assert verify(P, msg, sig)
            assert not verify(P, msg + b"!", sig)
            s, salt = sig
            assert not verify(P, msg, ([(s[0] + 1) % Q] + s[1:], salt))


def test_kipnis_shamir_breaks_balanced_oil_and_vinegar():
    rng = random.Random(5)
    for o in (4, 6):
        P, sk = keygen(o, o, rng)                 # v = o: balanced
        O = kipnis_shamir(P, rng)                 # public key only
        assert O is not None and len(O) == o
        assert rank(O + oil_space(sk)) == o       # the true oil space
        for i in range(10):
            msg = b"forged %d" % i
            assert verify(P, msg, sign_with_oil_space(P, O, msg, rng))


def test_kipnis_shamir_fails_on_unbalanced():
    """With v = 2o the invariant subspace argument breaks down."""
    rng = random.Random(6)
    P, _ = keygen(8, 4, rng)
    assert kipnis_shamir(P, rng, tries=20) is None
