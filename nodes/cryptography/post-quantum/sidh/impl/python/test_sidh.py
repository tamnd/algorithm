# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sidh/. The authors are listed in prov/HYTKQP.jsonl.

import random

import pytest

from sidh import SIKE_PARAMS, isogeny, keygen, order_is, setup, shared, sike_sizes


@pytest.fixture(scope="module")
def pp():
    return setup(4, 3, seed=1)


def is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def test_toy_prime(pp):
    assert pp.p == 431 == 2**4 * 3**3 - 1
    assert is_probable_prime(pp.p) and pp.p % 4 == 3


def test_torsion_bases(pp):
    E0 = pp.E0
    for P, n, ell in ((pp.PA, 16, 2), (pp.QA, 16, 2), (pp.PB, 27, 3), (pp.QB, 27, 3)):
        assert E0.on_curve(P)
        assert order_is(E0, P, n, ell)
    # Independent: [8] PA and [8] QA are different points of order 2.
    assert E0.mul(8, pp.PA) != E0.mul(8, pp.QA)


def test_public_keys(pp):
    rng = random.Random(2)
    a, (EA, U, V) = keygen(pp, "A", rng)
    assert EA.on_curve(U) and EA.on_curve(V)
    # phi_A has degree 16, prime to 27, so it keeps the order of the 3-torsion basis.
    assert order_is(EA, U, 27, 3) and order_is(EA, V, 27, 3)
    b, (EB, U, V) = keygen(pp, "B", rng)
    assert order_is(EB, U, 16, 2) and order_is(EB, V, 16, 2)


def test_both_sides_agree(pp):
    rng = random.Random(3)
    for _ in range(15):
        a, pkA = keygen(pp, "A", rng)
        b, pkB = keygen(pp, "B", rng)
        assert shared(pp, "A", a, pkB) == shared(pp, "B", b, pkA)


def test_commutative_diagram(pp):
    # E0 / <RA, RB> computed in both orders gives the same j-invariant.
    E0 = pp.E0
    a, b = 5, 11
    RA = E0.add(pp.PA, E0.mul(a, pp.QA))
    RB = E0.add(pp.PB, E0.mul(b, pp.QB))
    EA, (rb,) = isogeny(E0, RA, 2, 4, [RB])
    EB, (ra,) = isogeny(E0, RB, 3, 3, [RA])
    assert isogeny(EA, rb, 3, 3, [])[0].j() == isogeny(EB, ra, 2, 4, [])[0].j()


def test_wrong_secret_changes_the_key(pp):
    rng = random.Random(4)
    a, pkA = keygen(pp, "A", rng)
    b, pkB = keygen(pp, "B", rng)
    good = shared(pp, "A", a, pkB)
    others = {shared(pp, "A", x, pkB).key() for x in range(16) if x != a}
    # Some other secrets give other keys; the toy key space is tiny.
    assert len(others - {good.key()}) >= 3


def test_sike_parameters():
    expected = {
        "SIKEp434": (434, 330, 346),
        "SIKEp503": (503, 378, 402),
        "SIKEp610": (610, 462, 486),
        "SIKEp751": (751, 564, 596),
    }
    for name, (eA, eB, _, _) in SIKE_PARAMS.items():
        p = 2**eA * 3**eB - 1
        assert is_probable_prime(p)
        bits, pk, ct = expected[name]
        assert p.bit_length() == bits
        assert sike_sizes(name) == (pk, ct)
