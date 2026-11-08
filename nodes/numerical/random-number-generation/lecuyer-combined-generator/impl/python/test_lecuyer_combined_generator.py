# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lecuyer-combined-generator/. The authors are listed in prov/9FJDDG.jsonl.

import math
from fractions import Fraction

import pytest

from lecuyer_combined_generator import (
    MRG,
    MRG32K3A_M1,
    MRG32K3A_M2,
    CombinedMRG,
    equivalent_mrg,
    lecuyer1988,
    lecuyer1988_next,
    mrg32k3a,
    mrg_is_primitive,
    state_period,
)


def test_lecuyer1988_multipliers_are_primitive_roots_and_period():
    # L'Ecuyer (1988): m1 = 2147483563, a1 = 40014; m2 = 2147483399, a2 = 40692.
    assert mrg_is_primitive(2147483563, [40014])
    assert mrg_is_primitive(2147483399, [40692])
    assert math.gcd(2147483562, 2147483398) == 2
    period = math.lcm(2147483562, 2147483398)
    assert period == 2305842648436451838  # about 2.3 * 10^18


def test_lecuyer1988_outputs_in_range():
    c1, c2 = lecuyer1988(1, 1)
    for _ in range(1000):
        z = lecuyer1988_next(c1, c2)
        assert 1 <= z <= 2147483562


def test_mrg32k3a_components_have_maximal_period():
    # Both characteristic polynomials are primitive, so each period is m^3 - 1.
    assert mrg_is_primitive(MRG32K3A_M1, [0, 1403580, -810728])
    assert mrg_is_primitive(MRG32K3A_M2, [527612, 0, -1370589])
    g = math.gcd(MRG32K3A_M1**3 - 1, MRG32K3A_M2**3 - 1)
    assert g == 2
    rho = (MRG32K3A_M1**3 - 1) * (MRG32K3A_M2**3 - 1) // 2
    assert 2**190 < rho < 2**191  # L'Ecuyer (1999): period about 2^191


def test_mrg32k3a_first_values_and_range():
    g = mrg32k3a()
    zs = [g.next_z() for _ in range(3)]
    # Exact integer arithmetic from the all-12345 seed (the RngStreams default seed).
    assert zs == [545508589, 1368065410, 1327943761]
    assert abs(545508589 / (MRG32K3A_M1 + 1) - 0.12701112204657714) < 1e-15
    g = mrg32k3a()
    for _ in range(2000):
        u = g.uniform()
        assert 0.0 < u < 1.0


def test_combination_equals_single_mrg_modulo_product():
    # Small components with prime moduli: the exact combination w_n is m X_n where
    # X_n follows one MRG modulo m = m1 m2 (Chinese remainder theorem).
    comps = [MRG(31, [3, 0, 5], [1, 2, 3]), MRG(29, [0, 2, 7], [4, 0, 1])]
    deltas = [1, -1]
    m, coeffs, weights = equivalent_mrg(comps, deltas)
    assert m == 31 * 29
    big = MRG(m, coeffs, [sum(wt * c.state[i] for wt, c in zip(weights, comps)) % m for i in range(3)])
    g = CombinedMRG(comps, deltas, denominator_plus_one=False)
    for _ in range(2000):
        z = g.next_z()
        w = g.exact_w()
        x = big.next()
        assert Fraction(x, m) == w
        # With deltas (1, -1): z/m1 - w = x2 (1/m2 - 1/m1) modulo 1, a small shift.
        x2 = g.last_x[1]
        diff = Fraction(z, 31) - w
        assert (diff - Fraction(x2 * (31 - 29), 31 * 29)) % 1 == 0


def test_combined_period_is_lcm_of_components():
    # LCG components with primitive roots: 3 modulo 31 and 2 modulo 29.
    assert mrg_is_primitive(31, [3]) and mrg_is_primitive(29, [2])
    assert state_period(MRG(31, [3], [1])) == 30
    assert state_period(MRG(29, [2], [5])) == 28
    g = CombinedMRG([MRG(31, [3], [1]), MRG(29, [2], [5])], [1, -1], denominator_plus_one=False)
    seen = {}
    n = 0
    while True:
        key = (tuple(g.comp[0].state), tuple(g.comp[1].state))
        if key in seen:
            break
        seen[key] = n
        g.next_z()
        n += 1
    assert n - seen[key] == math.lcm(30, 28) == 420


def test_non_primitive_detected():
    assert not mrg_is_primitive(31, [1])  # z - 1: a = 1 is not a primitive root
    assert not mrg_is_primitive(31, [5])  # 5 has order 3 modulo 31
    assert state_period(MRG(31, [5], [1])) == 3


def test_chi_square_of_mrg32k3a():
    g = mrg32k3a((1, 2, 3, 4, 5, 6))
    counts = [0] * 16
    n = 16000
    for _ in range(n):
        counts[int(g.uniform() * 16)] += 1
    chi2 = sum((c - n / 16) ** 2 / (n / 16) for c in counts)
    assert chi2 < 37.70  # 0.999 quantile, 15 degrees of freedom


def test_edge_cases():
    with pytest.raises(ValueError):
        MRG(31, [3], [0])  # the zero state is a fixed point
    with pytest.raises(ValueError):
        MRG(31, [3, 1], [1])
    with pytest.raises(ValueError):
        equivalent_mrg([MRG(6, [5], [1]), MRG(4, [3], [1])], [1, 1])
    # largest seed values just below the moduli
    g = mrg32k3a((MRG32K3A_M1 - 1,) * 3 + (MRG32K3A_M2 - 1,) * 3)
    for _ in range(100):
        assert 0 <= g.next_z() < MRG32K3A_M1
