# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/viterbi-training/. The authors are listed in prov/W6039V.jsonl.

import math
import random
from itertools import product

import pytest

from nlslog import safe_log
from viterbi_training import (
    hard_counts,
    log_likelihood,
    reestimate,
    uniform_segmentation_start,
    viterbi_path,
    viterbi_training,
)


def joint(pi, A, B, obs, q):
    s = safe_log(pi[q[0]]) + safe_log(B[q[0]][obs[0]])
    for t in range(1, len(obs)):
        s += safe_log(A[q[t - 1]][q[t]]) + safe_log(B[q[t]][obs[t]])
    return s


def best_brute(pi, A, B, obs):
    N = len(pi)
    return max(joint(pi, A, B, obs, q) for q in product(range(N), repeat=len(obs)))


def objective(seqs, pi, A, B):
    return sum(best_brute(pi, A, B, o) for o in seqs)


def row(rng, n):
    xs = [rng.uniform(0.05, 1.0) for _ in range(n)]
    s = sum(xs)
    return [x / s for x in xs]


def random_hmm(rng, N, M):
    return row(rng, N), [row(rng, N) for _ in range(N)], [row(rng, M) for _ in range(N)]


def logs(m):
    return [[safe_log(p) for p in r] for r in m]


def test_alignment_step_against_brute_force():
    rng = random.Random(1)
    for _ in range(100):
        N, M = rng.randint(1, 3), rng.randint(2, 3)
        pi, A, B = random_hmm(rng, N, M)
        obs = [rng.randrange(M) for _ in range(rng.randint(1, 6))]
        q, s = viterbi_path([safe_log(p) for p in pi], logs(A), logs(B), obs)
        assert s == pytest.approx(best_brute(pi, A, B, obs), abs=1e-9)
        assert joint(pi, A, B, obs, q) == pytest.approx(s, abs=1e-9)


def test_reestimate_maximizes_the_joint_of_fixed_paths():
    rng = random.Random(2)
    for _ in range(30):
        N, M = 2, 3
        pi, A, B = random_hmm(rng, N, M)
        seqs = [[rng.randrange(M) for _ in range(rng.randint(2, 6))] for _ in range(3)]
        paths = [[rng.randrange(N) for _ in o] for o in seqs]
        p2, A2, B2 = reestimate(seqs, paths, pi, A, B)
        best = sum(joint(p2, A2, B2, o, q) for o, q in zip(seqs, paths))
        for _ in range(50):
            p3, A3, B3 = random_hmm(rng, N, M)
            assert sum(joint(p3, A3, B3, o, q) for o, q in zip(seqs, paths)) <= best + 1e-12


def test_counts():
    n_pi, n_A, n_B = hard_counts([[0, 1, 1], [1, 0]], [[0, 0, 1], [1, 1]], 2, 2)
    assert n_pi == [1, 1]
    assert n_A == [[1, 1], [0, 1]]
    assert n_B == [[1, 1], [1, 2]]


def test_objective_never_decreases_and_stops():
    rng = random.Random(3)
    for _ in range(40):
        N, M = rng.randint(2, 3), rng.randint(2, 4)
        pi, A, B = random_hmm(rng, N, M)
        seqs = [[rng.randrange(M) for _ in range(rng.randint(2, 6))] for _ in range(rng.randint(1, 4))]
        _, _, _, hist = viterbi_training(seqs, pi, A, B, max_rounds=200)
        assert len(hist) < 200
        assert all(hist[k + 1] >= hist[k] - 1e-9 for k in range(len(hist) - 1))
        assert hist[0] == pytest.approx(objective(seqs, pi, A, B), abs=1e-9)


def test_rows_sum_to_one():
    rng = random.Random(4)
    pi, A, B = random_hmm(rng, 3, 4)
    seqs = [[rng.randrange(4) for _ in range(8)] for _ in range(5)]
    p2, A2, B2, _ = viterbi_training(seqs, pi, A, B)
    for r in [p2] + A2 + B2:
        assert sum(r) == pytest.approx(1.0, abs=1e-12)
        assert all(0 <= x <= 1 for x in r)


def test_total_likelihood_can_decrease():
    # The example of the page: O = (x, y, x), two states.
    seqs = [[0, 1, 0]]
    pi, A, B = [0.2, 0.8], [[0.5, 0.5], [0.5, 0.5]], [[0.8, 0.2], [0.5, 0.5]]
    p2, A2, B2, hist = viterbi_training(seqs, pi, A, B, max_rounds=1)
    assert math.exp(hist[0]) == pytest.approx(0.04, abs=1e-12)
    assert p2 == [0.0, 1.0] and B2 == [[1.0, 0.0], [0.5, 0.5]]
    assert math.exp(log_likelihood(seqs, pi, A, B)) == pytest.approx(0.1274, abs=1e-12)
    assert math.exp(log_likelihood(seqs, p2, A2, B2)) == pytest.approx(0.09375, abs=1e-12)
    assert math.exp(objective(seqs, p2, A2, B2)) == pytest.approx(0.0625, abs=1e-12)


def sample(rng, pi, A, B, T):
    def draw(p):
        u, c = rng.random(), 0.0
        for i, x in enumerate(p):
            c += x
            if u < c:
                return i
        return len(p) - 1

    q, out = draw(pi), []
    for _ in range(T):
        out.append(draw(B[q]))
        q = draw(A[q])
    return out


def test_learns_a_left_to_right_model():
    rng = random.Random(5)
    pi = [1.0, 0.0, 0.0]
    A = [[0.8, 0.2, 0.0], [0.0, 0.8, 0.2], [0.0, 0.0, 1.0]]
    B = [[0.9, 0.05, 0.05], [0.05, 0.9, 0.05], [0.05, 0.05, 0.9]]
    seqs = [sample(rng, pi, A, B, 20) for _ in range(30)]
    # A start from equal segments learns the model.
    p0, A0, B0 = uniform_segmentation_start(seqs, 3, 3)
    p2, A2, B2, hist = viterbi_training(seqs, p0, A0, B0)
    assert all(hist[k + 1] >= hist[k] - 1e-9 for k in range(len(hist) - 1))
    for j in range(3):
        assert B2[j][j] > 0.85
    assert A2[0][2] == 0.0 and A2[1][0] == 0.0  # zeros of the topology stay zero
    assert abs(A2[0][0] - 0.8) < 0.1 and abs(A2[1][1] - 0.8) < 0.1
    good = hist[-1]
    # A near-flat start gets stuck at a worse fixed point: a local optimum.
    init_A = [[0.5, 0.5, 0.0], [0.0, 0.5, 0.5], [0.0, 0.0, 1.0]]
    init_B = [[0.4, 0.3, 0.3], [0.3, 0.4, 0.3], [0.3, 0.3, 0.4]]
    _, A3, B3, hist3 = viterbi_training(seqs, pi, init_A, init_B)
    assert hist3[-1] < good - 100
    assert A3[0] == [0.0, 1.0, 0.0]


def test_zero_probability_sequence():
    with pytest.raises(ValueError):
        viterbi_training([[1]], [1.0, 0.0], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]])
