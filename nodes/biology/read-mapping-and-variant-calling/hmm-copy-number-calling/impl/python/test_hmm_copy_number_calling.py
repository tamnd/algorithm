# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmm-copy-number-calling/. The authors are listed in prov/HP6C4B.jsonl.

import itertools
import math
import random

from biostoch import logsumexp, poisson, poisson_pmf
from hmm_copy_number_calling import (backward, call_copy_number, emission_logs, forward, posteriors,
                                     segments, transition_logs, viterbi)

EXAMPLE = [19, 22, 10, 8, 11, 20, 21, 32, 29, 31]


def path_log_prob(path, init, T, E):
    s = init[path[0]] + E[0][path[0]]
    for t in range(1, len(path)):
        s += T[path[t - 1]][path[t]] + E[t][path[t]]
    return s


def brute(init, T, E):
    """The best path and the total log probability by enumeration of all K^n paths."""
    K, n = len(init), len(E)
    best, best_path, scores = -math.inf, None, []
    for path in itertools.product(range(K), repeat=n):
        s = path_log_prob(path, init, T, E)
        scores.append(s)
        if s > best + 1e-12:
            best, best_path = s, list(path)
    return best_path, best, logsumexp(scores)


def random_model(rng, K, n):
    lam = rng.uniform(5, 30)
    counts = [rng.randint(0, 40) for _ in range(n)]
    p = rng.uniform(0.01, 0.4)
    return [-math.log(K)] * K, transition_logs(K, p), emission_logs(counts, lam, K)


def test_emission_is_poisson():
    E = emission_logs([0, 7, 30], 20.0, 4, eps=0.05)
    for t, x in enumerate([0, 7, 30]):
        for c in range(4):
            assert abs(math.exp(E[t][c]) - poisson_pmf(x, 20.0 * max(c, 0.05) / 2)) < 1e-12


def test_transition_rows_sum_to_one():
    for K in (1, 2, 5):
        for row in transition_logs(K, 0.1):
            assert abs(sum(math.exp(v) for v in row) - 1.0) < 1e-12


def test_viterbi_and_forward_against_brute_force():
    rng = random.Random(4)
    for K, n in [(2, 1), (2, 8), (3, 7), (4, 5), (5, 4)]:
        for _ in range(6):
            init, T, E = random_model(rng, K, n)
            path, score = viterbi(init, T, E)
            bpath, bscore, btotal = brute(init, T, E)
            assert abs(score - bscore) < 1e-9
            assert path == bpath
            assert abs(path_log_prob(path, init, T, E) - score) < 1e-9
            _, total = forward(init, T, E)
            assert abs(total - btotal) < 1e-9


def test_backward_agrees_with_forward():
    rng = random.Random(5)
    init, T, E = random_model(rng, 3, 9)
    _, total = forward(init, T, E)
    B = backward(T, E)
    assert abs(logsumexp(init[c] + E[0][c] + B[0][c] for c in range(3)) - total) < 1e-9
    for row in posteriors(init, T, E):
        assert abs(sum(row) - 1.0) < 1e-12


def test_example_calls():
    path, segs = call_copy_number(EXAMPLE, K=4, p=0.1, lam=20.0)
    assert path == [2, 2, 1, 1, 1, 2, 2, 3, 3, 3]
    assert segs == [(0, 2, 2), (2, 5, 1), (5, 7, 2), (7, 10, 3)]
    init = [-math.log(4)] * 4
    T, E = transition_logs(4, 0.1), emission_logs(EXAMPLE, 20.0, 4)
    bpath, bscore, btotal = brute(init, T, E)
    assert path == bpath
    assert abs(bscore - (-36.532)) < 1e-3
    assert abs(btotal - (-35.482)) < 1e-3
    # The two diploid windows between the loss and the gain are not sure calls, and at
    # window 6 the state of largest posterior (3) is not the Viterbi state (2).
    post = posteriors(init, T, E)
    assert 0.57 < post[5][2] < 0.58
    assert 0.48 < post[6][2] < 0.49 < 0.51 < post[6][3] < 0.52
    # With p = 0.05 one jump from 1 to 3 is cheaper than the two jumps 1 to 2 to 3.
    path, _ = call_copy_number(EXAMPLE, K=4, p=0.05, lam=20.0)
    assert path == [2, 2, 1, 1, 1, 3, 3, 3, 3, 3]


def test_sticky_transition_merges_short_runs():
    # A very small switch probability makes one odd window too costly to call.
    path, _ = call_copy_number([20, 20, 20, 40, 20, 20, 20], K=5, p=1e-6, lam=20.0)
    assert path == [2] * 7
    path, _ = call_copy_number([20, 20, 20, 40, 20, 20, 20], K=5, p=0.1, lam=20.0)
    assert path == [2, 2, 2, 4, 2, 2, 2]


def test_segments_and_empty():
    assert segments([]) == []
    assert segments([1, 1, 0, 0, 0, 2]) == [(0, 2, 1), (2, 5, 0), (5, 6, 2)]
    assert call_copy_number([]) == ([], [])
    assert viterbi([0.0], [[0.0]], []) == ([], 0.0)


def test_simulated_genome():
    rng = random.Random(2007)
    truth = [(0, 120, 2), (120, 150, 1), (150, 260, 2), (260, 300, 3), (300, 320, 0), (320, 400, 2)]
    lam = 20.0
    states, counts = [], []
    for lo, hi, c in truth:
        for _ in range(lo, hi):
            states.append(c)
            counts.append(poisson(rng, lam * max(c, 0.05) / 2))
    path, segs = call_copy_number(counts, K=5, p=1e-3)
    wrong = sum(a != b for a, b in zip(path, states))
    assert wrong <= 4
    assert len(segs) == len(truth)
    for (lo, hi, c), (lo2, hi2, c2) in zip(segs, truth):
        assert c == c2 and abs(lo - lo2) <= 2 and abs(hi - hi2) <= 2
    # The mean count of the diploid windows is close to lam: z = 4 times sigma over sqrt(n).
    diploid = [x for x, c in zip(counts, states) if c == 2]
    mean = sum(diploid) / len(diploid)
    assert abs(mean - lam) <= 4 * math.sqrt(lam) / math.sqrt(len(diploid))
