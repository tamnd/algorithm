# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/locally-decodable-codes/. The authors are listed in prov/53AB3R.jsonl.

import random

from locally_decodable_codes import (hadamard_decode_all, hadamard_encode, hadamard_local_decode,
                                     hadamard_success, interpolate_at_zero, rm_encode,
                                     rm_local_decode, rm_success)

K = 8
N = 1 << K


def corrupt(word, positions):
    w = list(word)
    for a in positions:
        w[a] ^= 1
    return w


def test_hadamard_exact_success_at_least_one_minus_two_delta():
    rng = random.Random(1)
    for frac in (0.05, 0.1, 0.2, 0.24):
        x = rng.getrandbits(K)
        bad = rng.sample(range(N), int(frac * N))
        w = corrupt(hadamard_encode(x, K), bad)
        delta = len(bad) / N
        for i in range(K):
            assert hadamard_success(w, x, i, K) >= 1 - 2 * delta


def test_hadamard_monte_carlo_fixed_seed():
    rng = random.Random(2)
    x = 0b10110010
    bad = rng.sample(range(N), 25)  # delta = 25/256, about 0.098
    w = corrupt(hadamard_encode(x, K), bad)
    delta = 25 / N
    trials = 2000
    for i in range(K):
        ok = sum(hadamard_local_decode(w.__getitem__, i, K, rng) == (x >> i & 1)
                 for _ in range(trials))
        assert ok / trials >= 1 - 2 * delta - 0.03


def test_bound_is_tight_and_breaks_at_one_quarter():
    x, i = 0b01101001, 3
    zero_side = [a for a in range(N) if not a >> i & 1]  # S and S + e_i never meet
    for size in (16, 40, 64):
        w = corrupt(hadamard_encode(x, K), zero_side[:size])
        assert hadamard_success(w, x, i, K) == 1 - 2 * size / N
    # at delta = 1/4 this corruption leaves the decoder for bit i at 1/2: a coin toss
    w = corrupt(hadamard_encode(x, K), zero_side[:N // 4])
    assert hadamard_success(w, x, i, K) == 0.5


def test_hadamard_decode_whole_message_by_majority():
    rng = random.Random(3)
    for _ in range(10):
        x = rng.getrandbits(K)
        w = corrupt(hadamard_encode(x, K), rng.sample(range(N), 25))
        assert hadamard_decode_all(w, K, 31, rng) == x


def test_reed_muller_line_decoder():
    p, m, r = 13, 2, 3  # n = 169, r + 1 = 4 queries
    rng = random.Random(4)
    coeffs = {(a, b): rng.randrange(p) for a in range(r + 1) for b in range(r + 1 - a)}
    truth = rm_encode(coeffs, m, p)
    assert interpolate_at_zero([1, 2, 3], [5, 7, 9], 13) == 3  # the line 3 + 2t
    bad = rng.sample(sorted(truth), 12)
    word = dict(truth)
    for pt in bad:
        word[pt] = (word[pt] + rng.randrange(1, p)) % p
    for x in rng.sample(sorted(truth), 15) + bad[:3]:
        hits = sum(pt != x for pt in bad)  # x itself is never queried
        assert rm_success(word, truth, x, r, p) >= 1 - (r + 1) * hits / (p ** m - 1)
    x = bad[0]
    ok = sum(rm_local_decode(word, x, r, p, rng) == truth[x] for _ in range(500))
    assert ok / 500 >= 1 - (r + 1) * 12 / 168 - 0.05
