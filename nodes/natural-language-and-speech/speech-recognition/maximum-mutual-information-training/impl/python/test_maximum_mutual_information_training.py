# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-mutual-information-training/. The authors are listed in prov/BW4ZT9.jsonl.

import math
import random

import pytest

import nlslog
from maximum_mutual_information_training import (
    Graph,
    brute_force_log_z,
    discrete_loglik,
    ebw_counts,
    ebw_update,
    forward_backward,
    mmi_objective,
    mmi_objective_and_grad,
    smallest_safe_d,
    union,
    word_sequence_graph,
)
from nlslog import NEG_INF, log_add

LS, LN = math.log(0.6), math.log(0.4)


def one_state_words():
    models = {"A": [0], "B": [1]}
    ll = [[math.log(0.6), math.log(0.3)], [math.log(0.5), math.log(0.4)]]
    a = word_sequence_graph(["A"], models, 0.0, NEG_INF, math.log(0.5))
    b = word_sequence_graph(["B"], models, 0.0, NEG_INF, math.log(0.5))
    return ll, a, union([a, b])


def random_task(rng, T, P=3):
    models = {"A": [0, 1], "B": [1, 2], "C": [2, 0, 1]}
    words = ["A", "B", "C"]
    ref = [rng.choice(words) for _ in range(rng.randint(1, 2))]
    lm = math.log(1 / 3) * len(ref)
    num = word_sequence_graph(ref, models, LS, LN, lm)
    comps = [[w] for w in words] + [[u, v] for u in words for v in words]
    comps = [c for c in comps if sum(len(models[w]) for w in c) <= T]
    if ref not in comps:
        comps.append(ref)
    den = union([word_sequence_graph(c, models, LS, LN, math.log(1 / 3) * len(c)) for c in comps])
    loglik = [[rng.uniform(-3.0, 0.0) for _ in range(P)] for _ in range(T)]
    return loglik, num, den


def test_helper_header():
    with open(nlslog.__file__, encoding="utf-8") as f:
        lines = f.read().splitlines()
    assert lines[1] == "# Shared helper of the natural-language-and-speech pages of https://algorithm.tamnd.com/. The authors are listed in prov/."


def test_log_add_check_value():
    assert log_add(math.log(0.5), math.log(0.25)) == pytest.approx(-0.287682, abs=1e-6)


def test_page_example():
    ll, num, den = one_state_words()
    F, grad, g_num, g_den = mmi_objective_and_grad(ll, num, den, 1.0)
    assert math.exp(F) == pytest.approx(0.15 / 0.21, abs=1e-12)
    assert F == pytest.approx(-0.336472, abs=1e-6)
    for t in range(2):
        assert grad[t] == pytest.approx([2 / 7, -2 / 7], abs=1e-12)
    F, grad, _, _ = mmi_objective_and_grad(ll, num, den, 0.5)
    post = 0.5 * math.sqrt(0.30) / (0.5 * math.sqrt(0.30) + 0.5 * math.sqrt(0.12))
    assert math.exp(F) == pytest.approx(post, abs=1e-12)
    assert math.exp(F) == pytest.approx(0.612574, abs=1e-6)
    assert grad[0] == pytest.approx([0.5 * (1 - post), -0.5 * (1 - post)], abs=1e-12)


def test_forward_against_brute_force():
    rng = random.Random(1)
    for _ in range(15):
        T = rng.randint(2, 5)
        loglik, num, den = random_task(rng, T)
        kappa = rng.choice([1.0, 0.5, 0.1])
        for g in (num, den):
            try:
                lz, gamma = forward_backward(g, loglik, kappa)
            except ValueError:
                assert brute_force_log_z(g, loglik, kappa) == NEG_INF
                continue
            assert lz == pytest.approx(brute_force_log_z(g, loglik, kappa), abs=1e-10)
            for t in range(T):
                assert sum(gamma[t]) == pytest.approx(1.0, abs=1e-12)


def test_objective_is_a_log_posterior():
    # When the denominator holds the numerator paths, F = ln P(reference | O) <= 0.
    rng = random.Random(2)
    for _ in range(10):
        loglik, num, den = random_task(rng, rng.randint(3, 6))
        try:
            F = mmi_objective(loglik, num, den, 0.3)
        except ValueError:
            continue
        assert F <= 1e-12


