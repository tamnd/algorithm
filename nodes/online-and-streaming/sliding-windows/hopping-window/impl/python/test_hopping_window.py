# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hopping-window/. The authors are listed in prov/RTYVEA.jsonl.

import random

from hopping_window import hopping_assign, hopping_sums_direct, hopping_sums_panes


def brute_windows(ts, size, hop, offset):
    out = []
    for j in range(-200, 201):
        lo = offset + j * hop
        if lo <= ts < lo + size:
            out.append((lo, lo + size))
    return out


def test_page_examples():
    assert hopping_assign(12, 10, 5) == [(5, 15), (10, 20)]
    assert hopping_assign(12, 10, 3) == [(3, 13), (6, 16), (9, 19), (12, 22)]
    assert hopping_assign(11, 10, 3) == [(3, 13), (6, 16), (9, 19)]
    # Dataflow: Sliding(2m, 1m), 12:00 is minute 720.
    assert hopping_assign(720, 2, 1) == [(719, 721), (720, 722)]


def test_assignment_matches_definition_and_count():
    rng = random.Random(3)
    for _ in range(3000):
        size = rng.randint(1, 9)
        hop = rng.randint(1, 9)
        offset = rng.randint(-4, 4)
        ts = rng.randint(-50, 50)
        got = hopping_assign(ts, size, hop, offset)
        assert got == brute_windows(ts, size, hop, offset)
        assert len(got) in (size // hop, -(-size // hop))
        if size % hop == 0:
            assert len(got) == size // hop


def test_hop_equal_size_is_tumbling():
    for size in range(1, 7):
        for ts in range(-20, 21):
            j = ts // size
            assert hopping_assign(ts, size, size) == [(j * size, (j + 1) * size)]


def test_pane_sums_equal_direct_sums():
    rng = random.Random(4)
    for _ in range(400):
        size = rng.randint(1, 12)
        hop = rng.randint(1, 12)
        offset = rng.randint(-3, 3)
        events = [(rng.randint(0, 40), rng.randint(-5, 9)) for _ in range(rng.randint(0, 20))]
        assert hopping_sums_panes(events, size, hop, offset) == hopping_sums_direct(events, size, hop, offset)
