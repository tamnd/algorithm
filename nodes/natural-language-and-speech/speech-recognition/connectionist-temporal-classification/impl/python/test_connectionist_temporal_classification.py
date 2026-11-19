# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/connectionist-temporal-classification/. The authors are listed in prov/7KBK03.jsonl.

import math
import random

import pytest

import nlslog
from connectionist_temporal_classification import (
    brute_force_log_prob,
    collapse,
    ctc_forward,
    ctc_loss,
    ctc_loss_and_grad,
    extend_labels,
    greedy_decode,
    labeling_posteriors,
    log_alpha,
    log_beta,
    min_frames,
)
from nlslog import COUNTING, LOG, NEG_INF, POS_INF, PROB, VITERBI, log_add, log_softmax, log_sum

# The worked example of the page: symbols _ (blank, index 0), a (1), b (2), T = 3.
Y = [[0.5, 0.4, 0.1], [0.4, 0.3, 0.3], [0.3, 0.1, 0.6]]
LY = [[math.log(p) for p in row] for row in Y]


def random_logits(rng, T, K, scale=2.0):
    return [[rng.uniform(-scale, scale) for _ in range(K)] for _ in range(T)]


def test_helper_header():
    with open(nlslog.__file__, encoding="utf-8") as f:
        lines = f.read().splitlines()
    assert lines[1] == "# Shared helper of the natural-language-and-speech pages of https://algorithm.tamnd.com/. The authors are listed in prov/."


def test_log_add_check_value():
    assert log_add(math.log(0.5), math.log(0.25)) == pytest.approx(-0.287682, abs=1e-6)


def test_collapse_removes_repeats_then_blanks():
    a, b = 1, 2
    assert collapse([a, 0, a, b, 0]) == (a, a, b)
    assert collapse([0, a, a, 0, 0, a, b, b]) == (a, a, b)
    assert collapse([a, a, b]) == (a, b)
    assert collapse([0, 0, 0]) == ()
    # Blanks first, then repeats, would give a different map: "a_a" -> "aa" -> "a".
    assert collapse([a, 0, a]) == (a, a)


def test_extended_labels():
    assert extend_labels([1, 2]) == [0, 1, 0, 2, 0]
    for U in range(6):
        assert len(extend_labels([1] * U)) == 2 * U + 1
    with pytest.raises(ValueError):
        extend_labels([1, 0])


def test_path_count_check_values():
    def count(T, labels, K=4):
        return ctc_forward(COUNTING, [[1] * K] * T, labels)

    assert count(3, [1, 2]) == 5  # _ab, a_b, aab, ab_, abb
    assert count(3, [1, 1]) == 1  # a_a
    assert count(4, [1, 1]) == 5
    assert count(4, [1, 2]) == 15
    assert count(5, [3, 1, 2]) == 28  # "cat"
    assert count(2, [1, 1]) == 0
    assert min_frames([1, 1]) == 3 and min_frames([1, 2, 2, 2]) == 6 and min_frames([]) == 0


def test_path_count_against_enumeration():
    import itertools

    for T in range(1, 6):
        for labels in [(), (1,), (1, 2), (1, 1), (2, 1, 2), (1, 1, 1)]:
            n = sum(1 for p in itertools.product(range(3), repeat=T) if collapse(p) == labels)
            assert ctc_forward(COUNTING, [[1] * 3] * T, list(labels)) == n
            assert (n > 0) == (T >= min_frames(labels))


def test_page_example():
    ext = extend_labels([1, 2])
    alpha = log_alpha(LY, ext)
    beta = log_beta(LY, ext)
    want_alpha = [[0.5, 0.4, 0, 0, 0], [0.2, 0.27, 0.16, 0.12, 0], [0.06, 0.047, 0.129, 0.33, 0.036]]
    want_beta = [[0.18, 0.69, 0.51, 0.39, 0.12], [0, 0.6, 0.6, 0.9, 0.3], [0, 0, 0, 1, 1]]
    for t in range(3):
        assert [math.exp(x) for x in alpha[t]] == pytest.approx(want_alpha[t], abs=1e-12)
        assert [math.exp(x) for x in beta[t]] == pytest.approx(want_beta[t], abs=1e-12)
    assert ctc_forward(PROB, Y, [1, 2]) == pytest.approx(0.366, abs=1e-12)
    assert ctc_loss(LY, [1, 2]) == pytest.approx(-math.log(0.366), abs=1e-12)
    # The best single path is a_b, with probability 0.4 * 0.4 * 0.6.
    assert math.exp(ctc_forward(VITERBI, LY, [1, 2])) == pytest.approx(0.096, abs=1e-12)


def test_alpha_beta_give_p_at_every_frame():
    rng = random.Random(7)
    for _ in range(20):
        T, K = rng.randint(3, 8), rng.randint(2, 5)
        U = rng.randint(0, 3)
        labels = [rng.randint(1, K - 1) for _ in range(U)]
        if T < min_frames(labels):
            continue
        ly = [log_softmax(u) for u in random_logits(rng, T, K)]
        ext = extend_labels(labels)
        alpha, beta = log_alpha(ly, ext), log_beta(ly, ext)
        log_p = -ctc_loss(ly, labels)
        for t in range(T):
            assert log_sum([alpha[t][s] + beta[t][s] for s in range(len(ext))]) == pytest.approx(log_p, abs=1e-10)


