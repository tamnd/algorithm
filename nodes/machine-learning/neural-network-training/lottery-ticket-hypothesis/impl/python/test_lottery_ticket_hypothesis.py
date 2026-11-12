# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lottery-ticket-hypothesis/. The authors are listed in prov/66QJ8T.jsonl.

import random
from fractions import Fraction as F

import pytest

from lottery_ticket_hypothesis import imp, least_squares, magnitude_prune, masked_gd, random_mask


def sparse_problem(seed, p=40, n=30, ntest=200):
    rng = random.Random(seed)
    beta = [2.0, -1.5, 1.0, -0.8, 0.6] + [0.0] * (p - 5)
    xs = [[rng.gauss(0, 1) for _ in range(p)] for _ in range(n)]
    ys = [sum(a * b for a, b in zip(r, beta)) + rng.gauss(0, 0.1) for r in xs]
    xt = [[rng.gauss(0, 1) for _ in range(p)] for _ in range(ntest)]
    yt = [sum(a * b for a, b in zip(r, beta)) for r in xt]
    theta0 = [rng.gauss(0, 0.5) for _ in range(p)]
    return xs, ys, xt, yt, theta0


def test_prune_counts_and_nested_masks():
    xs, ys, _, _, theta0 = sparse_problem(7)
    _, grad = least_squares(xs, ys)
    _, _, hist = imp(theta0, grad, 8, F(1, 5), 0.05, 50)
    counts = [sum(h["mask"]) for h in hist]
    assert counts == [40, 32, 26, 21, 17, 14, 12, 10, 8]
    for a, b in zip(hist, hist[1:]):
        assert all(mb <= ma for ma, mb in zip(a["mask"], b["mask"]))


def test_rewind_to_init_and_pruned_weights_stay_zero():
    xs, ys, _, _, theta0 = sparse_problem(8)
    _, grad = least_squares(xs, ys)
    _, _, hist = imp(theta0, grad, 3, F(1, 4), 0.05, 40)
    for h in hist[1:]:
        assert h["start"] == [t * m for t, m in zip(theta0, h["mask"])]
        assert all(w == 0 for w, m in zip(h["trained"], h["mask"]) if not m)


def test_late_rewinding_resets_to_the_dense_iterate():
    xs, ys, _, _, theta0 = sparse_problem(9)
    _, grad = least_squares(xs, ys)
    dense = masked_gd(theta0, [1] * 40, grad, 0.05, 40)
    _, _, hist = imp(theta0, grad, 2, F(1, 2), 0.05, 40, rewind=5)
    for h in hist[1:]:
        assert h["start"] == [t * m for t, m in zip(dense[5], h["mask"])]
    with pytest.raises(ValueError):
        imp(theta0, grad, 1, F(1, 2), 0.05, 40, rewind=41)


def test_magnitude_prune_removes_the_smallest_alive_weights():
    rng = random.Random(3)
    for _ in range(20):
        theta = [rng.uniform(-1, 1) for _ in range(15)]
        mask = [rng.randint(0, 1) for _ in range(15)]
        new = magnitude_prune(theta, mask, F(1, 3))
        removed = [i for i in range(15) if mask[i] and not new[i]]
        kept = [i for i in range(15) if new[i]]
        assert len(removed) == sum(mask) // 3
        assert all(new[i] <= mask[i] for i in range(15))
        assert all(abs(theta[r]) <= abs(theta[k]) for r in removed for k in kept)


def test_ticket_beats_random_mask_of_the_same_size_on_a_sparse_problem():
    xs, ys, xt, yt, theta0 = sparse_problem(7)
    _, grad = least_squares(xs, ys)
    test_loss, _ = least_squares(xt, yt)
    mask, trained, hist = imp(theta0, grad, 8, F(1, 5), 0.05, 300)
    assert all(mask[j] for j in range(5))
    dense_test = test_loss(hist[0]["trained"])
    ticket_test = test_loss(trained)
    assert ticket_test < 0.1 * dense_test
    for seed in range(3):
        rm = random_mask(40, sum(mask), random.Random(seed))
        rt = masked_gd(theta0, rm, grad, 0.05, 300)[-1]
        assert ticket_test < test_loss(rt)
