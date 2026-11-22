# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/correlation-power-analysis/. The authors are listed in prov/H5FN0Q.jsonl.

import math
import random
import statistics

import pytest
from correlation_power_analysis import (
    PRESENT_SBOX,
    correlation_power_analysis,
    hamming_weight,
    simulate_traces,
    traces_needed,
)

IDENTITY = tuple(range(16))


def oracle_scores(traces, sbox, signed):
    """Scores written out with statistics.correlation."""
    t_len = len(traces[0][1])
    out = []
    for g in range(len(sbox)):
        h = [float(hamming_weight(sbox[p ^ g])) for p, _ in traces]
        rs = []
        for j in range(t_len):
            col = [row[j] for _, row in traces]
            try:
                rs.append(statistics.correlation(h, col))
            except statistics.StatisticsError:
                rs.append(0.0)
        out.append(max(rs) if signed else max(abs(r) for r in rs))
    return out


def exact_correlation(delta):
    """Exact corr(HW(S(X)), HW(S(X ^ delta))) for X uniform on 4 bits."""
    a = [hamming_weight(PRESENT_SBOX[x]) for x in range(16)]
    b = [hamming_weight(PRESENT_SBOX[x ^ delta]) for x in range(16)]
    return statistics.correlation(a, b)


def balanced_traces(key, sbox=PRESENT_SBOX):
    return [(p, [float(hamming_weight(sbox[p ^ key]))]) for p in range(16)]


def test_worked_example() -> None:
    best, scores = correlation_power_analysis(balanced_traces(0xB), signed=True)
    assert best == 0xB
    want = [0.125, 0.5, 0.375, -0.5, -0.625, 0.5, 0.125, -0.5,
            0.25, -0.375, -0.25, 1.0, 0.25, -0.75, -0.25, 0.125]
    assert scores == pytest.approx(want, abs=1e-12)
    _, absolute = correlation_power_analysis(balanced_traces(0xB))
    assert sorted(absolute, reverse=True)[:2] == pytest.approx([1.0, 0.75])


def test_noiseless_scores_are_the_exact_correlations() -> None:
    for key in range(16):
        best, scores = correlation_power_analysis(balanced_traces(key), signed=True)
        assert best == key
        for g in range(16):
            assert scores[g] == pytest.approx(exact_correlation(g ^ key), abs=1e-12)
    assert max(abs(exact_correlation(d)) for d in range(1, 16)) == pytest.approx(0.75)


def test_linear_target_pitfall() -> None:
    # Without the S-box, HW(p ^ g) and HW(p ^ g ^ 0xF) are exact negatives.
    for key in range(16):
        _, scores = correlation_power_analysis(balanced_traces(key, IDENTITY), sbox=IDENTITY)
        assert scores[key] == pytest.approx(1.0)
        assert scores[key ^ 0xF] == pytest.approx(1.0)


def test_edges() -> None:
    with pytest.raises(ValueError):
        correlation_power_analysis([])
    best, scores = correlation_power_analysis([(3, [0.5])])
    assert best == 0 and scores == [0.0] * 16
    best, scores = correlation_power_analysis([(1, [2.0]), (2, [2.0]), (7, [2.0])])
    assert scores == [0.0] * 16


def test_against_oracle_random() -> None:
    rng = random.Random(20240502)
    for _ in range(500):
        m = rng.randrange(2, 12)
        t_len = rng.randrange(1, 4)
        signed = rng.random() < 0.5
        traces = [(rng.randrange(16), [rng.uniform(-3, 3) for _ in range(t_len)]) for _ in range(m)]
        best, scores = correlation_power_analysis(traces, signed=signed)
        want = oracle_scores(traces, PRESENT_SBOX, signed)
        assert scores == pytest.approx(want, abs=1e-9)
        assert want[best] == pytest.approx(max(want), abs=1e-9)


def test_correlation_of_the_right_key() -> None:
    # rho = 1 / sqrt(1 + sigma^2) for epsilon = 1, since Var(HW) = 1.
    rng = random.Random(3)
    rho = 1.0 / math.sqrt(2.0)
    for _ in range(3):
        traces = simulate_traces(rng, 5, m=2000, sigma=1.0, samples=1, leak_sample=0)
        _, scores = correlation_power_analysis(traces)
        assert abs(scores[5] - rho) < 0.05


def test_success_rate_with_noise() -> None:
    rng = random.Random(9)
    runs = 20
    hits = 0
    for _ in range(runs):
        key = rng.randrange(16)
        best, _ = correlation_power_analysis(simulate_traces(rng, key, m=200, sigma=1.0))
        hits += best == key
    assert hits >= runs - 1


def test_rule_of_thumb() -> None:
    assert traces_needed(1.0 / math.sqrt(2.0)) == pytest.approx(38.61, abs=0.01)
    assert traces_needed(0.5) == pytest.approx(94.7, abs=0.1)
    assert traces_needed(0.1) == pytest.approx(2750.8, abs=0.5)