def test_forward_against_brute_force():
    rng = random.Random(11)
    for _ in range(30):
        T, K = rng.randint(1, 5), rng.randint(2, 4)
        U = rng.randint(0, 3)
        labels = [rng.randint(1, K - 1) for _ in range(U)]
        logits = random_logits(rng, T, K)
        ly = [log_softmax(u) for u in logits]
        want = brute_force_log_prob(ly, labels)
        if want == NEG_INF:
            assert ctc_loss(logits, labels) == POS_INF
            with pytest.raises(ValueError):
                ctc_loss_and_grad(logits, labels)
            continue
        assert -ctc_loss(logits, labels) == pytest.approx(want, abs=1e-10)
        assert ctc_forward(LOG, ly, labels) == pytest.approx(want, abs=1e-10)
        assert ctc_forward(PROB, [[math.exp(x) for x in r] for r in ly], labels) == pytest.approx(math.exp(want), rel=1e-10)


def test_labeling_probabilities_sum_to_one():
    rng = random.Random(3)
    ly = [log_softmax(u) for u in random_logits(rng, 5, 3)]
    post = labeling_posteriors(ly)
    assert log_sum(list(post.values())) == pytest.approx(0.0, abs=1e-12)
    for lab, v in post.items():
        assert ctc_forward(LOG, ly, list(lab)) == pytest.approx(v, abs=1e-10)


def test_gradient_against_finite_differences():
    rng = random.Random(5)
    h = 1e-6
    for labels, T, K in [([1, 2], 4, 3), ([1, 1], 5, 3), ([2, 1, 3], 6, 4), ([], 3, 2), ([1], 1, 2)]:
        logits = random_logits(rng, T, K)
        _, grad = ctc_loss_and_grad(logits, labels)
        for t in range(T):
            for k in range(K):
                up = [row[:] for row in logits]
                dn = [row[:] for row in logits]
                up[t][k] += h
                dn[t][k] -= h
                num = (ctc_loss(up, labels) - ctc_loss(dn, labels)) / (2 * h)
                assert grad[t][k] == pytest.approx(num, abs=1e-5)
            # The gradient of a frame sums to 0, because softmax ignores a shift of the logits.
            assert sum(grad[t]) == pytest.approx(0.0, abs=1e-12)


def test_gradient_check_values_of_the_example():
    _, grad = ctc_loss_and_grad(LY, [1, 2])
    want = [[0.254098, -0.354098, 0.1], [0.137705, -0.142623, 0.004918], [0.201639, 0.1, -0.301639]]
    for t in range(3):
        assert grad[t] == pytest.approx(want[t], abs=1e-6)


def test_greedy_is_not_the_most_probable_labeling():
    # Page example: the best path __b gives "b" (0.294), but "ab" has 0.366.
    post = labeling_posteriors(LY)
    best = max(post, key=post.get)
    assert best == (1, 2)
    assert greedy_decode(LY) == (2,)
    assert math.exp(post[(2,)]) == pytest.approx(0.294, abs=1e-12)
    # A smaller case: two frames with blank 0.6, a 0.4. Greedy gives "" (0.36), "a" has 0.64.
    ly = [[math.log(0.6), math.log(0.4)]] * 2
    assert greedy_decode(ly) == ()
    assert math.exp(ctc_forward(LOG, ly, [1])) == pytest.approx(0.64, abs=1e-12)


def test_product_of_probabilities_underflows_and_log_space_does_not():
    T, K = 300, 30
    probs = [[1.0 / K] * K for _ in range(T)]
    assert ctc_forward(PROB, probs, [1, 2]) == 0.0
    n = ctc_forward(COUNTING, [[1] * K] * T, [1, 2])
    assert n == 339746225
    want = math.log(n) - T * math.log(K)
    assert want < -1000
    lp = [[math.log(1.0 / K)] * K for _ in range(T)]
    assert ctc_forward(LOG, lp, [1, 2]) == pytest.approx(want, abs=1e-9)
    assert ctc_loss(lp, [1, 2]) == pytest.approx(-want, abs=1e-9)


def test_long_random_utterance_gradient_is_finite():
    rng = random.Random(13)
    T, K = 200, 6
    labels = [rng.randint(1, K - 1) for _ in range(40)]
    logits = random_logits(rng, T, K, scale=5.0)
    loss, grad = ctc_loss_and_grad(logits, labels)
    assert 0 < loss < POS_INF
    for row in grad:
        assert all(math.isfinite(g) for g in row)
        assert sum(row) == pytest.approx(0.0, abs=1e-9)


def test_errors():
    with pytest.raises(ValueError):
        ctc_loss([], [1])
    with pytest.raises(ValueError):
        ctc_loss_and_grad([[0.0, 0.0]] * 2, [1, 1])
    assert ctc_loss([[0.0, 0.0]] * 2, [1, 1]) == POS_INF
