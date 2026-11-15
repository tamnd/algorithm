# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sasrec/. The authors are listed in prov/QW5Y7Z.jsonl.

import random

import pytest

import sasrec as m

FD_STEP = 1e-6
FD_TOL = 1e-6


def random_params(seed: int) -> m.Params:
    """Random weights with gains and biases away from 1 and 0, so that every term is tested."""
    p = m.init(5, 4, 4, seed=seed, scale=0.6)
    rng = random.Random(seed + 100)
    for name in ("g1", "g2"):
        p[name] = [[rng.uniform(0.5, 1.5) for _ in range(4)]]
    for name in ("b1", "b2", "c1", "c2"):
        p[name] = [[rng.uniform(-0.3, 0.3) for _ in range(4)]]
    return p


def cyclic(seed: int, n: int, count: int) -> list[list[int]]:
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        s, length = rng.randrange(n), rng.randint(3, 5)
        out.append([(s + k) % n for k in range(length)])
    return out


@pytest.mark.parametrize("seed", [3, 8])
def test_every_gradient_matches_finite_differences(seed):
    p = random_params(seed)
    seq, pos, neg = [0, 3, 1, 4], [3, 1, 4, 2], [2, 0, 0, 1]
    _, grads = m.loss_and_grad(p, seq, pos, neg)
    for name, mat in p.items():
        for r in range(len(mat)):
            for c in range(len(mat[r])):
                old = mat[r][c]
                mat[r][c] = old + FD_STEP
                up = m.loss(p, seq, pos, neg)
                mat[r][c] = old - FD_STEP
                down = m.loss(p, seq, pos, neg)
                mat[r][c] = old
                fd = (up - down) / (2 * FD_STEP)
                assert abs(fd - grads[name][r][c]) <= FD_TOL * max(1.0, abs(fd)), (name, r, c)


def test_causal_mask_later_items_do_not_change_earlier_outputs():
    p = random_params(5)
    base = [0, 3, 1, 4]
    f, _ = m.forward(p, base)
    for t in range(1, len(base)):
        for other in range(5):
            changed = base[:t] + [other] + base[t + 1:]
            g, _ = m.forward(p, changed)
            for u in range(t):
                assert g[u] == f[u]
    g, _ = m.forward(p, [0, 3, 2, 2])
    assert g[3] != f[3]


def test_attention_rows_are_causal_distributions():
    p = random_params(6)
    _, cache = m.forward(p, [1, 2, 0, 3])
    for t, row in enumerate(cache["att"]):
        assert len(row) == t + 1
        assert abs(sum(row) - 1.0) <= 1e-12
        assert all(a > 0 for a in row)


def test_page_example():
    zero = [[0.0, 0.0], [0.0, 0.0]]
    p = {
        "M": [[2.0, 0.0], [0.0, 3.0], [1.0, 1.0]], "P": [[0.0, 0.0], [0.0, 1.0]],
        "g1": [[1.0, 1.0]], "b1": [[0.0, 0.0]],
        "WQ": zero, "WK": zero, "WV": [[1.0, 0.0], [0.0, 1.0]],
        "g2": [[1.0, 1.0]], "b2": [[0.0, 0.0]],
        "W1": zero, "c1": [[0.0, 0.0]], "W2": zero, "c2": [[0.0, 0.0]],
    }
    f, cache = m.forward(p, [0, 1])
    assert cache["e"] == [[2.0, 0.0], [0.0, 4.0]]
    for got, want in zip(cache["x"], ([1.0, -1.0], [-1.0, 1.0])):
        assert all(abs(a - b) <= 1e-6 for a, b in zip(got, want))
    assert cache["att"] == [[1.0], [0.5, 0.5]]
    for got, want in zip(f, ([3.0, -1.0], [0.0, 4.0])):
        assert all(abs(a - b) <= 1e-6 for a, b in zip(got, want))
    assert abs(m.dot(f[1], p["M"][2]) - 4.0) <= 1e-6
    assert m.next_items(p, [0, 1], 1) == [2]


def test_training_learns_a_cyclic_pattern():
    n = 6
    sequences = cyclic(4, n, 40)
    p = m.train(sequences, n + 2, 8, 20, 0.05, seed=2)
    before = m.init(n + 2, 8, 4, seed=2)

    def hits(q):
        total = 0
        for length in (1, 2, 3, 4):
            for x in range(n):
                prefix = [(x - length + 1 + k) % n for k in range(length)]
                total += m.next_items(q, prefix, 1) == [(x + 1) % n]
        return total

    assert hits(before) <= 12
    assert hits(p) == 24


def test_preconditions():
    with pytest.raises(ValueError):
        m.train([[0]], 3, 2, 1, 0.1)
    with pytest.raises(ValueError):
        m.train([[0, 1, 2]], 3, 2, 1, 0.1)
