# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/differential-power-analysis/. The authors are listed in prov/NV7DCA.jsonl.

import math
import random
import statistics

import pytest
from differential_power_analysis import (
    PRESENT_SBOX,
    differential_power_analysis,
    hamming_weight,
    simulate_traces,
)


def oracle_scores(traces, sbox, bit, signed):
    """Difference of means written out directly with statistics.mean."""
    t_len = len(traces[0][1])
    out = []
    for g in range(len(sbox)):
        ones = [row for p, row in traces if (sbox[p ^ g] >> bit) & 1]
        zeros = [row for p, row in traces if not (sbox[p ^ g] >> bit) & 1]
        if not ones or not zeros:
            out.append(-math.inf)
            continue
        delta = [
            statistics.mean(r[j] for r in ones) - statistics.mean(r[j] for r in zeros)
            for j in range(t_len)
        ]
        out.append(max(delta) if signed else max(abs(x) for x in delta))
    return out


def expected_difference(delta, bit):
    """Exact E[HW(S(X)) | bit of S(X ^ delta) = 1] - E[... = 0] for uniform X."""
    s = PRESENT_SBOX
    one = [hamming_weight(s[x]) for x in range(16) if (s[x ^ delta] >> bit) & 1]
    zero = [hamming_weight(s[x]) for x in range(16) if not (s[x ^ delta] >> bit) & 1]
    return sum(one) / len(one) - sum(zero) / len(zero)


def balanced_traces(key, epsilon=1.0):
    """Each of the 16 inputs once, no noise, one sample."""
    return [(p, [epsilon * hamming_weight(PRESENT_SBOX[p ^ key])]) for p in range(16)]


def test_worked_example() -> None:
    # Key 0xB, one noiseless trace for each input: the page's example.
    best, scores = differential_power_analysis(balanced_traces(0xB))
    assert best == 0xB
    assert scores[0xB] == pytest.approx(1.0)
    assert scores[0xB ^ 0x5] == pytest.approx(0.75)
    assert scores[0xB ^ 0x6] == pytest.approx(-1.25)
    assert scores[0xB ^ 0xB] == pytest.approx(0.75)
    assert sorted(scores, reverse=True)[1] == pytest.approx(0.75)


def test_balanced_noiseless_equals_exact_expectation() -> None:
    for key in range(16):
        for bit in range(4):
            _, scores = differential_power_analysis(balanced_traces(key), bit=bit)
            for g in range(16):
                assert scores[g] == pytest.approx(expected_difference(g ^ key, bit))


def test_signed_bit1_recovers_every_key_without_noise() -> None:
    for key in range(16):
        best, _ = differential_power_analysis(balanced_traces(key), bit=1)
        assert best == key


def test_absolute_value_pitfall() -> None:
    # With |delta|, the guess key ^ 6 scores 1.25 > 1 on bit 1.
    for key in range(16):
        best, scores = differential_power_analysis(balanced_traces(key), bit=1, signed=False)
        assert best == key ^ 6
        assert scores[key ^ 6] == pytest.approx(1.25)
    # On bit 0, seven wrong guesses tie with the right one at |delta| = 1.
    _, scores = differential_power_analysis(balanced_traces(0), bit=0, signed=False)
    assert sum(1 for s in scores if abs(s - 1.0) < 1e-12) == 8


def test_edges() -> None:
    with pytest.raises(ValueError):
        differential_power_analysis([])
    best, scores = differential_power_analysis([(3, [0.5, 1.0])])
    assert best == -1 and all(s == -math.inf for s in scores)
    # Two traces: some guesses split them, some do not.
    tr = [(0, [1.0]), (1, [0.0])]
    assert differential_power_analysis(tr)[1] == oracle_scores(tr, PRESENT_SBOX, 1, True)


def test_against_oracle_random() -> None:
    rng = random.Random(20240501)
    for _ in range(500):
        m = rng.randrange(1, 12)
        t_len = rng.randrange(1, 4)
        bit = rng.randrange(4)
        signed = rng.random() < 0.5
        traces = [(rng.randrange(16), [rng.uniform(-3, 3) for _ in range(t_len)]) for _ in range(m)]
        best, scores = differential_power_analysis(traces, bit=bit, signed=signed)
        want = oracle_scores(traces, PRESENT_SBOX, bit, signed)
        for a, b in zip(scores, want):
            assert a == b or a == pytest.approx(b, abs=1e-9)
        finite = [i for i, s in enumerate(want) if s != -math.inf]
        if finite:
            top = max(want[i] for i in finite)
            assert want[best] == pytest.approx(top, abs=1e-9)
        else:
            assert best == -1


def test_success_rate_with_noise() -> None:
    rng = random.Random(7)
    hits = 0
    runs = 12
    for r in range(runs):
        key = rng.randrange(16)
        traces = simulate_traces(rng, key, m=800, sigma=0.5)
        best, _ = differential_power_analysis(traces)
        hits += best == key
    assert hits >= runs - 1


def test_too_few_traces_often_fail() -> None:
    rng = random.Random(11)
    hits = sum(
        differential_power_analysis(simulate_traces(rng, k, m=8, sigma=2.0))[0] == k
        for k in range(16)
    )
    assert hits <= 8
