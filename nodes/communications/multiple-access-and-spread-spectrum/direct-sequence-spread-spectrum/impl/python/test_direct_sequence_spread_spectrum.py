# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-sequence-spread-spectrum/. The authors are listed in prov/5PQ8PD.jsonl.

import random

from direct_sequence_spread_spectrum import decide, despread, mseq_chips, spread

POLYS = {3: [3, 1, 0], 5: [5, 2, 0], 7: [7, 1, 0]}


def test_check_value_degree_three() -> None:
    c = mseq_chips(POLYS[3])
    assert c == [-1, 1, 1, -1, 1, -1, -1]  # bits 1001011
    assert spread([1, -1], c) == c + [-v for v in c]
    assert despread(spread([1, -1], c), c) == [7, -7]


def test_round_trip_without_noise() -> None:
    rng = random.Random(1)
    for poly in POLYS.values():
        c = mseq_chips(poly)
        d = [rng.choice((-1, 1)) for _ in range(50)]
        z = despread(spread(d, c), c)
        assert z == [len(c) * v for v in d]
        assert decide(z) == d


def test_constant_jammer_is_reduced_to_minus_its_amplitude() -> None:
    # The chips of an m-sequence sum to -1, so a constant A adds exactly -A per symbol.
    rng = random.Random(2)
    for poly in POLYS.values():
        c = mseq_chips(poly)
        n = len(c)
        assert sum(c) == -1
        d = [rng.choice((-1, 1)) for _ in range(20)]
        for a in (1, 5, 40):
            r = [x + a for x in spread(d, c)]
            assert despread(r, c) == [n * v - a for v in d]


def test_second_user_on_a_shifted_code() -> None:
    # Two shifts of one m-sequence have periodic cross-correlation -1.
    rng = random.Random(3)
    c = mseq_chips(POLYS[5])
    n = len(c)
    for tau in (1, 7, 30):
        c2 = c[tau:] + c[:tau]
        d1 = [rng.choice((-1, 1)) for _ in range(30)]
        d2 = [rng.choice((-1, 1)) for _ in range(30)]
        r = [x + y for x, y in zip(spread(d1, c), spread(d2, c2))]
        assert despread(r, c) == [n * a - b for a, b in zip(d1, d2)]


def test_white_noise_gain_equals_code_length() -> None:
    # Per chip: signal 1, noise variance s2. After despreading: signal N^2, noise N s2.
    rng = random.Random(4)
    c = mseq_chips(POLYS[5])
    n = len(c)
    s2 = 4.0
    count = 4000
    d = [rng.choice((-1, 1)) for _ in range(count)]
    r = [x + rng.gauss(0.0, s2 ** 0.5) for x in spread(d, c)]
    z = despread(r, c)
    noise = [zi - n * di for zi, di in zip(z, d)]
    var = sum(v * v for v in noise) / count
    assert abs(var / (n * s2) - 1) < 0.1