def test_gradient_against_finite_differences():
    rng = random.Random(3)
    h = 1e-6
    done = 0
    while done < 4:
        T = rng.randint(3, 5)
        loglik, num, den = random_task(rng, T)
        kappa = rng.choice([1.0, 0.25])
        try:
            _, grad, _, _ = mmi_objective_and_grad(loglik, num, den, kappa)
        except ValueError:
            continue
        done += 1
        for t in range(T):
            for p in range(len(loglik[0])):
                up = [r[:] for r in loglik]
                dn = [r[:] for r in loglik]
                up[t][p] += h
                dn[t][p] -= h
                fd = (mmi_objective(up, num, den, kappa) - mmi_objective(dn, num, den, kappa)) / (2 * h)
                assert grad[t][p] == pytest.approx(fd, abs=1e-5)
            # Both posteriors sum to 1 at each frame, so the gradient of a frame sums to 0.
            assert sum(grad[t]) == pytest.approx(0.0, abs=1e-12)


def test_gradient_is_zero_when_there_is_no_competitor():
    ll, num, _ = one_state_words()
    F, grad, _, _ = mmi_objective_and_grad(ll, num, num, 1.0)
    assert F == 0.0
    assert all(abs(x) < 1e-15 for row in grad for x in row)


def test_extended_baum_welch_never_decreases_the_objective():
    rng = random.Random(4)
    models = {"A": [0, 1], "B": [1, 2], "C": [2, 0]}
    P, V = 3, 3
    b = [[rng.random() + 0.2 for _ in range(V)] for _ in range(P)]
    b = [[x / sum(r) for x in r] for r in b]
    data = []
    for _ in range(4):
        obs = [rng.randrange(V) for _ in range(rng.randint(4, 6))]
        ref = rng.choice("ABC")
        num = word_sequence_graph([ref], models, LS, LN, math.log(1 / 3))
        den = union([word_sequence_graph([w], models, LS, LN, math.log(1 / 3)) for w in "ABC"])
        data.append((obs, num, den))
    values = []
    for _ in range(8):
        F, c_num, c_den = ebw_counts(data, b)
        values.append(F)
        D = 2 * smallest_safe_d(b, c_num, c_den) + 1.0
        b = ebw_update(b, c_num, c_den, D)
        for row in b:
            assert min(row) > 0 and sum(row) == pytest.approx(1.0, abs=1e-12)
    assert all(values[i + 1] >= values[i] - 1e-12 for i in range(len(values) - 1))
    assert values[-1] > values[0] + 1.0


def test_ebw_counts_are_the_gradient_in_log_b():
    # d F / d ln b[p][v] = c_num[p][v] - c_den[p][v] (kappa = 1).
    rng = random.Random(5)
    models = {"A": [0, 1], "B": [1, 0]}
    b = [[0.3, 0.7], [0.6, 0.4]]
    obs = [rng.randrange(2) for _ in range(5)]
    num = word_sequence_graph(["A"], models, LS, LN, math.log(0.5))
    den = union([word_sequence_graph([w], models, LS, LN, math.log(0.5)) for w in "AB"])
    _, c_num, c_den = ebw_counts([(obs, num, den)], b)
    h = 1e-6
    for p in range(2):
        for v in range(2):
            def f(delta):
                bb = [r[:] for r in b]
                bb[p][v] = b[p][v] * math.exp(delta)
                return mmi_objective(discrete_loglik(bb, obs), num, den, 1.0)

            fd = (f(h) - f(-h)) / (2 * h)
            assert c_num[p][v] - c_den[p][v] == pytest.approx(fd, abs=1e-5)


def test_errors():
    models = {"A": [0, 1, 0]}
    g = word_sequence_graph(["A"], models, LS, LN)
    with pytest.raises(ValueError):
        forward_backward(g, [[0.0, 0.0]] * 2, 1.0)  # 3 states, 2 frames
    with pytest.raises(ValueError):
        ebw_update([[0.5, 0.5]], [[0.0, 0.0]], [[1.0, 0.0]], 1.0)
    assert isinstance(g, Graph)
