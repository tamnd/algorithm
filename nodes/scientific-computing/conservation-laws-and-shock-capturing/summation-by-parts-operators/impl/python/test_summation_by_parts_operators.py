# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/summation-by-parts-operators/. The authors are listed in prov/SK4AFB.jsonl.

import math
import random
from fractions import Fraction as Fr

import pytest

from summation_by_parts_operators import (
    apply, energy_rate, q_matrix, sat_advection_rhs, sbp21, sbp42, solve_advection,
)


@pytest.mark.parametrize("op,n", [(sbp21, 2), (sbp21, 7), (sbp42, 8), (sbp42, 15)])
def test_sbp_property_holds_exactly(op, n):
    H, D = op(n, Fr(1, n))
    Q = q_matrix(H, D)
    for i in range(n + 1):
        for j in range(n + 1):
            b = -1 if i == j == 0 else 1 if i == j == n else 0
            assert Q[i][j] + Q[j][i] == b
    assert all(w > 0 for w in H)
    assert sum(H) == 1                                        # H integrates constants exactly


@pytest.mark.parametrize("op,n,p_in,p_bd", [(sbp21, 9, 2, 1), (sbp42, 14, 4, 2)])
def test_accuracy_inside_and_at_the_boundary(op, n, p_in, p_bd):
    H, D = op(n, Fr(1, n))
    x = [Fr(i, n) for i in range(n + 1)]
    nb = 1 if op is sbp21 else 4
    for p in range(p_in + 1):
        Du = apply(D, [xi ** p for xi in x])
        for i in range(n + 1):
            exact = p * x[i] ** (p - 1) if p else 0
            if i < nb or i > n - nb:
                assert (Du[i] == exact) == (p <= p_bd), (p, i)
            else:
                assert Du[i] == exact


def test_hand_example():
    H, D = sbp21(2, Fr(1, 2))
    assert H == [Fr(1, 4), Fr(1, 2), Fr(1, 4)]
    u = [Fr(1), Fr(2), Fr(0)]
    assert sat_advection_rhs(H, D, u, 1, 0) == [-6, 1, 4]
    assert energy_rate(H, D, u, 1, 0) == -1


@pytest.mark.parametrize("op,n", [(sbp21, 6), (sbp42, 11)])
def test_energy_identity_with_sat_is_exact(op, n):
    rng = random.Random(n)
    h = Fr(1, n)
    H, D = op(n, h)
    for tau in (Fr(1, 2), Fr(1), Fr(3)):
        for _ in range(5):
            u = [Fr(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(n + 1)]
            a = Fr(rng.randint(1, 4))
            rate = energy_rate(H, D, u, a, 0, tau)
            assert rate == -a * u[-1] ** 2 - a * (2 * tau - 1) * u[0] ** 2
            assert rate <= 0


def test_too_weak_penalty_can_create_energy():
    H, D = sbp21(4, Fr(1, 4))
    u = [Fr(1), 0, 0, 0, 0]
    assert energy_rate(H, D, u, 1, 0, Fr(1, 4)) > 0


@pytest.mark.parametrize("op,p_min", [(sbp21, 1.9), (sbp42, 2.85)])
def test_global_order_is_boundary_order_plus_one(op, p_min):
    errs = []
    for n in (20, 40, 80):
        h = 1.0 / n
        u = solve_advection(op, n, 1.0, 0.5, 0.5, lambda x: math.sin(2 * math.pi * x),
                            lambda t: math.sin(-2 * math.pi * t))
        H, _ = op(n, h)
        errs.append(math.sqrt(sum(float(w) * (x - math.sin(2 * math.pi * (i * h - 0.5))) ** 2
                                  for i, (w, x) in enumerate(zip(H, u)))))
    assert math.log2(errs[1] / errs[2]) > p_min, errs


def test_rejects_small_grids():
    with pytest.raises(ValueError):
        sbp42(5, 0.1)
