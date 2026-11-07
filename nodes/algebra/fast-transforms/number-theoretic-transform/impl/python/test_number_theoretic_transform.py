# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/number-theoretic-transform/. The authors are listed in prov/7AWXWS.jsonl.

import random

import pytest

from number_theoretic_transform import NTT_PRIMES, multiply_exact, multiply_mod, ntt, root_of_unity

# (prime, primitive root): 3 for 17 and 998244353, 5 for 97.
PRIMES = [(17, 3), (97, 5), (998244353, 3)]


def naive_dft(x: list[int], w: int, p: int) -> list[int]:
    n = len(x)
    return [sum(x[j] * pow(w, j * k, p) for j in range(n)) % p for k in range(n)]


def schoolbook(a: list[int], b: list[int], p: int | None = None) -> list[int]:
    c = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            c[i + j] += u * v
    return c if p is None else [v % p for v in c]


def max_len(p: int) -> int:
    n = 1
    while (p - 1) % (2 * n) == 0 and n < 64:
        n *= 2
    return n


def test_roots() -> None:
    for p, g in PRIMES + [(q, h) for q, h, _ in NTT_PRIMES]:
        n = max_len(p)
        while n >= 1:
            w = root_of_unity(n, p, g)
            assert pow(w, n, p) == 1
            if n > 1:
                assert pow(w, n // 2, p) == p - 1
            n //= 2
    with pytest.raises(ValueError):
        root_of_unity(3, 17, 3)


def test_examples() -> None:
    assert root_of_unity(4, 17, 3) == 13
    x = [1, 2, 3, 0]
    ntt(x, 13, 17)
    assert x == [6, 7, 2, 6]
    assert multiply_mod([1, 2, 3], [4, 5], 17) == [4, 13, 5, 15]
    assert multiply_mod([1, 2, 3], [4, 5]) == [4, 13, 22, 15]
    assert multiply_exact([1, 2, 3], [4, 5]) == [4, 13, 22, 15]


def test_edges() -> None:
    for p, g in PRIMES:
        for n in (1, 2, 4, 8, 16):
            w = root_of_unity(n, p, g)
            zeros = [0] * n
            ntt(zeros, w, p)
            assert zeros == [0] * n
            for pos in range(n):
                imp = [int(j == pos) for j in range(n)]
                ntt(imp, w, p)
                assert imp == [pow(w, pos * k, p) for k in range(n)]
            const = [3] * n
            ntt(const, w, p)
            assert const == [3 * n % p] + [0] * (n - 1)
        assert multiply_mod([5], [7], p, g) == [35 % p]
        assert multiply_mod([0, 0, 0], [1, 2], p, g) == [0, 0, 0, 0]
        assert multiply_mod([1], [3, 1, 4], p, g) == [3, 1, 4]
    assert multiply_mod([], [1, 2]) == []
    assert multiply_exact([2, -3], [-4, 5]) == [-8, 22, -15]


def test_errors() -> None:
    for n in (0, 3, 6, 12):
        with pytest.raises(ValueError):
            ntt([1] * n, 1, 17)
    # Length 32 does not divide 16 = 17 - 1.
    with pytest.raises(ValueError):
        multiply_mod([1] * 10, [1] * 10, 17, 3)


def test_random_against_naive() -> None:
    rng = random.Random(1971)
    for _ in range(500):
        p, g = PRIMES[rng.randrange(len(PRIMES))]
        n = 1 << rng.randint(0, max_len(p).bit_length() - 1)
        w = root_of_unity(n, p, g)
        x = [rng.randrange(p) for _ in range(n)]
        y = list(x)
        ntt(y, w, p)
        assert y == naive_dft(x, w, p)
        ntt(y, pow(w, -1, p), p)
        n_inv = pow(n, -1, p)
        assert [v * n_inv % p for v in y] == x


def test_random_multiply() -> None:
    rng = random.Random(1975)
    for _ in range(200):
        p, g = PRIMES[rng.randrange(len(PRIMES))]
        lim = max_len(p)
        la = rng.randint(1, lim // 2)
        lb = rng.randint(1, lim // 2)
        a = [rng.randrange(p) for _ in range(la)]
        b = [rng.randrange(p) for _ in range(lb)]
        assert multiply_mod(a, b, p, g) == schoolbook(a, b, p)


def test_exact_large_coefficients() -> None:
    rng = random.Random(1959)
    for _ in range(30):
        la, lb = rng.randint(1, 120), rng.randint(1, 120)
        a = [rng.randint(-(10**9), 10**9) for _ in range(la)]
        b = [rng.randint(-(10**9), 10**9) for _ in range(lb)]
        assert multiply_exact(a, b) == schoolbook(a, b)


def test_large_length() -> None:
    rng = random.Random(23)
    a = [rng.randrange(800) for _ in range(1500)]
    b = [rng.randrange(800) for _ in range(1500)]  # 1500 * 800^2 < p, so exact
    c = multiply_mod(a, b)
    for m in rng.sample(range(len(c)), 10):
        ref = sum(a[i] * b[m - i] for i in range(max(0, m - 1499), min(m, 1499) + 1))
        assert c[m] == ref
