# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/membership-inference-attack/. The authors are listed in prov/52KYBB.jsonl.

"""Tests of the shadow model membership attack on logistic models trained on seeded synthetic blobs."""

import math
import random
from fractions import Fraction

from mlkit import make_blobs, train_logistic
from membership_inference_attack import best_threshold, confidence, infer, rates, shadow_attack, tpr_at_fpr


def brute_rates(si, so, tau):
    return sum(s >= tau for s in si) / len(si), sum(s >= tau for s in so) / len(so)


def brute_best(si, so):
    best_tau, best_adv = math.inf, Fraction(0)
    for tau in sorted(set(si) | set(so), reverse=True):
        adv = Fraction(sum(s >= tau for s in si), len(si)) - Fraction(sum(s >= tau for s in so), len(so))
        if adv > best_adv:
            best_tau, best_adv = tau, adv
    return best_tau, float(best_adv)


def test_example_of_the_page() -> None:
    tau, adv = best_threshold([0.9, 0.8, 0.7], [0.75, 0.6, 0.5])
    assert tau == 0.8 and abs(adv - 2 / 3) < 1e-12
    tpr, fpr = rates([0.95, 0.85, 0.6], [0.82, 0.55, 0.4], tau)
    assert (tpr, fpr) == (2 / 3, 1 / 3)
    assert tpr_at_fpr([0.95, 0.85, 0.6], [0.82, 0.55, 0.4], 0.0) == 2 / 3


def test_threshold_matches_brute_force() -> None:
    rng = random.Random(7302)
    for _ in range(500):
        si = [rng.randint(0, 6) / 6 for _ in range(rng.randint(1, 8))]
        so = [rng.randint(0, 6) / 6 for _ in range(rng.randint(1, 8))]
        tau, adv = best_threshold(si, so)
        btau, badv = brute_best(si, so)
        assert abs(adv - badv) < 1e-12 and tau == btau
        if tau != math.inf:
            tpr, fpr = rates(si, so, tau)
            assert abs(tpr - fpr - adv) < 1e-12


def test_tpr_at_low_fpr_matches_brute_force() -> None:
    rng = random.Random(7303)
    for _ in range(500):
        si = [rng.randint(0, 9) / 9 for _ in range(rng.randint(1, 8))]
        so = [rng.randint(0, 9) / 9 for _ in range(rng.randint(1, 8))]
        alpha = rng.choice([0.0, 0.01, 0.1, 0.25, 0.5, 1.0])
        expect = max(
            [t for t, f in (brute_rates(si, so, tau) for tau in set(si) | set(so)) if f <= alpha] + [0.0]
        )
        assert tpr_at_fpr(si, so, alpha) == expect


def run_game(seed: int, l2: float, ignore_data: bool) -> tuple[float, float]:
    """The membership game on 10 target models; returns (advantage of the shadow threshold, TPR at FPR 0.05)."""
    rng = random.Random(seed)
    d, n, steps, lr = 8, 16, 200, 1.0
    centers = [[0.3] * d, [-0.3] * d]
    shadows = [make_blobs(rng, 2 * n, d, centers, 1.5) for _ in range(4)]
    tau = shadow_attack(shadows, steps, lr, l2)
    si, so = [], []
    for _ in range(10):
        members = make_blobs(rng, n, d, centers, 1.5)
        others = make_blobs(rng, n, d, centers, 1.5)
        train_on = make_blobs(rng, n, d, centers, 1.5) if ignore_data else members
        target = train_logistic(train_on, steps, lr, l2)
        si += [confidence(target, x, y) for x, y in members]
        so += [confidence(target, x, y) for x, y in others]
        assert all(infer(target, tau, x, y) == (confidence(target, x, y) >= tau) for x, y in members)
    tpr, fpr = rates(si, so, tau)
    return tpr - fpr, tpr_at_fpr(si, so, 0.05)


def test_overfit_model_leaks_membership() -> None:
    """A measurement: 16 training points in d = 8 with no penalty, so the model fits its members better."""
    adv, low = run_game(7304, 0.0, False)
    assert adv >= 0.15
    assert low < adv  # the threshold attack is weak at a low false positive rate


def test_regularization_and_a_model_that_ignores_its_data() -> None:
    adv_reg, _ = run_game(7304, 1.0, False)
    adv_free, _ = run_game(7304, 0.0, False)
    adv_none, _ = run_game(7304, 0.0, True)
    assert adv_reg < adv_free
    assert abs(adv_none) <= 0.1
