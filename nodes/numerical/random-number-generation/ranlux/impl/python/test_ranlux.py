# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ranlux/. The authors are listed in prov/WG0HW1.jsonl.

from itertools import product
from math import gcd

from ranlux import (
    Ranlux,
    SubtractWithBorrow,
    ranlux24,
    ranlux24_base,
    ranlux48,
    ranlux48_base,
)


def _nth(gen, n: int) -> int:
    f = gen.step if hasattr(gen, "step") else gen.next
    for _ in range(n - 1):
        f()
    return f()


def test_cpp_standard_10000th_values() -> None:
    # The C++ standard ([rand.predef]) requires these values for the 10000th call
    # of a default-constructed engine; a C++ library run gives the same.
    assert _nth(ranlux24_base(), 10000) == 7937952
    assert _nth(ranlux48_base(), 10000) == 61839128582725
    assert _nth(ranlux24(), 10000) == 9901578
    assert _nth(ranlux48(), 10000) == 249142670248501


def test_first_values() -> None:
    # libc++ std::ranlux24 and std::ranlux24_base agree on the first 23 values.
    g, h = ranlux24_base(), ranlux24()
    first = [g.step() for _ in range(5)]
    assert first == [15039276, 16323925, 14283486, 7150092, 68089]
    assert [h.next() for _ in range(5)] == first


def test_three_term_relation_of_swb() -> None:
    # x_n - x_(n-s) + x_(n-r) = b c_n - c_(n-1), which is -1, 0, b - 1 or b:
    # consecutive SWB outputs lie on a few hyperplanes, the reason for discarding.
    g = ranlux24_base()
    xs = [g.step() for _ in range(5000)]
    b = 1 << 24
    vals = {xs[n] - xs[n - 10] + xs[n - 24] for n in range(24, len(xs))}
    assert vals <= {-1, 0, b - 1, b}


def _order(g: int, m: int) -> int:
    if m == 1:
        return 1
    k, v = 1, g % m
    while v != 1:
        v, k = v * g % m, k + 1
    return k


def _k_value(xs, c, b, r, s):
    # K_n = A_s - A_r - c_(n-1), with A_r the last r values and A_s the last s values,
    # read as base-b numbers with the oldest value as the lowest digit.
    a_r = sum(x * b**k for k, x in enumerate(xs))
    a_s = sum(x * b**k for k, x in enumerate(xs[r - s :]))
    return a_s - a_r - c


def test_period_theorem_exhaustive_small() -> None:
    # Every state of every SWB with b^r <= 700: K_(n+1) b = K_n - m x_n, cycles have
    # -m <= K <= 0, and the cycle length is the order of b modulo m / gcd(K, m).
    for b, r in product((2, 3, 4, 5), range(2, 6)):
        if b**r > 700:
            continue
        for s in range(1, r):
            m = b**r - b**s + 1
            for xs, c in product(product(range(b), repeat=r), (0, 1)):
                g = SubtractWithBorrow(1, s, r)
                g.b, g.x, g.i, g.c = b, list(xs), 0, c
                seen, state = {}, (xs, c)
                while state not in seen:
                    seen[state] = len(seen)
                    k = _k_value(*state, b, r, s)
                    x = g.step()
                    state = (tuple(g.x[g.i :] + g.x[: g.i]), g.c)
                    assert _k_value(*state, b, r, s) * b == k - m * x
                length = len(seen) - seen[state]
                k = _k_value(*state, b, r, s)
                assert -m <= k <= 0
                expect = 1 if k in (0, -m) else _order(b, m // gcd(k, m))
                assert length == expect


def _trial_factor(n: int) -> dict[int, int]:
    f, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            f[p], n = f.get(p, 0) + 1, n // p
        p += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def test_ranlux_modulus_is_prime_and_period_bounds() -> None:
    m = 2**576 - 2**240 + 1  # b^r - b^s + 1 for (2^24, 24, 10) and for (2^48, 12, 5)
    assert m == (2**24) ** 24 - (2**24) ** 10 + 1 == (2**48) ** 12 - (2**48) ** 5 + 1
    # Pocklington: F = 2^240 lcm(2^48 - 1, 2^56 - 1) divides m - 1, F^2 > m, and for
    # each prime q dividing F a base a with a^(m-1) = 1 and gcd(a^((m-1)/q) - 1, m) = 1.
    lcm = (2**48 - 1) * (2**56 - 1) // gcd(2**48 - 1, 2**56 - 1)
    fac = _trial_factor(lcm)
    fac[2] = 240
    f = 2**240 * lcm
    assert (m - 1) % f == 0 and f * f > m
    for q in fac:
        for a in range(2, 100):
            assert pow(a, m - 1, m) == 1
            if gcd(pow(a, (m - 1) // q, m) - 1, m) == 1:
                break
        else:
            raise AssertionError(q)
    # The period ord_m(2^24) divides N = (m - 1)/48, and q^e | ord for each known q^e || N.
    n = (m - 1) // 48
    b = 2**24
    assert pow(b, n, m) == 1
    lower = 1
    for q in fac:
        e, t = 0, n
        while t % q == 0:
            t, e = t // q, e + 1
        assert pow(b, n // q, m) != 1
        lower *= q**e
    assert lower > 2**333 and n > 2**570


def test_luxury_discards() -> None:
    # With p = q the decimated generator is the base generator itself.
    a, b = ranlux24_base(5), Ranlux(ranlux24_base(5), 24, 24)
    assert [a.step() for _ in range(100)] == [b.next() for _ in range(100)]
    # With p = 2q, the outputs are the base outputs with every other block of q removed.
    base = ranlux24_base(5)
    ref = [base.step() for _ in range(96)]
    d = Ranlux(ranlux24_base(5), 48, 24)
    assert [d.next() for _ in range(48)] == ref[0:24] + ref[48:72]


def test_uniformity_of_ranlux24() -> None:
    g = ranlux24(12345)
    counts = [0] * 16
    for _ in range(4000):
        counts[g.next() >> 20] += 1
    chi2 = sum((k - 250) ** 2 / 250 for k in counts)
    assert chi2 < 37.70  # the 0.999 quantile of chi-square with 15 degrees of freedom
