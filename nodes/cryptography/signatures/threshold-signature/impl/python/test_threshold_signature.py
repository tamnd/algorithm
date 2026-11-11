# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/threshold-signature/. The authors are listed in prov/YVV26W.jsonl.

import itertools
import random

from threshold_signature import (
    GEN,
    R,
    add,
    combine,
    deal,
    hash_to_g1,
    lagrange_at_zero,
    mul,
    partial_sign,
    partial_verify,
    pedersen_dkg,
    verify,
)

MSG = b"release v1.0"


def test_any_t_shares_sign_and_give_the_bls_signature() -> None:
    rng = random.Random(2003)
    x = rng.randrange(1, R)
    pub, shares, vks = deal(x, 3, 5, rng)
    partials = {i: partial_sign(s, MSG) for i, s in shares.items()}
    expected = mul(x, hash_to_g1(MSG))
    for subset in itertools.combinations(range(1, 6), 3):
        sig = combine({i: partials[i] for i in subset})
        assert sig == expected  # BLS signatures are unique, so every subset agrees
    assert verify(pub, MSG, expected)
    assert all(partial_verify(vks[i], MSG, partials[i]) for i in (1, 4))


def test_t_minus_1_shares_do_not_sign() -> None:
    rng = random.Random(7)
    x = rng.randrange(1, R)
    pub, shares, _ = deal(x, 3, 5, rng)
    partials = {i: partial_sign(shares[i], MSG) for i in (2, 5)}
    assert not verify(pub, MSG, combine(partials))


def test_t_minus_1_shares_fit_every_secret() -> None:
    # Two shares of a degree 2 polynomial are consistent with any value at 0:
    # for each candidate secret s, the polynomial through (0, s), (2, x_2), (5, x_5)
    # has degree at most 2 and gives those shares.
    rng = random.Random(8)
    _, shares, _ = deal(rng.randrange(1, R), 3, 5, rng)
    pts = {2: shares[2], 5: shares[5]}
    for s in (0, 1, 123456, R - 1):
        known = {0: s, **pts}
        ids = sorted(known)
        # Interpolate at 2 and at 5 from the three points; we must get the shares back.
        for z in (2, 5):
            val = 0
            for i in ids:
                num, den = 1, 1
                for j in ids:
                    if j != i:
                        num = num * (z - j) % R
                        den = den * (i - j) % R
                val = (val + known[i] * num * pow(den, -1, R)) % R
            assert val == pts[z]


def test_bad_partial_is_detected_and_replaced() -> None:
    rng = random.Random(9)
    x = rng.randrange(1, R)
    pub, shares, vks = deal(x, 2, 3, rng)
    good = {i: partial_sign(s, MSG) for i, s in shares.items()}
    bad = add(good[1], GEN)
    assert not partial_verify(vks[1], MSG, bad)
    assert not verify(pub, MSG, combine({1: bad, 2: good[2]}))
    # Robustness: drop the bad share and use the third party instead.
    assert verify(pub, MSG, combine({2: good[2], 3: good[3]}))


def test_pedersen_dkg_output_signs() -> None:
    rng = random.Random(1991)
    pub, shares, vks = pedersen_dkg(2, 3, rng)
    partials = {i: partial_sign(shares[i], MSG) for i in (1, 3)}
    assert all(partial_verify(vks[i], MSG, partials[i]) for i in partials)
    assert verify(pub, MSG, combine(partials))
    lam = lagrange_at_zero([1, 3], 1)
    assert lam == 3 * pow(2, -1, R) % R
