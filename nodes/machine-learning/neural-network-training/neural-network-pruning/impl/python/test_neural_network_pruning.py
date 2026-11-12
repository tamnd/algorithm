# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neural-network-pruning/. The authors are listed in prov/8KRCTK.jsonl.

import random
from fractions import Fraction as F

from neural_network_pruning import (
    constrained_minimizer,
    inverse,
    magnitude_mask,
    magnitude_saliency,
    obd_saliency,
    obs_prune,
    obs_saliency,
    obs_update,
    quad_loss,
)

H = [[F(4), F(2), F(0)], [F(2), F(3), F(1)], [F(0), F(1), F(2)]]
W = [F(1, 2), F(-1), F(3, 4)]


def random_spd(n, rng):
    a = [[F(rng.randint(-3, 3)) for _ in range(n)] for _ in range(n)]
    return [[sum(a[i][k] * a[j][k] for k in range(n)) + (1 if i == j else 0) for j in range(n)] for i in range(n)]


def test_inverse_is_exact():
    hinv = inverse(H)
    for i in range(3):
        for j in range(3):
            assert sum(H[i][k] * hinv[k][j] for k in range(3)) == (1 if i == j else 0)


def test_obs_predicted_increase_equals_actual_increase_exactly():
    rng = random.Random(1)
    for h, w in [(H, W)] + [(random_spd(5, rng), [F(rng.randint(-9, 9), 4) for _ in range(5)]) for _ in range(10)]:
        hinv = inverse(h)
        sal = obs_saliency(hinv, w)
        for q in range(len(w)):
            new = [a + b for a, b in zip(w, obs_update(hinv, w, q))]
            assert new[q] == 0
            assert quad_loss(h, w, new) == sal[q]
            # No other point with w_q = 0 has a smaller loss.
            assert constrained_minimizer(h, w, [q]) == new


def test_obd_is_the_increase_without_compensation_and_obs_is_never_larger():
    rng = random.Random(2)
    for _ in range(10):
        h = random_spd(4, rng)
        w = [F(rng.randint(-9, 9), 3) for _ in range(4)]
        hinv = inverse(h)
        obd, obs = obd_saliency(h, w), obs_saliency(hinv, w)
        for q in range(4):
            only_q = list(w)
            only_q[q] = F(0)
            assert quad_loss(h, w, only_q) == obd[q]
            assert obs[q] <= obd[q]


def test_diagonal_hessian_makes_obs_equal_obd():
    h = [[F(3), 0, 0], [0, F(1, 2), 0], [0, 0, F(5)]]
    w = [F(1), F(-2), F(1, 3)]
    hinv = inverse(h)
    assert obs_saliency(hinv, w) == obd_saliency(h, w)
    dw = obs_update(hinv, w, 1)
    assert dw == [0, F(2), 0]


def test_iterated_obs_reaches_the_constrained_minimizer():
    rng = random.Random(3)
    for _ in range(5):
        h = random_spd(6, rng)
        w = [F(rng.randint(-9, 9), 2) for _ in range(6)]
        new, pruned, gains = obs_prune(h, w, 3)
        assert sorted(pruned) == sorted(set(pruned))
        assert all(new[q] == 0 for q in pruned)
        assert new == constrained_minimizer(h, w, pruned)
        assert quad_loss(h, w, new) == sum(gains)


def test_first_obs_choice_is_the_best_single_weight():
    rng = random.Random(4)
    for _ in range(10):
        h = random_spd(4, rng)
        w = [F(rng.randint(-9, 9), 2) for _ in range(4)]
        _, pruned, gains = obs_prune(h, w, 1)
        best = min(quad_loss(h, w, constrained_minimizer(h, w, [q])) for q in range(4))
        assert gains[0] == best


def test_float_version_agrees():
    hf = [[float(v) for v in row] for row in H]
    wf = [float(v) for v in W]
    hinv = inverse(hf)
    sal = obs_saliency(hinv, wf)
    for q in range(3):
        new = [a + b for a, b in zip(wf, obs_update(hinv, wf, q))]
        assert abs(quad_loss(hf, wf, new) - sal[q]) < 1e-12


def test_magnitude_mask():
    w = [0.3, -0.1, 2.0, -0.05, 0.7, 0.0]
    assert magnitude_saliency(w)[1] == 0.1
    mask = magnitude_mask(w, 0.5)
    assert mask == [1, 0, 1, 0, 1, 0]
    assert magnitude_mask(w, 0) == [1] * 6
