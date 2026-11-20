# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multifidelity-monte-carlo/. The authors are listed in prov/SQG1XP.jsonl.
import math
import random

import pytest

from multifidelity_monte_carlo import (
    check_conditions,
    integer_counts,
    mfmc,
    mfmc_allocation,
    mfmc_estimate,
    mfmc_variance,
    optimal_variance,
    pilot_statistics,
)

E = math.e
# f_1 = exp(z), f_2 = 1 + z + z^2 / 2, f_3 = 1 + z with z uniform on [0, 1]
MODELS = [math.exp, lambda z: 1.0 + z + z * z / 2.0, lambda z: 1.0 + z]
W = [1.0, 0.01, 0.001]
MEAN = E - 1.0
SIG = [math.sqrt((E * E - 1) / 2 - (E - 1) ** 2), math.sqrt(17.0 / 90.0), math.sqrt(1.0 / 12.0)]
RHO = [1.0, ((2 - E / 2) / 3) / (SIG[0] * SIG[1]), ((3 - E) / 2) / (SIG[0] * SIG[2])]


def draw(rng):
    return rng.random()


def test_exact_statistics_of_the_example():
    assert abs(SIG[0] - 0.4919711) < 1e-7
    assert abs(RHO[1] - 0.9990758) < 1e-7
    assert abs(RHO[2] - 0.9918268) < 1e-7


def test_allocation_of_the_example():
    m, alpha = mfmc_allocation(SIG, RHO, W, 100.0)
    assert abs(m[0] - 49.7711) < 1e-3
    assert abs(m[1] - 1391.077) < 1e-2
    assert abs(m[2] - 36318.12) < 1e-1
    assert abs(sum(wi * mi for wi, mi in zip(W, m)) - 100.0) < 1e-9
    assert abs(alpha[1] - 1.130928) < 1e-6 and abs(alpha[2] - 1.690309) < 1e-6
    assert abs(mfmc_variance(SIG, RHO, m, alpha) - optimal_variance(SIG, RHO, W, 100.0)) < 1e-15
    assert abs(optimal_variance(SIG, RHO, W, 100.0) - 1.805113e-5) < 1e-10


def test_allocation_beats_a_brute_force_grid_with_two_models():
    sig, rho, w, p = SIG[:2], RHO[:2], [1.0, 0.05], 10.0
    m, alpha = mfmc_allocation(sig, rho, w, p)
    best = mfmc_variance(sig, rho, m, alpha)
    for k in range(1, 200):
        m1 = k * p / (200 * w[0])
        m2 = (p - w[0] * m1) / w[1]
        if m2 < m1:
            continue
        for a in (alpha[1] * 0.9, alpha[1], alpha[1] * 1.1):
            assert mfmc_variance(sig, rho, [m1, m2], [1.0, a]) >= best - 1e-15


def test_estimator_is_unbiased_with_the_stated_variance():
    m, alpha = mfmc_allocation(SIG, RHO, W, 5.0)
    mi = integer_counts(m)
    assert mi[0] >= 2 and mi[0] <= mi[1] <= mi[2]
    rng = random.Random(42)
    reps = 300
    vals = [mfmc_estimate(MODELS, draw, mi, alpha, rng) for _ in range(reps)]
    mean = sum(vals) / reps
    var = sum((v - mean) ** 2 for v in vals) / (reps - 1)
    v_theory = mfmc_variance(SIG, RHO, mi, alpha)
    assert abs(mean - MEAN) < 4 * math.sqrt(v_theory / reps)
    assert abs(var / v_theory - 1.0) < 4 * math.sqrt(2.0 / (reps - 1))


def test_full_method_with_pilot_beats_plain_monte_carlo():
    rng = random.Random(9)
    res = mfmc(MODELS, W, 20.0, draw, rng, n_pilot=200)
    assert abs(res["estimate"] - MEAN) < 4 * math.sqrt(res["variance"])
    plain_variance = SIG[0] ** 2 / 20.0  # 20 runs of f_1 cost the same budget
    assert res["variance"] < plain_variance / 10


def test_pilot_statistics_are_close_to_the_exact_ones():
    sig, rho = pilot_statistics(MODELS, draw, 2000, random.Random(1))
    assert abs(sig[0] - SIG[0]) < 0.03
    assert abs(rho[2] - RHO[2]) < 0.002


def test_conditions_reject_a_model_that_is_too_expensive():
    with pytest.raises(ValueError):
        # w_2 / w_3 = 0.01 is below (rho_2^2 - rho_3^2) / rho_3^2 = 0.01467
        check_conditions(RHO, [1.0, 0.01, 1.0])
    with pytest.raises(ValueError):
        check_conditions([1.0, 0.5, 0.9], W)
