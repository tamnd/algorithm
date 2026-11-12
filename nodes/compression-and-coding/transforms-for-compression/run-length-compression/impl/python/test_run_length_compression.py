# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/run-length-compression/. The authors are listed in prov/Y9ZKV2.jsonl.

# Oracles: the Golomb code table for m = 3 and the worked example of the page,
# a numeric search for the best m (it must equal the rule of Gallager and Van
# Voorhis), the entropy bound H <= E[L] < H + 1 of an optimal prefix code, the
# Kraft sum of the code, and round trips.

import math
import random

from run_length_compression import (
    expected_golomb_length,
    golomb_decode,
    golomb_encode,
    golomb_parameter,
    run_entropy,
    runs_decode,
    runs_encode,
)


def test_golomb_tables() -> None:
    assert [golomb_encode(k, 1) for k in range(4)] == ["0", "10", "110", "1110"]
    assert [golomb_encode(k, 3) for k in range(7)] == [
        "00", "010", "011", "100", "1010", "1011", "1100",
    ]
    assert [golomb_encode(k, 4) for k in range(5)] == ["000", "001", "010", "011", "1000"]
    for m in range(1, 40):
        for k in range(200):
            code = golomb_encode(k, m)
            assert golomb_decode(code + "1", 0, m) == (k, len(code))


def test_prefix_free_and_complete() -> None:
    # The Kraft sum over all k is 1 (the code is complete): sum over the
    # m remainders in each of the infinitely many quotient groups.
    for m in range(1, 30):
        group = sum(2.0 ** -len(golomb_encode(k, m)) for k in range(m))
        assert abs(group - 0.5) < 1e-12  # each quotient group adds half of the rest
        codes = [golomb_encode(k, m) for k in range(3 * m + 5)]
        for a in codes:
            for b in codes:
                assert a == b or not b.startswith(a)


def test_parameter_rule() -> None:
    assert golomb_parameter(0.0) == 1
    assert golomb_parameter(0.5) == 1
    assert golomb_parameter(0.9) == 7
    for theta in (0.3, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.97):
        m = golomb_parameter(theta)
        assert theta**m + theta ** (m + 1) <= 1 < theta ** (m - 1) + theta**m
        lengths = {mm: expected_golomb_length(theta, mm) for mm in range(1, 80)}
        assert lengths[m] <= min(lengths.values()) + 1e-9


def test_entropy_bound() -> None:
    for theta in (0.1, 0.5, 0.75, 0.9, 0.95, 0.99):
        m = golomb_parameter(theta)
        h = run_entropy(theta)
        e = expected_golomb_length(theta, m, terms=200000)
        assert h - 1e-9 <= e < h + 1


def test_worked_example() -> None:
    bits = [0] * 9 + [1] + [0] * 2 + [1] + [0] * 14 + [1] + [0] * 3
    code = runs_encode(bits, 0.9)
    assert golomb_parameter(0.9) == 7
    # m = 7: remainder 0 takes 2 bits "00", remainders 1 to 6 take 3 bits (r + 1).
    assert len(bits) == 31
    assert code == "10" "011" + "0" "011" + "110" "00" + "0" "100"
    assert runs_decode(code, len(bits), 0.9) == bits


def test_round_trips() -> None:
    rng = random.Random(1975)
    for theta in (0.0, 0.5, 0.8, 0.95):
        for n in (0, 1, 2, 50, 3000):
            bits = [0 if rng.random() < theta else 1 for _ in range(n)]
            assert runs_decode(runs_encode(bits, theta), n, theta) == bits
    for bits in ([0] * 500, [1] * 500, [0, 1] * 100):
        for theta in (0.2, 0.9):
            assert runs_decode(runs_encode(bits, theta), len(bits), theta) == bits


def test_rate_on_a_sparse_source() -> None:
    # Bits per source bit approach the entropy h(theta) for a long string.
    rng = random.Random(11)
    theta, n = 0.95, 200000
    bits = [0 if rng.random() < theta else 1 for _ in range(n)]
    rate = len(runs_encode(bits, theta)) / n
    h = -theta * math.log2(theta) - (1 - theta) * math.log2(1 - theta)
    assert h < rate < h + 0.02
