# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ftcs-method/. The authors are listed in prov/RYE9V7.jsonl.

import math
import random
from fractions import Fraction

import pytest

from ftcs_method import amplification_factor, ftcs_method, mesh_ratio


def sine_grid(big_j, k=1):
    u = [math.sin(k * math.pi * j / big_j) for j in range(big_j + 1)]
    u[0] = u[-1] = 0.0
    return u


def max_error(big_j, r, t_end):
    dx = 1 / big_j
    dt = r * dx * dx
    n = round(t_end / dt)
    u = ftcs_method(sine_grid(big_j), 1.0, dx, dt, n)
    t = n * dt
    return max(abs(u[j] - math.exp(-math.pi ** 2 * t) * math.sin(math.pi * j / big_j))
               for j in range(big_j + 1))


def test_worked_example():
    u = sine_grid(5)
    rows = []
    for _ in range(3):
        u = ftcs_method(u, 1.0, 0.2, 0.01, 1)
        rows.append([round(u[1], 6), round(u[2], 6)])
    assert rows == [[0.531657, 0.860239], [0.480888, 0.778093], [0.434967, 0.703792]]


def test_discrete_mode_is_eigenvector():
    big_j, r = 16, 0.4
    for k in (1, 3, 15):
        u = ftcs_method(sine_grid(big_j, k), 1.0, 1 / big_j, r / big_j ** 2, 25)
        g = amplification_factor(r, k * math.pi / big_j)
        for j in range(big_j + 1):
            assert abs(u[j] - g ** 25 * math.sin(k * math.pi * j / big_j)) < 1e-12


def test_second_order_in_space_with_fixed_ratio():
    e = [max_error(big_j, 0.25, 0.1) for big_j in (10, 20, 40)]
    p = [math.log2(e[i] / e[i + 1]) for i in range(2)]
    assert all(abs(q - 2) < 0.02 for q in p)


def test_fourth_order_when_ratio_is_one_sixth():
    e = [max_error(big_j, 1 / 6, 0.1) for big_j in (10, 20, 40)]
    p = [math.log2(e[i] / e[i + 1]) for i in range(2)]
    assert all(abs(q - 4) < 0.02 for q in p)


def test_maximum_principle_random_exact():
    rng = random.Random(1928)
    for _ in range(500):
        big_j = rng.randint(1, 9)
        r = Fraction(rng.randint(0, 50), 100)  # r in [0, 1/2]
        u0 = [Fraction(rng.randint(-20, 20), rng.randint(1, 5)) for _ in range(big_j + 1)]
        u = ftcs_method(u0, r, Fraction(1), Fraction(1), rng.randint(0, 6))
        assert max(u) <= max(u0) and min(u) >= min(u0)
        assert u[0] == u0[0] and u[-1] == u0[-1]


def test_stable_at_one_half_unstable_just_above():
    big_j = 20
    u0 = [s + 1e-10 * (-1) ** j for j, s in enumerate(sine_grid(big_j))]
    u0[0] = u0[-1] = 0.0
    dx = 1 / big_j
    ok = ftcs_method(u0, 1.0, dx, 0.5 * dx * dx, 400)
    bad = ftcs_method(u0, 1.0, dx, 0.52 * dx * dx, 385)
    assert max(map(abs, ok)) < 0.01
    assert max(map(abs, bad)) > 1.0


def test_time_dependent_boundary_linear_steady_state():
    # u = x + 1 is a steady solution: the scheme keeps it exactly
    u0 = [Fraction(j, 4) + 1 for j in range(5)]
    u = ftcs_method(u0, Fraction(1), Fraction(1, 4), Fraction(1, 64), 7,
                    left=lambda t: Fraction(1), right=lambda t: Fraction(2))
    assert u == u0
    v = ftcs_method([0.0, 0.0, 0.0], 1.0, 0.5, 0.1, 1, left=lambda t: t, right=lambda t: 2 * t)
    assert v[0] == 0.1 and v[2] == 0.2


def test_edges_and_ratio():
    assert ftcs_method([1.0, 2.0, 3.0], 1.0, 0.1, 0.001, 0) == [1.0, 2.0, 3.0]
    assert ftcs_method([4.0, 5.0], 1.0, 0.1, 0.001, 3) == [4.0, 5.0]
    assert mesh_ratio(2, Fraction(1, 10), Fraction(1, 400)) == Fraction(1, 2)
    with pytest.raises(ValueError):
        ftcs_method([1.0], 1.0, 0.1, 0.001, 1)
