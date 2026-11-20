# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rake-receiver/. The authors are listed in prov/MRC17X.jsonl.

import math
import random

from cbb import cn, dot, wilson
from rake_receiver import bpsk_error_probability, code_gram, composite, energy, mseq_code, output_snr, rake, receive

C7 = mseq_code([3, 1, 0])
C31 = mseq_code([5, 2, 0])


def test_check_values_length_seven() -> None:
    assert abs(sum(abs(v) ** 2 for v in C7) - 1) < 1e-12
    rr = code_gram(C7, [0, 2])
    assert abs(rr[0][0] - 1) < 1e-12 and abs(rr[0][1] + 1 / 7) < 1e-12
    assert abs(energy(C7, [0, 2], [0.8, 0.6]) - (1 - 0.96 / 7)) < 1e-12
    assert abs(energy(C7, [0, 2], [0.8, 0.6j]) - 1) < 1e-12


def test_rake_is_the_matched_filter_to_the_received_pulse() -> None:
    rng = random.Random(1)
    for _ in range(50):
        n_paths = rng.randint(1, 4)
        delays = rng.sample(range(31), n_paths)
        gains = [cn(rng, 1.0) for _ in range(n_paths)]
        r = [cn(rng, 1.0) for _ in range(31)]
        g = composite(C31, delays, gains)
        assert abs(rake(r, C31, delays, gains) - dot(g, r)) < 1e-9


def test_noiseless_symbols_are_recovered() -> None:
    rng = random.Random(2)
    for _ in range(50):
        delays = rng.sample(range(31), 3)
        gains = [cn(rng, 1.0) for _ in range(3)]
        b = rng.choice((-1, 1))
        r = receive(rng, b, C31, delays, gains, 1.0, 0.0)
        y = rake(r, C31, delays, gains)
        assert abs(y - b * energy(C31, delays, gains)) < 1e-9


def test_maximal_ratio_weights_maximize_the_output_snr() -> None:
    rng = random.Random(3)
    delays = [0, 1, 5]
    gains = [0.9, 0.5 - 0.3j, 0.2j]
    best = output_snr(C7, delays, gains, gains, 1.0, 1.0)
    assert abs(best - energy(C7, delays, gains)) < 1e-12
    for _ in range(500):
        a = [cn(rng, 1.0) for _ in range(3)]
        assert output_snr(C7, delays, gains, a, 1.0, 1.0) <= best + 1e-12
    one_finger = output_snr(C7, delays, gains, [1, 0, 0], 1.0, 1.0)
    assert one_finger < best


def test_bit_error_rate_matches_the_formula() -> None:
    rng = random.Random(4)
    delays, gains = [0, 2], [0.8, 0.6]
    es, n0 = 1.0, 1.0
    pb = bpsk_error_probability(C7, delays, gains, es, n0)
    errors = trials = 0
    while errors < 150:
        b = rng.choice((-1, 1))
        y = rake(receive(rng, b, C7, delays, gains, es, n0), C7, delays, gains)
        trials += 1
        if (1 if y.real >= 0 else -1) != b:
            errors += 1
    lo, hi = wilson(errors, trials)
    assert lo <= pb <= hi


def test_formula_value() -> None:
    pb = bpsk_error_probability(C7, [0, 2], [0.8, 0.6], 1.0, 1.0)
    assert abs(pb - 0.5 * math.erfc(math.sqrt(1 - 0.96 / 7))) < 1e-15
