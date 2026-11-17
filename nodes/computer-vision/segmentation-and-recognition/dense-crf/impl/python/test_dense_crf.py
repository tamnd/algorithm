# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dense-crf/. The authors are listed in prov/9CMFRH.jsonl.

import math
import random

from dense_crf import (
    concave_objective,
    dense_crf,
    free_energy,
    gaussian_messages,
    kernel_matrix,
    labels_of,
    log_partition,
    mean_field_sequential,
    softmax_neg,
)


def random_problem(rng, w, h, nl, levels=3):
    img = [[rng.randrange(levels) * 4 for _ in range(w)] for _ in range(h)]
    unary = [[rng.uniform(0.0, 2.0) for _ in range(nl)] for _ in range(w * h)]
    return img, unary


def test_row_example():
    img = [[0, 0, 10, 10]]
    unary = [[-math.log(1 - p), -math.log(p)] for p in (0.2, 0.6, 0.7, 0.9)]
    k = kernel_matrix(img, 2.0, 2.0, 3.0, 0.5, 1.0)
    assert abs(k[0][1] - 2.0683) < 1e-4 and abs(k[1][2] - 0.3101) < 1e-4
    q = dense_crf(unary, k, 1)
    assert abs(q[1][1] - 0.3422) < 1e-4
    assert labels_of(q) == [0, 0, 1, 1]
    q5 = dense_crf(unary, k, 5)
    assert labels_of(q5) == [0, 0, 1, 1]
    assert abs(free_energy(q5, unary, k) - 1.6484) < 1e-4
    assert free_energy(q5, unary, k) >= -log_partition(unary, k)


def test_marginals_are_distributions():
    rng = random.Random(11)
    img, unary = random_problem(rng, 4, 3, 3)
    q = dense_crf(unary, kernel_matrix(img, 1.5, 2.0, 3.0, 1.0, 1.0), 4)
    for qi in q:
        assert all(x > 0 for x in qi) and abs(sum(qi) - 1.0) < 1e-12


def test_zero_weights_give_the_unary_softmax():
    rng = random.Random(12)
    img, unary = random_problem(rng, 3, 3, 4)
    q = dense_crf(unary, kernel_matrix(img, 0.0, 2.0, 3.0, 0.0, 1.0), 5)
    for qi, ui in zip(q, unary):
        z = sum(math.exp(-x) for x in ui)
        assert all(abs(a - math.exp(-x) / z) < 1e-12 for a, x in zip(qi, ui))


def test_separable_filter_equals_the_naive_sum():
    rng = random.Random(13)
    w, h, nl, theta = 5, 4, 3, 1.3
    q = [softmax_neg([rng.uniform(0, 3) for _ in range(nl)]) for _ in range(w * h)]
    k = kernel_matrix([[0] * w for _ in range(h)], 0.0, 1.0, 1.0, 1.0, theta)
    fast = gaussian_messages(q, w, h, theta)
    for i in range(w * h):
        for l in range(nl):
            naive = sum(k[i][j] * q[j][l] for j in range(w * h))
            assert abs(fast[i][l] - naive) < 1e-12


def test_sequential_updates_never_raise_the_free_energy():
    rng = random.Random(14)
    for _ in range(5):
        img, unary = random_problem(rng, 3, 2, 3)
        k = kernel_matrix(img, 3.0, 2.0, 2.0, 2.0, 1.0)
        trace = []
        q = mean_field_sequential(unary, k, 4, trace)
        start = free_energy([softmax_neg(u) for u in unary], unary, k)
        values = [start] + trace
        assert all(b <= a + 1e-12 for a, b in zip(values, values[1:]))
        assert values[-1] >= -log_partition(unary, k) - 1e-12


def test_free_energy_bounds_log_z_and_is_tight_without_coupling():
    rng = random.Random(15)
    img, unary = random_problem(rng, 4, 2, 2)
    k = kernel_matrix(img, 1.0, 2.0, 3.0, 1.0, 1.0)
    q = dense_crf(unary, k, 6)
    assert free_energy(q, unary, k) >= -log_partition(unary, k)
    zero = kernel_matrix(img, 0.0, 2.0, 3.0, 0.0, 1.0)
    q0 = dense_crf(unary, zero, 1)
    assert abs(free_energy(q0, unary, zero) + log_partition(unary, zero)) < 1e-10


def test_parallel_update_can_oscillate():
    # Two pixels with a strong Potts link and opposite unaries swap their beliefs each step.
    unary = [[0.0, 1.0], [1.0, 0.0]]
    k = kernel_matrix([[0, 0]], 0.0, 1.0, 1.0, 5.0, 3.0)
    q = [dense_crf(unary, k, t) for t in range(6)]
    assert labels_of(q[1]) == [1, 0] and labels_of(q[2]) == [0, 1]
    assert labels_of(q[3]) == [1, 0] and labels_of(q[4]) == [0, 1]
    seq = mean_field_sequential(unary, k, 3)
    assert labels_of(seq) == [1, 1]


def test_self_term_variant_decreases_its_objective():
    rng = random.Random(16)
    cases = [([[0, 0]], [[0.0, 1.0], [1.0, 0.0]], (0.0, 1.0, 1.0, 5.0, 3.0))]
    for _ in range(4):
        img, unary = random_problem(rng, 3, 3, 3)
        cases.append((img, unary, (2.0, 1.5, 3.0, 1.0, 1.0)))
    for img, unary, (w1, ta, tb, w2, tg) in cases:
        k = kernel_matrix(img, w1, ta, tb, w2, tg)
        values = [concave_objective(dense_crf(unary, k, t, include_self=w1 + w2), unary, k, w1 + w2) for t in range(8)]
        assert all(b <= a + 1e-12 for a, b in zip(values, values[1:]))


def test_denoising_two_regions():
    rng = random.Random(17)
    w = h = 10
    truth = [1 if u >= 5 else 0 for v in range(h) for u in range(w)]
    img = [[100 * (1 if u >= 5 else 0) + rng.randint(-10, 10) for u in range(w)] for v in range(h)]
    unary = []
    for t in truth:
        # The probability of the true label: right with chance 0.75, wrong otherwise.
        p = rng.uniform(0.55, 0.9) if rng.random() < 0.75 else rng.uniform(0.1, 0.45)
        probs = [1 - p, p] if t == 1 else [p, 1 - p]
        unary.append([-math.log(x) for x in probs])
    k = kernel_matrix(img, 3.0, 3.0, 20.0, 1.0, 1.0)
    before = sum(a == b for a, b in zip(labels_of(dense_crf(unary, k, 0)), truth))
    after = sum(a == b for a, b in zip(labels_of(dense_crf(unary, k, 5)), truth))
    assert before < 90 and after == 100
