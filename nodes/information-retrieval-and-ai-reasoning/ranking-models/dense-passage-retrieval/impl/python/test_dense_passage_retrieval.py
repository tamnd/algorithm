# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dense-passage-retrieval/. The authors are listed in prov/GDMYGR.jsonl.

import math
import random

from dense_passage_retrieval import (
    dot,
    in_batch_gradients,
    in_batch_loss,
    similarity,
    softmax,
    top_k,
)

Q = [[1.0, 0.0], [0.0, 1.0]]
C = [[2.0, 0.0], [1.0, 1.0], [0.0, -1.0], [1.0, 2.0]]


def test_page_example():
    assert similarity(Q, C) == [[2.0, 1.0, 0.0, 1.0], [0.0, 1.0, -1.0, 2.0]]
    assert [round(v, 4) for v in softmax([2.0, 1.0, 0.0, 1.0])] == [0.5344, 0.1966, 0.0723, 0.1966]
    assert [round(v, 4) for v in softmax([0.0, 1.0, -1.0, 2.0])] == [0.0871, 0.2369, 0.0321, 0.6439]
    assert round(in_batch_loss(Q, C), 4) == 1.0334
    # Without the two hard negatives, only the other positive is a negative.
    assert round(in_batch_loss(Q, C[:2]), 4) == 0.3133
    gq, gc = in_batch_gradients(Q, C)
    assert [round(v, 4) for v in gq[0]] == [-0.2689, 0.2588]
    assert [round(v, 4) for v in gc[3]] == [0.0983, 0.3220]


def test_gradients_by_finite_differences():
    rng = random.Random(1)
    h = 1e-6
    for _ in range(20):
        b = rng.randint(1, 4)
        m = b + rng.randint(0, b)
        d = rng.randint(1, 4)
        qs = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(b)]
        cs = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(m)]
        gq, gc = in_batch_gradients(qs, cs)
        for mat, grad in ((qs, gq), (cs, gc)):
            for r in range(len(mat)):
                for c in range(d):
                    old = mat[r][c]
                    mat[r][c] = old + h
                    up = in_batch_loss(qs, cs)
                    mat[r][c] = old - h
                    down = in_batch_loss(qs, cs)
                    mat[r][c] = old
                    assert abs((up - down) / (2 * h) - grad[r][c]) < 1e-6


def test_loss_with_one_passage_per_question_is_cross_entropy_of_the_rows():
    rng = random.Random(2)
    qs = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(3)]
    cs = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(3)]
    s = similarity(qs, cs)
    direct = 0.0
    for i in range(3):
        direct += -s[i][i] + math.log(sum(math.exp(v) for v in s[i]))
    assert abs(in_batch_loss(qs, cs) - direct / 3) < 1e-12


def test_small_step_lowers_loss():
    rng = random.Random(3)
    qs = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(4)]
    cs = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(8)]
    before = in_batch_loss(qs, cs)
    gq, gc = in_batch_gradients(qs, cs)
    eta = 1e-3
    qs2 = [[a - eta * g for a, g in zip(q, gr)] for q, gr in zip(qs, gq)]
    cs2 = [[a - eta * g for a, g in zip(c, gr)] for c, gr in zip(cs, gc)]
    assert in_batch_loss(qs2, cs2) < before


def test_loss_bounds():
    # The loss is positive and is at most log m when every score is equal.
    qs = [[0.0, 0.0], [0.0, 0.0]]
    cs = [[1.0, 1.0], [2.0, 0.0], [0.5, 0.5]]
    assert abs(in_batch_loss(qs, cs) - math.log(3)) < 1e-12
    assert in_batch_loss(Q, C) > 0


def test_top_k_exact_with_ties():
    passages = [[1.0, 0.0], [0.0, 1.0], [1.0, 0.0], [0.5, 0.5], [2.0, -1.0]]
    assert top_k([1.0, 0.0], passages, 3) == [4, 0, 2]
    rng = random.Random(4)
    for _ in range(50):
        ps = [[rng.randint(-2, 2) for _ in range(3)] for _ in range(10)]
        q = [rng.randint(-2, 2) for _ in range(3)]
        got = top_k(q, ps, 4)
        brute = sorted(range(10), key=lambda p: (-dot(q, ps[p]), p))[:4]
        assert got == brute
        kth = dot(q, ps[got[-1]])
        assert all(dot(q, ps[p]) <= kth for p in range(10) if p not in got)
