# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neural-architecture-search/. The authors are listed in prov/Z1X9SG.jsonl.

import random

from neural_architecture_search import (
    discretize_cell,
    discretize_edge,
    mixed_op,
    mixed_op_alpha_grad,
    softmax,
)

NAMES = ["none", "skip", "scale", "relu", "square"]
OPS = [
    lambda x: [0.0 for _ in x],
    lambda x: list(x),
    lambda x: [2.0 * a for a in x],
    lambda x: [max(a, 0.0) for a in x],
    lambda x: [a * a for a in x],
]


def test_mixing_weights_sum_to_one_and_are_positive():
    rng = random.Random(1)
    for _ in range(200):
        alpha = [rng.uniform(-50, 50) for _ in range(rng.randint(1, 8))]
        w = softmax(alpha)
        assert abs(sum(w) - 1) < 1e-12
        assert all(x >= 0 for x in w)


def test_shift_invariance_and_uniform_start():
    alpha = [0.3, -1.2, 2.0, 0.0, 0.7]
    a = softmax(alpha)
    b = softmax([x + 100 for x in alpha])
    assert max(abs(p - q) for p, q in zip(a, b)) < 1e-12
    assert softmax([0.0] * 5) == [0.2] * 5


def test_mixed_op_is_a_convex_combination_and_tends_to_one_op():
    x = [1.0, -2.0, 0.5]
    mix = mixed_op(x, OPS, [0.0] * 5)
    outs = [op(x) for op in OPS]
    assert max(abs(m - sum(o[t] for o in outs) / 5) for t, m in enumerate(mix)) < 1e-12
    hard = mixed_op(x, OPS, [0, 0, 60, 0, 0])
    assert max(abs(a - b) for a, b in zip(hard, OPS[2](x))) < 1e-20 + 1e-12


def test_alpha_gradient_matches_finite_differences():
    rng = random.Random(2)
    for _ in range(20):
        x = [rng.uniform(-2, 2) for _ in range(4)]
        alpha = [rng.uniform(-2, 2) for _ in range(5)]
        up = [rng.uniform(-1, 1) for _ in range(4)]
        g = mixed_op_alpha_grad(x, OPS, alpha, up)
        assert abs(sum(g)) < 1e-12
        h = 1e-6
        for o in range(5):
            a1, a2 = list(alpha), list(alpha)
            a1[o] += h
            a2[o] -= h
            f1 = sum(u * m for u, m in zip(up, mixed_op(x, OPS, a1)))
            f2 = sum(u * m for u, m in zip(up, mixed_op(x, OPS, a2)))
            assert abs((f1 - f2) / (2 * h) - g[o]) < 1e-7


def test_discretization_ignores_none_and_keeps_top_two_edges():
    assert discretize_edge([5.0, 1.0, 2.0, 0.0, 0.0], NAMES)[0] == "scale"
    alphas = {
        (0, 2): [0.0, 3.0, 0.0, 0.0, 0.0],
        (1, 2): [0.0, 0.0, 0.0, 1.0, 0.0],
        (0, 3): [0.0, 0.0, 0.5, 0.0, 0.0],
        (1, 3): [4.0, 0.0, 0.0, 0.0, 2.0],
        (2, 3): [0.0, 0.0, 0.0, 0.0, 0.0],
    }
    cell = discretize_cell(alphas, NAMES, k=2)
    assert cell[2] == [(0, "skip"), (1, "relu")]
    # Edge (1, 3) puts most weight on "none", so its best real op has weight
    # e^2 / (e^4 + 3 + e^2) < 0.2, below the uniform edge (2, 3).
    assert cell[3] == [(0, "scale"), (2, "skip")]
