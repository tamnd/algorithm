# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gru4rec/. The authors are listed in prov/6CBA3Q.jsonl.

import math
import random

import pytest

import gru4rec as g

FD_STEP = 1e-6
FD_TOL = 1e-6


def cyclic_sessions(seed: int, n: int, count: int) -> list[list[int]]:
    """Sessions in which the item after x is always (x + 1) mod n."""
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        s, length = rng.randrange(n), rng.randint(3, 6)
        out.append([(s + k) % n for k in range(length)])
    return out


@pytest.mark.parametrize("kind", ["bpr", "top1"])
def test_every_gradient_matches_finite_differences(kind):
    p = g.init(5, 3, seed=7, scale=0.6)
    for row in p["c"]:
        for c in range(len(row)):
            row[c] = 0.1 * (c - 2)
    xs, ys = [0, 3, 1, 4], [3, 1, 4, 2]
    negs = [[1, 2], [0, 4], [2], [0, 1, 3]]
    h0 = [0.2, -0.3, 0.1]
    _, grads, _ = g.sequence_loss_and_grad(p, xs, ys, negs, h0, kind)
    for name, mat in p.items():
        for r in range(len(mat)):
            for c in range(len(mat[r])):
                old = mat[r][c]
                mat[r][c] = old + FD_STEP
                up = g.sequence_loss_and_grad(p, xs, ys, negs, h0, kind)[0]
                mat[r][c] = old - FD_STEP
                down = g.sequence_loss_and_grad(p, xs, ys, negs, h0, kind)[0]
                mat[r][c] = old
                fd = (up - down) / (2 * FD_STEP)
                assert abs(fd - grads[name][r][c]) <= FD_TOL * max(1.0, abs(fd)), (name, r, c)


@pytest.mark.parametrize("kind", ["bpr", "top1"])
def test_loss_derivative_in_the_scores(kind):
    rs = [0.3, -0.2, 0.5, 1.1]
    _, d = g.step_loss(kind, rs)
    for k in range(len(rs)):
        up, down = rs[:], rs[:]
        up[k] += FD_STEP
        down[k] -= FD_STEP
        fd = (g.step_loss(kind, up)[0] - g.step_loss(kind, down)[0]) / (2 * FD_STEP)
        assert abs(fd - d[k]) <= FD_TOL


def test_session_parallel_batches_cover_every_event_once():
    sessions = [[0, 1, 2, 3], [4, 5], [6], [7, 8, 9], [1, 3, 5, 7, 9], [2, 4]]
    batches = g.session_parallel_batches(sessions, 3)
    seen = []
    for batch in batches:
        assert len(batch) <= 3
        assert len({s for s, _, _, _ in batch}) == len(batch)
        seen.extend(batch)
    expected = []
    for s, seq in enumerate(sessions):
        expected.extend((s, seq[t], seq[t + 1], t == 0) for t in range(len(seq) - 1))
    assert sorted(seen) == sorted(expected)
    for s, seq in enumerate(sessions):
        order = [(x, y) for b in batches for s2, x, y, _ in b if s2 == s]
        assert order == [(seq[t], seq[t + 1]) for t in range(len(seq) - 1)]
    assert batches[0] == [(0, 0, 1, True), (1, 4, 5, True), (3, 7, 8, True)]
    assert batches[1] == [(0, 1, 2, False), (4, 1, 3, True), (3, 8, 9, False)]


def test_page_example():
    p = {
        "Wz": [[0.0]], "Wr": [[0.0]], "Wh": [[math.log(3.0)]],
        "Uz": [[0.0]], "Ur": [[0.0]], "Uh": [[0.0]],
        "O": [[1.0], [-1.0]], "c": [[0.0, 0.0]],
    }
    c = g.gru_step(p, 0, [0.0])
    assert c["z"] == [0.5] and c["r"] == [0.5]
    assert abs(c["hh"][0] - 0.8) <= 1e-12
    assert abs(c["h"][0] - 0.4) <= 1e-12
    rs = g.scores(p, c["h"], [0, 1])
    bpr, d_bpr = g.step_loss("bpr", rs)
    top1, _ = g.step_loss("top1", rs)
    assert abs(bpr - math.log1p(math.exp(-0.8))) <= 1e-12
    assert abs(bpr - 0.3711006659477777) <= 1e-12
    assert abs(d_bpr[0] + 1 / (1 + math.exp(0.8))) <= 1e-12
    assert abs(top1 - (1 / (1 + math.exp(0.8)) + 1 / (1 + math.exp(-0.16)))) <= 1e-12


@pytest.mark.parametrize("kind", ["bpr", "top1"])
def test_training_learns_a_cyclic_pattern(kind):
    n = 6
    sessions = cyclic_sessions(4, n, 30)
    before = g.init(n, 6, seed=2)
    p = g.train(sessions, n, 6, 5, 10, 0.1, kind, seed=2)
    hits_before = sum(g.next_items(before, [(x - 1) % n, x], n, 1) == [(x + 1) % n] for x in range(n))
    hits = sum(g.next_items(p, [(x - 1) % n, x], n, 1) == [(x + 1) % n] for x in range(n))
    assert hits_before <= 2
    assert hits == n


def test_unknown_loss_is_rejected():
    with pytest.raises(ValueError):
        g.step_loss("hinge", [0.0, 1.0])
