# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-preference-optimization/. The authors are listed in prov/ZDWMJ1.jsonl.

import math
import random

import pytest

from direct_preference_optimization import (bradley_terry_pairs, dpo_loss, fit_tabular, implicit_reward,
                                            kl_objective, log_partition, neg_log_sigmoid, optimal_policy,
                                            reward_model_loss, sigmoid, tabular_dpo_loss)


def test_worked_example():
    # beta = 0.1, a_w = -12, b_w = -13, a_l = -15, b_l = -14, so z = 0.2.
    loss, grads = dpo_loss([(-12.0, -13.0, -15.0, -14.0)], 0.1)
    assert loss == pytest.approx(math.log1p(math.exp(-0.2)), abs=1e-12)
    assert loss == pytest.approx(0.598139, abs=1e-6)
    gw, gl = grads[0]
    assert gw == pytest.approx(-0.0450166, abs=1e-7)
    assert gl == pytest.approx(0.0450166, abs=1e-7)


def test_zero_margin_gives_log_2():
    loss, grads = dpo_loss([(-5.0, -5.0, -7.0, -7.0)], 0.5)
    assert loss == pytest.approx(math.log(2), abs=1e-15)
    assert grads[0] == pytest.approx((-0.25, 0.25), abs=1e-15)


def test_loss_is_the_bradley_terry_loss_of_the_implicit_rewards():
    rng = random.Random(1)
    for _ in range(50):
        beta = rng.uniform(0.05, 2.0)
        a_w, b_w, a_l, b_l = (rng.uniform(-60, -1) for _ in range(4))
        loss, _ = dpo_loss([(a_w, b_w, a_l, b_l)], beta)
        r_w = implicit_reward(a_w, b_w, beta)
        r_l = implicit_reward(a_l, b_l, beta)
        direct = -math.log(1.0 / (1.0 + math.exp(-(r_w - r_l))))
        assert loss == pytest.approx(direct, abs=1e-12)
        assert reward_model_loss(r_w, r_l) == pytest.approx(direct, abs=1e-12)


def test_gradient_against_finite_differences():
    rng = random.Random(2)
    beta = 0.7
    pairs = [tuple(rng.uniform(-8, -1) for _ in range(4)) for _ in range(5)]
    _, grads = dpo_loss(pairs, beta)
    h = 1e-6
    for i in range(len(pairs)):
        for slot, g in ((0, grads[i][0]), (2, grads[i][1])):
            up = [list(p) for p in pairs]
            dn = [list(p) for p in pairs]
            up[i][slot] += h
            dn[i][slot] -= h
            num = (dpo_loss([tuple(p) for p in up], beta)[0] - dpo_loss([tuple(p) for p in dn], beta)[0]) / (2 * h)
            assert num == pytest.approx(g, abs=1e-5)


def test_the_reference_enters_with_the_opposite_sign():
    # dL/db_w = -dL/da_w, so the loss depends on a - b only.
    base = (-10.0, -11.0, -12.0, -11.5)
    l0, _ = dpo_loss([base], 0.3)
    shifted = (base[0] + 4.0, base[1] + 4.0, base[2] - 2.0, base[3] - 2.0)
    l1, _ = dpo_loss([shifted], 0.3)
    assert l0 == pytest.approx(l1, abs=1e-12)


def test_large_margins_are_stable():
    # Sequence log probabilities of a few thousand nats and margins of 1000.
    loss, grads = dpo_loss([(-2000.0, -3000.0, -3000.0, -2000.0)], 0.5)
    assert loss == pytest.approx(0.0, abs=1e-300)
    assert grads[0][0] == 0.0 or abs(grads[0][0]) < 1e-300
    loss, grads = dpo_loss([(-3000.0, -2000.0, -2000.0, -3000.0)], 0.5)
    assert loss == pytest.approx(1000.0, abs=1e-9)
    assert grads[0] == pytest.approx((-0.5, 0.5), abs=1e-15)
    assert neg_log_sigmoid(-1000.0) == pytest.approx(1000.0, abs=1e-9)
    assert sigmoid(-1000.0) == 0.0 and sigmoid(1000.0) == 1.0


def test_wrong_order_gets_a_larger_gradient():
    _, g_right = dpo_loss([(-10.0, -12.0, -12.0, -10.0)], 1.0)
    _, g_wrong = dpo_loss([(-12.0, -10.0, -10.0, -12.0)], 1.0)
    assert abs(g_wrong[0][0]) > abs(g_right[0][0])
    assert abs(g_wrong[0][0]) == pytest.approx(sigmoid(4.0), abs=1e-15)


def test_batch_loss_is_the_mean():
    pairs = [(-1.0, -2.0, -3.0, -1.0), (-4.0, -4.5, -2.0, -2.2), (-3.0, -3.0, -3.0, -3.0)]
    loss, grads = dpo_loss(pairs, 0.2)
    singles = [dpo_loss([p], 0.2) for p in pairs]
    assert loss == pytest.approx(sum(s[0] for s in singles) / 3, abs=1e-15)
    for g, s in zip(grads, singles):
        assert g[0] == pytest.approx(s[1][0][0] / 3, abs=1e-15)


