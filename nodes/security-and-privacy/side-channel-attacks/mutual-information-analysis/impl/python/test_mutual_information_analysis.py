# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutual-information-analysis/. The authors are listed in prov/DNRK95.jsonl.

import math
import random
import statistics
from collections import Counter

import pytest
from mutual_information_analysis import (
    PRESENT_SBOX,
    hamming_weight,
    mutual_information_analysis,
    simulate_traces,
)


def quad(w: int) -> float:
    return float((w - 2) ** 2)


def oracle_mi(xs, ys):
    """I(X; Y) in bits as the sum of p(x, y) log p(x, y) / (p(x) p(y))."""
    n = len(xs)
    px = Counter(xs)
    py = Counter(ys)
    total = 0.0
    for (x, y), c in Counter(zip(xs, ys)).items():
        total += c / n * math.log2(c * n / (px[x] * py[y]))
    return total


def oracle_bins(column, bins):
    lo, hi = min(column), max(column)
    if hi == lo:
        return [0] * len(column)
    out = []
    for v in column:
        b = 0
        while b < bins - 1 and v >= lo + (b + 1) * (hi - lo) / bins:
            b += 1
        out.append(b)
    return out


def oracle_scores(traces, bins, model):
    t_len = len(traces[0][1])
    cols = [oracle_bins([row[j] for _, row in traces], bins) for j in range(t_len)]
    return [
        max(oracle_mi([model(PRESENT_SBOX[p ^ g]) for p, _ in traces], cols[j]) for j in range(t_len))
        for g in range(16)
    ]


def balanced_traces(key, leak=float):
    return [(p, [leak(hamming_weight(PRESENT_SBOX[p ^ key]))]) for p in range(16)]


def test_worked_example() -> None:
    best, scores = mutual_information_analysis(balanced_traces(0xB), bins=5)
    assert best == 0xB
    assert scores[0xB] == pytest.approx(2.0306390622, abs=1e-9)
    assert sorted(scores, reverse=True)[1] == pytest.approx(1.2806390622, abs=1e-9)
    for g in range(16):
        a = [hamming_weight(PRESENT_SBOX[p ^ 0xB]) for p in range(16)]
        b = [hamming_weight(PRESENT_SBOX[p ^ g]) for p in range(16)]
        assert scores[g] == pytest.approx(oracle_mi(a, b), abs=1e-9)


def test_noiseless_recovers_every_key() -> None:
    for key in range(16):
        assert mutual_information_analysis(balanced_traces(key), bins=5)[0] == key


def test_injective_model_pitfall() -> None:
    # With the S-box output itself as the model, every guess scores H(HW).
    _, scores = mutual_information_analysis(balanced_traces(3), bins=5, model=lambda v: v)
    assert all(s == pytest.approx(2.0306390622, abs=1e-9) for s in scores)


def test_too_many_bins_pitfall() -> None:
    # With one trace in each bin, the score of g is only H of its model values.
    rng = random.Random(5)
    traces = [(rng.randrange(16), [float(i)]) for i in range(30)]
    _, scores = mutual_information_analysis(traces, bins=60)
    assert len(set(oracle_bins([row[0] for _, row in traces], 60))) == 30
    for g in range(16):
        h = [hamming_weight(PRESENT_SBOX[p ^ g]) for p, _ in traces]
        n = len(h)
        ent = -sum(c / n * math.log2(c / n) for c in Counter(h).values())
        assert scores[g] == pytest.approx(ent, abs=1e-9)


def test_nonlinear_leakage() -> None:
    # Leakage (HW - 2)^2 has zero correlation with HW at the right key.
    want = [1.4056, 0.4528, 0.5613, 0.2806, 0.5613, 0.4528, 0.3113, 0.2806,
            0.2335, 0.3113, 0.6556, 0.5841, 0.2335, 0.5841, 0.6556, 1.0]
    for key in range(16):
        best, scores = mutual_information_analysis(balanced_traces(key, quad), bins=4)
        assert best == key
        for g in range(16):
            assert scores[g] == pytest.approx(want[g ^ key], abs=1e-4)
    a = [hamming_weight(PRESENT_SBOX[x]) for x in range(16)]
    b = [quad(w) for w in a]
    assert statistics.covariance(a, b) == pytest.approx(0.0, abs=1e-12)


def test_edges() -> None:
    with pytest.raises(ValueError):
        mutual_information_analysis([])
    best, scores = mutual_information_analysis([(2, [1.0, 1.0])])
    assert best == 0 and scores == [0.0] * 16


def test_against_oracle_random() -> None:
    rng = random.Random(20240503)
    for _ in range(500):
        m = rng.randrange(1, 14)
        t_len = rng.randrange(1, 3)
        bins = rng.randrange(1, 6)
        identity = rng.random() < 0.3
        model = (lambda v: v) if identity else hamming_weight
        traces = [(rng.randrange(16), [rng.uniform(-3, 3) for _ in range(t_len)]) for _ in range(m)]
        best, scores = mutual_information_analysis(traces, bins=bins, model=model)
        want = oracle_scores(traces, bins, model)
        assert scores == pytest.approx(want, abs=1e-9)
        assert want[best] == pytest.approx(max(want), abs=1e-9)


def test_success_rate_with_noise() -> None:
    rng = random.Random(13)
    runs = 20
    hits_hw = hits_quad = 0
    for _ in range(runs):
        key = rng.randrange(16)
        t = simulate_traces(rng, key, m=200, sigma=1.0)
        hits_hw += mutual_information_analysis(t)[0] == key
        t = simulate_traces(rng, key, m=400, sigma=1.0, leak=quad)
        hits_quad += mutual_information_analysis(t)[0] == key
    assert hits_hw >= runs - 2
    assert hits_quad >= runs - 2
