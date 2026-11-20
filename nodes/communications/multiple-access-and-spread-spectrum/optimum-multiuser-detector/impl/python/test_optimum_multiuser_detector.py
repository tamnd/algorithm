# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimum-multiuser-detector/. The authors are listed in prov/H2AQFV.jsonl.

import itertools
import math
import random

import pytest

import constel
from optimum_multiuser_detector import (
    bit_waveforms,
    log_likelihood,
    optimum_detector,
    optimum_synchronous,
    received,
)

R8 = 1.0 / math.sqrt(8.0)
# The signatures of the page: s1 s2 = 0.5, s1 s3 = 0.25, s2 s3 = -0.25.
S_PAGE = [
    [R8 * c for c in (1, 1, 1, 1, 1, 1, 1, 1)],
    [R8 * c for c in (1, 1, 1, 1, 1, 1, -1, -1)],
    [R8 * c for c in (1, -1, 1, -1, 1, -1, 1, 1)],
]


def random_sigs(rng: random.Random, k: int, n: int) -> list[list[float]]:
    s = 1.0 / math.sqrt(n)
    return [[s * rng.choice((1, -1)) for _ in range(n)] for _ in range(k)]


def brute_force(y, sigs, delays, amps, m):
    best, arg = -math.inf, None
    k = len(sigs)
    for flat in itertools.product((1, -1), repeat=k * m):
        b = [list(flat[u * m:(u + 1) * m]) for u in range(k)]
        v = log_likelihood(y, sigs, delays, amps, b)
        if v > best:
            best, arg = v, b
    return arg


def test_page_example_synchronous() -> None:
    # The matched filter outputs of the page come from these chip samples.
    amps = [1.0, 4.0, 2.0]
    b = [1, -1, 1]
    y = received(S_PAGE, [0, 0, 0], amps, [[v] for v in b])
    z = [sum(a * c for a, c in zip(s, y)) for s in S_PAGE]
    assert [round(v, 12) for v in z] == [-0.5, -4.0, 3.25]
    assert optimum_synchronous(y, S_PAGE, amps) == b


def test_synchronous_matches_brute_force_ml() -> None:
    rng = random.Random(4101)
    pts = constel.pam(2)  # [+1, -1]
    for k in range(1, 7):
        for _ in range(25):
            sigs = random_sigs(rng, k, 8)
            amps = [rng.uniform(0.3, 3.0) for _ in range(k)]
            b = [rng.choice((1, -1)) for _ in range(k)]
            y = received(sigs, [0] * k, amps, [[v] for v in b], sigma=0.6, rng=rng)
            h = [[amps[u] * sigs[u][c] for u in range(k)] for c in range(8)]
            idx = constel.ml_vector([complex(v) for v in y], h, pts)
            ref = [1 if i == 0 else -1 for i in idx]
            assert optimum_synchronous(y, sigs, amps) == ref


@pytest.mark.parametrize("k,m,seed", [(2, 4, 11), (3, 2, 12), (3, 3, 13), (4, 2, 14)])
def test_asynchronous_matches_brute_force(k: int, m: int, seed: int) -> None:
    rng = random.Random(seed)
    n = 7
    for _ in range(12):
        sigs = random_sigs(rng, k, n)
        delays = [0] + [rng.randrange(n) for _ in range(k - 1)]
        amps = [rng.uniform(0.3, 3.0) for _ in range(k)]
        b = [[rng.choice((1, -1)) for _ in range(m)] for _ in range(k)]
        y = received(sigs, delays, amps, b, sigma=0.8, rng=rng)
        assert optimum_detector(y, sigs, delays, amps, m) == brute_force(y, sigs, delays, amps, m)


def test_noiseless_frames_are_recovered() -> None:
    rng = random.Random(4102)
    for k in range(1, 6):
        sigs = random_sigs(rng, k, 16)
        if k > 1:
            sigs[1] = list(sigs[0])  # two users with the same signature but other delays
        delays = [rng.randrange(16) for _ in range(k)]
        if k > 1:
            delays[1] = (delays[0] + 5) % 16
        amps = [rng.uniform(0.5, 2.0) for _ in range(k)]
        b = [[rng.choice((1, -1)) for _ in range(5)] for _ in range(k)]
        y = received(sigs, delays, amps, b)
        assert optimum_detector(y, sigs, delays, amps, 5) == b


def test_each_bit_overlaps_only_k_minus_one_neighbors() -> None:
    rng = random.Random(4103)
    for k in range(1, 6):
        n = 9
        delays = [rng.randrange(n) for _ in range(k)]
        _, starts, _ = bit_waveforms([[1.0] * n] * k, delays, 4)
        for t in range(len(starts)):
            for u in range(t + k, len(starts)):
                assert starts[u] - starts[t] >= n


def test_errors() -> None:
    with pytest.raises(ValueError):
        bit_waveforms([[1.0, 0.0]], [2], 1)
    with pytest.raises(ValueError):
        bit_waveforms([[1.0, 0.0], [1.0]], [0, 0], 1)
    with pytest.raises(ValueError):
        optimum_detector([0.0], [[1.0, 0.0]], [0], [1.0], 1)
