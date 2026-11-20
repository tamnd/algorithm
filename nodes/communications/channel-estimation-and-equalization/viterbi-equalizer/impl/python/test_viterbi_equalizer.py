# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/viterbi-equalizer/. The authors are listed in prov/8TQVP4.jsonl.

import itertools
import math
import random

import pytest

from viterbi_equalizer import brute_force, min_distance_bpsk, sequence_metric, viterbi_equalize


def cn(rng, var):
    s = math.sqrt(var / 2)
    return complex(rng.gauss(0, s), rng.gauss(0, s))


def channel_out(f, x, pre):
    mem = len(f) - 1
    full = list(pre) + list(x)
    return [sum(f[l] * full[mem + k - l] for l in range(len(f))) for k in range(len(x))]


def qfunc(x):
    return 0.5 * math.erfc(x / math.sqrt(2))


def wilson(k, n, z=3.29):
    p = k / n
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return mid - half, mid + half


def test_example_on_the_page() -> None:
    y = [1.4, 0.1, -1.2, 0.6]
    d = viterbi_equalize(y, [1, 0.5], [1, -1], pre=[1])
    assert d == [1, -1, -1, 1]
    assert abs(sequence_metric(y, [1, 0.5], d, pre=[1]) - 0.47) < 1e-12
    # the symbol-by-symbol slicer on y gets x[1] wrong
    assert [1 if v > 0 else -1 for v in y] == [1, 1, -1, 1]


def test_equals_brute_force_bpsk_with_and_without_tail() -> None:
    rng = random.Random(7501)
    for trial in range(16):
        taps = rng.randint(1, 4)
        f = [rng.gauss(0, 1) for _ in range(taps)]
        pre = [rng.choice((-1, 1)) for _ in range(taps - 1)]
        n = 10
        tail = [rng.choice((-1, 1)) for _ in range(taps - 1)] if trial % 2 else []
        x = [rng.choice((-1, 1)) for _ in range(n)]
        y = [v + rng.gauss(0, 0.8) for v in channel_out(f, x + tail, pre)]
        v = viterbi_equalize(y, f, [1, -1], pre=pre, tail=tail)
        b = brute_force(y, f, [1, -1], pre=pre, tail=tail)
        assert len(v) == n
        assert abs(sequence_metric(y, f, v + tail, pre) - sequence_metric(y, f, b + tail, pre)) < 1e-9
        assert v == b


def test_equals_brute_force_complex_qpsk() -> None:
    rng = random.Random(7502)
    qpsk = [complex(a, b) for a in (-1, 1) for b in (-1, 1)]
    for _ in range(10):
        taps = rng.randint(2, 3)
        f = [cn(rng, 1.0) for _ in range(taps)]
        pre = [rng.choice(qpsk) for _ in range(taps - 1)]
        x = [rng.choice(qpsk) for _ in range(5)]
        y = [v + cn(rng, 1.0) for v in channel_out(f, x, pre)]
        v = viterbi_equalize(y, f, qpsk, pre=pre)
        b = brute_force(y, f, qpsk, pre=pre)
        assert abs(sequence_metric(y, f, v, pre) - sequence_metric(y, f, b, pre)) < 1e-9
        assert v == b


def test_equals_brute_force_4pam() -> None:
    rng = random.Random(7503)
    pam = [3, 1, -1, -3]
    for _ in range(4):
        f = [1.0, rng.uniform(-0.9, 0.9)]
        x = [rng.choice(pam) for _ in range(6)]
        y = [v + rng.gauss(0, 0.7) for v in channel_out(f, x, [3])]
        assert viterbi_equalize(y, f, pam, pre=[3]) == brute_force(y, f, pam, pre=[3])


def test_noiseless_recovery_on_known_channels() -> None:
    rng = random.Random(7504)
    for f in ([1, 0.5], [0.407, 0.815, 0.407], [0.227, 0.460, 0.688, 0.460, 0.227]):
        x = [rng.choice((-1, 1)) for _ in range(300)]
        pre = [1] * (len(f) - 1)
        assert viterbi_equalize(channel_out(f, x, pre), f, [1, -1], pre=pre) == x


def test_minimum_distance_against_short_error_sequences() -> None:
    assert abs(min_distance_bpsk([1, 0.5]) - 5.0) < 1e-12
    for f in ([1, 0.5], [0.407, 0.815, 0.407], [1, -0.9, 0.3]):
        best = float("inf")
        for n in range(1, 9):
            for e in itertools.product((-2, 0, 2), repeat=n):
                if e[0] == 0:
                    continue
                full = [sum(f[l] * e[k - l] for l in range(len(f)) if 0 <= k - l < n) for k in range(n + len(f) - 1)]
                best = min(best, sum(v * v for v in full))
        assert abs(min_distance_bpsk(f) - best) < 1e-12
    # the channel B of Proakis: d_min^2 = 2.6569 against the matched filter bound 4 ||f||^2 = 3.9821
    assert abs(min_distance_bpsk([0.407, 0.815, 0.407]) - 2.656904) < 1e-9


def test_bit_error_rate_is_between_the_matched_filter_bound_and_twice_it() -> None:
    # f = (1, 0.5) has d_min^2 = 4 ||f||^2, so at high SNR the BER is close to Q(sqrt(2 ||f||^2 / N0))
    rng = random.Random(7505)
    f, n0 = [1, 0.5], 0.4
    sigma = math.sqrt(n0 / 2)  # real BPSK: only the real part of CN(0, N0) noise matters
    errors = total = 0
    while total < 60000:
        x = [rng.choice((-1, 1)) for _ in range(200)]
        y = [v + rng.gauss(0, sigma) for v in channel_out(f, x, [1])]
        d = viterbi_equalize(y, f, [1, -1], pre=[1])
        errors += sum(a != b for a, b in zip(d, x))
        total += len(x)
    assert errors >= 100
    lo, hi = wilson(errors, total)
    mfb = qfunc(math.sqrt(2 * 1.25 / n0))
    assert lo >= mfb
    assert hi <= 2 * mfb


def test_input_checks() -> None:
    with pytest.raises(ValueError):
        viterbi_equalize([1, 2], [1, 0.5], [1, -1], pre=[])
    with pytest.raises(ValueError):
        viterbi_equalize([1], [1, 0.5], [1, -1], tail=[1, 1])
    with pytest.raises(ValueError):
        viterbi_equalize([1, 2], [1, 0.5], [1, -1], tail=[3])
