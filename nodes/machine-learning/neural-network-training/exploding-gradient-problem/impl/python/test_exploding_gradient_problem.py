# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exploding-gradient-problem/. The authors are listed in prov/7ABN4Y.jsonl.

import math
import random

from exploding_gradient_problem import (log_norm_rate, power_norms, power_rate, predicted_rate,
                                        tanh_rnn)


def test_random_products_grow_at_the_predicted_rate():
    for m, s in ((8, 2.0), (4, 1.5), (8, 1.2), (16, 1.5)):
        pred = predicted_rate(m, s)
        emp = log_norm_rate(m, 2000, s, random.Random(m))
        assert pred > 0
        assert abs(emp - pred) < 0.02, (m, s, emp, pred)


def test_growth_needs_more_than_unit_scale():
    # s slightly above 1 still decays for a narrow layer; the threshold is above 1
    assert predicted_rate(4, 1.1) < 0 < predicted_rate(4, 1.2)


def test_linear_recurrence_grows_like_the_spectral_radius():
    W = [[1.1, 1.0], [0.0, 0.5]]  # eigenvalues 1.1 and 0.5
    W2 = [[1.3, -0.2], [0.8, 0.3]]  # S W S^-1 with S = [[1, 2], [1, 3]]: same eigenvalues
    for A, v in ((W, [0.3, 1.0]), (W2, [1.0, 0.0])):
        assert abs(power_rate(A, v, 400) - math.log(1.1)) < 0.005
        assert power_rate(A, v, 400) > 0
    # spectral radius 0.9 < 1: decay in the long run
    assert power_rate([[0.9, 0.0], [0.3, 0.6]], [1.0, 1.0], 400) < 0


def test_non_normal_matrix_grows_before_it_decays():
    N = power_norms([[0.9, 5.0], [0.0, 0.9]], 200)
    peak = max(range(200), key=lambda i: N[i])
    assert peak + 1 == 9 and N[peak] > 19.0  # W^9 has norm about 19.4
    assert N[199] < 1e-6  # rho = 0.9 wins in the end


def test_tanh_cliff():
    # at the unstable fixed point 0 every factor is w * tanh'(0) = 3
    h, d = tanh_rnn(3.0, 0.0, 20, 0.0)
    assert h == 0.0 and d == 3.0 ** 20
    # a tiny change of h_0 sends h_T to one of the two stable states
    hp, dp = tanh_rnn(3.0, 0.0, 20, 1e-3)
    hm, dm = tanh_rnn(3.0, 0.0, 20, -1e-3)
    assert hp > 0.99 and hm < -0.99 and dp < 1e-15 and dm < 1e-15