def test_bad_arguments():
    with pytest.raises(ValueError):
        dpo_loss([], 0.1)
    with pytest.raises(ValueError):
        dpo_loss([(-1.0, -1.0, -1.0, -1.0)], 0.0)


# ------------------------------------------------------------ the derivation


def test_optimal_policy_worked_example():
    pi = optimal_policy([0.5, 0.3, 0.2], [0.0, 1.0, 2.0], 1.0)
    assert pi == pytest.approx([0.17900, 0.29194, 0.52906], abs=1e-5)
    assert sum(pi) == pytest.approx(1.0, abs=1e-15)
    value = kl_objective(pi, [0.5, 0.3, 0.2], [0.0, 1.0, 2.0], 1.0)
    assert value == pytest.approx(log_partition([0.5, 0.3, 0.2], [0.0, 1.0, 2.0], 1.0), abs=1e-12)
    assert value == pytest.approx(1.02722, abs=1e-5)


def test_no_policy_beats_the_closed_form():
    rng = random.Random(3)
    for _ in range(20):
        K = rng.randint(2, 6)
        beta = rng.uniform(0.1, 3.0)
        ref = [rng.uniform(0.1, 1.0) for _ in range(K)]
        s = sum(ref)
        ref = [p / s for p in ref]
        reward = [rng.uniform(-2, 2) for _ in range(K)]
        best = beta * log_partition(ref, reward, beta)
        star = optimal_policy(ref, reward, beta)
        assert kl_objective(star, ref, reward, beta) == pytest.approx(best, abs=1e-12)
        for _ in range(200):
            q = [rng.random() + 1e-9 for _ in range(K)]
            t = sum(q)
            q = [v / t for v in q]
            assert kl_objective(q, ref, reward, beta) <= best + 1e-12


def test_reward_shift_by_a_constant_does_not_change_the_optimum():
    ref, reward = [0.2, 0.5, 0.3], [1.0, -0.5, 0.25]
    a = optimal_policy(ref, reward, 0.4)
    b = optimal_policy(ref, [r + 7.0 for r in reward], 0.4)
    assert a == pytest.approx(b, abs=1e-12)


def test_reward_is_recovered_from_the_optimal_policy():
    # r(y) = beta log(pi*(y) / pi_ref(y)) + beta log Z.
    ref, reward, beta = [0.4, 0.4, 0.2], [0.3, -1.0, 2.0], 0.8
    star = optimal_policy(ref, reward, beta)
    logz = log_partition(ref, reward, beta)
    for p, q, r in zip(star, ref, reward):
        assert beta * math.log(p / q) + beta * logz == pytest.approx(r, abs=1e-12)


def test_tabular_gradient_against_finite_differences():
    rng = random.Random(4)
    K, beta = 4, 0.6
    theta = [rng.gauss(0, 1) for _ in range(K)]
    log_ref = [math.log(p) for p in (0.1, 0.2, 0.3, 0.4)]
    pairs = bradley_terry_pairs([0.5, -1.0, 2.0, 0.0])
    _, g = tabular_dpo_loss(theta, log_ref, pairs, beta)
    h = 1e-6
    for j in range(K):
        up, dn = list(theta), list(theta)
        up[j] += h
        dn[j] -= h
        num = (tabular_dpo_loss(up, log_ref, pairs, beta)[0] - tabular_dpo_loss(dn, log_ref, pairs, beta)[0]) / (2 * h)
        assert num == pytest.approx(g[j], abs=1e-5)


def test_population_dpo_reaches_the_kl_regularized_optimum():
    for ref, reward, beta in [([0.5, 0.3, 0.2], [0.0, 1.0, 2.0], 1.0),
                              ([0.25, 0.25, 0.25, 0.25], [1.0, 0.0, -1.0, 0.5], 0.5),
                              ([0.6, 0.3, 0.1], [0.0, 0.5, 3.0], 2.0)]:
        log_ref = [math.log(p) for p in ref]
        pairs = bradley_terry_pairs(reward)
        pi = fit_tabular(log_ref, pairs, beta, steps=4000, lr=2.0)
        assert pi == pytest.approx(optimal_policy(ref, reward, beta), abs=1e-6)


def test_deterministic_preferences_push_without_limit():
    # If y_0 always wins, the loss keeps falling as pi(y_0) / pi(y_1) grows: no finite minimizer.
    log_ref = [math.log(0.5), math.log(0.5)]
    pairs = [(0, 1, 1.0)]
    losses = []
    theta = list(log_ref)
    for _ in range(5):
        loss, g = tabular_dpo_loss(theta, log_ref, pairs, 0.1)
        losses.append(loss)
        theta = [t - 50.0 * gi for t, gi in zip(theta, g)]
    assert all(b < a for a, b in zip(losses, losses[1:]))
    assert theta[0] - theta[1] > 5.0
