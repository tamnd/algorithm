# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/castryck-decru-attack/. The authors are listed in prov/R81X70.jsonl.

import random

import pytest

from castryck_decru_attack import (
    Curve,
    Fp2,
    candidates_by_j,
    isomorphisms,
    kernels_equal,
    keygen,
    public_key,
    recover_secret,
    roots,
    setup,
)


@pytest.fixture(scope="module")
def pp():
    return setup(4, 3, seed=1)


def test_recovers_every_secret(pp):
    for side, n in (("A", 16), ("B", 27)):
        for s in range(n):
            assert recover_secret(pp, side, public_key(pp, side, s)) == [s]


def test_j_alone_is_ambiguous(pp):
    # Without the torsion images, most toy keys match several secrets.
    for side, n, ambiguous in (("A", 16, 11), ("B", 27, 22)):
        count = 0
        for s in range(n):
            c = candidates_by_j(pp, side, public_key(pp, side, s))
            assert s in c
            for t in c:
                if t != s:
                    assert not kernels_equal(pp, side, s, t)
            count += len(c) > 1
        assert count == ambiguous


def test_worked_example(pp):
    rng = random.Random(2024)
    a, pkA = keygen(pp, "A", rng)
    b, pkB = keygen(pp, "B", rng)
    assert (a, b) == (15, 5)
    assert candidates_by_j(pp, "A", pkA) == [4, 10, 15]
    assert candidates_by_j(pp, "B", pkB) == [0, 5]
    assert recover_secret(pp, "A", pkA) == [15]
    assert recover_secret(pp, "B", pkB) == [5]


def test_works_on_another_model(pp):
    E, U, V = public_key(pp, "A", 15)
    u = Fp2(3, 7, pp.p)
    E2 = Curve(u**4 * E.a, u**6 * E.b)
    U2 = (u * u * U[0], u**3 * U[1])
    V2 = (u * u * V[0], u**3 * V[1])
    assert E2.j() == E.j() and not (E2 == E)
    assert any(w == u for w in isomorphisms(E, E2))
    assert recover_secret(pp, "A", (E2, U2, V2)) == [15]


def test_wrong_images_are_rejected(pp):
    E, U, V = public_key(pp, "A", 15)
    bad = E.add(U, V)
    assert recover_secret(pp, "A", (E, U, bad)) == []


def test_roots():
    r = Fp2(5, 9, 431)
    for k in (2, 3, 4, 6):
        zs = roots(r, k)
        assert all(z**k == r for z in zs)
        assert len(set(zs)) == len(zs)


def test_sikep434_needs_guessed_steps():
    # 3^137 > 2^216, so the first steps must be guessed before c = 2^a - 3^(b - beta) > 0.
    assert 3**137 > 2**216 > 3**136 > 3**135
