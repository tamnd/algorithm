# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burnikel-ziegler-division/. The authors are listed in prov/V436BS.jsonl.

import random

import pytest

from burnikel_ziegler_division import Stats, bz_divmod, div_2n_1n, div_3n_2n


def test_example_base16():
    # w = 4: beta = 16, b = 0xC3A5 has n = 4 limbs and is normalized.
    a, b = 0x9F2E_71B4, 0xC3A5
    st = Stats()
    q, r = div_2n_1n(a, b, 4, 4, st, n0=1)
    assert (q, r) == divmod(a, b) == (0xD049, 0x97A7)
    # the second 3n/2n step needs exactly one correction (line L9)
    assert st.corrections >= 1 and st.max_corrections <= 2


def test_exhaustive_small_base2():
    for b in range(1, 64):
        for a in range(0, 1 << 9):
            assert bz_divmod(a, b, w=1, n0=1) == divmod(a, b)


def test_random_many_sizes():
    rng = random.Random(1998)
    for _ in range(600):
        w = rng.choice((1, 2, 4, 8, 16))
        nb = rng.randint(1, 48)
        b = rng.getrandbits(nb * w) | 1
        a = rng.getrandbits(rng.randint(0, 3 * nb * w))
        st = Stats()
        assert bz_divmod(a, b, w, n0=rng.choice((1, 2, 4)), st=st) == divmod(a, b)
        assert st.max_corrections <= 2


def test_adversarial_top_limbs():
    rng = random.Random(7)
    for w in (2, 4, 8):
        beta = 1 << w
        for n in (2, 4, 8, 16, 32):
            for _ in range(20):
                b = (beta >> 1) << (w * (n - 1)) | rng.getrandbits(w * (n - 1))
                q = rng.getrandbits(w * n)
                r = rng.randint(0, b - 1)
                a = q * b + r
                st = Stats()
                assert div_2n_1n(a, b, n, w, st, n0=1) == (q, r)
                assert st.max_corrections <= 2
            top = (1 << (w * n)) - 1
            assert div_2n_1n(top * top, top, n, w, Stats(), n0=1) == (top, 0)


def test_product_counts():
    # D(n) = 2 D3(n/2) and D3(h) = D(h) + one h x h product: for n = 2^k and
    # n0 = 1, 2^j products of size n / 2^j occur at each level, j = 1..k.
    rng = random.Random(3)
    w = 4
    for k in range(1, 7):
        n = 1 << k
        b = (1 << (w * n - 1)) | rng.getrandbits(w * n - 1)
        a = rng.randint(0, (b << (w * n)) - 1)
        st = Stats()
        assert div_2n_1n(a, b, n, w, st, n0=1) == divmod(a, b)
        expected = {n >> j: 1 << j for j in range(1, k + 1)}
        assert st.products == expected


def test_3n_2n_cap_branch():
    # a1 == b1 forces the branch Q = beta^h - 1 (line L7).
    w, h = 4, 2
    b = 0xC3A5
    b1 = b >> (w * h)
    a = (b1 << (2 * w * h)) | 0x0FFF
    assert a < (b << (w * h))
    assert div_3n_2n(a, b, h, w, Stats(), n0=1) == divmod(a, b)


def test_errors():
    with pytest.raises(ValueError):
        bz_divmod(5, 0)
    with pytest.raises(ValueError):
        bz_divmod(-1, 3)
    assert bz_divmod(0, 7) == (0, 0)
