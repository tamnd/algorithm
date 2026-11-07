# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schonhage-strassen-multiplication/. The authors are listed in prov/XRQ0DB.jsonl.

import math
import random

import pytest

from schonhage_strassen_multiplication import Stats, _fft, mul2exp, mulmod, ssa_multiply


def limbs(x: int, w: int, n: int) -> list[int]:
    return [(x >> (w * i)) & ((1 << w) - 1) for i in range(n)]


def value(d: list[int], w: int) -> int:
    v = 0
    for x in reversed(d):
        v = (v << w) | x
    return v


def test_example() -> None:
    n2, K, t = 12, 4, 3
    mod2 = (1 << n2) + 1
    a, b = [4, 3, 2, 1], [8, 7, 6, 5]
    aw = [mul2exp(a[j], j * t, n2) for j in range(K)]
    bw = [mul2exp(b[j], j * t, n2) for j in range(K)]
    assert aw == [4, 24, 128, 512] and bw == [8, 56, 384, 2560]
    fa, fb = _fft(aw, 2 * t, n2), _fft(bw, 2 * t, n2)
    assert fa == [668, 1420, 3693, 2429] and fb == [3008, 3248, 1873, 97]
    fc = [x * y % mod2 for x, y in zip(fa, fb)]
    assert fc == [1814, 3035, 1253, 2084]
    c = _fft(fc, -2 * t, n2)
    assert c == [4089, 1152, 2045, 4067]
    cj = [mul2exp(c[j], -(2 + j * t), n2) for j in range(K)]
    assert cj == [4095, 36, 56, 60]
    signed = [x - mod2 if x >= (j + 1) << 8 else x for j, x in enumerate(cj)]
    assert signed == [-2, 36, 56, 60]
    assert sum(v << (4 * j) for j, v in enumerate(signed)) % 65537 == 64059 == 4660 * 22136 % 65537
    st = Stats()
    assert mulmod(4660, 22136, 16, 8, st) == 64059
    assert st.levels[0] == [(16, 4, 12)]


def test_mul2exp() -> None:
    rng = random.Random(1)
    for m in (1, 2, 5, 12, 64, 100):
        mod = (1 << m) + 1
        for _ in range(100):
            x, s = rng.randrange(mod), rng.randrange(-5 * m, 5 * m)
            assert mul2exp(x, s, m) == x * pow(2, s, mod) % mod
        assert mul2exp(1 << m, 1, m) == mod - 2


def test_mulmod_random_and_edges() -> None:
    rng = random.Random(2)
    sizes = {1: list(range(1, 65)), 32: list(range(1, 200)) + [256, 1000], 64: [100, 256, 1000, 3000, 4096]}
    for th, ns in sizes.items():
        for n in ns:
            mod = (1 << n) + 1
            cases = [(0, 0), (1, 1 << n), (1 << n, 1 << n), ((1 << n) - 1, (1 << n) - 1), (1 << n, 5 % mod)]
            cases += [(rng.randrange(mod), rng.randrange(mod)) for _ in range(3)]
            for A, B in cases:
                assert mulmod(A, B, n, th) == A * B % mod


@pytest.mark.parametrize("w", [4, 8])
def test_limbs_random(w: int) -> None:
    rng = random.Random(10 + w)
    for _ in range(80):
        m, n = rng.randint(1, 90), rng.randint(1, 90)
        x, y = rng.randrange(1 << (w * m)), rng.randrange(1 << (w * n))
        out = ssa_multiply(limbs(x, w, m), limbs(y, w, n), w, 32)
        assert len(out) == m + n
        assert value(out, w) == x * y


@pytest.mark.parametrize("w", [4, 8])
def test_limbs_edges(w: int) -> None:
    B = 1 << w
    for n in (1, 2, 3, 16, 64 // w * 4, 100 // w * 4):
        top = B**n - 1
        for x in (0, 1, top, B ** (n - 1)):
            for y in (0, 1, top, B ** (n - 1), top - 1):
                assert value(ssa_multiply(limbs(x, w, n), limbs(y, w, n), w, 32), w) == x * y
    assert ssa_multiply([], [], w) == []


def test_large_and_depth() -> None:
    rng = random.Random(4)
    for N, depth in ((1 << 10, 2), (1 << 12, 2)):
        x, y = rng.randrange(1 << N), rng.randrange(1 << N)
        st = Stats()
        assert value(ssa_multiply(limbs(x, 8, N // 8), limbs(y, 8, N // 8), 8, 64, st), 8) == x * y
        assert st.max_depth == depth
        assert st.max_depth <= math.log2(math.log2(2 * N)) + 1
    st = Stats()
    N = 1 << 14
    x, y = rng.randrange(1 << N), rng.randrange(1 << N)
    assert value(ssa_multiply(limbs(x, 8, N // 8), limbs(y, 8, N // 8), 8, 64, st), 8) == x * y
    assert (st.levels[0][0], st.levels[1][0], st.levels[2][0]) == ((33024, 128, 640), (640, 16, 96), (96, 8, 32))
    assert st.base_products == 16384 and st.max_depth == 3


def test_bad_radix() -> None:
    with pytest.raises(ValueError):
        ssa_multiply([1], [1], 3)
