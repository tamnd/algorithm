# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/furer-multiplication/. The authors are listed in prov/V5N955.jsonl.

import random

import pytest

from furer_multiplication import (
    Q,
    Counts,
    FurerRing,
    capacity,
    expected_counts,
    furer_multiply,
    ring_mul,
    shift,
)

RINGS = {(m, L): FurerRing(m, L) for m, L in [(2, 1), (2, 2), (2, 3), (4, 1), (4, 2), (4, 3), (8, 1), (8, 2)]}


def naive_dft(vec, root):
    n = len(vec)
    m = len(vec[0])
    out = []
    power = [[1] + [0] * (m - 1)]
    for _ in range(1, n):
        power.append(ring_mul(power[-1], root))
    for k in range(n):
        acc = [0] * m
        for j, a in enumerate(vec):
            t = ring_mul(a, power[(j * k) % n])
            acc = [(p + r) % Q for p, r in zip(acc, t)]
        out.append(acc)
    return out


@pytest.mark.parametrize("key", sorted(RINGS))
def test_root_properties(key):
    ring = RINGS[key]
    m, K, N = ring.m, ring.K, ring.N
    one = [1] + [0] * (m - 1)
    assert ring.powers[N // K] == shift(one, 1)  # rho^(N/K) = x
    assert ring.powers[N // 2] == [Q - 1] + [0] * (m - 1)  # rho^(N/2) = -1
    assert ring_mul(ring.powers[N - 1], ring.rho) == one  # rho^N = 1


def test_shift_matches_ring_mul():
    rng = random.Random(11)
    for m in (2, 4, 8, 16):
        for _ in range(40):
            a = [rng.randrange(Q) for _ in range(m)]
            e = rng.randrange(-4 * m, 4 * m)
            xe = shift([1] + [0] * (m - 1), e)
            assert shift(a, e) == ring_mul(a, xe)


@pytest.mark.parametrize("key", [(2, 1), (2, 2), (4, 1), (4, 2), (8, 1)])
def test_fft_matches_naive_dft(key):
    ring = RINGS[key]
    rng = random.Random(sum(key))
    for sign in (1, -1):
        vec = [[rng.randrange(Q) for _ in range(ring.m)] for _ in range(ring.N)]
        root = ring.root_power(sign)
        assert ring.fft(vec, 1, sign, Counts()) == naive_dft(vec, root)


@pytest.mark.parametrize("key", sorted(RINGS))
def test_operation_counts(key):
    ring = RINGS[key]
    rng = random.Random(5)
    counts = Counts()
    vec = [[rng.randrange(Q) for _ in range(ring.m)] for _ in range(ring.N)]
    ring.fft(vec, 1, 1, counts)
    assert (counts.shifts, counts.twiddle_products) == expected_counts(ring.K, ring.L)
    assert counts.pointwise_products == 0


def test_example_from_the_page():
    counts = Counts()
    assert furer_multiply(0xBEEF, 0xCAFE, RINGS[(2, 2)], b=4, counts=counts) == 0x97660722
    assert (counts.shifts, counts.twiddle_products, counts.pointwise_products) == (96, 27, 16)


def test_table_rows():
    assert expected_counts(4, 2) == (32, 9)
    assert expected_counts(8, 3) == (2304, 833)
    assert expected_counts(8, 4) == (24576, 10241)
    assert expected_counts(16, 3) == (24576, 7425)


def test_edge_cases():
    for key, ring in RINGS.items():
        if ring.N > 64:
            continue
        for b in (1, 4, 8):
            if (ring.N // 2) * (ring.m // 2) * ((1 << b) - 1) ** 2 >= Q:
                continue
            top = (1 << capacity(ring, b)) - 1
            for u, v in [(0, 0), (0, top), (1, 1), (1, top), (top, top), (1 << (capacity(ring, b) - 1), top)]:
                assert furer_multiply(u, v, ring, b=b) == u * v


def test_random_against_python_ints():
    rng = random.Random(2007)
    checked = 0
    for key in [(2, 1), (2, 2), (4, 1), (4, 2), (8, 1)]:
        ring = RINGS[key]
        for b in (2, 5, 8):
            cap = capacity(ring, b)
            for _ in range(30):
                u = rng.getrandbits(rng.randrange(1, cap + 1))
                v = rng.getrandbits(rng.randrange(1, cap + 1))
                assert furer_multiply(u, v, ring, b=b) == u * v
                checked += 1
    for _ in range(100):
        u, v = rng.getrandbits(rng.randrange(1, 200)), rng.getrandbits(rng.randrange(1, 200))
        assert furer_multiply(u, v) == u * v
        checked += 1
    assert checked >= 500


def test_large_ring_once():
    ring = FurerRing(4, 3)
    rng = random.Random(4096)
    u, v = rng.getrandbits(capacity(ring, 8)), rng.getrandbits(capacity(ring, 8))
    assert furer_multiply(u, v, ring) == u * v


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        furer_multiply(-1, 3)
    with pytest.raises(ValueError):
        furer_multiply(1 << 64, 3, RINGS[(2, 1)])
    with pytest.raises(ValueError):
        FurerRing(3, 1)
    with pytest.raises(ValueError):
        furer_multiply(1, 1, RINGS[(8, 2)], b=12)
