# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/undetected-error-probability/. The authors are listed in prov/SD1VWV.jsonl.

from fractions import Fraction

from undetected_error_probability import (
    deg, dual_weight_distribution, is_proper, macwilliams, monte_carlo, p_ud, p_ud_dual, weight_distribution,
    worst_p,
)

HAMMING = 0xB  # x^3 + x + 1, the cyclic [7, 4] Hamming code
SMBUS = 0x107  # CRC-8/SMBUS
ARC = 0x18005  # CRC-16/ARC
POOR = 0x101  # x^8 + 1


def test_hamming_7_4() -> None:
    # Lin and Costello, Section 3.6: A(z) = 1 + 7z^3 + 7z^4 + z^7 and
    # P_u(E) = 7p^3(1 - p)^4 + 7p^4(1 - p)^3 + p^7.
    a = weight_distribution(HAMMING, 7)
    assert a == [1, 0, 0, 7, 7, 0, 0, 1]
    assert dual_weight_distribution(HAMMING, 7) == [1, 0, 0, 0, 7, 0, 0, 0]  # simplex code
    for p in (Fraction(1, 100), Fraction(1, 7), Fraction(1, 2)):
        want = 7 * p**3 * (1 - p) ** 4 + 7 * p**4 * (1 - p) ** 3 + p**7
        assert p_ud(a, 7, p) == want


def test_dual_formula_equals_direct_sum() -> None:
    for g, n in ((HAMMING, 15), (SMBUS, 9), (SMBUS, 20), (POOR, 22), (ARC, 29)):
        r = deg(g)
        a = weight_distribution(g, n)
        b = dual_weight_distribution(g, n)
        assert sum(a) == 2 ** (n - r) and sum(b) == 2**r
        assert macwilliams(b, n, 2**r) == a
        for p in (Fraction(1, 1000), Fraction(1, 33), Fraction(3, 10), Fraction(1, 2)):
            assert p_ud(a, n, p) == p_ud_dual(b, n, r, p)


def test_value_at_one_half() -> None:
    # At p = 1/2 every pattern is equally likely: P_ud = (2^k - 1) / 2^n.
    for g, n in ((HAMMING, 7), (SMBUS, 64), (ARC, 200), (POOR, 64)):
        r = deg(g)
        b = dual_weight_distribution(g, n)
        assert p_ud_dual(b, n, r, Fraction(1, 2)) == Fraction(2 ** (n - r) - 1, 2**n)


def test_improper_code() -> None:
    # x^8 + 1 at n = 64 has 8 * C(8, 2) = 224 codewords of weight 2, so P_ud
    # rises far above 2^-8.
    b = dual_weight_distribution(POOR, 64)
    assert macwilliams(b, 64, 256)[:3] == [1, 0, 224]
    v, p = worst_p(b, 64, 8)
    assert v > 0.034 and 0.03 < p < 0.04
    assert v > 8 * 2**-8 and not is_proper(b, 64, 8)
    # CRC-16/ARC shortened to n = 128 bits is improper too: exact value at p = 7/200.
    b = dual_weight_distribution(ARC, 128)
    assert p_ud_dual(b, 128, 16, Fraction(7, 200)) > Fraction(3, 2**16)
    assert not is_proper(b, 128, 16)
    # The cyclic Hamming codes of length 7 and 15 are proper.
    for g, n in ((HAMMING, 7), (0x13, 15)):  # 0x13 = x^4 + x + 1
        assert is_proper(dual_weight_distribution(g, n), n, deg(g))


def test_monte_carlo_with_fixed_seed() -> None:
    trials = 100_000
    for g, n, p in ((POOR, 64, 1 / 32), (SMBUS, 64, 0.2), (HAMMING, 7, 0.1)):
        r = deg(g)
        exact = p_ud_dual(dual_weight_distribution(g, n), n, r, p)
        got = monte_carlo(g, n, p, trials, seed=1982)
        sigma = (exact * (1 - exact) / trials) ** 0.5
        assert abs(got - exact) < 5 * sigma, (hex(g), got, exact)
