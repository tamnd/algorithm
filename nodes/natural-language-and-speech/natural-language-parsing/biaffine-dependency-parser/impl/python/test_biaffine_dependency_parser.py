# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/biaffine-dependency-parser/. The authors are listed in prov/XMKHK7.jsonl.

import itertools
import math
import random

from biaffine_dependency_parser import (
    arc_scores,
    biaffine,
    decode,
    head_log_probs,
    head_loss_and_grads,
    is_tree,
    label_scores,
    parse,
    relu_layer,
)


def all_trees(n):
    return [[-1] + list(hs) for hs in itertools.product(range(n + 1), repeat=n) if is_tree([-1] + list(hs))]


TREES = {n: all_trees(n) for n in range(1, 6)}


def mat(rng, r, k):
    return [[rng.uniform(-1, 1) for _ in range(k)] for _ in range(r)]


def vec(rng, k):
    return [rng.uniform(-1, 1) for _ in range(k)]


def params(rng, dr, k, kl, n_labels):
    return {
        "W_ah": mat(rng, k, dr), "b_ah": vec(rng, k),
        "W_ad": mat(rng, k, dr), "b_ad": vec(rng, k),
        "U": mat(rng, k, k), "u": vec(rng, k),
        "W_lh": mat(rng, kl, dr), "b_lh": vec(rng, kl),
        "W_ld": mat(rng, kl, dr), "b_ld": vec(rng, kl),
        "Us": [mat(rng, kl, kl) for _ in range(n_labels)],
        "ws": [vec(rng, 2 * kl) for _ in range(n_labels)],
        "cs": vec(rng, n_labels),
    }


def tree_score(S, heads):
    return math.fsum(S[heads[d]][d] for d in range(1, len(heads)))


def test_counts():
    assert [len(TREES[n]) for n in range(1, 6)] == [1, 3, 16, 125, 1296]


def test_relu_and_biaffine():
    assert relu_layer([[1.0, -1.0], [2.0, 0.0]], [0.0, -7.0], [3.0, 1.0]) == [2.0, 0.0]
    a, e = [1.0, 2.0], [3.0, -1.0]
    U, u = [[1.0, 0.0], [2.0, 1.0]], [0.5, -1.0]
    # a^T U e = [1, 2] . [3, 5] = 13 and a^T u = -1.5
    assert biaffine(a, U, e, u) == 11.5


def test_arc_scores_and_head_prior():
    rng = random.Random(1)
    A = [vec(rng, 3) for _ in range(5)]
    E = [vec(rng, 3) for _ in range(5)]
    U, u = mat(rng, 3, 3), vec(rng, 3)
    S = arc_scores(A, E, U, u)
    S0 = arc_scores(A, E, U, [0.0] * 3)
    for h in range(5):
        for d in range(5):
            assert abs(S[h][d] - biaffine(A[h], U, E[d], u)) <= 1e-12
        # The term a_h^T u depends on the head only: it adds a constant to row h.
        diffs = [S[h][d] - S0[h][d] for d in range(5)]
        assert max(diffs) - min(diffs) <= 1e-12
    for d in range(1, 5):
        lp = head_log_probs(S, d)
        assert d not in lp and abs(math.fsum(math.exp(v) for v in lp.values()) - 1.0) <= 1e-12


def test_loss_gradients_by_finite_differences():
    rng = random.Random(2)
    k, m = 3, 5
    A = [vec(rng, k) for _ in range(m)]
    E = [vec(rng, k) for _ in range(m)]
    U, u = mat(rng, k, k), vec(rng, k)
    gold = [-1, 2, 0, 2, 3]
    loss, gU, gu = head_loss_and_grads(A, E, U, u, gold)
    eps = 1e-6
    for i in range(k):
        old = u[i]
        u[i] = old + eps
        up = head_loss_and_grads(A, E, U, u, gold)[0]
        u[i] = old - eps
        down = head_loss_and_grads(A, E, U, u, gold)[0]
        u[i] = old
        assert abs((up - down) / (2 * eps) - gu[i]) <= 1e-6
        for j in range(k):
            old = U[i][j]
            U[i][j] = old + eps
            up = head_loss_and_grads(A, E, U, u, gold)[0]
            U[i][j] = old - eps
            down = head_loss_and_grads(A, E, U, u, gold)[0]
            U[i][j] = old
            assert abs((up - down) / (2 * eps) - gU[i][j]) <= 1e-6
    assert loss > 0


def test_greedy_heads_can_form_a_cycle():
    # Each of the two words prefers the other as head; the root is a weak head.
    S = [[0.0, 1.0, 0.0], [0.0, 0.0, 10.0], [0.0, 10.0, 0.0]]
    heads, used = decode(S)
    assert used and heads == [-1, 0, 1] and tree_score(S, heads) == 11.0
    S = [[0.0, 5.0, 0.0], [0.0, 0.0, 10.0], [0.0, 1.0, 0.0]]
    assert decode(S) == ([-1, 0, 1], False)


def test_decoder_against_brute_force():
    rng = random.Random(3)
    cycles = 0
    for n in range(1, 6):
        for _ in range(30 if n < 5 else 10):
            S = [[rng.uniform(-3, 3) for _ in range(n + 1)] for _ in range(n + 1)]
            heads, used = decode(S)
            cycles += used
            assert is_tree(heads)
            best = max(tree_score(S, t) for t in TREES[n])
            assert abs(tree_score(S, heads) - best) <= 1e-9
            if n <= 4:
                # The same tree maximizes the sum of the head log probabilities,
                # because each word has its own softmax and its normalizer is a constant.
                logp = lambda t: math.fsum(head_log_probs(S, d)[t[d]] for d in range(1, n + 1))
                assert abs(logp(heads) - max(logp(t) for t in TREES[n])) <= 1e-9
    assert cycles > 0


def test_parse_forward_pass_and_labels():
    rng = random.Random(4)
    labels = ["nsubj", "obj", "root", "det"]
    for _ in range(10):
        n = rng.randint(1, 5)
        p = params(rng, 4, 3, 2, len(labels))
        R = [vec(rng, 4) for _ in range(n + 1)]
        heads, labs, S, _ = parse(R, p, labels)
        assert is_tree(heads)
        Ah = [relu_layer(p["W_lh"], p["b_lh"], r) for r in R]
        Ed = [relu_layer(p["W_ld"], p["b_ld"], r) for r in R]
        for d in range(1, n + 1):
            ls = label_scores(Ah, Ed, p["Us"], p["ws"], p["cs"], heads[d], d)
            assert labs[d] == labels[max(range(len(labels)), key=lambda l: ls[l])]
        assert abs(tree_score(S, heads) - max(tree_score(S, t) for t in TREES[n])) <= 1e-9
