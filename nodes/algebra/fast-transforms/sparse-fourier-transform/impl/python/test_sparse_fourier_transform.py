# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-fourier-transform/. The authors are listed in prov/E4WS9H.jsonl.

import cmath
import math
import random

import pytest

from sparse_fourier_transform import crt, sparse_dft

P = 998244353  # P - 1 = 2^23 * 7 * 17, generator 3


def root(p: int, g: int, n: int) -> int:
    assert (p - 1) % n == 0
    return pow(g, (p - 1) // n, p)


def dft_mod(x, w, p):
    n = len(x)
    return [sum(x[j] * pow(w, j * k, p) for j in range(n)) % p for k in range(n)]


def dft_c(x):
    n = len(x)
    return [sum(x[j] * cmath.exp(-2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]


def signal_mod(X, n, w, p):
    """x with spectrum X (a dict), by the inverse DFT."""
    wi, ni = pow(w, -1, p), pow(n, -1, p)
    return [ni * sum(v * pow(wi, j * k, p) for k, v in X.items()) % p for j in range(n)]


def check_mod(factors, p, g, K, trials, seed, need=1.0):
    n = math.prod(factors)
    w = root(p, g, n)
    rng = random.Random(seed)
    wins = 0
    for _ in range(trials):
        k = rng.randint(0, K)
        X = {f: rng.randrange(1, p) for f in rng.sample(range(n), k)}
        x = signal_mod(X, n, w, p)
        got, ok, reads = sparse_dft(lambda j: x[j], factors, K, w=w, p=p)
        for f, v in got.items():  # every reported coefficient is right
            assert X.get(f) == v
        if ok:
            assert got == X
            wins += 1
    assert wins >= need * trials


def test_crt():
    for a in range(5):
        for b in range(7):
            for c in range(9):
                k = crt([a, b, c], [5, 7, 9])
                assert 0 <= k < 315 and (k % 5, k % 7, k % 9) == (a, b, c)


def test_mod_998244353_many():
    check_mod((8, 7, 17), P, 3, 6, 120, 1, need=0.9)
    check_mod((16, 7, 17), P, 3, 8, 60, 2, need=0.9)


def test_mod_97_and_17():
    check_mod((32, 3), 97, 5, 4, 150, 3, need=0.6)
    check_mod((16,), 17, 3, 3, 100, 4)


def test_single_factor_is_full_dft():
    # with d = 1 every bucket holds one frequency, so any spectrum is recovered
    rng = random.Random(5)
    w = root(17, 3, 16)
    for _ in range(30):
        x = [rng.randrange(17) for _ in range(16)]
        X = dft_mod(x, w, 17)
        got, ok, _ = sparse_dft(lambda j: x[j], (16,), 16, w=w, p=17)
        assert ok and got == {k: v for k, v in enumerate(X) if v}


def test_stopping_set_fails_safely():
    # four frequencies forming a rectangle: every bucket of both stages holds two
    n, w = 96, root(97, 5, 96)
    sup = [crt([a, b], [32, 3]) for a in (3, 10) for b in (0, 2)]
    X = {k: v for k, v in zip(sup, (1, 2, 3, 4))}
    x = signal_mod(X, n, w, 97)
    got, ok, _ = sparse_dft(lambda j: x[j], (32, 3), 4, w=w, p=97)
    assert not ok and got == {}
    # one more frequency in the same residue classes is still stuck; one outside is found
    X[crt([20, 1], [32, 3])] = 5
    x = signal_mod(X, n, w, 97)
    got, ok, _ = sparse_dft(lambda j: x[j], (32, 3), 5, w=w, p=97)
    assert not ok and got == {crt([20, 1], [32, 3]): 5}


def test_worked_example_mod_13():
    x = [7, 1, 2, 8, 6, 9, 2, 3, 7, 9, 3, 8]
    assert dft_mod(x, 2, 13) == [0, 1, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0]
    got, ok, reads = sparse_dft(lambda j: x[j], (4, 3), 3, w=2, p=13)
    assert ok and got == {1: 1, 5: 3, 6: 2} and reads == 35


def test_complex_against_direct_dft():
    rng = random.Random(6)
    factors = (7, 8, 9)
    n = 504
    for _ in range(6):
        X = {k: complex(rng.gauss(0, 1), rng.gauss(0, 1)) for k in rng.sample(range(n), 5)}
        x = [sum(v * cmath.exp(2j * math.pi * j * k / n) for k, v in X.items()) / n for j in range(n)]
        ref = dft_c(x)
        got, ok, _ = sparse_dft(lambda j: x[j], factors, 5)
        assert ok
        for k in range(n):
            assert abs(got.get(k, 0) - ref[k]) <= 1e-9 * n


def test_complex_large_oracle():
    rng = random.Random(7)
    factors = (49, 50, 51)
    n = math.prod(factors)
    wins = 0
    for _ in range(4):
        X = {k: complex(rng.gauss(0, 1), rng.gauss(0, 1)) for k in rng.sample(range(n), 12)}
        oracle = lambda j: sum(v * cmath.exp(2j * math.pi * j * k / n) for k, v in X.items()) / n
        got, ok, reads = sparse_dft(oracle, factors, 12)
        assert reads == 150 * len(set(range(13)) | {n // 49, n // 50, n // 51})
        if ok:
            wins += 1
            assert set(got) == set(X)
            assert max(abs(got[k] - X[k]) for k in X) <= 1e-9
    assert wins >= 3


def test_inverse_recovers_input():
    rng = random.Random(8)
    n, w = 952, root(P, 3, 952)
    for _ in range(10):
        X = {k: rng.randrange(1, P) for k in rng.sample(range(n), 4)}
        x = signal_mod(X, n, w, P)
        got, ok, _ = sparse_dft(lambda j: x[j], (8, 7, 17), 4, w=w, p=P)
        assert ok and signal_mod(got, n, w, P) == x


def test_edge_cases():
    # zero signal
    got, ok, _ = sparse_dft(lambda j: 0, (8, 7, 17), 3, w=root(P, 3, 952), p=P)
    assert ok and got == {}
    # n = 1 and n = 2
    got, ok, _ = sparse_dft(lambda j: 5, (1,), 1, w=1, p=17)
    assert ok and got == {0: 5}
    got, ok, _ = sparse_dft(lambda j: (3, 1)[j], (2,), 2, w=16, p=17)
    assert ok and got == {0: 4, 1: 2}
    # constant signal: one frequency, X_0 = n c
    got, ok, _ = sparse_dft(lambda j: 2, (8, 7, 17), 2, w=root(P, 3, 952), p=P)
    assert ok and got == {0: 2 * 952}
    # impulse: flat spectrum, not sparse; nothing wrong is reported
    x = [1] + [0] * 951
    got, ok, _ = sparse_dft(lambda j: x[j], (8, 7, 17), 3, w=root(P, 3, 952), p=P)
    assert not ok and all(v == 1 for v in got.values())
    # complex zero and a single tone
    got, ok, _ = sparse_dft(lambda j: 0j, (7, 8, 9), 2)
    assert ok and got == {}
    got, ok, _ = sparse_dft(lambda j: cmath.exp(2j * math.pi * 100 * j / 504), (7, 8, 9), 1)
    assert ok and set(got) == {100} and abs(got[100] - 504) < 1e-9


def test_bad_parameters():
    with pytest.raises(ValueError):
        sparse_dft(lambda j: 0, (4, 6), 1, w=root(P, 3, 8), p=P)
    with pytest.raises(ValueError):
        sparse_dft(lambda j: 0, (4, 3), 1, w=pow(2, 2, 13), p=13)  # order 6, not 12
