# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-likelihood-sequence-estimation/. The authors are listed in prov/FM9AE7.jsonl.

import itertools
import math
import random

from maximum_likelihood_sequence_estimation import (
    branch_metric,
    conv_encode,
    isi_mlse,
    q_function,
    union_bound_ber,
    viterbi_decode,
)

G75 = [7, 5]
G_K7 = [int("171", 8), int("133", 8)]


def brute_force(r, gens, k, length, soft):
    best, arg = None, None
    for m in itertools.product((0, 1), repeat=length):
        c = conv_encode(m, gens, k)
        d = branch_metric(r, c, soft)
        if best is None or d < best - 1e-12:
            best, arg = d, list(m)
    return best, arg


def test_worked_example() -> None:
    c = conv_encode([1, 0, 1, 1], G75, 3)
    assert c == [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1]
    r = list(c)
    r[2] ^= 1
    r[7] ^= 1
    assert viterbi_decode(r, G75, 3, soft=False) == [1, 0, 1, 1]


def test_no_noise_and_edges() -> None:
    assert viterbi_decode(conv_encode([], G75, 3), G75, 3, soft=False) == []
    for m in ([0], [1], [1] * 9, [0] * 9):
        c = conv_encode(m, G_K7, 7)
        assert viterbi_decode(c, G_K7, 7, soft=False) == m
        assert viterbi_decode([1.0 - 2 * b for b in c], G_K7, 7) == m


def test_viterbi_equals_brute_force_ml() -> None:
    rng = random.Random(3)
    for trial in range(500):
        gens, k = (G75, 3) if trial % 2 else ([int("15", 8), int("17", 8)], 4)
        length = rng.randrange(1, 7)
        c = conv_encode([rng.randrange(2) for _ in range(length)], gens, k)
        soft = trial % 3 != 0
        if soft:
            r = [1 - 2 * b + rng.gauss(0, 0.9) for b in c]
        else:
            r = [b ^ (rng.random() < 0.15) for b in c]
        got = viterbi_decode(r, gens, k, soft=soft)
        best, _ = brute_force(r, gens, k, length, soft)
        assert abs(branch_metric(r, conv_encode(got, gens, k), soft) - best) < 1e-9


def test_corrects_up_to_half_free_distance() -> None:
    # d_free = 5 for (7, 5): every pattern of 2 errors in a short block is corrected.
    m = [1, 0, 0, 1, 1, 0]
    c = conv_encode(m, G75, 3)
    for i, j in itertools.combinations(range(len(c)), 2):
        r = list(c)
        r[i] ^= 1
        r[j] ^= 1
        assert viterbi_decode(r, G75, 3, soft=False) == m


def test_truncated_traceback_matches_full_with_long_depth() -> None:
    rng = random.Random(8)
    for _ in range(40):
        m = [rng.randrange(2) for _ in range(60)]
        y = [1 - 2 * b + rng.gauss(0, 0.6) for b in conv_encode(m, G75, 3)]
        assert viterbi_decode(y, G75, 3, depth=15) == viterbi_decode(y, G75, 3)


def test_isi_mlse_equals_brute_force() -> None:
    rng = random.Random(4)
    for _ in range(500):
        h = [1.0, rng.uniform(-0.9, 0.9), rng.uniform(-0.5, 0.5)]
        t = rng.randrange(1, 7)
        b = [rng.randrange(2) for _ in range(t)]

        def mean(bits, i):
            return sum(h[j] * ((1 - 2 * bits[i - j]) if i - j >= 0 else 1.0) for j in range(len(h)))

        y = [mean(b, i) + rng.gauss(0, 0.5) for i in range(t)]

        def cost(bits):
            return sum((y[i] - mean(bits, i)) ** 2 for i in range(t))

        best = min(cost(list(x)) for x in itertools.product((0, 1), repeat=t))
        assert abs(cost(isi_mlse(y, h)) - best) < 1e-9


def test_monte_carlo_ber_against_union_bound() -> None:
    # (7, 5) code, BPSK on AWGN, soft decisions. Es = R Eb with Es = 1, so the
    # noise standard deviation is sqrt(1 / (2 R Eb/N0)). B_d = (d - 4) 2^(d - 5).
    ebn0_db, rate = 3.0, 0.5
    spec = [(d, (d - 4) * 2 ** (d - 5)) for d in range(5, 13)]
    bound = union_bound_ber(spec, rate, ebn0_db)
    sigma = math.sqrt(1 / (2 * rate * 10 ** (ebn0_db / 10)))
    rng = random.Random(2024)
    err = tot = 0
    for _ in range(200):
        m = [rng.randrange(2) for _ in range(100)]
        y = [1 - 2 * b + rng.gauss(0, sigma) for b in conv_encode(m, G75, 3)]
        err += sum(a != b for a, b in zip(m, viterbi_decode(y, G75, 3)))
        tot += len(m)
    ber = err / tot
    uncoded = q_function(math.sqrt(2 * 10 ** (ebn0_db / 10)))
    assert 0.3 * bound < ber < 1.3 * bound
    assert ber < uncoded / 2
