# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/belady-anomaly/. The authors are listed in prov/8EZ63W.jsonl.

import itertools
import random

from belady_anomaly import find_anomaly, fifo_faults, fifo_trace, lru_faults, second_chance_faults

CLASSIC = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]


def test_classic_anomaly() -> None:
    assert fifo_faults(CLASSIC, 3) == 9
    assert fifo_faults(CLASSIC, 4) == 10
    assert [fifo_faults(CLASSIC, f) for f in range(1, 6)] == [12, 12, 9, 10, 5]


def test_classic_trace() -> None:
    three = fifo_trace(CLASSIC, 3)
    four = fifo_trace(CLASSIC, 4)
    assert "".join("F" if f else "." for f, _ in three) == "FFFFFFF..FF."
    assert "".join("F" if f else "." for f, _ in four) == "FFFF..FFFFFF"
    assert three[6][1] == (1, 2, 5)
    assert four[6][1] == (2, 3, 4, 5)


def test_lru_has_no_anomaly() -> None:
    assert [lru_faults(CLASSIC, f) for f in range(1, 6)] == [12, 12, 10, 8, 5]
    for n in range(1, 9):
        for seq in itertools.product(range(4), repeat=n):
            f = [lru_faults(seq, k) for k in range(1, 5)]
            assert all(a >= b for a, b in zip(f, f[1:]))


def test_search_on_short_sequences() -> None:
    assert find_anomaly(fifo_faults, 4, 7, 4) is None
    assert find_anomaly(lru_faults, 4, 7, 4) is None


def test_second_chance_anomaly() -> None:
    seq = (1, 1, 2, 2, 3, 4, 3)
    assert second_chance_faults(seq, 2) == 4
    assert second_chance_faults(seq, 3) == 5
    assert find_anomaly(second_chance_faults, 4, 7, 3) == (seq, 2)


def test_fifo_simulator_against_naive() -> None:
    rng = random.Random(12)
    for _ in range(300):
        seq = [rng.randrange(6) for _ in range(rng.randrange(30))]
        k = rng.randrange(1, 6)
        loaded, faults = [], 0
        for x in seq:
            if x not in loaded:
                faults += 1
                loaded.append(x)
                if len(loaded) > k:
                    del loaded[0]
        assert fifo_faults(seq, k) == faults
