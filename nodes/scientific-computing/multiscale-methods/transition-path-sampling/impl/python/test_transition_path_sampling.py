# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transition-path-sampling/. The authors are listed in prov/MA0G4J.jsonl.
import math
import random

import pytest

from transition_path_sampling import transition_path_sampling

# Metropolis random walk on 0..4 with a barrier in the middle, beta = 1.
ENERGY = [0.0, 2.0, 3.0, 2.0, 0.0]
S = len(ENERGY)
N = 8
INITIAL = [0, 1, 2, 3, 4, 4, 4, 4, 4]


def step(i, rng):
    j = i + (1 if rng.random() < 0.5 else -1)
    if j < 0 or j >= S:
        return i
    if rng.random() < math.exp(-(ENERGY[j] - ENERGY[i])):
        return j
    return i


def in_a(i):
    return i == 0


def in_b(i):
    return i == S - 1


def transition_matrix():
    p = [[0.0] * S for _ in range(S)]
    for i in range(S):
        for j in (i - 1, i + 1):
            if 0 <= j < S:
                p[i][j] = 0.5 * min(1.0, math.exp(-(ENERGY[j] - ENERGY[i])))
        p[i][i] = 1.0 - sum(p[i])
    return p


def powers(p, n):
    out = [[[float(i == j) for j in range(S)] for i in range(S)]]
    for _ in range(n):
        a = out[-1]
        out.append([[sum(a[i][k] * p[k][j] for k in range(S)) for j in range(S)] for i in range(S)])
    return out


def exact_slice(k):
    """P(x_k = j) in the path ensemble: p^k(0, j) p^(N-k)(j, 4) / p^N(0, 4)."""
    pw = powers(transition_matrix(), N)
    z = pw[N][0][S - 1]
    return [pw[k][0][j] * pw[N - k][j][S - 1] / z for j in range(S)]


def first_entry(x):
    return next(t for t, v in enumerate(x) if in_b(v))


def test_exact_ensemble_of_the_page():
    assert [round(v, 4) for v in exact_slice(4)] == [0.1033, 0.2667, 0.2601, 0.2667, 0.1033]
    assert [round(v, 4) for v in exact_slice(2)] == [0.4642, 0.3406, 0.1952, 0.0, 0.0]


def test_paths_stay_reactive_and_keep_their_length():
    x, samples, accepted, work = transition_path_sampling(INITIAL, step, in_a, in_b, random.Random(7), 300)
    assert 0 < accepted < 300
    for path in samples:
        assert len(path) == N + 1 and in_a(path[0]) and in_b(path[-1])
        assert all(abs(a - b) <= 1 for a, b in zip(path, path[1:]))
    assert samples[-1] == x


def test_non_reactive_start_is_refused():
    with pytest.raises(ValueError):
        transition_path_sampling([0] * (N + 1), step, in_a, in_b, random.Random(1), 1)


def test_slice_and_first_entry_match_the_exact_ensemble():
    rng = random.Random(0)
    _, samples, _, work = transition_path_sampling(INITIAL, step, in_a, in_b, rng, 3500)
    assert work <= 10000
    n = len(samples)
    exact = exact_slice(4)
    for j in range(S):
        assert abs(sum(x[4] == j for x in samples) / n - exact[j]) < 0.08
    # Exact mean first entry time into B in the ensemble: 6.4283.
    assert abs(sum(first_entry(x) for x in samples) / n - 6.4283) < 0.3
