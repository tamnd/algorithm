# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gmm-ubm-speaker-verification/. The authors are listed in prov/AXV6G0.jsonl.

import math
import random

import pytest

from gmm_ubm_speaker_verification import (
    bayes_threshold,
    decide,
    enroll,
    frame_loglik,
    score,
    score_top_c,
)

UBM1 = ([0.5, 0.5], [[-1.0], [1.0]], [[1.0], [1.0]])


def plain_density(x, gmm):
    w, mu, var = gmm
    tot = 0.0
    for c, m, v in zip(w, mu, var):
        p = c
        for xi, mi, vi in zip(x, m, v):
            p *= math.exp(-0.5 * (xi - mi) ** 2 / vi) / math.sqrt(2 * math.pi * vi)
        tot += p
    return tot


def random_ubm(rng, M, d):
    w = [rng.uniform(0.5, 1.5) for _ in range(M)]
    z = sum(w)
    return ([x / z for x in w], [[rng.uniform(-3, 3) for _ in range(d)] for _ in range(M)],
            [[rng.uniform(0.5, 1.5) for _ in range(d)] for _ in range(M)])


def draw(rng, gmm, T):
    w, mu, var = gmm
    out = []
    for _ in range(T):
        u, m, acc = rng.random(), 0, w[0]
        while u > acc and m < len(w) - 1:
            m += 1
            acc += w[m]
        out.append([rng.gauss(a, math.sqrt(v)) for a, v in zip(mu[m], var[m])])
    return out


def test_page_example():
    spk = enroll([[1.5], [2.0], [2.5], [0.5]], UBM1, r=4.0)
    assert spk[1][0][0] == pytest.approx(-0.861932, abs=1e-6)
    assert spk[1][1][0] == pytest.approx(1.337217, abs=1e-6)
    assert spk[0] == UBM1[0] and spk[2] == UBM1[2]
    assert score([[1.8], [2.2]], spk, UBM1) == pytest.approx(0.283261, abs=1e-6)
    assert score([[-1.2], [0.8]], spk, UBM1) == pytest.approx(-0.067896, abs=1e-6)


def test_score_against_direct_ratio_of_products():
    rng = random.Random(1)
    ubm = random_ubm(rng, 4, 3)
    spk = enroll(draw(rng, ubm, 50), ubm, r=8.0)
    test = draw(rng, ubm, 6)
    num = 1.0
    den = 1.0
    for y in test:
        num *= plain_density(y, spk)
        den *= plain_density(y, ubm)
    assert score(test, spk, ubm) == pytest.approx(math.log(num / den) / len(test), abs=1e-10)
    for y in test:
        assert frame_loglik(y, ubm) == pytest.approx(math.log(plain_density(y, ubm)), abs=1e-10)


def test_log_space_where_the_product_underflows():
    rng = random.Random(2)
    ubm = random_ubm(rng, 4, 3)
    spk = enroll(draw(rng, ubm, 40), ubm)
    test = draw(rng, ubm, 200)
    prod = 1.0
    for y in test:
        prod *= plain_density(y, ubm)
    assert prod == 0.0
    s = score(test, spk, ubm)
    assert math.isfinite(s)
    assert s == pytest.approx(sum(frame_loglik(y, spk) - frame_loglik(y, ubm) for y in test) / 200, abs=1e-9)


def test_ubm_against_itself_scores_zero_and_large_r_gives_the_ubm():
    rng = random.Random(3)
    ubm = random_ubm(rng, 3, 2)
    test = draw(rng, ubm, 20)
    assert score(test, ubm, ubm) == 0.0
    spk = enroll(draw(rng, ubm, 30), ubm, r=1e15)
    assert abs(score(test, spk, ubm)) < 1e-9


def test_enrollment_with_small_r_gives_the_ml_means():
    ubm = UBM1
    frames = [[1.5], [2.0], [2.5], [0.5]]
    spk = enroll(frames, ubm, r=1e-12)
    g = []
    for x in frames:
        a = 0.5 * math.exp(-0.5 * (x[0] + 1) ** 2)
        b = 0.5 * math.exp(-0.5 * (x[0] - 1) ** 2)
        g.append(b / (a + b))
    want = sum(gi * x[0] for gi, x in zip(g, frames)) / sum(g)
    assert spk[1][1][0] == pytest.approx(want, abs=1e-9)


def test_component_without_data_keeps_its_mean():
    ubm = ([0.5, 0.5], [[0.0], [1e4]], [[1.0], [1.0]])
    spk = enroll([[0.1], [-0.2]], ubm)
    assert spk[1][1] == [1e4]


def test_top_c():
    rng = random.Random(4)
    ubm = random_ubm(rng, 6, 2)
    spk = enroll(draw(rng, ubm, 40), ubm, r=2.0)
    test = draw(rng, ubm, 30)
    assert score_top_c(test, spk, ubm, C=6) == pytest.approx(score(test, spk, ubm), abs=1e-12)
    assert score_top_c(test, spk, ubm, C=3) == pytest.approx(score(test, spk, ubm), abs=0.05)
    assert score_top_c(test, spk, ubm, C=1) != score(test, spk, ubm)


def test_target_trials_score_higher_than_nontarget_trials():
    rng = random.Random(5)
    ubm = random_ubm(rng, 8, 2)

    def speaker(seed):
        r = random.Random(seed)
        return (ubm[0], [[a + r.uniform(-1.5, 1.5) for a in mu] for mu in ubm[1]], ubm[2])

    speakers = [speaker(s) for s in range(6)]
    models = [enroll(draw(rng, sp, 120), ubm, r=4.0) for sp in speakers]
    tgt, non = [], []
    for i, sp in enumerate(speakers):
        test = draw(rng, sp, 60)
        for j, mdl in enumerate(models):
            (tgt if i == j else non).append(score(test, mdl, ubm))
    assert min(tgt) > 0.0
    assert sum(tgt) / len(tgt) > sum(non) / len(non) + 0.05
    wins = sum(t > n for t in tgt for n in non)
    assert wins / (len(tgt) * len(non)) > 0.9


def test_decision_and_bayes_threshold():
    assert decide(0.5, 0.5) and not decide(0.49, 0.5)
    assert bayes_threshold(0.5) == 0.0
    assert bayes_threshold(0.01, c_miss=10.0, c_fa=1.0) == pytest.approx(math.log(9.9), abs=1e-12)


def test_empty_input():
    with pytest.raises(ValueError):
        score([], UBM1, UBM1)
    with pytest.raises(ValueError):
        enroll([[0.0]], UBM1, r=0.0)
