# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-exponential-backoff/. The authors are listed in prov/R0C39B.jsonl.

import random
from fractions import Fraction

import pytest

from binary_exponential_backoff import (
    ATTEMPT_LIMIT,
    backoff_slots,
    expected_collisions_two_stations,
    simulate,
)


class Zero:
    """An rng that always picks k = 0, so that two stations never separate."""

    def randrange(self, stop: int) -> int:
        return 0


class Recorder:
    def __init__(self) -> None:
        self.stops: list[int] = []

    def randrange(self, stop: int) -> int:
        self.stops.append(stop)
        return 0


def test_window_doubles_then_is_truncated() -> None:
    rec = Recorder()
    for n in range(1, 16):
        backoff_slots(n, rec)
    assert rec.stops == [2, 4, 8, 16, 32, 64, 128, 256, 512] + [1024] * 6
    with pytest.raises(ValueError):
        backoff_slots(0, rec)


def test_draws_are_uniform() -> None:
    rng = random.Random(4)
    counts = [0] * 8
    for _ in range(80000):
        counts[backoff_slots(3, rng)] += 1
    assert all(abs(c - 10000) < 400 for c in counts)


def test_frame_dropped_after_sixteen_attempts() -> None:
    a, b = simulate([1, 1], Zero())
    assert a.sent == b.sent == []
    assert a.dropped == b.dropped == 1
    assert a.collisions == ATTEMPT_LIMIT == 16


def test_every_frame_is_sent_or_dropped() -> None:
    for seed in range(20):
        rng = random.Random(seed)
        frames = [rng.randint(0, 6) for _ in range(rng.randint(1, 12))]
        res = simulate(frames, rng)
        assert [len(s.sent) + s.dropped for s in res] == frames
        slots = [t for s in res for t in s.sent]
        assert len(slots) == len(set(slots))  # one success per slot


def test_two_stations_expected_collisions() -> None:
    exact = sum(
        Fraction(1, 2 ** sum(min(j, 10) for j in range(1, c))) for c in range(1, ATTEMPT_LIMIT + 1)
    )
    assert abs(expected_collisions_two_stations() - float(exact)) < 1e-12
    assert round(float(exact), 4) == 1.6416
    rng = random.Random(1)
    trials = 20000
    mean = sum(simulate([1, 1], rng)[0].collisions for _ in range(trials)) / trials
    assert abs(mean - float(exact)) < 0.03


def test_capture_effect() -> None:
    # Two busy stations: the winner of a contention restarts at n = 0 and
    # keeps winning against a station whose window has grown.
    for seed in range(5):
        a, b = simulate([100, 100], random.Random(seed))
        events = sorted([(t, "a") for t in a.sent] + [(t, "b") for t in b.sent])
        changes = sum(x[1] != y[1] for x, y in zip(events, events[1:]))
        assert changes == 1, seed  # one station sends all its frames first
