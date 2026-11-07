# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-exponentiation/. The authors are listed in prov/YXZZ39.jsonl.

import random

import pytest

from sliding_window_exponentiation import (
    Counter,
    best_width,
    fixed_window_power,
    from_limbs,
    limb_mul,
    modpow_limbs,
    power,
    power_limbs,
    to_limbs,
    windows,
)


def imul(a, b):
    return a * b


def test_windows_reassemble_and_shape():
    rng = random.Random(1)
    for _ in range(2000):
        e = rng.getrandbits(rng.randint(1, 200)) or 1
        k = rng.randint(1, 8)
        acc = 0
        ws = windows(e, k)
        for u, length in ws:
            acc = (acc << length) | u
            if u:
                assert u & 1 and 1 <= length <= k and u >> (length - 1) == 1
            else:
                assert length == 1
        assert acc == e
        t = e.bit_length()
        nwin = sum(1 for u, _ in ws if u)
        assert nwin <= -(-t // k)  # proved bound on the number of windows


def test_power_integers_all_small():
    for k in range(1, 7):
        for x in (0, 1, 2, 3, -5):
            for e in range(0, 300):
                assert power(x, e, k, imul, 1) == x**e


def test_counts_bound_and_exactness():
    rng = random.Random(2)
    for _ in range(1500):
        t = rng.randint(1, 300)
        e = rng.getrandbits(t) | (1 << (t - 1))
        k = rng.randint(1, 8)
        c = Counter()
        assert power(7, e, k, lambda a, b: a * b % 1000003, 1, c) == pow(7, e, 1000003)
        ws = windows(e, k)
        nwin = sum(1 for u, _ in ws if u)
        table = 0 if (k == 1 or e == 1) else (min((1 << k) - 1, e) + 1) // 2
        assert c.total == table + (t - ws[0][1]) + (nwin - 1)
        assert c.total <= t - 2 + -(-t // k) + 2 ** (k - 1)
    for t in (1, 2, 10, 64):  # all ones is the worst case of the binary method
        c = Counter()
        assert power(3, (1 << t) - 1, 1, lambda a, b: a * b % 1000003, 1, c) == pow(3, (1 << t) - 1, 1000003)
        assert c.total == 2 * t - 2


def test_worked_example():
    e = 2989
    assert bin(e) == "0b101110101101"
    assert windows(e, 3) == [(5, 3), (3, 2), (0, 1), (5, 3), (5, 3)]
    exps, y = [], 0
    for u, length in windows(e, 3):
        y = (y << length) + u
        exps.append(y)
    assert exps == [5, 23, 46, 373, 2989]
    c = Counter()
    assert power(3, e, 3, imul, 1, c) == 3**e
    assert (c.squarings, c.products) == (10, 6)
    b = Counter()
    power(3, e, 1, imul, 1, b)
    assert (b.squarings, b.products) == (11, 7)
    f = Counter()
    assert fixed_window_power(3, e, 3, imul, 1, f) == 3**e
    assert f.total == 18
    assert windows(13, 3) == [(3, 2), (0, 1), (1, 1)]


def test_average_counts_and_best_width():
    rng = random.Random(1)
    t = 1024
    es = [rng.getrandbits(t) | (1 << (t - 1)) for _ in range(60)]
    means = {}
    for k in range(1, 8):
        tot = nwin = 0
        for e in es:
            c = Counter()
            power(1, e, k, lambda a, b: a, 1, c)
            tot += c.total
            nwin += sum(1 for u, _ in windows(e, k) if u)
        means[k] = tot / len(es)
        assert abs(nwin / len(es) - t / (k + 1)) < 0.03 * t / (k + 1)
        assert abs(means[k] - (t - 1 + t / (k + 1) + 2 ** (k - 1))) < 15
    assert min(means, key=means.get) == 6
    fixed = []
    for k in (5, 6):
        tot = 0
        for e in es:
            c = Counter()
            fixed_window_power(1, e, k, lambda a, b: a, 1, c)
            tot += c.total
        fixed.append(tot / len(es))
    assert min(fixed) > means[6] + 30
    assert [best_width(t) for t in (64, 256, 512, 1024, 2048, 4096)] == [3, 5, 5, 6, 7, 7]


@pytest.mark.parametrize("w", [4, 8])
def test_limbs_against_python(w):
    rng = random.Random(10 + w)
    for _ in range(100):
        a = rng.getrandbits(rng.randint(0, 32))
        e = rng.randint(0, 60)
        k = rng.randint(1, 6)
        assert from_limbs(power_limbs(to_limbs(a, w), e, k, w), w) == a**e
    for _ in range(120):
        m = rng.getrandbits(rng.randint(1, 96)) or 1
        a = rng.getrandbits(rng.randint(0, 120))
        e = rng.getrandbits(rng.randint(0, 200))
        k = rng.randint(1, 7)
        r = modpow_limbs(to_limbs(a, w), e, to_limbs(m, w), k, w)
        assert from_limbs(r, w) == pow(a, e, m)
        assert all(0 <= d < (1 << w) for d in r)
    edge = [(0, 0, 7), (0, 5, 7), (5, 0, 1), (2, 100, 1), ((1 << 64) - 1, (1 << 64) - 1, (1 << 61) - 1)]
    for a, e, m in edge:
        assert from_limbs(modpow_limbs(to_limbs(a, w), e, to_limbs(m, w), 4, w), w) == pow(a, e, m)
    assert limb_mul([], [1], w) == []


def test_matrix_monoid():
    def mm(p, q):
        return (
            (p[0][0] * q[0][0] + p[0][1] * q[1][0], p[0][0] * q[0][1] + p[0][1] * q[1][1]),
            (p[1][0] * q[0][0] + p[1][1] * q[1][0], p[1][0] * q[0][1] + p[1][1] * q[1][1]),
        )

    one = ((1, 0), (0, 1))
    fib = [0, 1]
    for _ in range(400):
        fib.append(fib[-1] + fib[-2])
    for e in range(0, 400, 7):
        for k in (1, 3, 5):
            assert power(((1, 1), (1, 0)), e, k, mm, one)[0][1] == fib[e]


def test_errors():
    with pytest.raises(ValueError):
        power(2, 5, 0, imul, 1)
    with pytest.raises(ValueError):
        windows(0, 3)
    with pytest.raises(ZeroDivisionError):
        modpow_limbs([2], 3, [], 2, 8)
