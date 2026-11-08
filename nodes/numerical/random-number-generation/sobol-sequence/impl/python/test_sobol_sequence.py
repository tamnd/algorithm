# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sobol-sequence/. The authors are listed in prov/Z7GN5H.jsonl.

import random
from fractions import Fraction
from math import prod

from sobol_sequence import (
    JOE_KUO,
    MAX_DIM,
    W,
    Sobol,
    direction_table,
    is_primitive,
    polynomial,
    sobol_point,
    t_value,
)

# Points X_i * 2^32 printed by Joe and Kuo's reference program sobol.cc with the file
# new-joe-kuo-6.21201, 21 dimensions, Gray-code order.
REFERENCE = {
    1: [2147483648] * 21,
    2: [3221225472, 1073741824, 1073741824, 1073741824, 3221225472, 3221225472, 1073741824,
        3221225472, 3221225472, 3221225472, 3221225472, 3221225472, 1073741824, 1073741824,
        3221225472, 1073741824, 3221225472, 1073741824, 3221225472, 1073741824, 1073741824],
    7: [536870912, 2684354560, 1610612736, 536870912, 536870912, 1610612736, 2684354560,
        2684354560, 2684354560, 3758096384, 2684354560, 536870912, 2684354560, 1610612736,
        536870912, 536870912, 536870912, 536870912, 2684354560, 3758096384, 3758096384],
    100: [1778384896, 1107296256, 3321888768, 3120562176, 3791650816, 3187671040, 100663296,
          2046820352, 2717908992, 2986344448, 1979711488, 2919235584, 2046820352, 3657433088,
          1375731712, 2113929216, 2919235584, 3187671040, 3590324224, 1442840576, 3254779904],
    1000: [943718400, 415236096, 2227175424, 2906652672, 1203765248, 3896508416, 197132288,
           3862953984, 2151677952, 297795584, 364904448, 1094713344, 692060160, 1648361472,
           616562688, 1589641216, 3091202048, 1480589312, 4257218560, 3116367872, 2243952640],
    4095: [1048576, 4042260480, 1435500544, 3872391168, 4038066176, 338690048, 4077912064,
           1678770176, 823132160, 1058013184, 2446327808, 1380974592, 1584398336, 2232418304,
           2366636032, 1789919232, 267386880, 2616197120, 3492806656, 2238709760, 969932800],
}


def test_reference_points():
    s = Sobol(MAX_DIM)
    pts = [s.next_int() for _ in range(4096)]
    assert pts[0] == [0] * MAX_DIM
    for i, want in REFERENCE.items():
        assert pts[i] == want


def test_first_points_in_two_dimensions():
    s = Sobol(2)
    got = [s.next() for _ in range(8)]
    assert got == [[0, 0], [0.5, 0.5], [0.75, 0.25], [0.25, 0.75],
                   [0.375, 0.375], [0.875, 0.875], [0.625, 0.125], [0.125, 0.625]]


def test_gray_code_order_and_skip():
    s = Sobol(6)
    for n in range(1024):
        assert s.next_int() == sobol_point(n ^ (n >> 1), 6)
    t = Sobol(6)
    t.skip_to(777)
    u = Sobol(6)
    for _ in range(777):
        u.next_int()
    assert t.next_int() == u.next_int()


def test_polynomials_are_all_primitive_ones_in_order():
    polys = [polynomial(s, a) for s, a, _ in JOE_KUO]
    assert all(is_primitive(f) for f in polys)
    # Brute force over all polynomials of degree 1..6: the table lists every primitive one.
    every = [f for deg in range(1, 7) for f in range(1 << deg, 1 << (deg + 1)) if is_primitive(f)]
    assert polys[: len(every)] == every
    assert [sum(1 for f in every if f.bit_length() - 1 == d) for d in range(1, 7)] == [1, 1, 2, 2, 6, 6]
    # A reducible polynomial and an irreducible non-primitive one are rejected.
    assert not is_primitive(0b101)  # x^2 + 1 = (x + 1)^2
    assert not is_primitive(0b11111)  # x^4 + x^3 + x^2 + x + 1 has order 5


def test_direction_numbers_odd_and_bounded():
    for v in direction_table(MAX_DIM):
        for k in range(1, W + 1):
            m_k = v[k] >> (W - k)
            assert v[k] == m_k << (W - k)
            assert m_k % 2 == 1 and m_k < 1 << k


def test_one_dimensional_stratification():
    m = 10
    s = Sobol(MAX_DIM)
    pts = [s.next_int() for _ in range(2 << m)]
    for block in (pts[: 1 << m], pts[1 << m :]):
        for j in range(MAX_DIM):
            assert sorted(p[j] >> (W - m) for p in block) == list(range(1 << m))


def _is_net_by_counting(points, t, m, dims):
    """Count points in every elementary interval of volume 2^(t-m)."""
    from itertools import product as cart

    for ds in cart(range(m - t + 1), repeat=dims):
        if sum(ds) != m - t:
            continue
        counts = {}
        for p in points:
            key = tuple(p[j] >> (W - ds[j]) for j in range(dims))
            counts[key] = counts.get(key, 0) + 1
        if len(counts) != 1 << (m - t) or set(counts.values()) != {1 << t}:
            return False
    return True


def test_nets_by_counting_and_by_rank():
    m = 8
    s = Sobol(3)
    pts = [s.next_int() for _ in range(4 << m)]
    for b in range(4):
        block = pts[b << m : (b + 1) << m]
        assert _is_net_by_counting([p[:2] for p in block], 0, m, 2)
        assert _is_net_by_counting(block, 1, m, 3)
        assert not _is_net_by_counting(block, 0, m, 3)
    # Exact t-values from the generator matrices.
    for m in range(1, 13):
        assert t_value(2, m) == 0
    sobol_bound = {1: 0, 2: 0, 3: 1, 4: 3, 5: 5}  # sum of (degree - 1)
    for d in range(1, 6):
        for m in range(1, 11):
            assert t_value(d, m) <= sobol_bound[d]
    assert [t_value(5, m) for m in range(1, 11)] == [0, 1, 2, 2, 2, 3, 3, 3, 3, 3]


def test_integration_error_beats_monte_carlo():
    # f(x) = prod |4 x_j - 2| has integral 1 over [0,1]^5 and variance (4/3)^5 - 1 > 3.2.
    n = 1 << 12
    s = Sobol(5)
    qmc = sum(prod(abs(4 * x - 2) for x in s.next()) for _ in range(n)) / n
    assert abs(qmc - 1) < 0.005
    mc_sd = ((Fraction(4, 3) ** 5 - 1) / n) ** 0.5
    assert mc_sd > 0.027  # a plain Monte Carlo estimate has standard deviation above 0.027
    rng = random.Random(2024)
    errs = []
    for _ in range(20):
        est = sum(prod(abs(4 * rng.random() - 2) for _ in range(5)) for _ in range(1024)) / 1024
        errs.append(abs(est - 1))
    assert sum(errs) / len(errs) > 0.01


def test_bounds():
    try:
        Sobol(MAX_DIM + 1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    s = Sobol(1, bits=3)
    for _ in range(8):
        s.next_int()
    try:
        s.next_int()
    except OverflowError:
        pass
    else:
        raise AssertionError("expected OverflowError")
