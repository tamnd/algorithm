# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pyin/. The authors are listed in prov/FCGMHH.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from nlslog import NEG_INF, safe_log
from pyin import (
    beta_cdf,
    bin_frequency,
    candidates,
    cmndf,
    difference,
    initial,
    observations,
    pitch_transition,
    pyin,
    threshold_prior,
    transition_prob,
    viterbi,
    yin_period,
)

FS = 8000


def tone(n, f=220.0, noise=0.0, seed=0):
    rng = random.Random(seed)
    return [
        0.6 * math.sin(2 * math.pi * f * i / FS) + 0.3 * math.sin(4 * math.pi * f * i / FS + 0.5) + rng.gauss(0, noise)
        for i in range(n)
    ]


def test_prior_sums_to_one_exactly_and_has_mean_near_one_tenth():
    prior = threshold_prior()
    assert len(prior) == 100
    assert sum(prior) == 1
    assert all(p > 0 for p in prior)
    mean = sum(Fraction(i, 100) * p for i, p in enumerate(prior, 1))
    assert abs(float(mean) - 0.105) < 1e-3  # right ends of the bins of a Beta(2, 18) with mean 0.1
    assert max(range(100), key=lambda i: prior[i]) == 5  # s = 0.06, near the mode 1/18


def test_beta_cdf_matches_numerical_integration():
    def pdf(x):
        return 342 * x * (1 - x) ** 17  # Beta(2, 18): 1 / B(2, 18) = 19! / (1! 17!) = 18 * 19

    for x in (0.05, 0.1, 0.3):
        n = 1000
        h = x / n
        simpson = h / 3 * sum((1 if k in (0, n) else 4 if k % 2 else 2) * pdf(k * h) for k in range(n + 1))
        assert abs(beta_cdf(x, 2, 18) - simpson) < 1e-9


def test_yin_period_is_the_smallest_local_minimum_below_the_threshold():
    rng = random.Random(4)
    for _ in range(300):
        dp = [rng.random() for _ in range(15)]
        s = rng.random()
        lo, hi = 2, 13
        got = yin_period(dp, s, lo, hi)
        brute = [t for t in range(lo, hi + 1) if dp[t] < s and (t == hi or dp[t + 1] >= dp[t])]
        if brute:
            assert got == (brute[0], True)
        else:
            assert got == (min(range(lo, hi + 1), key=lambda t: (dp[t], t)), False)


def test_candidate_mass_is_the_sum_over_thresholds():
    frame = tone(400, noise=0.12, seed=3)
    prior = threshold_prior()
    cands = candidates(frame, FS, 200, 55, 880, prior)
    dp = cmndf(difference(frame, 200, 147))
    total = 0.0
    for i in range(1, 101):
        _, below = yin_period(dp, i / 100, 9, 146)
        total += (1.0 if below else 0.01) * float(prior[i - 1])
    assert abs(sum(p for _, p in cands) - total) < 1e-12
    assert 0 < total < 1
    assert len(cands) >= 2  # noise splits the mass between periods


def test_clean_sine_gives_one_certain_candidate():
    frame = [math.sin(2 * math.pi * 200 * i / FS) for i in range(400)]
    cands = candidates(frame, FS, 200, 55, 880, threshold_prior())
    assert len(cands) == 1
    f, p = cands[0]
    assert abs(f - 200) < 0.1
    assert abs(p - 1) < 1e-12


def brute_force_best(obs, m, jump, p_stay, start):
    rows = pitch_transition(m, jump)
    init = initial(m, start)
    best = NEG_INF
    for seq in itertools.product(range(2 * m), repeat=len(obs)):
        score = init[seq[0]] + safe_log(obs[0][seq[0]])
        for t in range(1, len(obs)):
            score += safe_log(transition_prob(seq[t - 1], seq[t], m, rows, p_stay)) + safe_log(obs[t][seq[t]])
        best = max(best, score)
    return best


def path_score(path, obs, m, jump, p_stay, start):
    rows = pitch_transition(m, jump)
    score = initial(m, start)[path[0]] + safe_log(obs[0][path[0]])
    for t in range(1, len(obs)):
        score += safe_log(transition_prob(path[t - 1], path[t], m, rows, p_stay)) + safe_log(obs[t][path[t]])
    return score


def test_viterbi_matches_brute_force():
    rng = random.Random(11)
    for trial in range(6):
        m, jump, frames = 3, 1, 4
        obs = []
        for _ in range(frames):
            p = [rng.random() for _ in range(m)]
            z = sum(p) * rng.uniform(1.0, 2.0)
            p = [v / z for v in p]  # candidate mass per bin, total below 1
            obs.append([0.5 * v for v in p] + [0.5 * (1 - sum(p))] * m)
        for start in ("all", "unvoiced"):
            path, score = viterbi(obs, m, jump, 0.9, start)
            best = brute_force_best(obs, m, jump, 0.9, start)
            assert abs(score - best) < 1e-9
            assert abs(path_score(path, obs, m, jump, 0.9, start) - best) < 1e-9


def test_log_space_survives_where_the_product_underflows():
    m, frames = 2, 400
    obs = [[1e-3, 1e-4, 1e-5, 1e-5] for _ in range(frames)]
    assert math.prod(o[0] for o in obs) == 0.0
    path, score = viterbi(obs, m, 1, 0.99)
    assert path == [0] * frames
    assert math.isfinite(score)


def test_paper_start_fails_when_the_first_frame_is_surely_voiced():
    obs = [observations([(220.0, 1.0)], 3, 220.0), observations([(220.0, 0.5)], 3, 220.0)]
    assert obs[0] == [0.5, 0.0, 0.0, 0.0, 0.0, 0.0]
    with pytest.raises(ValueError):
        viterbi(obs, 3, 1, 0.99, "unvoiced")
    path, _ = viterbi(obs, 3, 1, 0.99, "all")
    assert path[0] < 3


def test_track_of_a_tone_then_silence():
    x = tone(1000, noise=0.05, seed=3) + [0.0] * 600
    track = pyin(x, FS, 200, 200, m_bins=250)
    assert track == [220.0] * 4 + [None] * 3
    assert bin_frequency(240) == 220.0
